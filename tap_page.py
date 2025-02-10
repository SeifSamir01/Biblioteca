# tap_page.py
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from homePage import home
from books import books
from borrowing import borrow
from fines import fine

class TapPages(QWidget):
    def __init__(self, stacked, cursor, session):
        super().__init__()
        self.stackedWidget = stacked
        self.cursor = cursor
        self.session = session
        self.username = ""
        self.setup_ui()

    def setup_ui(self):
        self.tabs = QTabWidget(self)
        self.page1 = home(self.cursor, self.stackedWidget)
        self.page2 = books(self.cursor)
        self.page3 = borrow(self.cursor)
        self.page4 = fine(self.cursor)
        self.tabs.addTab(self.page1, "Home")
        self.tabs.addTab(self.page2, "Books")
        self.tabs.addTab(self.page3, "Borrow")
        self.tabs.addTab(self.page4, "Fines")
        self.tabs.currentChanged.connect(self.tabchange)
        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        self.setLayout(vbox)
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                top: -1px; 
            }
            QTabWidget::tab-bar {
                alignment: center; 
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                padding: 2px 10px;
                min-height: 40px;
                min-width: 200px;
                font-size: 22px;
                border-radius: 10px;
            }
            QTabBar::tab:selected {
                background-color: hsl(247, 59%, 38%);
                color: white;
                border: 1px solid #4CAF50;
            }
            QTabBar::tab:hover {
                background-color: hsl(247, 59%, 60%);
            }
            QLabel {
                font-size: 20px;
                font-family: Arial;
            }
        """)

    def tabchange(self, index):
        if index == 1:
            self.page2.load_data()
        elif index == 2:
            self.page3.load_data()
        elif index == 3:
            self.page4.load_data()

    def set_user(self, username):
        self.username = username
        self.cursor.execute("SELECT nat_id FROM User WHERE user_name = ?", (username,))
        user_data = self.cursor.fetchone()
        if user_data:
            user_id = user_data[0]
            self.page1.set_user1(username)
            self.page2.set_user2(username)
            self.page3.set_user3(username, user_id)
            self.page4.set_user4(username, user_id)
