from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from database import get_users, get_admin

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)

class UserPage(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        uic.loadUi("UserPage.ui", self)
        self.admin = None

        # Flag to indicate that the long press action has been triggered.
        self.long_press_triggered = False



    def update_page(self, user, is_admin):
        self.load_users(is_admin)


    def load_users(self, is_admin=False):
        """Dynamically load user buttons into the scrollable area."""
        if is_admin:
            users = get_admin()
        else:
            users = get_users()

        layout = self.findChild(QVBoxLayout, "userLayout")

        # Make sure to load fresh each time
        clear_layout(layout)

        for index, user in enumerate(users):
            btn = QPushButton(user.Name)
            btn.setFixedHeight(160)
            btn.setStyleSheet("font-size: 35px; font-weight: bold")

            if index == 0 and not is_admin:
                # 5 second long press to access Admin login page
                timer = QtCore.QTimer(btn)
                timer.setSingleShot(True)
                timer.setInterval(5000)  # 5 seconds

                def start_timer():
                    self.long_press_triggered = False
                    timer.start()

                def stop_timer():
                    # If the timer is still active when released, stop it.
                    if timer.isActive():
                        timer.stop()

                def on_timeout():
                    self.long_press_triggered = True
                    # Trigger admin sign in after 5 seconds
                    self.navigator.navigate_to_admin("userPage", None, True)

                # Connect the button's pressed and released signals.
                btn.pressed.connect(start_timer)
                btn.released.connect(stop_timer)
                timer.timeout.connect(on_timeout)

                # Override the clicked action.
                # If the long press did not trigger, then process the normal user action.
                btn.clicked.connect(lambda checked, u=user:
                    None if self.long_press_triggered
                         else self.navigator.navigate_to("authPage", u)
                )
            else:
                btn.clicked.connect(lambda checked, u=user: self.navigator.navigate_to("authPage", u))
            layout.addWidget(btn)


    def load_admin(self):
        admins = get_admin()
        self.admin = admins[0]
