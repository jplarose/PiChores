import datetime
from database import get_weeks_earnings, get_years_earnings, log_action

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


def get_current_date_string():
    current_date = datetime.datetime.now()
    week = current_date.strftime("%W")
    year = current_date.strftime("%Y")

    week = int(week) + 1

    return f'{year}-W{week}'


class UserHome(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.user = None
        self.navigator = navigator
        uic.loadUi("UserHome.ui", self)

        self.logout_button.clicked.connect(lambda: self.handle_logout())
        self.logChoresButton.clicked.connect(lambda: self.handle_log_chores())
        self.viewloggedchoresbutton.clicked.connect(lambda: self.handle_view_chores())

    def update_page(self, user):
        self.user = user
        self.welcomeLabel.setText(f"Welcome, {user.Name}!")

        earning_date = datetime.datetime.strptime(get_current_date_string() + '-1', '%G-W%V-%u')
        self.earnings_box.setTitle(f"Week of {earning_date}")


        """Calculate earnings for the week/year"""
        week_earnings = get_weeks_earnings(user.Id, earning_date)
        year_earnings = get_years_earnings(user.Id)

        week_earned = sum(e.ChoreValue for e in week_earnings)
        year_earned = sum(e.ChoreValue for e in year_earnings)

        self.week_earned_value.setText(f"${week_earned:,.2f}")
        self.week_earned_value.setEnabled(True)
        self.week_earned_value.setStyleSheet("color: green;")

        self.year_earned_value.setText(f"${year_earned:,.2f}")
        self.year_earned_value.setEnabled(True)
        self.year_earned_value.setStyleSheet("color: green;")


    # Click the log chore button
    def handle_log_chores(self):
        self.navigator.navigate_to("ChoreLog", self.user)

    def handle_logout(self):
        log_action(self.user.Id, "Logout", f"User {self.user.Id} logged out.")
        self.navigator.navigate_to("userPage")

    def handle_view_chores(self):
        self.navigator.navigate_to("UserLoggedChores", self.user)



