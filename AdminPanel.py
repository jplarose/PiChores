from PyQt5 import uic, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from database import fetch_logs, get_weeks_earnings, get_chore_dates_in_week, fetch_chores_for_week, get_users
import datetime
import sys

def get_current_date_string():
    current_date = datetime.datetime.now()
    week = current_date.strftime("%W")
    year = current_date.strftime("%Y")

    week = int(week) + 1

    return f'{year}-W{week}'

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

        earning_date = datetime.datetime.strptime(get_current_date_string() + '-1', '%G-W%V-%u')

        # Create and add a widget for each user
        for person in users:

            # Get the number of chores and their sum from last week
            week_earnings = get_weeks_earnings(person.Id, earning_date)
            week_earned = sum(e.ChoreValue for e in week_earnings)

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
            chores_label = QLabel(f"Completed {len(week_earnings)} Chores: ${week_earned:,.2f}")
            chores_label.setAlignment(QtCore.Qt.AlignCenter)
            chores_font = chores_label.font()
            chores_font.setPointSize(20)
            chores_label.setFont(chores_font)

            # View chores button
            view_button = QPushButton("View Chores")
            view_button.setMinimumHeight(100)
            view_button.setFont(button_font)
            # wire up click event

            # View logs button
            log_button = QPushButton("View Logs")
            log_button.setMinimumHeight(100)
            log_button.setFont(button_font)
            # wire up click event

            # Add widgets to the layout
            user_layout.addWidget(name_label)
            user_layout.addWidget(chores_label)
            user_layout.addWidget(view_button)
            user_layout.addWidget(log_button)

            layout.addWidget(user_widget)

    def handle_go_back(self):
        self.navigator.navigate_to_admin("userPage")




