from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class UserPage(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        uic.loadUi("UserPage.ui", self)
        self.load_users()

    def load_users(self):
        """Dynamically load user buttons into the scrollable area."""
        from database import get_users  # Ensure we import the function
        users = get_users()

        layout = self.findChild(QVBoxLayout, "userLayout")
        for user in users:
            btn = QPushButton(user.Name)
            btn.setFixedHeight(160)  # Large button for touchscreens
            btn.clicked.connect(lambda checked, u=user: self.navigator.navigate_to("authPage", u))
            layout.addWidget(btn)
