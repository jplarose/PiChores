import sys
import os
import sqlite3
from pathlib import Path
from collections import namedtuple
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QStackedWidget, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,  QGridLayout
)
from PyQt5.QtCore import Qt

# SQLite Database Path
DB_PATH = Path(__file__).with_name('Chores.db')

# Database Functions
def log_interaction(page, action):
    """Logs user interactions into the SQLite database."""
#    try:
#        conn = sqlite3.connect(DB_PATH)
#        cursor = conn.cursor()
#        cursor.execute("INSERT INTO user_interactions (page, action) VALUES (?, ?)", (page, action))
#        conn.commit()
#        cursor.close()
#        conn.close()
#    except Exception as e:
#        print(f"Database error: {e}")

def get_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT Name as name, Id as id FROM Users WHERE IsVisible = 1")
        User = namedtuple("User", ["name", "id"])
        users = [User(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Database error: {e}")

def fetch_logs():
    """Fetches user interaction logs from SQLite."""
#    try:
#        conn = sqlite3.connect(DB_PATH)
#        cursor = conn.cursor()
#        cursor.execute("SELECT id, timestamp, page, action FROM user_interactions ORDER BY timestamp DESC")
#        logs = cursor.fetchall()
#        cursor.close()
#        conn.close()
#        return logs
#    except Exception as e:
#        print(f"Database error: {e}")
#        return []


class NavigationManager(QStackedWidget):
    """Manages navigation between multiple pages dynamically."""
    
    def __init__(self):
        super().__init__()
        self.pages = {}

    def add_page(self, page_name, page_instance):
        """Adds a new page to the navigation system."""
        self.pages[page_name] = page_instance
        self.addWidget(page_instance)

    def navigate_to(self, page_name, user=None):
        """Passes user data dynamically and switches pages."""
        if page_name in self.pages:
            page = self.pages[page_name]

            # If the page supports dynamic updates, refresh its content
            if hasattr(page, "update_page"):
                page.update_page(user)

            self.setCurrentWidget(page)
        else:
            print(f"Page '{page_name}' not found!")



from PyQt5.QtCore import QTimer

class UserPage(QWidget):
    """User selection page with normal and secret admin access."""
    
    SECRET_ACCESS_TIME = 1000  # Time window (milliseconds) for simultaneous press

    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Fetch users dynamically
        self.load_users()

        # Secret button tracking
        self.secret_timer = QTimer()
        self.secret_timer.setSingleShot(True)
        self.secret_timer.timeout.connect(self.reset_secret_access)

        self.first_button_pressed = False
        self.second_button_pressed = False

    def load_users(self):
        """Fetch and display users dynamically with hidden admin trigger."""
        # Clear old buttons before loading new ones
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        users = get_users()
        
        if len(users) < 2:
            print("Not enough users to enable secret function.")
            return

        # Create buttons for the first two users
        self.btn1 = QPushButton(users[0].name)
        self.btn2 = QPushButton(users[1].name)

        self.btn1.pressed.connect(lambda: self.handle_button_press(1, users[0]))
        self.btn2.pressed.connect(lambda: self.handle_button_press(2, users[1]))

        self.btn1.released.connect(lambda: self.handle_button_release(1, users[0]))
        self.btn2.released.connect(lambda: self.handle_button_release(2, users[1]))

        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)

    def handle_button_press(self, button_id, user):
        """Handle button press events and check for secret access."""
        if button_id == 1:
            self.first_button_pressed = True
        elif button_id == 2:
            self.second_button_pressed = True

        if self.first_button_pressed and self.second_button_pressed:
            self.secret_timer.start(self.SECRET_ACCESS_TIME)  # Start the timer

    def handle_button_release(self, button_id, user):
        """Handle button release events and navigate if necessary."""
        if button_id == 1:
            self.first_button_pressed = False
        elif button_id == 2:
            self.second_button_pressed = False

        # If the timer is still running, it's a secret function activation
        if self.secret_timer.isActive():
            print("Secret access granted!")
            self.navigator.navigate_to("AdminAuthPage")  # Navigate to admin authentication
            self.secret_timer.stop()
        else:
            # Normal behavior: navigate to AuthPage for the selected user
            self.navigator.navigate_to("authPage", user)

    def reset_secret_access(self):
        """Reset secret access tracking if time window expires."""
        self.first_button_pressed = False
        self.second_button_pressed = False


class AuthPage(QWidget):
    """Numeric keypad for PIN authentication."""
    
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.user = None  # Store current user
        self.entered_pin = ""  # Store PIN input

        layout = QVBoxLayout()
        self.label = QLabel("Enter PIN for Authentication")
        layout.addWidget(self.label)

        self.pin_display = QLabel("•" * 4)  # Masked PIN display
        self.pin_display.setStyleSheet("font-size: 24px; padding: 10px; border: 1px solid black;")
        self.pin_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pin_display)

        # Create the numeric keypad
        keypad_layout = QGridLayout()
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Clear', 3, 0), ('0', 3, 1), ('Enter', 3, 2),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("font-size: 20px; padding: 15px;")
            btn.clicked.connect(lambda checked, t=text: self.handle_keypad_input(t))
            keypad_layout.addWidget(btn, row, col)

        layout.addLayout(keypad_layout)
        self.setLayout(layout)

    def update_page(self, user):
        """Update page content when a user is selected."""
        self.user = user
        self.label.setText(f"Enter PIN for {self.user.name}")
        self.entered_pin = ""  # Reset PIN when opening page
        self.pin_display.setText("•" * 4)

    def handle_keypad_input(self, key):
        """Handle keypad button presses."""
        if key.isdigit():
            if len(self.entered_pin) < 4:
                self.entered_pin += key
                self.pin_display.setText("•" * len(self.entered_pin))
        elif key == "Clear":
            self.entered_pin = ""
            self.pin_display.setText("•" * 4)
        elif key == "Enter":
            self.check_pin()

    def check_pin(self):
        """Verify PIN from database and navigate if correct."""
        if not self.user:
            return

        stored_pin = self.get_user_pin(self.user.id)  # Fetch PIN from DB
        
        if self.entered_pin == stored_pin:
            print(f"User {self.user.name} authenticated!")
            self.navigator.navigate_to("userHome", self.user)  # Navigate to User Home
        else:
            self.pin_display.setText("Incorrect PIN!")
            self.entered_pin = ""

    def get_user_pin(self, user_id):
        """Fetch the user's PIN from the database."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT Pin FROM Users WHERE Id = ?", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            print(f"Database error: {e}")
            return None




class UserHome(QWidget):
    """User Home Page - Updates dynamically when user logs in."""

    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.user = None  # Placeholder for selected user

        main_layout = QVBoxLayout()

        self.welcome_label = QLabel("Welcome!")  # Will update dynamically
        main_layout.addWidget(self.welcome_label)

        btn_admin = QPushButton("Go to Admin Panel")
        btn_admin.clicked.connect(lambda: self.navigator.navigate_to("AdminPanel", self.user))
        main_layout.addWidget(btn_admin)

        self.setLayout(main_layout)

    def update_page(self, user):
        """Update page content dynamically."""
        self.user = user
        self.welcome_label.setText(f"Welcome, {self.user.name}!")  # Update label dynamically



class AdminPanel(QWidget):
    """Admin Panel to view logged interactions."""
    
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator

        layout = QVBoxLayout()

        self.label = QLabel("Admin Panel: User Interaction Logs")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        refresh_button = QPushButton("Refresh Logs")
        refresh_button.clicked.connect(self.load_logs)
        layout.addWidget(refresh_button)

        back_button = QPushButton("Back to Page 3")
        back_button.clicked.connect(lambda: self.navigator.navigate_to("Page3"))
        layout.addWidget(back_button)

        self.setLayout(layout)

        self.load_logs()
        
    def load_logs(self):
        """Fetch logs from the database and display them in the table."""
#        logs = fetch_logs()
#
#        self.table.setRowCount(len(logs))
#        self.table.setColumnCount(4)
#        self.table.setHorizontalHeaderLabels(["ID", "Timestamp", "Page", "Action"])
#
#        for row_idx, row_data in enumerate(logs):
#            for col_idx, col_data in enumerate(row_data):
#                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chores App")
        self.setGeometry(100, 100, 800, 500)

        self.navigator = NavigationManager()

        userPage = UserPage(self.navigator)
        authPage = AuthPage(self.navigator)
        userHome = UserHome(self.navigator)
        admin_panel = AdminPanel(self.navigator)

        self.navigator.add_page("userPage", userPage)
        self.navigator.add_page("authPage", authPage)
        self.navigator.add_page("userHome", userHome)
        self.navigator.add_page("AdminPanel", admin_panel)

        self.navigator.navigate_to("userPage")

        layout = QVBoxLayout()
        layout.addWidget(self.navigator)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar
    # window.showFullScreen()  # Run in fullscreen mode
    window.show()
    sys.exit(app.exec_())
