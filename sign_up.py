from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFontMetrics, QFont
import queries_to_DB_for_GUI as query


class SignUpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign up")

        self.login = QLineEdit()
        self.password = QLineEdit()
        self.sign_up_but = QPushButton("Sign up")

        font = QFont('Arial', 12)
        font_height = (QFontMetrics(font)).height()
        height_of_LineEdit = 2 * font_height

        self.login.setPlaceholderText("Login")
        self.login.setFont(font)
        self.login.setStyleSheet("background-color: white;")
        self.login.setFixedHeight(height_of_LineEdit)

        self.password.setPlaceholderText("Password")
        self.password.setFont(font)
        self.password.setStyleSheet("background-color: white;")
        self.password.setFixedHeight(height_of_LineEdit)

        self.sign_up_but.setFont(font)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.sign_up_but)

        self.setLayout(self.layout)

        self.sign_up_but.clicked.connect(self.sign_up)


    def sign_up(self):
        login_text = self.login.text()
        password_text = self.password.text()
        query.save_user(login_text, password_text)