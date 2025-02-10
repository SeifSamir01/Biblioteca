# login_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class LoginPage(QWidget):
    def __init__(self, stacked, cursor, tab_page, session):
        super().__init__()
        self.stackedWidget = stacked
        self.cursor = cursor
        self.tab_p = tab_page
        self.session = session
        self.setup_ui()

    def setup_ui(self):
        label1 = QLabel("Username: ")
        label2 = QLabel("Password: ")

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("your username goes here")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("your password goes here")
        self.password.setEchoMode(QLineEdit.Password)

        self.username.setMinimumWidth(300)
        self.password.setMinimumWidth(300)

        login_button = QPushButton("Login")
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        login_button.clicked.connect(self.login_check)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(label1)
        hbox1.addSpacing(20)
        hbox1.addWidget(self.username)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(label2)
        hbox2.addSpacing(20)
        hbox2.addWidget(self.password)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(back_button)
        hbox3.addSpacing(60)
        hbox3.addWidget(login_button)
        hbox3.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addSpacing(50)
        vbox.addLayout(hbox2)
        vbox.addSpacing(50)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.setStyleSheet("""
            QPushButton{
                font-size: 35px;
                font-family: Arial;
                border-radius: 10px;
                background-color: hsl(247, 59%, 38%);
                color: white;
                padding: 10px 20px;
            }
            QPushButton:hover{
                background-color: hsl(247, 59%, 60%);
            }
            QLabel{
                font-size: 35px;
                font-family: Arial; 
            }
            QLineEdit{
                font-size: 20px;
                font-family: Arial;
                border: 2px solid green;
                border-radius: 5px;
                padding: 5px;
                text-align: center;
            }
        """)

    def login_check(self):
        user_input = self.username.text()
        pass_input = self.password.text()
        if not user_input or not pass_input:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        query = "SELECT user_name, password FROM User WHERE user_name = ? AND password = ?"
        self.cursor.execute(query, (user_input, pass_input))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.information(self, "Login Successful", "Welcome to Minuf Library!")
            self.username.clear()
            self.password.clear()
            self.username.setPlaceholderText("your username goes here")
            self.password.setPlaceholderText("your password goes here")
            # Store the current user in the session
            self.session.set_user(user_input)
            # Update the tab pages with the logged-in user
            self.tab_p.set_user(user_input)
            self.stackedWidget.setCurrentIndex(3)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
