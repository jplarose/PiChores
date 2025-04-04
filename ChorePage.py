from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox
from database import log_chore, log_action, was_chore_logged_recently
from datetime import date

class ChorePage(QWidget):
    """Page for adding completed chores to your record"""
    def __init__(self, navigator):
        super().__init__()
        self.user = None
        self.chore = None

        self.navigator = navigator
        uic.loadUi("ChorePage.ui", self)

        self.go_back_button.clicked.connect(lambda: self.handle_go_back())
        self.log_button.clicked.connect(lambda: self.handle_log_chore())

    def update_page(self, user, chore):
        """Populate the page with the chore information"""
        self.user = user
        self.chore = chore

        self.chore_name_label.setText(chore.Name)
        self.frequency_label.setText(chore.Frequency)

    def handle_go_back(self):
        """Clear labels and navigate to the previous page"""
        self.chore_name_label.setText("")
        self.frequency_label.setText("")

        self.navigator.navigate_to("ChoreLog", self.user)

    def handle_log_chore(self):
        """Controller method: orchestrates the logging of a chore"""
        selected_pydate, selected_date_str = self.get_selected_date()

        if not self.confirm_future_date(selected_pydate, selected_date_str):
            return

        if not self.check_and_confirm_frequency(selected_pydate, selected_date_str):
            return

        self.log_chore_and_notify(selected_date_str)

    def get_selected_date(self):
        qdate = self.chore_calendar.selectedDate()
        pydate = qdate.toPyDate()
        date_str = pydate.strftime("%Y-%m-%d %H:%M")
        return pydate, date_str

    def confirm_future_date(self, selected_pydate, date_str):
        if selected_pydate > date.today():
            confirm_box = QMessageBox(self)

            # Remove the title bar and window frame
            confirm_box.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
            # Increase font sizes and button padding for touch friendliness
            confirm_box.setStyleSheet("""
                QLabel { font-size: 20pt; }
                QPushButton { font-size: 20pt; padding: 15px 25px; }
                QMessageBox { background-color: white; }
            """)

            confirm_box.setIcon(QMessageBox.Question)
            confirm_box.setWindowTitle("Future Date Selected")
            confirm_box.setText(
                "You selected a date in the future.\n"
                "Are you sure you want to log this chore for that date?"
            )
            confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if confirm_box.exec_() == QMessageBox.No:
                return False

            log_action(self.user.Id, "ConfirmFutureChoreLog",
                       f"User confirmed future date chore log for Chore Id {self.chore.Id} on {date_str}")
        return True

    def check_and_confirm_frequency(self, selected_pydate, date_str):
        freq = self.chore.Frequency.lower()
        if freq in ["daily", "weekly"]:
            already_logged = was_chore_logged_recently(
                self.user.Id, self.chore.Id, selected_pydate, freq)

            if already_logged:
                repeat_box = QMessageBox(self)

                # Remove the title bar and window frame
                repeat_box.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
                # Increase font sizes and button padding for touch friendliness
                repeat_box.setStyleSheet("""
                    QLabel { font-size: 20pt; }
                    QPushButton { font-size: 20pt; padding: 15px 25px; }
                    QMessageBox { background-color: white; }
                """)

                repeat_box.setIcon(QMessageBox.Warning)
                repeat_box.setWindowTitle("Chore Already Logged")
                repeat_box.setText(
                    f"This chore has already been logged this {freq}.\n"
                    "Are you sure you want to log it again?"
                )
                repeat_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                if repeat_box.exec_() == QMessageBox.No:
                    return False

                log_action(self.user.Id, "ConfirmRepeatChoreLog",
                           f"User confirmed repeat log of Chore Id {self.chore.Id} on {date_str} (Frequency: {self.chore.Frequency})")
        return True

    def log_chore_and_notify(self, date_str):
        result = log_chore(self.user.Id, self.chore.Id, date_str)
        msg = QMessageBox(self)

        # Remove the title bar and window frame
        msg.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        # Increase font sizes and button padding for touch friendliness
        msg.setStyleSheet("""
            QLabel { font-size: 20pt; }
            QPushButton { font-size: 20pt; padding: 15px 25px; }
            QMessageBox { background-color: white; }
        """)

        if result is not True:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Chore Log Failed")
            msg.setText("There was an error logging the chore, please try again.")
            msg.setStandardButtons(QMessageBox.Close)
            log_action(self.user.Id, "LogChore",
                       f"Error logging Chore Id {self.chore.Id}: {result}")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Chore Logged")
            msg.setText("Chore has been successfully logged!")
            msg.setStandardButtons(QMessageBox.Ok)
            log_action(self.user.Id, "LogChore",
                       f"Chore Id {self.chore.Id} logged successfully for {date_str}.")

        msg.exec_()
        self.navigator.navigate_to("ChoreLog", self.user)
