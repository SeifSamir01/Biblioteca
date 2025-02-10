# first_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class FirstPage(QWidget):
    def __init__(self, stacked):
        super().__init__()
        self.stackedWidget = stacked
        self.setup_ui()

    def setup_ui(self):
        label1 = QLabel("Welcome To Minuf Library")
        label1.setAlignment(Qt.AlignCenter)

        login_button = QPushButton("Login")
        register_button = QPushButton("Register")

        login_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        register_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

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
                font-size: 40px;
                font-family: Arial;
                font-weight: bold;
                background-color: green;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
        """)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(login_button)
        hbox.addSpacing(60)
        hbox.addWidget(register_button)
        hbox.addStretch(1)

        vbox.addStretch(1)
        vbox.addWidget(label1)
        vbox.addSpacing(50)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)
