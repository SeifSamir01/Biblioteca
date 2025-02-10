# homePage.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class home(QWidget):
    def __init__(self, cursor, stacked):
        super().__init__()
        self.cursor = cursor
        self.stackedWidget = stacked
        # These variables will be set in set_user1
        self.username = ""
        self.email = ""
        self.firstname = ""
        self.lastname = ""
        self.natid = ""

    def set_user1(self, username):
        self.username = username
        query = "SELECT * FROM User WHERE user_name = ?"
        self.cursor.execute(query, (self.username,))
        info = self.cursor.fetchone()
        if info:
            self.natid = info[0]
            self.email = info[1]
            self.firstname = info[4]
            self.lastname = info[5]
        # Build the UI to display user info
        label = QLabel("Welcome To Minuf Library")
        label.setAlignment(Qt.AlignCenter)
        userinfo = QLabel("User Info: ")
        fn = QLabel("First name: ")
        ln = QLabel("Last name: ")
        un = QLabel("User name: ")
        nid = QLabel("National ID: ")
        email_label = QLabel("Email: ")

        fn_value = QLabel(self.firstname)
        ln_value = QLabel(self.lastname)
        un_value = QLabel(self.username)
        nid_value = QLabel(self.natid)
        email_value = QLabel(self.email)
        label.setObjectName("label")
        userinfo.setObjectName("userinfo")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label)
        vbox.addStretch(1)
        vbox.addWidget(userinfo)

        grid_layout = QGridLayout()
        grid_layout.addWidget(fn, 0, 0)
        grid_layout.addWidget(fn_value, 0, 1)
        grid_layout.addWidget(ln, 1, 0)
        grid_layout.addWidget(ln_value, 1, 1)
        grid_layout.addWidget(un, 2, 0)
        grid_layout.addWidget(un_value, 2, 1)
        grid_layout.addWidget(nid, 3, 0)
        grid_layout.addWidget(nid_value, 3, 1)
        grid_layout.addWidget(email_label, 4, 0)
        grid_layout.addWidget(email_value, 4, 1)

        vbox.addLayout(grid_layout)
        vbox.addStretch(1)
        logout = QPushButton("Logout")
        logout.setMinimumWidth(150)
        logout.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(logout)
        hbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.setStyleSheet("""
            QLabel{
               color:black;
               font-size: 40px;
               font-family: Arial;
            }
            QLabel#label{
               color: white;
               background-color: green;
               padding: 10px;
               border-radius: 10px;
           }
            QLabel#userinfo{
               color: #b52ec9;
           }
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
        """)
