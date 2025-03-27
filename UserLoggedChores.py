from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
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

        uic.loadUi("UserLoggedChores.ui", self)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Header label
        self.weekLabel = QLabel("This Week")
        self.weekLabel.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.layout.addWidget(self.weekLabel, alignment=Qt.AlignCenter)

        # Layout for days
        self.daysLayout = QHBoxLayout()
        self.layout.addLayout(self.daysLayout)

        # Navigation buttons
        self.navLayout = QHBoxLayout()
        self.prevButton = QPushButton("← Previous Week")
        self.nextButton = QPushButton("Next Week →")
        self.navLayout.addWidget(self.prevButton)
        self.navLayout.addWidget(self.nextButton)
        self.layout.addLayout(self.navLayout)
        self.backButton = QPushButton("← Back to Home")
        self.backButton.setStyleSheet("font-size: 18px; padding: 10px;")
        self.backButton.clicked.connect(lambda: self.navigator.navigate_to("userHome", self.user))
        self.layout.addWidget(self.backButton, alignment=Qt.AlignRight)

        # Event handling
        self.prevButton.clicked.connect(lambda: self.change_week(-1))
        self.nextButton.clicked.connect(lambda: self.change_week(1))

        # Initial week
        self.offset_weeks = 0


    def update_page(self, user):
        self.user = user

        self.update_week()

    def get_week_dates(self):
        today = date.today() + timedelta(weeks=self.offset_weeks)
        monday = today - timedelta(days=today.weekday())
        return [monday + timedelta(days=i) for i in range(7)]

    def update_week(self):
        # Clear layout
        for i in reversed(range(self.daysLayout.count())):
            widget = self.daysLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        week = self.get_week_dates()
        self.weekLabel.setText(f"Week of {week[0].strftime('%b %d, %Y')}")

        # Get chore counts
        chore_counts = get_chore_dates_in_week(week[0], self.user.Id)

        for day in week:
            count = chore_counts.get(day, 0)
            label = f"{day.strftime('%a')}\n{day.strftime('%b %d')}"
            if count > 0:
                label += f"\n🔵 {count} chores"

            btn = QPushButton(label)
            btn.setMinimumSize(120, 120)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 10px;
                }
            """)
            btn.clicked.connect(partial(self.handle_day_click, day.strftime("%Y-%m-%d")))
            self.daysLayout.addWidget(btn)

    # def update_week(self):
    #     # Clear layout
    #     for i in reversed(range(self.daysLayout.count())):
    #         widget = self.daysLayout.itemAt(i).widget()
    #         if widget:
    #             widget.setParent(None)
    #
    #     week = self.get_week_dates()
    #     self.weekLabel.setText(f"Week of {week[0].strftime('%b %d, %Y')}")
    #
    #     # Get dates with chores
    #     chore_days = get_chore_dates_in_week(week[0])
    #
    #     for day in week:
    #         label = day.strftime("%a\n%b %d")
    #         if day in chore_days:
    #             label += "\n🔵"  # Or use a styled dot
    #
    #         btn = QPushButton(label)
    #         btn.setMinimumSize(100, 80)
    #         btn.setStyleSheet("font-size: 16px;")
    #         btn.clicked.connect(partial(self.handle_day_click, day.strftime("%Y-%m-%d %H:%M")))
    #         self.daysLayout.addWidget(btn)

    def change_week(self, direction):
        self.offset_weeks += direction
        self.update_week()

    def handle_day_click(self, selected_date):
        self.navigator.navigate_to_selected_chore("DayLogPopup", self.user, selected_date)

