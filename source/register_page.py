# register_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class RegisterPage(QWidget):
    def __init__(self, stacked, cursor):
        super().__init__()
        self.stackedWidget = stacked
        self.cursor = cursor
        self.setup_ui()

    def setup_ui(self):
        fname = QLabel("First name: ")
        lname = QLabel("Last name: ")
        uname = QLabel("Username: ")
        nid = QLabel("National ID: ")
        email = QLabel("Email: ")
        pwd = QLabel("Password: ")

        self.firstname = QLineEdit(self)
        self.firstname.setPlaceholderText("Enter your first name")

        self.lastname = QLineEdit(self)
        self.lastname.setPlaceholderText("Enter your last name")

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter your username")

        self.national = QLineEdit(self)
        self.national.setPlaceholderText("Enter your National ID")

        self.mail = QLineEdit(self)
        self.mail.setPlaceholderText("Enter your Email")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)

        for widget in (self.firstname, self.lastname, self.username, self.national, self.mail, self.password):
            widget.setMinimumWidth(400)

        reg_button = QPushButton("Register")
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        reg_button.clicked.connect(self.reg_check)

        grid = QGridLayout()
        grid.addWidget(fname, 0, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.firstname, 0, 1, alignment=Qt.AlignLeft)
        grid.addWidget(lname, 1, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.lastname, 1, 1, alignment=Qt.AlignLeft)
        grid.addWidget(uname, 2, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.username, 2, 1, alignment=Qt.AlignLeft)
        grid.addWidget(nid, 3, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.national, 3, 1, alignment=Qt.AlignLeft)
        grid.addWidget(email, 4, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.mail, 4, 1, alignment=Qt.AlignLeft)
        grid.addWidget(pwd, 5, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.password, 5, 1, alignment=Qt.AlignLeft)
        grid.setVerticalSpacing(40)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(back_button)
        hbox.addSpacing(60)
        hbox.addWidget(reg_button)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
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
                padding: 10px;
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

    def reg_check(self):
        first_name = self.firstname.text()
        last_name = self.lastname.text()
        username = self.username.text()
        national_id = self.national.text()
        email = self.mail.text()
        password = self.password.text()
        if not (first_name and last_name and username and national_id and email and password):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return
        query = "SELECT * FROM User WHERE nat_id = ? OR email = ? OR user_name = ?"
        self.cursor.execute(query, (national_id, email, username))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Error", "This user already exists!")
            return
        if len(national_id) != 14:
            QMessageBox.warning(self, "Error", "National id must be 14 characters")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Too short password\nPassword must be at least 6 characters")
            return
        try:
            insertq = "INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)"
            self.cursor.execute(insertq, (national_id, email, password, username, first_name, last_name))
            self.cursor.connection.commit()
            QMessageBox.information(self, "Success", "Registration successful!\nYou will be redirected to Login page")
            self.stackedWidget.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
