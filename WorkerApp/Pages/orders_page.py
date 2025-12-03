from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QHBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt

from Services.responses import get_response_with_user_data
from WorkerApp.constants import NEW_ORDER, ACTIVE_ORDER, COMPLETED_ORDER
from WorkerApp.popups.order_popup import OrderPopUp

class OrdersPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.open_new_orders_button = QPushButton("Новые")
        self.open_active_orders_button = QPushButton("Активные")
        self.open_completed_orders_button = QPushButton("Завершенные")
        self.empty_label = QLabel("Заказов нет")
        self.orders_type = NEW_ORDER
        self.setWindowTitle("Заказы")
        self.setFixedSize(600, 500)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.orders_list = QListWidget()

        self.modify_filter_buttons()
        self.modify_empty_label()
        self.layout.addWidget(self.orders_list)
        self.create_back_button()
        self.set_styles_sheet()

    def modify_filter_buttons(self):
        filters_layout = QHBoxLayout()
        self.open_new_orders_button.clicked.connect(self.open_new_orders)
        self.open_active_orders_button.clicked.connect(self.open_active_orders)
        self.open_completed_orders_button.clicked.connect(self.open_completed_orders)
        filters_layout.addWidget(self.open_new_orders_button)
        filters_layout.addWidget(self.open_active_orders_button)
        filters_layout.addWidget(self.open_completed_orders_button)
        self.layout.addLayout(filters_layout)

    def modify_empty_label(self):
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #1A3E6E; font-size: 18px;")
        self.empty_label.hide()
        self.layout.addWidget(self.empty_label)

    def open_new_orders(self):
        self.orders_type = NEW_ORDER
        self.update_ui()

    def open_active_orders(self):
        self.orders_type = ACTIVE_ORDER
        self.update_ui()

    def open_completed_orders(self):
        self.orders_type = COMPLETED_ORDER
        self.update_ui()

    def get_orders(self, url):
        response = get_response_with_user_data(url, self.router.user["username"])
        return response.json()

    def create_back_button(self):
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.router.open_main_page)
        back_button.setFixedHeight(40)
        self.layout.addWidget(back_button)

    def set_styles_sheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F7FAFF;
            }
            QPushButton {
                background-color: #6BA6FF;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #5A94EA;
            }
            QPushButton:pressed {
                background-color: #4C82D1;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #C7D8F7;
                border-radius: 8px;
                padding: 5px;
            }
            #orderButton {
                background-color: #ffffff;
                color: #1A3E6E;
                border: 2px solid #C7D8F7;
                border-radius: 8px;
                padding: 10px;
                text-align: left;
            }
            #orderButton:hover {
                background-color: #E8F1FF;
            }
        """)

    def update_ui(self):
        url = ""
        default_style = """
            QPushButton {
                background-color: #6BA6FF;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #5A94EA;
            }
            QPushButton:pressed {
                background-color: #4C82D1;
            }
        """
        active_style = """
            QPushButton {
                background-color: #C0D9FF;
                color: black;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                color: white;
                background-color: #96B5E3;
            }
            QPushButton:pressed {
                color: white;
                background-color: #6189C6;
            }
        """
        self.open_new_orders_button.setStyleSheet(default_style)
        self.open_active_orders_button.setStyleSheet(default_style)
        self.open_completed_orders_button.setStyleSheet(default_style)
        match self.orders_type:
            case 1:
                self.open_new_orders_button.setStyleSheet(active_style)
                url = "http://localhost:8080/worker/getNewOrders"
            case 2:
                self.open_active_orders_button.setStyleSheet(active_style)
                url = "http://localhost:8080/worker/getActiveOrders"
            case 3:
                self.open_completed_orders_button.setStyleSheet(active_style)
                url = "http://localhost:8080/worker/getCompletedOrders"
        response = get_response_with_user_data(url, self.router.user["username"])
        orders = response.json()

        self.orders_list.clear()

        if not orders:
            self.empty_label.show()
            return
        self.empty_label.hide()
        for order in orders:
            self.add_order_item(order)

    def add_order_item(self, order):
        item = QListWidgetItem()
        widget = QWidget()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 5, 0, 5)

        button = QPushButton(f"Заказ {order["_id"]["$oid"]}")
        button.setObjectName("orderButton")
        button.setFixedHeight(60)
        button.clicked.connect(lambda: self.open_order(order))

        vbox.addWidget(button)
        widget.setLayout(vbox)

        item.setSizeHint(widget.sizeHint())
        self.orders_list.addItem(item)
        self.orders_list.setItemWidget(item, widget)

    def open_order(self, order):
        popup = OrderPopUp(self.router, order)
        popup.exec()
