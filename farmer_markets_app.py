import sys
import queries_to_DB_for_GUI as q
from folium.plugins import FastMarkerCluster
import io
import folium
from PyQt5.QtWidgets import (QApplication, QWidget, QLayout, QPushButton, QVBoxLayout, QBoxLayout, QGridLayout,
                             QTextEdit, QFrame, QComboBox, QSizePolicy)
from PyQt5.QtWebEngineWidgets import QWebEngineView


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

        # header = QFrame(self)
        # header.setStyleSheet(f"background-color: #2E86C1; height: {window_height/20}; width: {window_width};")
        # layout.addWidget(header)

        show_markets_button = QPushButton(text="Show all farmer's markets", parent=self)
        layout.addWidget(show_markets_button, 0, 0, 1, 2)

        fmid_combo = QComboBox(self)
        layout.addWidget(fmid_combo, 1, 0, 1, 1)
        fmid_combo.addItems(q.get_markets_fmids())

        show_markets_by_fmid_button = QPushButton(text="show markets by fmid", parent=self)
        layout.addWidget(show_markets_by_fmid_button, 1, 1, 1, 1)

        city_combo = QComboBox(self)
        layout.addWidget(city_combo, 2, 0, 1, 1)
        city_combo.addItems(q.get_cities())

        show_markets_by_city_button = QPushButton(text="show markets in city", parent=self)
        layout.addWidget(show_markets_by_city_button, 2, 1, 1, 1)

        product_combo = QComboBox(self)
        layout.addWidget(product_combo, 3, 0, 1, 1)
        product_combo.addItems(q.get_products())

        show_markets_by_product = QPushButton(text="show markets by product", parent=self)
        layout.addWidget(show_markets_by_product, 3, 1, 1, 1)

        payment_method_combo = QComboBox(self)
        layout.addWidget(payment_method_combo, 4, 0, 1, 1)
        payment_method_combo.addItems(q.get_payment_methods())

        show_market_by_payment_method_button = QPushButton(text="show markets by payment method", parent=self)
        layout.addWidget(show_market_by_payment_method_button, 4, 1, 1, 1)

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
        layout.addWidget(webView, 0, 2, 3, 3)
        webView.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        info_text = QTextEdit(self)
        layout.addWidget(info_text, 3, 2, 2, 3)
        info_text.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.setLayout(layout)

        def updateMapMarkers():

            coordinate = (41.864268, -103.662538)
            m = folium.Map(
                title='Map',
                zoom_start=3,
                location=coordinate
            )
            coordinates = q.show_all_markets_GUI()
            FastMarkerCluster(data=coordinates).add_to(m)

            print(len(coordinates))

            data = io.BytesIO()
            m.save(data, close_file=False)

            html = data.getvalue().decode()
            webView.setHtml(html)

        show_markets_button.clicked.connect(updateMapMarkers)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())