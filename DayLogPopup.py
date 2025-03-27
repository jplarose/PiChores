from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QWidget, QHBoxLayout, QPushButton, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt

from ChoreLog import clear_layout
from database import fetch_chores_for_date, delete_chore_by_id

class DayLogPopup(QDialog):
    def __init__(self, navigator):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.list_widget = None
        self.label = None
        self.selected_date = None
        self.back_button = None
        self.navigator = navigator
        self.setMinimumSize(800, 480)
        self.setMaximumSize(800, 480)

        self.user = None

    def update_page(self, user, selected_date):
        self.user = user
        self.selected_date = selected_date

        # Clear current layout contents
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Rebuild widgets
        self.label = QLabel(f"Chores for {selected_date}")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.back_button = QPushButton("← Back")
        self.back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.load_chores()

    def load_chores(self):
        self.list_widget.clear()
        chores = fetch_chores_for_date(self.selected_date, self.user.Id)

        if not chores:
            self.list_widget.addItem(QListWidgetItem("No chores logged for this day."))
            return

        for chore_id, description, timestamp in chores:
            item_widget = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(10, 5, 10, 5)

            label = QLabel(f"{description} @ {timestamp}")
            label.setStyleSheet("font-size: 16px;")
            row_layout.addWidget(label)

            delete_btn = QPushButton("❌")
            delete_btn.setFixedSize(40, 40)
            delete_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #ff6666;
                    border: none;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #ff4444;
                }
            """)
            delete_btn.clicked.connect(lambda _, cid=chore_id: self.delete_chore(cid))

            row_layout.addWidget(delete_btn)
            item_widget.setLayout(row_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

    def delete_chore(self, chore_id):
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this chore?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_chore_by_id(chore_id)
            self.load_chores()  # Reload list after deletion

    def go_back(self):
        self.navigator.navigate_to("UserLoggedChores", self.user)

    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

