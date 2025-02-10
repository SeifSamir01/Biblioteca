# fines.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class fine(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.username = ""
        self.user_id = ""
        self.setup_ui()

    def set_user4(self, username, uid):
        self.username = username
        self.user_id = uid

    def setup_ui(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #005cbf;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004494;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #005cbf;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Fine ID", "Fine", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(500)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        finelabel = QLabel("FINE ID: ")
        self.finebar = QLineEdit()
        self.finebar.setPlaceholderText("Enter fine id")

        pay_button = QPushButton("Confirm Pay")
        pay_button.clicked.connect(self.pay)

        pay_layout = QHBoxLayout()
        pay_layout.addWidget(finelabel)
        pay_layout.addWidget(self.finebar)
        pay_layout.addWidget(pay_button)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(self.table)
        main_layout.addStretch(1)
        main_layout.addLayout(pay_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def load_data(self):
        self.cursor.execute("SELECT * FROM Fines WHERE nat_id = ?", (self.user_id,))
        fines = self.cursor.fetchall()

        self.table.setRowCount(len(fines))
        for i, fine in enumerate(fines):
            fine_id, nat_id, amount, paid = fine
            amount_display = f"{amount} EGP" if amount else "Not determined yet"
            self.table.setItem(i, 0, QTableWidgetItem(str(fine_id)))
            self.table.setItem(i, 1, QTableWidgetItem(amount_display))
            self.table.setItem(i, 2, QTableWidgetItem("Paid" if paid == "true" else "Unpaid"))

        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 300)

    def pay(self):
        fine_id = self.finebar.text().strip()
        if not fine_id.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid Fine ID!")
            return

        self.cursor.execute("SELECT paid FROM Fines WHERE fine_id = ?", (fine_id,))
        result = self.cursor.fetchone()
        if not result:
            QMessageBox.warning(self, "Not Found", "Fine ID not found!")
            return

        paid_status = result[0]
        if paid_status == "true":
            QMessageBox.information(self, "Already Paid", "This fine is already marked as paid.")
            return

        self.cursor.execute("UPDATE Fines SET paid = 'true' WHERE fine_id = ?", (fine_id,))
        self.cursor.connection.commit()
        QMessageBox.information(self, "Success", "Payment confirmed successfully!")
        self.load_data()
