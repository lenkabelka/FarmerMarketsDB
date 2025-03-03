import sys
import os
from functools import partial
from pathlib import Path
import queries_to_DB_for_GUI as q
from folium.plugins import FastMarkerCluster
import io
import folium
from PyQt6.QtWidgets import (QApplication, QWidget, QLayout, QPushButton, QVBoxLayout, QBoxLayout, QGridLayout,
                             QTextEdit, QLineEdit, QLabel, QListWidget, QFrame, QComboBox, QSizePolicy, QHBoxLayout,
                             QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QFont, QPixmap, QImage, QImageReader
from PyQt6.QtWebEngineWidgets import QWebEngineView



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()


    def initialize(self):
        screen = QApplication.primaryScreen().geometry()
        coef_width = 0.8
        coef_height = 0.8
        window_width = int(screen.width() * coef_width)
        window_height = int(screen.height() * coef_height)
        self.resize(window_width, window_height)
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.move(x, y)

        layout = QGridLayout()

        font = QFont('Arial', 12)
        font_height = (QFontMetrics(font)).height()
        height_of_LineEdit = 2 * font_height

        head_layout_ = QHBoxLayout()
        head_layout = QGridLayout()

        picture_label = QLabel()
        path_to_picture = Path(r"C:\Users\thimo23\PycharmProjects\FarmerMarketsDB\pictures\foods.png").resolve()
        image = QImage("C:/Users/thimo23/PycharmProjects/FarmerMarketsDB/foods_j.png").scaled(300,100)
        pixmap = QPixmap.fromImage(image)
        if image.isNull():
            print("Error: Failed to load image!")
        picture_label.setPixmap(pixmap)
        #picture_label.setScaledContents(True)

        head_layout.addWidget(picture_label)

        nickname = QLineEdit()
        nickname.setPlaceholderText("nickname")
        nickname.setFont(font)
        nickname.setFixedHeight(height_of_LineEdit)
        # print(nickname.sizePolicy().horizontalPolicy())
        # print(nickname.sizePolicy().verticalPolicy())
        password = QLineEdit()
        password.setPlaceholderText("password")
        password.setFont(font)
        password.setFixedHeight(height_of_LineEdit)
        login = QPushButton("Login")
        login.setFont(font)
        head_layout.addWidget(nickname, 0, 0, Qt.AlignmentFlag.AlignRight)
        head_layout.addWidget(password, 1, 0, Qt.AlignmentFlag.AlignRight)
        head_layout.addWidget(login, 2, 0, Qt.AlignmentFlag.AlignRight)

        head_layout_.addWidget(picture_label)
        head_layout_.addLayout(head_layout)

        #layout.addLayout(head_layout, 0, 0, 1, 5)

        # header = QFrame(self)
        # header.setStyleSheet(f"background-color: green")
        # layout.addWidget(header, 0, 0, 1, 5)
        # header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout_left = QGridLayout()

        show_markets_button = QPushButton(text="Show all farmer's markets", parent=self)
        show_markets_button.setFont(font)
        #layout.addWidget(show_markets_button, 1, 0, 1, 2)
        layout_left.addWidget(show_markets_button, 1, 0, 1, 2)
        #show_markets_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        fmid_combo = QComboBox(self)
        fmid_combo.setPlaceholderText("FMID")
        fmid_combo.setFont(font)
        #layout.addWidget(fmid_combo, 2, 0, 1, 1)
        layout_left.addWidget(fmid_combo, 2, 0)
        fmid_combo.addItems(q.get_markets_fmids())
        #fmid_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        show_markets_by_fmid_button = QPushButton(text="show markets by FMID", parent=self)
        show_markets_by_fmid_button.setFont(font)
        #layout.addWidget(show_markets_by_fmid_button, 2, 1, 1, 1)
        layout_left.addWidget(show_markets_by_fmid_button, 2, 1)
        #show_markets_by_fmid_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        state_combo = QComboBox(self)
        state_combo.setPlaceholderText("state")
        state_combo.setFont(font)
        #layout.addWidget(city_combo, 3, 0, 1, 1)
        layout_left.addWidget(state_combo, 3, 0)
        state_combo.addItems(q.get_states())
        #city_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        show_markets_in_state_button = QPushButton(text="show markets in state", parent=self)
        show_markets_in_state_button.setFont(font)
        #layout.addWidget(show_markets_by_city_button, 3, 1, 1, 1)
        layout_left.addWidget(show_markets_in_state_button, 3, 1)
        #show_markets_by_city_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        country_combo = QComboBox(self)
        country_combo.setPlaceholderText("country")
        country_combo.setFont(font)
        #layout.addWidget(city_combo, 3, 0, 1, 1)
        layout_left.addWidget(country_combo, 4, 0)
        country_combo.addItems(q.get_countries())
        #city_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        show_markets_in_country_button = QPushButton(text="show markets in country", parent=self)
        show_markets_in_country_button.setFont(font)
        #layout.addWidget(show_markets_by_city_button, 3, 1, 1, 1)
        layout_left.addWidget(show_markets_in_country_button, 4, 1)
        #show_markets_by_city_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        city_combo = QComboBox(self)
        city_combo.setPlaceholderText("city")
        city_combo.setFont(font)
        #layout.addWidget(city_combo, 3, 0, 1, 1)
        layout_left.addWidget(city_combo, 5, 0)
        city_combo.addItems(q.get_cities())
        #city_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        show_markets_by_city_button = QPushButton(text="show markets in city", parent=self)
        show_markets_by_city_button.setFont(font)
        #layout.addWidget(show_markets_by_city_button, 3, 1, 1, 1)
        layout_left.addWidget(show_markets_by_city_button, 5, 1)
        #show_markets_by_city_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        city_name = city_combo.currentText()
        #print(type(city_name))
        #print(city_name)
        show_markets_by_city_button.clicked.connect(lambda: q.get_markets_in_city(city_combo.currentText()))
        #show_markets_by_city_button.clicked.connect(partial(q.get_markets_in_city, city_combo.currentText))

        product_combo = QComboBox(self)
        product_combo.setPlaceholderText("product")
        product_combo.setFont(font)
        #layout.addWidget(product_combo, 4, 0, 1, 1)
        layout_left.addWidget(product_combo, 6, 0)
        product_combo.addItems(q.get_products())
        #product_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        show_markets_by_product = QPushButton(text="show markets by product", parent=self)
        show_markets_by_product.setFont(font)
        #layout.addWidget(show_markets_by_product, 4, 1, 1, 1)
        layout_left.addWidget(show_markets_by_product, 6, 1)
        #show_markets_by_product.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        payment_method_combo = QComboBox(self)
        payment_method_combo.setPlaceholderText("payment method")
        payment_method_combo.setFont(font)
        #layout.addWidget(payment_method_combo, 5, 0, 1, 1)
        layout_left.addWidget(payment_method_combo, 7, 0)
        payment_method_combo.addItems(q.get_payment_methods())
        #payment_method_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        show_market_by_payment_method_button = QPushButton(text="show markets by payment method", parent=self)
        show_market_by_payment_method_button.setFont(font)
        #layout.addWidget(show_market_by_payment_method_button, 5, 1, 1, 1)
        layout_left.addWidget(show_market_by_payment_method_button, 7, 1)
        #show_market_by_payment_method_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        list_of_markets_layout = QVBoxLayout()

        list_of_markets_label = QLabel("List of markets:")
        list_of_markets_label.setFont(font)

        list_of_markets = QListWidget()
        list_of_markets.setFont(font)

        list_of_markets_layout.addWidget(list_of_markets_label)
        list_of_markets_layout.addWidget(list_of_markets)
        #list_of_markets_layout.setContentsMargins(20, 5, 5, 5)

        def get_list_of_markets():
            list_of_markets.clear()
            list_of_markets.addItems(q.get_markets_in_city(city_combo.currentText()))

        show_markets_by_city_button.clicked.connect(get_list_of_markets)

        layout_left.addLayout(list_of_markets_layout, 8, 0, 1, 2)




        layout_right = QVBoxLayout()

        webView = QWebEngineView()

        coordinate = (41.864268, -103.662538)
        ma = folium.Map(
            title='Map',
            zoom_start=3,
            location=coordinate
        )

        data = io.BytesIO()
        ma.save(data, close_file=False)

        webView.setHtml(data.getvalue().decode())
        #layout.addWidget(webView, 1, 2, 3, 3)
        layout_right.addWidget(webView)
        webView.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #webView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        market_info_layout = QHBoxLayout()

        info_about_market_layout = QVBoxLayout()
        info_about_market_label = QLabel("Information about market:")
        info_about_market_label.setFont(font)
        info_about_market = QListWidget()
        info_about_market_layout.addWidget(info_about_market_label)
        info_about_market_layout.addWidget(info_about_market)

        comments_layout = QVBoxLayout()
        comments_label = QLabel("Comments:")
        comments_label.setFont(font)
        comments = QListWidget()
        comments_layout.addWidget(comments_label)
        comments_layout.addWidget(comments)

        market_info_layout.addLayout(info_about_market_layout)
        market_info_layout.addLayout(comments_layout)

        #info_text = QTextEdit(self)
        #layout.addWidget(info_text, 4, 2, 2, 3)
        layout_right.addLayout(market_info_layout)
        #info_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addLayout(head_layout_, 0, 0, 1, 2)
        layout.addLayout(layout_left, 1, 0, 1, 1)
        layout.addLayout(layout_right, 1, 1, 1, 1)

        self.setLayout(layout)

        def updateMapMarkers(coordinates):

            coordinate = (41.864268, -103.662538)
            m = folium.Map(
                title='Map',
                zoom_start=3,
                location=coordinate
            )
            #coordinates = q.show_all_markets_GUI()
            FastMarkerCluster(data=coordinates).add_to(m)

            print(len(coordinates))

            data = io.BytesIO()
            m.save(data, close_file=False)

            html = data.getvalue().decode()
            webView.setHtml(html)

        #show_markets_button.clicked.connect(updateMapMarkers)

        def get_lat_lon_and_info(item_text):
            coordinates = q.get_lat_lon(item_text)
            updateMapMarkers(coordinates)


        list_of_markets.itemDoubleClicked.connect(lambda item: get_lat_lon_and_info(item.text()))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())