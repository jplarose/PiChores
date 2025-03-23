from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class ChoreLog(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        uic.loadUi("ChoreLog.ui", self)

        self.GoBackButton.clicked.connect(lambda:self.handle_go_back)

    def update_page(self, user):
        # Get The chores for this user

        # Then populate the buttons in the grid layout


    def handle_go_back():
        self.navigator.navigate_to("userHome", self.user)
