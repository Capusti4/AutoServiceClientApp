import json

import requests
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QMessageBox, QDialog
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from WorkerApp.constants import NEW_ORDER, ACTIVE_ORDER


class OrderPopUp(QDialog):
    def __init__(self, router, order):
        super().__init__()
        self.router = router
        self.setWindowTitle("Заказы")
        self.setFixedSize(500, 260)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Заказы")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        label = QLabel(
            f"ID заказа: {order["_id"]["$oid"]}\n"
            f"Тип заказа: {order["type"]}\n"
            f"Комментарий: {order["comment"]}\n\n"
            f"Имя заказчика: {order["customerFirstName"]}\n"
            f"Фамилия заказчика: {order["customerLastName"]}\n"
            f"Номер телефона заказчика: {order["customerPhoneNum"]}"
        )
        label.setWordWrap(True)
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        order_type = self.router.orders_page.orders_type
        if order_type == NEW_ORDER:
            take_order_button = QPushButton("Взять заказ")
            take_order_button.setFixedHeight(40)
            take_order_button.clicked.connect(lambda: self.take_order(order))
            layout.addWidget(take_order_button)
        elif order_type == ACTIVE_ORDER:
            complete_order_button = QPushButton("Завершить заказ")
            complete_order_button.setFixedHeight(40)
            complete_order_button.clicked.connect(lambda: self.complete_order(order))
            layout.addWidget(complete_order_button)

        close_button = QPushButton("Закрыть")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        self.setStyleSheet("""
                    QDialog {
                        background-color: #F7FAFF;
                    }
                    QLabel {
                        color: #1A3E6E;
                    }
                    QPushButton {
                        background-color: #6BA6FF;
                        color: white;
                        border: none;
                        border-radius: 10px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #5A94EA;
                    }
                    QPushButton:pressed {
                        background-color: #4C82D1;
                    }
                """)

    def take_order(self, order):
        order_id = order["_id"]["$oid"]
        url = "http://localhost:8080/worker/startOrder"
        response = self.make_order_request(order_id, url)
        if response.status_code == 200:
            QMessageBox.information(self, "Заказ", f"Заказ {order_id} успешно взят")
        else:
            QMessageBox.information(self, "Заказ", response.text)
        self.router.orders_page.update_ui()
        self.close()

    def complete_order(self, order):
        order_id = order["_id"]["$oid"]
        url = "http://localhost:8080/worker/completeOrder"
        response = self.make_order_request(order_id, url)
        if response.status_code == 200:
            QMessageBox.information(self, "Заказ", f"Заказ {order_id} успешно завершен")
        else:
            QMessageBox.information(self, "Заказ", response.text)
        self.router.orders_page.update_ui()
        self.close()

    @staticmethod
    def make_order_request(order_id, url):
        with open("Data\\session.json", "r") as f:
            session_json = json.load(f)
        session_json["orderId"] = order_id
        return requests.post(url, json=session_json)
