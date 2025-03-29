from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtCore
from NavigationManager import NavigationManager
from UserPage import UserPage
from AuthPage import AuthPage
from UserHome import UserHome
from AdminPanel import AdminPanel
from ChoreLog import ChoreLog
from ChorePage import ChorePage
from UserLoggedChores import UserLoggedChores
from DayLogPopup import DayLogPopup
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chores App")
        self.setGeometry(0, 0, 800, 480)  # Exact touchscreen dimensions

        self.navigator = NavigationManager()

        # Initialize all pages
        userPage = UserPage(self.navigator)
        authPage = AuthPage(self.navigator)
        userHome = UserHome(self.navigator)
        adminAuthPage = AuthPage(self.navigator)
        adminPanel = AdminPanel(self.navigator)
        choreLog = ChoreLog(self.navigator)
        chorePage = ChorePage(self.navigator)
        userLoggedChores = UserLoggedChores(self.navigator)
        dayLogPopup = DayLogPopup(self.navigator)

        # Register pages in the navigation system
        self.navigator.add_page("userPage", userPage)
        self.navigator.add_page("authPage", authPage)
        self.navigator.add_page("userHome", userHome)
        self.navigator.add_page("AdminAuthPage", adminAuthPage)
        self.navigator.add_page("AdminPanel", adminPanel)
        self.navigator.add_page("ChoreLog", choreLog)
        self.navigator.add_page("ChorePage", chorePage)
        self.navigator.add_page("UserLoggedChores", userLoggedChores)
        self.navigator.add_page("DayLogPopup", dayLogPopup)

        # Start on UserPage
        self.navigator.navigate_to("userPage")

        layout = QVBoxLayout()
        layout.addWidget(self.navigator)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
   # app.setOverrideCursor(QtCore.Qt.BlankCursor)
    window = MainWindow()
   # window.showFullScreen()  # Runs in fullscreen mode for the touchscreen
    window.show()
    window.setFixedSize(800, 480)
    window.move(0,0)
    app.exec_()
