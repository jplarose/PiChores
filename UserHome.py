import datetime

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
        self.navigator = navigator
        uic.loadUi("UserHome.ui", self)

        self.logout_button.clicked.connect(lambda:self.handle_logout)

        #self.adminPanelBtn.clicked.connect(lambda: self.navigator.navigate_to("AdminPanel"))

    def update_page(self, user):
        self.welcomeLabel.setText(f"Welcome, {user.name}!")

        earning_date = datetime.datetime.strptime(get_current_date_string() + '-1', '%G-W%V-%u')
        self.earnings_box.setTitle(f"Week of {earning_date}")

        # Calculate earnings for the week/year


    # Click the log chore button

    def handle_logout():
        self.navigator.navigate_to("userPage")



