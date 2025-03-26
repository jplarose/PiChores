from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from database import log_chore, log_action

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
        self.chore_name_label.setText()
        self.frequency_label.setText()

        self.navigator.navigate_to("ChoreLog", self.user)

    def handle_log_chore(self):
        """Send the selected chore and date to the DB"""
        selected_date = self.chore_calendar.selectedDate().toPyDate().strftime("%Y-%m-%d %H:%M")
        print(selected_date)
        result = log_chore(self.user.Id, self.chore.Id, selected_date)



        # Show confirmation message
        msg = QMessageBox(self)
        if result != True:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Chore Log Failed")
            msg.setText("There was an error logging the chore, please try again")
            msg.setStandardButtons(QMessageBox.Close)
            log_action(self.user.Id, "LogChore", f"Error logging Chore Id {self.chore.Id}: {result}")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Chore Logged")
            msg.setText("Chore has been successfully logged!")
            msg.setStandardButtons(QMessageBox.Ok)
            log_action(self.user.Id, "LogChore", f"Chore Id {self.chore.Id} logged successfully.")

        # Show the dialog and wait for user to press OK
        msg.exec_()

        # Navigate back to ChoreLog
        self.navigator.navigate_to("ChoreLog", self.user)
