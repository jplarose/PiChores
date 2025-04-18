from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from database import get_user_pin, log_action

class AuthPage(QWidget):
    """Authentication Page - Loaded from Qt Designer UI file."""

    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.user = None
        self.IsAdmin = False
        self.entered_pin = ""

        # Load UI file
        uic.loadUi("AuthPage.ui", self)

        # Connect buttons from UI file
        self.btn_1.clicked.connect(lambda: self.handle_keypad_input("1"))
        self.btn_2.clicked.connect(lambda: self.handle_keypad_input("2"))
        self.btn_3.clicked.connect(lambda: self.handle_keypad_input("3"))
        self.btn_4.clicked.connect(lambda: self.handle_keypad_input("4"))
        self.btn_5.clicked.connect(lambda: self.handle_keypad_input("5"))
        self.btn_6.clicked.connect(lambda: self.handle_keypad_input("6"))
        self.btn_7.clicked.connect(lambda: self.handle_keypad_input("7"))
        self.btn_8.clicked.connect(lambda: self.handle_keypad_input("8"))
        self.btn_9.clicked.connect(lambda: self.handle_keypad_input("9"))
        self.btn_0.clicked.connect(lambda: self.handle_keypad_input("0"))
        self.btn_clear.clicked.connect(self.clear_pin)
        self.btn_enter.clicked.connect(self.check_pin)
        self.go_home_button.clicked.connect(self.go_home)

    def update_page(self, user):
        """Update page content when a user is selected."""
        self.user = user
        self.IsAdmin = user.IsAdmin
        self.entered_pin = ""
        self.pin_display.setText("••••")

    def handle_keypad_input(self, key):
        """Handle PIN input from the keypad."""
        if len(self.entered_pin) < 4:
            self.entered_pin += key
            self.pin_display.setText("•" * len(self.entered_pin))

    def clear_pin(self):
        """Clear the entered PIN."""
        self.entered_pin = ""
        self.pin_display.setText("••••")

    def check_pin(self):
        """Check the PIN and navigate if correct."""
        stored_pin = get_user_pin(self.user.Id)
        if self.entered_pin == stored_pin:
            if self.IsAdmin:
                log_action(self.user.Id, "Admin Sign-In", f"Admin {self.user.Id} successfully signed in.")
                self.navigator.navigate_to("AdminPanel", self.user)
            else:
                log_action(self.user.Id, "Sign-In", f"User {self.user.Id} successfully signed in.")
                self.navigator.navigate_to("userHome", self.user)
        else:
            log_action(self.user.Id, "Sign-In", f"User {self.user.Id} sign-in failed.")
            self.pin_display.setText("Incorrect PIN!")
            self.entered_pin = ""

    def go_home(self):
        self.entered_pin = ""
        self.pin_display.setText("••••")

        self.navigator.navigate_to_admin("userPage", None, False)
