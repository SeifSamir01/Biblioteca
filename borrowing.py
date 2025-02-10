# borrowing.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class borrow(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.username = ""
        self.user_id = ""
        self.setup_ui()

    def set_user3(self, username, uid):
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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Book Name", "Start Borrow Date", "Due Date", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(500)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Build the rating area
        title_label = QLabel("Book Title:")
        self.title_bar = QLineEdit()
        self.title_bar.setPlaceholderText("Book title you want to rate")
        self.rate_bar = QLineEdit()
        self.rate_bar.setPlaceholderText("your rating")
        rate_button = QPushButton("Confirm rate")
        rate_button.clicked.connect(self.insert_rate)

        rate_layout = QHBoxLayout()
        rate_layout.addWidget(title_label)
        rate_layout.addWidget(self.title_bar)
        rate_layout.addWidget(self.rate_bar)
        rate_layout.addWidget(rate_button)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(self.table)
        main_layout.addStretch(1)
        main_layout.addLayout(rate_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def load_data(self):
        # First, update overdue status
        self.cursor.execute("""
            UPDATE borrows_record
            SET status = 'overdue'
            WHERE status = 'borrowed' AND julianday('now') >= julianday(due_date)
        """)
        self.cursor.connection.commit()

        query = """
            SELECT title, start_date, due_date, status
            FROM Books
            JOIN borrows_record ON Books.book_id = borrows_record.book_id
            WHERE nat_id = ?
        """
        self.cursor.execute(query, (self.user_id,))
        data = self.cursor.fetchall()

        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 120)

    def insert_rate(self):
        title = self.title_bar.text().strip()
        rate_text = self.rate_bar.text().strip()

        if not title:
            self.title_bar.clear()
            self.title_bar.setPlaceholderText("You must insert a book title")
            return

        try:
            rate = float(rate_text)
        except ValueError:
            self.rate_bar.clear()
            self.rate_bar.setPlaceholderText("Rating must be a number between 1 and 5")
            return

        if rate < 1 or rate > 5:
            self.rate_bar.clear()
            self.rate_bar.setPlaceholderText("Rating must be between 1 and 5")
            return

        query = """
            SELECT Books.book_id 
            FROM Books 
            JOIN borrows_record ON Books.book_id = borrows_record.book_id 
            WHERE Books.title = ? AND borrows_record.nat_id = ?
        """
        self.cursor.execute(query, (title, self.user_id))
        book = self.cursor.fetchone()

        if not book:
            self.title_bar.clear()
            self.title_bar.setPlaceholderText("You can only rate books you have borrowed")
            return

        book_id = book[0]

        query_check_rating = """
            SELECT * FROM Ratings 
            WHERE book_id = ? AND nat_id = ?
        """
        self.cursor.execute(query_check_rating, (book_id, self.user_id))
        existing_rating = self.cursor.fetchone()

        if existing_rating:
            self.title_bar.clear()
            self.title_bar.setPlaceholderText("You have already rated this book")
            QMessageBox.information(self, "Already rated", "You have already rated this book")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Ratings (rating, book_id, nat_id) VALUES (?, ?, ?)",
                (rate, book_id, self.user_id)
            )
            self.cursor.connection.commit()
            QMessageBox.information(self, "Success", "Rating successfully added!")
            self.title_bar.clear()
            self.title_bar.setPlaceholderText("Book title you want to rate")
            self.rate_bar.clear()
            self.rate_bar.setPlaceholderText("your rating")
        except Exception as e:
            QMessageBox.critical(self, "Error", "Failed to add rating. Please try again.")
