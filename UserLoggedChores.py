from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import Qt
from datetime import date, timedelta
from database import get_chore_dates_in_week
from functools import partial

class UserLoggedChores(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.user = None
        self.navigator = navigator

        # Load the UI from the .ui file.
        uic.loadUi("UserLoggedChores.ui", self)

        # The following widgets are now defined in the .ui file:
        #   - self.weekLabel, self.daysLayout, self.prevButton, self.nextButton, self.backButton

        # Connect the navigation buttons.
        self.prevButton.clicked.connect(lambda: self.change_week(-1))
        self.nextButton.clicked.connect(lambda: self.change_week(1))
        self.backButton.clicked.connect(lambda: self.navigator.navigate_to("userHome", self.user))

        # Initial week offset.
        self.offset_weeks = 0

    def update_page(self, user):
        self.user = user
        self.update_week()

    def get_week_dates(self):
        today = date.today() + timedelta(weeks=self.offset_weeks)
        monday = today - timedelta(days=today.weekday())
        return [monday + timedelta(days=i) for i in range(7)]

    def update_week(self):
        # Clear the daysLayout.
        for i in reversed(range(self.daysLayout.count())):
            widget = self.daysLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        week = self.get_week_dates()
        self.weekLabel.setText(f"Week of {week[0].strftime('%b %d, %Y')}")

        # Get chore counts for the week.
        chore_counts = get_chore_dates_in_week(week[0], self.user.Id)

        # Dynamically create buttons for each day.
        for day in week:
            count = chore_counts.get(day, 0)
            label = f"{day.strftime('%a')}\n{day.strftime('%b %d')}"
            if count > 0:
                label += f"\n🔵 {count} chores"
            btn = QPushButton(label)
            btn.setMinimumSize(100, 100)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 0px;
                }
            """)
            btn.clicked.connect(partial(self.handle_day_click, day.strftime("%Y-%m-%d")))
            self.daysLayout.addWidget(btn)

    def change_week(self, direction):
        self.offset_weeks += direction
        self.update_week()

    def handle_day_click(self, selected_date):
        self.navigator.navigate_to_selected_chore("DayLogPopup", self.user, selected_date)
