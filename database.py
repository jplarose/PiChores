from datetime import date
import sqlite3
from collections import namedtuple
from pathlib import Path

DB_PATH = Path(__file__).with_name("Chores.db")

def log_action(user_id, action, message=""):
    """Log user actions and any associated errors"""

    sql = (
        "INSERT INTO Logs(UserId, Action, Message) "
        "VALUES ?, ?, ?"
    )

    params = (user_id, action, message)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return True
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_users():
    """Fetch users from the database as named tuples."""

    sql = (
    "SELECT Name AS Name, Id as Id "
    "FROM Users "
    "WHERE IsVisible = 1"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        User = namedtuple("User", ["Name", "Id"])
        users = [User(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Database error: {e}")
        return []

def fetch_logs():
    """Fetch user interaction logs from SQLite."""

    sql = (
    "SELECT u.Name AS UserName, l.Action AS Action, l.TimeStamp AS TimeStamp "
    "FROM Logs l "
    "INNER JOIN Users u ON l.UserId = u.Id "
    "ORDER BY TimeStamp DESC"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        Log = namedtuple("Log", ["UserName", "Action", "TimeStamp"])
        logs = [Log(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return logs
    except Exception as e:
        print(f"Database error: {e}")
        return []

def get_user_pin(user_id):
    """Fetch the user's PIN from the database."""

    sql = (
    "SELECT Pass "
    "FROM Users "
    f"WHERE Id = {user_id}"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_weeks_earnings(user_id, week_of_date):
    sql = (
        "SELECT cl.Id AS Id, c.ChoreValue AS ChoreValue "
        "FROM ChoreLog cl "
        "INNER JOIN Chores c ON c.Id = cl.ChoreId "
        "WHERE cl.UserId = ? "
        "AND cl.DateCompleted BETWEEN ? AND DateTime()"
    )

    params = (user_id, week_of_date)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        Earning = namedtuple("Earning", ["Id", "ChoreValue"])
        earnings = [Earning(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return earnings
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_years_earnings(user_id):
    sql = (
        "SELECT cl.Id AS Id, c.ChoreValue AS ChoreValue "
        "FROM ChoreLog cl "
        "INNER JOIN Chores c ON c.Id = cl.ChoreId "
        "WHERE cl.UserId = ? "
        "AND cl.DateCompleted BETWEEN ? AND DateTime()"
    )

    start_of_year = date.today().replace(month=1, day=1)
    params = (user_id, start_of_year.isoformat())

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        Earning = namedtuple("Earning", ["Id", "ChoreValue"])
        earnings = [Earning(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return earnings
    except Exception as e:
        print(f"Database error: {e}")
        return None

def log_chore(user_id, chore_id, date_completed):
    sql = (
        "INSERT INTO ChoreLog(UserId, ChoreId, DateCompleted) "
        "VALUES (?, ?, ?)"
    )

    params = (user_id, chore_id, date_completed)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return True
    except Exception as e:
        print(f"Database error: {e}")
        return e

def get_users_chores(user_id):
    sql = (
        "SELECT ChoreName AS Name, Id AS Id, Frequency AS Frequency "
        "FROM Chores "
        "WHERE UserId = ?"
    )

    params = (user_id,)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        Chore = namedtuple("Chore", ["Name", "Id", "Frequency"])
        chores = [Chore(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return chores
    except Exception as e:
        print(f"Database error: {e}")
        return None
