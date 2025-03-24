from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from database import get_users_chores

class ChoreLog(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.user = None
        self.navigator = navigator
        uic.loadUi("ChoreLog.ui", self)

        self.GoBackButton.clicked.connect(lambda: self.handle_go_back())

    def update_page(self, user):
        """Get The chores for this user"""
        self.user = user

        chores = get_users_chores(self.user.id)

        layout = self.findChild(QGridLayout, "choreButtonGridLayout")
        for i, chore in enumerate(chores):
            btn = QPushButton(chore.Name)
            btn.setFixedHeight(80)  # Large button for touchscreens
            btn.clicked.connect(lambda _, c=chore: self.navigator.navigate_to_chore("authPage", self.user, c))
            row = i // 3  # 3 buttons per row
            col = i % 3
            layout.addWidget(btn, row, col)

        #for chore in chores:
            #btn = QPushButton(chore.Name)
            # btn.setFixedHeight(80)  # Large button for touchscreens
            #btn.clicked.connect(lambda: self.navigator.navigate_to_chore("authPage", self.user, chore))
            #layout.addWidget(btn)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def handle_go_back(self):
        layout = self.findChild(QGridLayout, "choreButtonGridLayout")
        self.clear_layout(layout)
        self.navigator.navigate_to("userHome", self.user)


