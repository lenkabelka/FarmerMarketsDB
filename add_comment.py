from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QDialog
from PyQt6.QtGui import QFontMetrics, QFont, QGuiApplication, QRegularExpressionValidator, QIcon
from PyQt6.QtCore import Qt, QRegularExpression
import queries_to_DB_for_GUI as query


class AddComment(QDialog):
    def __init__(self, user_name, market_fmid, market_name):
        super().__init__()

        self.setWindowTitle("Add comment")
        self.setWindowIcon(QIcon("pig.ico"))

        self.user_name = user_name
        self.market_fmid = market_fmid

        screen_size = QGuiApplication.primaryScreen().size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()
        width_coef = 0.3    #coefizient for width of Add Comment window
        height_coef = 0.2   #coefizient for height of Add Comment window

        button_style = """
            QPushButton {
                padding-left: 20px;
                padding-right: 20px;
                padding-top: 10px;
                padding-bottom: 10px;
                background-color: lightgrey;
                border-radius: 10px;
                border: 2px solid #8ea688;
            }
            QPushButton:hover {
                background-color: lightblue;
                border: 2px solid #8ea688;
            }
            QPushButton:pressed {
                background-color: #8ea688;
                border: 2px solid #8ea688;
            }
        """

        text_field_style = """
            QTextEdit {
                border: 2px solid #8ea688;
                border-radius: 5px;
                background-color: white;
            }
        """

        lineedit_style = """
            QLineEdit {
                padding-top: 10px;
                padding-bottom: 10px;
                border: 2px solid #8ea688;
                border-radius: 5px;
                background-color: white;
                font-family: Arial;
                font-size: 20px;
                font-weight: bold;
            }
        """

        font = QFont('Arial', 14)

        self.layout = QVBoxLayout()

        self.name_of_market = QLabel(f"Name of market: {market_name}")
        self.name_of_market.setFont(font)
        self.market_mark = 0

        self.market_mark = QLineEdit()
        self.market_mark.setPlaceholderText("Give a mark to the market (1: very bad - 5: very good)")
        self.market_mark.setStyleSheet(lineedit_style)
        regex = QRegularExpression("[1-5]")
        validator = QRegularExpressionValidator(regex)
        self.market_mark.setValidator(validator)

        self.comment_text = QTextEdit()
        self.comment_text.setStyleSheet(text_field_style)
        self.comment_text.setMinimumSize(int(screen_width * width_coef), int(screen_height * height_coef))

        self.add_comment_but = QPushButton("Add comment")
        self.add_comment_but.setFont(font)
        self.setStyleSheet(button_style)

        self.layout.addWidget(self.name_of_market)
        self.layout.addWidget(self.market_mark)
        self.layout.addWidget(self.comment_text)
        self.layout.addWidget(self.add_comment_but)

        self.setLayout(self.layout)

        self.add_comment_but.clicked.connect(self.add_comment)


    def add_comment(self):
        if not self.comment_text.toPlainText():
             QMessageBox.warning(self, "Error", "Comment text cannot be empty!")
        elif not self.market_mark.text():
            QMessageBox.warning(self, "Error", "Please, give a mark to the market!")
        else:
             query.save_comment(self.market_fmid, self.user_name, int(self.market_mark.text()), self.comment_text.toPlainText())
             self.close()