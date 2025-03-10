import sys
import sign_up as s
import queries_to_DB_for_GUI as q
from folium.plugins import FastMarkerCluster
import io
import folium
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QBoxLayout,
                             QLineEdit, QLabel, QListWidget, QFrame, QComboBox, QSizePolicy,
                             QHBoxLayout, QStackedLayout, QSpacerItem, QDialog, QMessageBox)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QFontMetrics, QFont, QRegularExpressionValidator
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Farmer's Markets")

        screen = QApplication.primaryScreen().geometry()
        coef_width = 0.8
        coef_height = 0.8
        window_width = int(screen.width() * coef_width)
        window_height = int(screen.height() * coef_height)
        self.resize(window_width, window_height)
        x = (screen.width() - window_width) // 2
        y = 0
        #y = (screen.height() - window_height) // 2
        self.move(x, y)

        self.user_name = ""
        self.password_hash = ""

        layout = QGridLayout()

        font = QFont('Arial', 12)
        font_height = (QFontMetrics(font)).height()
        height_of_LineEdit = 2 * font_height
        font_for_labels = QFont('Arial', 14)

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
            QListWidget {
                border: 2px solid #8ea688;
                border-radius: 5px;
                background-color: white;
            }
        """


        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: #8ea688;")
        self.head_layout = QHBoxLayout(self.frame)


        self.head_label_layout = QHBoxLayout()
        self.head_label = QLabel("Buy only healthy food in Farmer's markets!", self.frame)
        self.font_head_label = QFont('Comic Sans MS', 30)
        self.head_label.setFont(self.font_head_label)
        self.head_label_layout.addWidget(self.head_label)

        self.frame_login_view = QFrame(self.frame)
        self.frame_logout_view = QFrame(self.frame)
        self.frame_login_view.setStyleSheet("background-color: #8ea688;")
        self.frame_logout_view.setStyleSheet("background-color: #8ea688;")

        self.head_layout_log_in = QGridLayout(self.frame_login_view)
        self.head_layout_log_out = QGridLayout(self.frame_logout_view)
        self.stack_layout = QStackedLayout()

########### Log in view ####################################

        self.login = QLineEdit()
        self.login.setPlaceholderText("Login")
        self.login.setFont(font)
        self.login.setStyleSheet("background-color: white;")
        self.login.setFixedHeight(height_of_LineEdit)
        regex = QRegularExpression(r"^[a-zA-Z0-9_-]{0,25}$")
        validator = QRegularExpressionValidator(regex)
        self.login.setValidator(validator)

        self.login_label = QLabel()

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setFont(font)
        self.password.setStyleSheet("background-color: white;")
        self.password.setFixedHeight(height_of_LineEdit)

        self.login_button = QPushButton("Log in")
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("background-color: white;")

        self.sign_up_button = QPushButton("Sign up")
        self.sign_up_button.setFont(font)
        self.sign_up_button.setStyleSheet("background-color: white;")

        self.head_layout_log_in.addWidget(self.login, 0, 0, Qt.AlignmentFlag.AlignRight)
        self.head_layout_log_in.addWidget(self.password, 1, 0, Qt.AlignmentFlag.AlignRight)
        self.head_layout_log_in.addWidget(self.login_button, 2, 0, Qt.AlignmentFlag.AlignRight)
        self.head_layout_log_in.addWidget(self.sign_up_button, 3, 0, Qt.AlignmentFlag.AlignRight)

        self.stack_layout.addWidget(self.frame_login_view)


########### Log out view ####################################

        self.logout_button = QPushButton("Log out")
        self.logout_button.setFont(font)
        self.logout_button.setStyleSheet("background-color: white;")


        self.head_layout_log_out.addWidget(self.login_label, 0, 1, Qt.AlignmentFlag.AlignRight)
        self.head_layout_log_out.addWidget(self.logout_button, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.stack_layout.addWidget(self.frame_logout_view)

        self.head_layout.addLayout(self.head_label_layout)
        self.head_layout.addLayout(self.stack_layout)

#################################################################

        self.layout_left = QGridLayout()

        self.show_markets_button = QPushButton("Show all farmer's markets")
        self.show_markets_button.setFont(font)
        self.show_markets_button.setStyleSheet(button_style)
        self.layout_left.addWidget(self.show_markets_button, 1, 0, 1, 2)

        self.fmid_combo = QComboBox()
        self.fmid_combo.setPlaceholderText("FMID")
        self.fmid_combo.setFont(font)
        self.layout_left.addWidget(self.fmid_combo, 2, 0)
        self.fmid_combo.addItems(q.get_fmids())

        self.show_markets_by_fmid_button = QPushButton("show market by FMID")
        self.show_markets_by_fmid_button.setFont(font)
        self.show_markets_by_fmid_button.setStyleSheet(button_style)
        self.layout_left.addWidget(self.show_markets_by_fmid_button, 2, 1)

        self.state_combo = QComboBox()
        self.state_combo.setPlaceholderText("state")
        self.state_combo.setFont(font)
        self.layout_left.addWidget(self.state_combo, 3, 0)
        self.state_combo.addItems(q.get_states())

        self.show_markets_in_state_button = QPushButton("show markets in state")
        self.show_markets_in_state_button.setFont(font)
        self.show_markets_in_state_button.setStyleSheet(button_style)
        self.layout_left.addWidget(self.show_markets_in_state_button, 3, 1)

        self.country_combo = QComboBox()
        self.country_combo.setPlaceholderText("county")
        self.country_combo.setFont(font)
        self.layout_left.addWidget(self.country_combo, 4, 0)
        self.country_combo.addItems(q.get_countries())

        self.show_markets_in_country_button = QPushButton("show markets in county")
        self.show_markets_in_country_button.setFont(font)
        self.show_markets_in_country_button.setStyleSheet(button_style)
        self.layout_left.addWidget(self.show_markets_in_country_button, 4, 1)

        self.city_combo = QComboBox()
        self.city_combo.setPlaceholderText("city")

        self.city_combo.setFont(font)
        self.layout_left.addWidget(self.city_combo, 5, 0)
        self.city_combo.addItems(q.get_cities())

        self.show_markets_by_city_button = QPushButton("show markets in city")
        self.show_markets_by_city_button.setFont(font)
        self.show_markets_by_city_button.setStyleSheet(button_style)
        self.layout_left.addWidget(self.show_markets_by_city_button, 5, 1)

        self.product_combo = QComboBox()
        self.product_combo.setPlaceholderText("product")
        self.product_combo.setFont(font)
        self.layout_left.addWidget(self.product_combo, 6, 0)
        self.product_combo.addItems(q.get_products())

        self.show_markets_by_product = QPushButton("show markets by product")
        self.show_markets_by_product.setStyleSheet(button_style)
        self.show_markets_by_product.setFont(font)
        self.layout_left.addWidget(self.show_markets_by_product, 6, 1)

        self.payment_method_combo = QComboBox()
        self.payment_method_combo.setPlaceholderText("payment method")
        self.payment_method_combo.setFont(font)
        self.layout_left.addWidget(self.payment_method_combo, 7, 0)
        self.payment_method_combo.addItems(q.get_payment_methods())

        self.show_market_by_payment_method_button = QPushButton(text="show markets by payment method", parent=self)
        self.show_market_by_payment_method_button.setFont(font)
        self.layout_left.addWidget(self.show_market_by_payment_method_button, 7, 1)
        self.show_market_by_payment_method_button.setStyleSheet(button_style)

        self.list_of_markets_layout = QVBoxLayout()
        self.list_of_markets_layout.setContentsMargins(0, 25, 0, 0)

        self.list_of_markets_label = QLabel("List of markets:")
        list_of_markets_label_font = QFont(font_for_labels)
        self.list_of_markets_label.setFont(list_of_markets_label_font)
        self.market_info_label = QLabel("(for detailed information, double-click on the market from the list)")
        market_info_label_font = QFont('Arial', 11)
        self.market_info_label.setFont(market_info_label_font)

        self.list_of_markets = QListWidget()
        self.list_of_markets.setFont(font)
        self.list_of_markets.setStyleSheet(text_field_style)

        self.list_of_markets_layout.addWidget(self.list_of_markets_label)
        self.list_of_markets_layout.addWidget(self.market_info_label)
        self.list_of_markets_layout.addWidget(self.list_of_markets)

########################### Connections ###################################################################################################################

        self.logout_button.clicked.connect(self.log_out)
        self.login_button.clicked.connect(self.log_in)
        self.sign_up_button.clicked.connect(self.sign_up)

        self.list_of_markets.itemDoubleClicked.connect(q.get_info_about_market_by_market_name)
        self.list_of_markets.itemDoubleClicked.connect(lambda item: self.updateMapMarkers(q.get_lat_lon(fmid=item.text().rsplit(" ", 1)[-1])))
        self.list_of_markets.itemDoubleClicked.connect(
            lambda item: q.get_information_about_market_by_fmid(item.text().rsplit(" ", 1)[-1]))

        def get_info_about_market_by_fmid(item):
            self.info_about_market.clear()
            self.info_about_market.addItems(q.get_information_about_market_by_fmid(item.text().rsplit(" ", 1)[-1]))

        self.list_of_markets.itemDoubleClicked.connect(get_info_about_market_by_fmid)

        def get_list_of_markets(*, product_name = None,
                                payment_method=None,
                                state_name=None,
                                country_name=None,
                                city_name=None, fmid=None,
                                all_markets_names=None):
            self.list_of_markets.clear()
            if state_name:
                self.list_of_markets.addItems(q.get_markets_names(state_name=state_name))
            elif country_name:
                self.list_of_markets.addItems(q.get_markets_names(country_name=country_name))
            elif city_name:
                self.list_of_markets.addItems(q.get_markets_names(city_name=city_name))
            elif fmid:
                self.list_of_markets.addItems(q.get_markets_names(fmid=fmid))
            elif product_name:
                self.list_of_markets.addItems(q.get_markets_names(product_name=product_name))
            elif payment_method:
                self.list_of_markets.addItems(q.get_markets_names(payment_method=payment_method))
            elif all_markets_names == "all_markets_names":
                self.list_of_markets.addItems(q.get_markets_names(all_markets_names="all_markets_names"))
            else:
                print("Error: Specify one of the parameters - state_name, country_name, city_name or fmid")

        self.show_markets_by_fmid_button.clicked.connect(
            lambda: get_list_of_markets(fmid=self.fmid_combo.currentText()))
        self.show_markets_by_city_button.clicked.connect(
            lambda: get_list_of_markets(city_name=self.city_combo.currentText()))
        self.show_markets_in_state_button.clicked.connect(
            lambda: get_list_of_markets(state_name=self.state_combo.currentText()))
        self.show_markets_in_country_button.clicked.connect(
            lambda: get_list_of_markets(country_name=self.country_combo.currentText()))
        self.show_markets_by_product.clicked.connect(
            lambda: get_list_of_markets(product_name=self.product_combo.currentText()))
        self.show_market_by_payment_method_button.clicked.connect(
             lambda: get_list_of_markets(payment_method=self.payment_method_combo.currentText()))
        self.show_markets_button.clicked.connect(
            lambda: get_list_of_markets(all_markets_names="all_markets_names"))


        self.show_markets_by_fmid_button.clicked.connect(lambda: self.updateMapMarkers(q.get_lat_lon(fmid=self.fmid_combo.currentText())))
        self.show_markets_by_city_button.clicked.connect(lambda: self.updateMapMarkers(q.get_lat_lon(city_name=self.city_combo.currentText())))
        self.show_markets_in_state_button.clicked.connect(lambda: self.updateMapMarkers(q.get_lat_lon(state_name=self.state_combo.currentText())))
        self.show_markets_in_country_button.clicked.connect(lambda: self.updateMapMarkers(q.get_lat_lon(country_name=self.country_combo.currentText())))

        self.show_markets_by_product.clicked.connect(
            lambda: self.updateMapMarkers(q.get_lat_lon(product_name=self.product_combo.currentText())))
        self.show_market_by_payment_method_button.clicked.connect(
            lambda: self.updateMapMarkers(q.get_lat_lon(payment_method=self.payment_method_combo.currentText())))

        self.show_markets_button.clicked.connect(lambda: self.updateMapMarkers(q.get_lat_lon(all_markets_names="all_markets")))

###############################################################################################################################################################

        self.layout_left.addLayout(self.list_of_markets_layout, 8, 0, 1, 2)

        self.layout_right = QVBoxLayout()

        self.webView = QWebEngineView()

        coordinate = (41.864268, -103.662538)
        self.map_OSM = folium.Map(
            title='Map',
            zoom_start=3,
            location=coordinate,
            attributionControl = 0
        )

        data = io.BytesIO()
        self.map_OSM.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())


        self.layout_right.addWidget(self.webView)


        self.webView.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.market_info_layout = QHBoxLayout()

        self.info_about_market_layout = QVBoxLayout()
        self.info_about_market_label = QLabel("Information about market:")
        self.info_about_market_label.setFont(font_for_labels)
        self.info_about_market_label.setStyleSheet(text_field_style)
        self.info_about_market = QListWidget()
        self.info_about_market.setFont(font)
        self.info_about_market.setStyleSheet(text_field_style)
        self.info_about_market_layout.addWidget(self.info_about_market_label)
        self.info_about_market_layout.addWidget(self.info_about_market)

        self.comments_layout = QVBoxLayout()
        self.comments_label = QLabel("Comments:")
        self.comments_label.setFont(font_for_labels)
        self.comments = QListWidget()
        self.comments.setFont(font)
        self.comments.setStyleSheet(text_field_style)
        self.add_comment_button = QPushButton("Add comment")
        self.add_comment_button.setFont(font)
        self.add_comment_button.setStyleSheet(button_style)
        self.comments_layout.addWidget(self.comments_label)
        self.comments_layout.addWidget(self.comments)
        self.comments_layout.addWidget(self.add_comment_button)

        self.market_info_layout.addLayout(self.info_about_market_layout)
        self.market_info_layout.addLayout(self.comments_layout)

        self.layout_right.addLayout(self.market_info_layout)

        layout.addWidget(self.frame, 0, 0, 1, 2)
        layout.addLayout(self.layout_left, 1, 0, 1, 1)
        layout.addLayout(self.layout_right, 1, 1, 1, 1)

        self.stack_layout.setCurrentWidget(self.frame_login_view)

        self.setLayout(layout)


    def updateMapMarkers(self, coordinates_str):

        coordinate = (41.864268, -103.662538)
        m = folium.Map(
            title='Map',
            zoom_start=3,
            location=coordinate,
            attr="OpenStreetMap",
            attributionControl=0
        )
        data = io.BytesIO()
        m.save(data, close_file=False)

        print(f"length_of_coordinates: {len(coordinates_str)}")
        print(f"coordinates_str: {coordinates_str}")

        if len(coordinates_str) == 1:
            latitude = coordinates_str[0][0]
            longitude = coordinates_str[0][1]
            folium.Marker(
                location=[latitude, longitude]
            ).add_to(m)
            html = m._repr_html_()
            self.webView.setHtml(html)

        elif len(coordinates_str) > 1:
            FastMarkerCluster(data=coordinates_str).add_to(m)
            data = io.BytesIO()
            m.save(data, close_file=False)
            html = data.getvalue().decode()
            self.webView.setHtml(html)


    def log_out(self):
        self.user_name = ""
        self.password_hash = ""
        self.stack_layout.setCurrentWidget(self.frame_login_view)


    def sign_up(self):
        dialog = s.SignUpDialog()
        dialog.exec()


    def log_in(self):
        self.stack_layout.setCurrentWidget(self.frame_login_view)
        user_name = self.login.text()
        password_hash = self.password.text()

        is_user_in_db = q.is_user_in_DB(user_name, password_hash)
        font = QFont('Arial', 20)
        if is_user_in_db:
            self.user_name = user_name
            self.password_hash = password_hash
            self.login_label.setText(f"{self.user_name}, you are logged in!")
            self.login_label.setFont(font)
            self.stack_layout.setCurrentWidget(self.frame_logout_view)
        else:
            QMessageBox.warning(self, "Incorrect login/password", "Your login/password is not correct")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())