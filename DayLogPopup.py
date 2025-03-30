from PyQt5.QtWidgets import QDialog, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from database import fetch_chores_for_date, delete_chore_by_id

class DayLogPopup(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.user = None
        self.selected_date = None

        # Load the UI from the .ui file.
        uic.loadUi("DayLogPopup.ui", self)

        # The following widgets are now defined in the .ui file:
        #   self.headerLabel, self.listWidget, self.backButton

        # Connect the back button.
        self.backButton.clicked.connect(self.go_back)

        # Set fixed size.
        self.setMinimumSize(800, 480)
        self.setMaximumSize(800, 480)

    def update_page(self, user, selected_date):
        self.user = user
        self.selected_date = selected_date

        # Update the header label with the selected date.
        self.headerLabel.setText(f"Chores for {selected_date}")

        # Load the chores dynamically.
        self.load_chores()

    def load_chores(self):
        self.listWidget.clear()
        chores = fetch_chores_for_date(self.selected_date, self.user.Id)

        if not chores:
            self.listWidget.addItem(QListWidgetItem("No chores logged for this day."))
            return

        for chore_log_id, description, timestamp in chores:
            # Create a custom widget for the list item.
            item_widget = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(10, 5, 10, 5)

            # Create a label to show chore description and timestamp.
            label = QLabel(f"{description} @ {timestamp}")
            label.setStyleSheet("font-size: 16px;")
            row_layout.addWidget(label)

            # Create a delete button.
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
            delete_btn.clicked.connect(lambda _, cid=chore_log_id: self.delete_chore(cid))
            row_layout.addWidget(delete_btn)

            item_widget.setLayout(row_layout)

            # Create a QListWidgetItem and set its size hint.
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, item_widget)

    def delete_chore(self, chore_log_id):
        delete_confirm_box = QMessageBox(self)

        # Remove the title bar and window frame
        delete_confirm_box.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        # Increase font sizes and button padding for touch friendliness
        delete_confirm_box.setStyleSheet("""
                    QLabel { font-size: 20pt; }
                    QPushButton { font-size: 20pt; padding: 15px 25px; }
                    QMessageBox { background-color: white; }
                """)
        delete_confirm_box.setIcon(QMessageBox.Warning)
        delete_confirm_box.setWindowTitle("Delete?")
        delete_confirm_box.setText("Are you sure you want to delete this chore?")
        delete_confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if delete_confirm_box.exec_() == QMessageBox.Yes:
            delete_chore_by_id(chore_log_id)
            self.load_chores()  # Reload the list after deletion.

    def go_back(self):
        self.navigator.navigate_to("UserLoggedChores", self.user)
