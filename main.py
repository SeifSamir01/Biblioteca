# main.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys, sqlite3

from first_page import FirstPage
from login_page import LoginPage
from register_page import RegisterPage
from tap_page import TapPages
from session import Session

class Mainwin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 1200, 800)
        self.setWindowTitle("Minuf Library")
        self.setWindowIcon(QIcon("menofia.jpeg"))
        self.connection = sqlite3.connect("library.db")
        self.cursor = self.connection.cursor()
        self.session = Session()  # Create our centralized session object
        self.objects()

    def objects(self):
        self.stacked = QStackedWidget()
        # Pass the session to pages that require it
        self.tab_p = TapPages(self.stacked, self.cursor, self.session)
        self.stacked.addWidget(FirstPage(self.stacked))
        self.stacked.addWidget(LoginPage(self.stacked, self.cursor, self.tab_p, self.session))
        self.stacked.addWidget(RegisterPage(self.stacked, self.cursor))
        self.stacked.addWidget(self.tab_p)
        self.setCentralWidget(self.stacked)

app = QApplication(sys.argv)
win = Mainwin()
win.show()
sys.exit(app.exec_())
