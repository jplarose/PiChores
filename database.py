import datetime
import sqlite3
from collections import namedtuple
from pathlib import Path

DB_PATH = Path(__file__).with_name("Chores.db")

def get_users():
    """Fetch users from the database as named tuples."""

    sql = (
    "SELECT Name AS name, Id as id "
    "FROM Users "
    "WHERE IsVisible = 1"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        User = namedtuple("User", ["name", "id"])
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
        "SELECT * "
        "FROM ChoreLog " 
        f"WHERE UserId = {user_id} "
        f"AND TimeStamp IN('{week_of_date}', DateTime())"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_years_earnings(user_id):
    sql = (
        "SELECT * "
        "FROM ChoreLog "
        f"WHERE UserId = {user_id} "
        f"AND TimeStamp IN('{datetime.date.year}', DateTime())"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None

def log_chore(user_id, chore_id, date):
    sql = (
        "INSERT INTO ChoreLog(UserId, ChoreId, DateCompleted) "
        f"VALUES ({user_id}, {chore_id}, '{date}')"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None
