from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from NavigationManager import NavigationManager
from UserPage import UserPage
from AuthPage import AuthPage
from UserHome import UserHome
from AdminPanel import AdminPanel
from ChoreLog import ChoreLog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chores App")
        self.setGeometry(100, 100, 800, 480)  # Exact touchscreen dimensions

        self.navigator = NavigationManager()

        # Initialize all pages
        userPage = UserPage(self.navigator)
        authPage = AuthPage(self.navigator)
        userHome = UserHome(self.navigator)
        adminAuthPage = AuthPage(self.navigator)
        adminPanel = AdminPanel(self.navigator)
        choreLog = ChoreLog(self.navigator)

        # Register pages in the navigation system
        self.navigator.add_page("userPage", userPage)
        self.navigator.add_page("authPage", authPage)
        self.navigator.add_page("userHome", userHome)
        self.navigator.add_page("AdminAuthPage", adminAuthPage)
        self.navigator.add_page("AdminPanel", adminPanel)
        self.navigator.add_page("ChoreLog", choreLog)

        # Start on UserPage
        self.navigator.navigate_to("userPage")

        layout = QVBoxLayout()
        layout.addWidget(self.navigator)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
#    window.showFullScreen()  # Runs in fullscreen mode for the touchscreen
    window.show()
    app.exec_()
