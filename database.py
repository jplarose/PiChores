from datetime import date, datetime, timedelta
import sqlite3
from collections import namedtuple
from pathlib import Path

DB_PATH = Path(__file__).with_name("Chores.db")

def log_action(user_id, action, message=None):
    """Log user actions and any associated errors"""

    sql = (
        "INSERT INTO Logs(UserId, Action, Message) "
        "VALUES (?, ?, ?)"
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

def was_chore_logged_recently(user_id, chore_id, selected_date, frequency):
    """Check if a chore has already been logged today or this week"""
    sql = (
        "SELECT DateCompleted FROM ChoreLog "
        "WHERE UserId = ? AND ChoreId = ? "
        "AND IsDeleted = 0"
    )

    params = (user_id, chore_id)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            for date_str in rows:
                logged_date = datetime.strptime(date_str[0].split(" ")[0], "%Y-%m-%d").date()

                if frequency == "daily":
                    if logged_date == selected_date:
                        return True

                elif frequency == "weekly":
                    # Monday = 0, Sunday = 6
                    weekday = selected_date.weekday()
                    start_of_week = selected_date - timedelta(days=weekday)
                    end_of_week = start_of_week + timedelta(days=6)

                    if start_of_week <= logged_date <= end_of_week:
                        return True

            return False
    except Exception as e:
        print(f"* Error checking chore frequency: {e}")
        return False


def get_users():
    """Fetch users from the database as named tuples."""

    sql = (
    "SELECT Name AS Name, Id as Id, IsAdmin as IsAdmin "
    "FROM Users "
    "WHERE IsVisible = 1"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        User = namedtuple("User", ["Name", "Id", "IsAdmin"])
        users = [User(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Database error: {e}")
        return []

def get_admin():
    """Fetch users from the database as named tuples."""

    sql = (
    "SELECT Name AS Name, Id as Id, IsAdmin as IsAdmin "
    "FROM Users "
    "WHERE IsVisible = 0 "
    "AND IsAdmin = 1"
    )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        User = namedtuple("User", ["Name", "Id", "IsAdmin"])
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
        "AND cl.DateCompleted BETWEEN ? AND DateTime() "
        "AND cl.IsDeleted = 0"
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
        "AND cl.DateCompleted BETWEEN ? AND DateTime() "
        "AND cl.IsDeleted = 0"
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
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            Chore = namedtuple("Chore", ["Name", "Id", "Frequency"])
            chores = [Chore(*row) for row in cursor.fetchall()]

            return chores
    except Exception as e:
        print(f"Database error: {e}")
        return None

def fetch_chores_for_date(selected_date, user_id):
    try:
        sql = (
            "SELECT cl.Id AS chore_log_id, c.ChoreName AS description, cl.DateCompleted AS timestamp "
            "FROM ChoreLog cl "
            "INNER JOIN Chores c ON cl.ChoreId = c.Id "
            "WHERE cl.UserId = ? "
            "AND cl.DateCompleted LIKE ? "
            "AND cl.IsDeleted = 0"
        )

        params = (user_id, f"{selected_date}%")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            Chore = namedtuple("Chore", ["chore_log_id", "description", "timestamp"])
            chores = [Chore(*row) for row in cursor.fetchall()]

            return chores
    except Exception as e:
        print(f"Database error: {e}")
        return None

def fetch_chores_for_week(selected_dates, user_id):
    try:
        sql = (
            "SELECT cl.Id AS chore_id, c.ChoreName AS description, cl.DateCompleted AS timestamp "
            "FROM ChoreLog cl "
            "INNER JOIN Chores c ON cl.ChoreId = c.Id "
            "WHERE cl.UserId = ? "
            "AND cl.DateCompleted IN ?"
        )

        params = (user_id, f"{selected_dates}%")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            Chore = namedtuple("Chore", ["chore_id", "description", "timestamp"])
            chores = [Chore(*row) for row in cursor.fetchall()]

            return chores
    except Exception as e:
        print(f"Database error: {e}")
        return None

def delete_chore_by_id(chore_log_id):

    sql = (
        "UPDATE ChoreLog "
        "SET IsDeleted = 1, "
        "DeletedOn = ? "
        "WHERE Id = ?"
    )

    params = (datetime.now().strftime("%Y-%m-%d %H:%M"), chore_log_id)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return True
    except Exception as e:
        print(f"Error Deleting Chore Log: {e}")
        return False

def get_chore_dates_in_week(start_date, user_id):
    """Returns a set of date objects for days that have chore logs in a 7-day range."""

    end_date = start_date + timedelta(days=6)
    sql = (
        "SELECT DISTINCT date(DateCompleted) AS day, COUNT(*) "
        "FROM ChoreLog "
        "WHERE (date(DateCompleted) BETWEEN ? AND ?) "
        "AND UserId = ? "
        "AND IsDeleted = 0 "
        "GROUP BY day"
    )

    params = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), user_id)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()

            return {date.fromisoformat(row[0]): row[1] for row in results}

    except Exception as e:
        print(f"Error getting chore dates: {e}")
        return set()

