from PyQt5 import uic, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from database import fetch_logs, get_weeks_earnings, get_chore_dates_in_week, fetch_chores_for_week, get_users
import sys


class AdminPanel(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.user = None
        self.navigator = navigator
        uic.loadUi("AdminPanel.ui", self)

        self.go_home_button.clicked.connect(lambda: self.handle_go_back())

    def update_page(self, user):
        self.user = user
        self.populate_users()

    def populate_users(self):
        # Get the users
        users = get_users()

        layout = self.UsersAreaLayout.layout()

        # Delete any existing Widgets
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        # Create and add a widget for each user
        for person in users:
            # Get the number of chores completed in the last week

            user_widget = QWidget()
            user_layout = QVBoxLayout(user_widget)

            # Define the styles
            label_font = QFont()
            label_font.setPointSize(20)
            label_font.setBold(True)
            label_font.setUnderline(True)

            button_font = QFont()
            button_font.setPointSize(20)
            button_font.setBold(True)

            # User name label
            name_label = QLabel(person.Name)
            name_label.setAlignment(QtCore.Qt.AlignCenter)
            name_label.setFont(label_font)

            # Completed chores label
            chores_label = QLabel("Completed Chores: ")# + str(user['completed_chores']))
            chores_label.setAlignment(QtCore.Qt.AlignCenter)
            chores_font = chores_label.font()
            chores_font.setPointSize(20)
            chores_label.setFont(chores_font)

            # View chores button
            view_button = QPushButton("View Chores")
            view_button.setMinimumHeight(100)
            # wire up click event
            view_button.setFont(button_font)

            # View logs button
            log_button = QPushButton("View Logs")
            log_button.setMinimumHeight(100)
            # wire up click event
            log_button.setFont(button_font)

            # Add widgets to the layout
            user_layout.addWidget(name_label)
            user_layout.addWidget(chores_label)
            user_layout.addWidget(view_button)
            user_layout.addWidget(log_button)

            layout.addWidget(user_widget)

    def handle_go_back(self):
        self.navigator.navigate_to_admin("userPage")




