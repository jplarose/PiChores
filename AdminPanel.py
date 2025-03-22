from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class AdminPanel(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        uic.loadUi("AdminPanel.ui", self)
        self.load_logs()

    def load_logs(self):
        """Load log data into the table."""
        from database import fetch_logs
        #logs = fetch_logs()

        #self.logTable.setRowCount(len(logs))
        #self.logTable.setColumnCount(4)
        #self.logTable.setHorizontalHeaderLabels(["ID", "Timestamp", "Page", "Action"])

        #for row_idx, row_data in enumerate(logs):
        #   for col_idx, col_data in enumerate(row_data):
        #        self.logTable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
