# books.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

class books(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.username = ""
        self.setup_ui()

    def set_user2(self, username):
        self.username = username

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

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search here")
        self.search_bar.setMinimumWidth(350)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.view_search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Book Name", "Author", "Rating", "Quantity Available"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(500)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_data()

        borrow_label = QLabel("Book Title:")
        self.borrow_bar = QLineEdit()
        self.borrow_bar.setPlaceholderText("Book title you want to borrow")
        borrow_button = QPushButton("Confirm Borrow")
        borrow_button.clicked.connect(self.insert_borrow)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_button)

        borrow_layout = QHBoxLayout()
        borrow_layout.addWidget(borrow_label)
        borrow_layout.addWidget(self.borrow_bar)
        borrow_layout.addWidget(borrow_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.table)
        main_layout.addStretch(1)
        main_layout.addLayout(borrow_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def load_data(self):
        query = """
            SELECT title, author, ROUND(AVG(rating), 2), quantity
            FROM Books 
            LEFT JOIN Ratings ON Books.book_id = Ratings.book_id
            GROUP BY Books.book_id
        """
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 120)

    def view_search(self):
        title = self.search_bar.text().strip()
        if title:
            query = """
                SELECT title, author, ROUND(AVG(rating), 2), quantity
                FROM Books 
                LEFT JOIN Ratings ON Books.book_id = Ratings.book_id
                WHERE title LIKE ?
                GROUP BY Books.book_id
            """
            self.cursor.execute(query, ('%' + title + '%',))
            data = self.cursor.fetchall()
            self.table.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def insert_borrow(self):
        title = self.borrow_bar.text().strip()
        self.cursor.execute("SELECT nat_id FROM User WHERE user_name = ?", (self.username,))
        result = self.cursor.fetchone()
        if result is None:
            QMessageBox.warning(self, "Error", "User not found. Please login again.")
            return
        user_id = result[0]
        if title:
            self.cursor.execute("SELECT book_id, quantity FROM Books WHERE title = ?", (title,))
            book_data = self.cursor.fetchone()
            if not book_data:
                self.borrow_bar.clear()
                QMessageBox.critical(self, "Not Found", "Book not Found")
                self.borrow_bar.setPlaceholderText("Book not found")
            else:
                book_id, quantity = book_data
                if quantity <= 0:
                    QMessageBox.critical(self, "Not Available", "Book not available")
                    self.borrow_bar.clear()
                    self.borrow_bar.setPlaceholderText("Book not available")
                else:
                    self.cursor.execute(
                        "SELECT COUNT(*) FROM borrows_record WHERE book_id = ? AND nat_id = ? AND (status = 'borrowed' OR status = 'overdue')",
                        (book_id, user_id)
                    )
                    already_borrowed = self.cursor.fetchone()[0]
                    if already_borrowed > 0:
                        self.borrow_bar.clear()
                        QMessageBox.critical(self, "Failed", "You have already borrowed this book")
                        self.borrow_bar.setPlaceholderText("You have already borrowed this book")
                    else:
                        query = """
                            INSERT INTO borrows_record (book_id, nat_id, start_date, due_date, status)
                            VALUES (?, ?, DATE('now'), DATE('now', '+14 days'), 'borrowed')
                        """
                        try:
                            self.cursor.execute(query, (book_id, user_id))
                            new_quantity = max(0, quantity - 1)
                            self.cursor.execute("UPDATE Books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
                            self.cursor.connection.commit()
                            self.borrow_bar.clear()
                            self.borrow_bar.setPlaceholderText("Borrow successful")
                            QMessageBox.information(self, "Success", "Book successfully borrowed!")
                            self.load_data()
                        except Exception as e:
                            self.borrow_bar.setPlaceholderText(f"Error occurred: {e}")
        else:
            self.borrow_bar.setPlaceholderText("Enter a book title")
