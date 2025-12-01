import json

import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QStackedWidget, QListWidget, QListWidgetItem, QHBoxLayout, QDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys

from Services.feedbacks import get_feedbacks
from Services.responses import get_user_info, get_response_with_user_data
from Services.sessions import check_session, delete_session

user = check_session("worker")


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = stack
        self.username_textbox = None
        self.password_textbox = None
        self.register_button = None
        self.login_button = None

        self.setWindowTitle("Вход")
        self.setFixedSize(360, 420)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.create_textboxes()
        self.create_tittle()
        self.create_form_layout()
        self.create_buttons()
        self.set_style_sheet()

    def create_textboxes(self):
        self.username_textbox = QLineEdit()
        self.username_textbox.setPlaceholderText("Логин")
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText("Пароль")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)

    def create_tittle(self):
        title = QLabel("Вход")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

    def create_form_layout(self):
        form_layout = QFormLayout()
        form_layout.addRow("Логин:", self.username_textbox)
        form_layout.addRow("Пароль:", self.password_textbox)
        self.layout.addLayout(form_layout)

    def create_buttons(self):
        self.login_button = QPushButton("Войти")
        self.login_button.setFixedHeight(45)
        self.login_button.clicked.connect(self.log_in)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setFixedHeight(45)
        self.register_button.clicked.connect(lambda: self.stack.setCurrentWidget(registration_page))
        self.layout.addWidget(self.register_button)

    def log_in(self):
        global user
        username = self.username_textbox.text().lower()
        password = self.password_textbox.text()
        url = "http://localhost:8080/worker/logIn"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            QMessageBox.information(self, "Вход", response.text)
        else:
            user = get_user_info(response)
            self.stack.setCurrentWidget(main_page)

    def set_style_sheet(self):
        self.setStyleSheet("""
                    QWidget {
                        background-color: #F7FAFF;
                    }
                    QLabel {
                        color: #1A3E6E;
                    }
                    QLineEdit {
                        color: #000000;
                        padding: 10px;
                        border-radius: 8px;
                        border: 2px solid #C7D8F7;
                        background: #ffffff;
                    }
                    QLineEdit[placeholderText]:!focus { color: #9fb4e6; }
                    QLineEdit:focus {
                        border: 2px solid #6BA6FF;
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


class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.register_button = None
        self.login_button = None
        self.phone_number_textbox = None
        self.lastname_textbox = None
        self.firstname_textbox = None
        self.password_textbox = None
        self.username_textbox = None
        self.form_layout = None
        self.stack = stack

        self.setWindowTitle("Регистрация")
        self.setFixedSize(360, 420)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.create_tittle()
        self.create_textboxes()
        self.create_form_layout()
        self.create_buttons()
        self.set_style_sheet()

    def create_tittle(self):
        title = QLabel("Регистрация")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

    def create_textboxes(self):
        self.username_textbox = QLineEdit()
        self.username_textbox.setPlaceholderText("Логин")

        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText("Пароль")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)

        self.firstname_textbox = QLineEdit()
        self.firstname_textbox.setPlaceholderText("Имя")

        self.lastname_textbox = QLineEdit()
        self.lastname_textbox.setPlaceholderText("Фамилия")

        self.phone_number_textbox = QLineEdit()
        self.phone_number_textbox.setPlaceholderText("Номер телефона")

    def create_form_layout(self):
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Логин:", self.username_textbox)
        self.form_layout.addRow("Пароль:", self.password_textbox)
        self.form_layout.addRow("Имя:", self.firstname_textbox)
        self.form_layout.addRow("Фамилия:", self.lastname_textbox)
        self.form_layout.addRow("Номер телефона:", self.phone_number_textbox)
        self.layout.addLayout(self.form_layout)

    def create_buttons(self):
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setFixedHeight(45)
        self.register_button.clicked.connect(self.register)

        self.login_button = QPushButton("Войти")
        self.login_button.setFixedHeight(45)
        self.login_button.clicked.connect(lambda: self.stack.setCurrentWidget(log_in_page))

        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.login_button)

    def set_style_sheet(self):
        self.setStyleSheet("""
                            QLabel {
                                color: #1A3E6E;
                            }
                            QLineEdit {
                                color: #000000;
                                padding: 10px;
                                border-radius: 8px;
                                border: 2px solid #C7D8F7;
                                background: #ffffff;
                            }
                            QLineEdit[placeholderText]:!focus { color: #9fb4e6; }
                            QLineEdit:focus {
                                border: 2px solid #6BA6FF;
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

    def register(self):
        global user
        username = self.username_textbox.text().lower()
        password = self.password_textbox.text()
        firstname = self.firstname_textbox.text().lower()
        lastname = self.lastname_textbox.text().lower()
        phone_number = self.phone_number_textbox.text()
        url = "http://localhost:8080/worker/register"
        data = {
            "username": username,
            "password": password,
            "firstName": firstname,
            "lastName": lastname,
            "phoneNum": phone_number
        }
        response = requests.post(url, json=data)
        self.check_response(response)

    def check_response(self, response):
        global user
        if response.status_code != 201:
            QMessageBox.information(self, "Регистрация", response.text)
        else:
            user = get_user_info(response)
            self.stack.setCurrentWidget(main_page)


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.logout_button = QPushButton()
        self.reviews_button = QPushButton()
        self.notifications_button = QPushButton()
        self.orders_button = QPushButton()
        self.layout = QVBoxLayout()
        self.stack = stack

        self.setWindowTitle("Главное меню")
        self.setFixedSize(360, 420)

        self.create_layout()
        self.create_tittle()
        self.create_buttons()
        self.set_style_sheet()

    def create_layout(self):
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

    def create_tittle(self):
        title = QLabel("Главное меню")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

    def create_buttons(self):
        self.orders_button.setText("Посмотреть заказы")
        self.orders_button.clicked.connect(self.open_orders_page)
        self.notifications_button.setText("Посмотреть уведомления")
        self.notifications_button.clicked.connect(self.open_notifications_page)
        self.reviews_button.setText("Открыть меню отзывов")
        self.reviews_button.clicked.connect(self.open_feedbacks_page)
        self.logout_button.setText("Выйти из аккаунта")
        self.logout_button.clicked.connect(self.exit_from_account)
        for button in [self.orders_button, self.notifications_button, self.reviews_button, self.logout_button]:
            button.setFixedHeight(45)
            self.layout.addWidget(button)

    def open_orders_page(self):
        orders_page.update_ui()
        self.stack.setCurrentWidget(orders_page)

    def set_style_sheet(self):
        self.setStyleSheet("""
                    QWidget {
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

    def open_notifications_page(self):
        notifications_page.update_ui()
        self.stack.setCurrentWidget(notifications_page)

    def open_feedbacks_page(self):
        feedbacks_page.update_ui()
        self.stack.setCurrentWidget(feedbacks_page)

    def exit_from_account(self):
        response = delete_session("worker")
        if response.status_code != 200:
            QMessageBox.information(self, "Ошибка", response.text)
        else:
            QMessageBox.information(self, "Выход", response.text)
            self.stack.setCurrentWidget(log_in_page)


class NotificationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = stack
        self.read_all_button = QPushButton("Прочитать все")
        self.back_button = QPushButton("Назад")

        self.setWindowTitle("Уведомления")
        self.setFixedSize(600, 400)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.create_buttons()
        self.set_style_sheet()

    def create_buttons(self):
        hbox = QHBoxLayout()
        hbox.addStretch()
        self.read_all_button.clicked.connect(self.read_all_notifications)
        self.read_all_button.setFixedSize(150, 40)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(main_page))
        self.back_button.setFixedSize(70, 40)
        hbox.addWidget(self.read_all_button)
        hbox.addWidget(self.back_button)
        hbox.addStretch()
        self.layout.addLayout(hbox)

    def read_all_notifications(self):
        url = "http://localhost:8080/worker/readAllNotifications"
        response = get_response_with_user_data(url, user["username"])
        QMessageBox.information(self, "Прочитать все", response.text)

    def set_style_sheet(self):
        self.setStyleSheet("""
                            QWidget {
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
                            #notificationButton {
                                color: #1A3E6E;
                                background-color: #ffffff;
                                border: 2px solid #C7D8F7;
                                border-radius: 8px;
                            }
                            #notificationButton:hover {
                                background-color: #fff000;
                            }
                            #notificationButton:pressed {
                                background-color: #4C82D1;
                            }
                            #unredNotificationButton {
                                color: #1A3E6E;
                                background-color: #ffff00;
                                border: 2px solid #C7D8F7;
                                border-radius: 8px;
                            }
                            #unredNotificationButton:hover {
                                background-color: #fff000;
                            }
                            #unredNotificationButton:pressed {
                                background-color: #4C82D1;
                            }
                        """)

    def update_ui(self):
        url = "http://localhost:8080/worker/getNotifications"
        response = get_response_with_user_data(url, user["username"])
        if response.status_code != 200:
            QMessageBox.information(self, "Ошибка", response.text)
            self.stack.setCurrentWidget(log_in_page)
            return
        else:
            notifications = response.json()

        self.list_widget.clear()

        for notification in notifications:
            self.add_notification(notification)

    def add_notification(self, notification):
        item = QListWidgetItem()
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setSpacing(2)
        type_id = notification["typeId"]
        text = self.match_type_id(type_id)

        notification_button = QPushButton(text)
        if notification["isRead"]:
            notification_button.setObjectName("notificationButton")
        else:
            notification_button.setObjectName("unredNotificationButton")
        notification_button.clicked.connect(lambda: self.open_notification(notification, user["username"], "worker"))
        vbox.addWidget(notification_button)

        widget.setLayout(vbox)
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    @staticmethod
    def match_type_id(type_id):
        match type_id:
            case 1:
                text = "Важное уведомление"
            case 2:
                text = "Ваш заказ взят в работу"
            case 3:
                text = "Ваш заказ завершен"
            case 4:
                text = "Вам оставили отзыв"
            case 5:
                text = "Вы завершили заказ, оставьте отзыв о клиенте"
            case _:
                text = "Error"
        return text

    def open_notification(self, notification, username, app_name):
        url = f"http://localhost:8080/{app_name}/readNotification"
        with open("Data\\session.json", "r") as f:
            session_token = json.load(f)["sessionToken"]
        data = {
            'username': username,
            'sessionToken': session_token,
            'notificationId': notification["_id"]["$oid"],
        }
        response = requests.post(url=url, json=data)
        if response.status_code != 200:
            popup = NotificationPopUp(response.text)
        else:
            popup = NotificationPopUp(notification)
        self.update_ui()
        popup.exec()


class NotificationPopUp(QDialog):
    def __init__(self, notification):
        super().__init__()
        self.setWindowTitle("Уведомление")
        self.setFixedSize(380, 260)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Заголовок
        title = QLabel("Уведомление")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текст уведомления
        message = QLabel(notification["text"])
        message.setWordWrap(True)
        message.setFont(QFont("Arial", 14))
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        # Кнопка закрыть
        close_button = QPushButton("Удалить")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(lambda: self.delete_notification(notification))
        layout.addWidget(close_button)

        # Кнопка закрыть
        close_button = QPushButton("Закрыть")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Стиль
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

    def delete_notification(self, notification):
        notification_id = notification["_id"]["$oid"]
        url = "http://localhost:8080/worker/deleteNotification"
        with open("Data\\session.json", "r") as f:
            session_token = json.load(f)["sessionToken"]
        data = {
            'username': user["username"],
            'sessionToken': session_token,
            'notificationId': notification_id,
        }
        response = requests.post(url=url, json=data)
        QMessageBox.information(self, "Уведомление", response.text)
        NotificationsPage.update_ui(notifications_page)


class OrdersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.stack = stack
        self.setWindowTitle("Заказы")
        self.setFixedSize(600, 500)
        self.orders_type = 1

        self.create_layout()
        self.create_filter_buttons()
        self.create_empty_label()
        self.create_orders_list()
        self.create_back_button()
        self.apply_styles()

    # ----------------------------- UI -----------------------------

    def create_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def create_filter_buttons(self):
        self.filters_layout = QHBoxLayout()

        self.open_new_orders_button = QPushButton("Новые")
        self.open_new_orders_button.clicked.connect(self.open_new_orders)
        self.open_active_orders_button = QPushButton("Активные")
        self.open_active_orders_button.clicked.connect(self.open_active_orders)
        self.open_completed_orders_button = QPushButton("Завершенные")
        self.open_completed_orders_button.clicked.connect(self.open_completed_orders)

        # Ничего не делают, как просил
        self.filters_layout.addWidget(self.open_new_orders_button)
        self.filters_layout.addWidget(self.open_active_orders_button)
        self.filters_layout.addWidget(self.open_completed_orders_button)

        self.layout.addLayout(self.filters_layout)

    def create_empty_label(self):
        self.empty_label = QLabel("Заказов нет")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #1A3E6E; font-size: 18px;")
        self.empty_label.hide()
        self.layout.addWidget(self.empty_label)

    def open_new_orders(self):
        self.orders_type = 1
        self.update_ui()

    def open_active_orders(self):
        self.orders_type = 2
        self.update_ui()

    def open_completed_orders(self):
        self.orders_type = 3
        self.update_ui()

    @staticmethod
    def get_orders(url):
        response = get_response_with_user_data(url, user["username"])
        return response.json()

    def create_orders_list(self):
        self.orders_list = QListWidget()
        self.layout.addWidget(self.orders_list)

    def create_back_button(self):
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(main_page))
        self.back_button.setFixedHeight(40)
        self.layout.addWidget(self.back_button)  # пока не привязываем обработчик

    def apply_styles(self):
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

    # ----------------------------- UPDATE UI -----------------------------

    def update_ui(self):
        """
        orders — массив словарей
        каждый словарь содержит order_text — текст заказа
        """
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
                background-color: #5A94EA;
            }
            QPushButton:pressed {
                background-color: #4C82D1;
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
        response = get_response_with_user_data(url, user["username"])
        orders = response.json()

        self.orders_list.clear()

        if not orders:
            self.empty_label.show()
            return
        self.empty_label.hide()
        for order in orders:
            self.add_order_item(order)

    # ----------------------------- ADD ONE ORDER -----------------------------

    def add_order_item(self, order):
        item = QListWidgetItem()
        widget = QWidget()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 5, 0, 5)

        button = QPushButton(f"Заказ {order["_id"]["$oid"]}")
        button.setObjectName("orderButton")
        button.setFixedHeight(60)
        match self.orders_type:
            case 1:
                button.clicked.connect(lambda: self.open_new_order(order))
            case 2:
                button.clicked.connect(lambda: self.open_active_order(order))
            case 3:
                button.clicked.connect(lambda: self.open_completed_order(order))

        vbox.addWidget(button)
        widget.setLayout(vbox)

        item.setSizeHint(widget.sizeHint())
        self.orders_list.addItem(item)
        self.orders_list.setItemWidget(item, widget)

    @staticmethod
    def open_new_order(order):
        popup = NewOrderPopUp(order)
        popup.exec()

    @staticmethod
    def open_active_order(order):
        popup = ActiveOrderPopUp(order)
        popup.exec()

    @staticmethod
    def open_completed_order(order):
        popup = CompletedOrderPopUp(order)
        popup.exec()


class NewOrderPopUp(QDialog):
    def __init__(self, order):
        super().__init__()
        self.setWindowTitle("Заказы")
        self.setFixedSize(500, 260)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Заголовок
        title = QLabel("Заказы")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текст уведомления

        text = (
            f"ID заказа: {order["_id"]["$oid"]}\n"
            f"Тип заказа: {order["type"]}\n"
            f"Комментарий: {order["comment"]}\n\n"
            f"Имя заказчика: {order["customerFirstName"]}\n"
            f"Фамилия заказчика: {order["customerLastName"]}\n"
            f"Номер телефона заказчика: {order["customerPhoneNum"]}"
        )
        message = QLabel(text)
        message.setWordWrap(True)
        message.setFont(QFont("Arial", 14))
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        take_order_button = QPushButton("Взять заказ")
        take_order_button.setFixedHeight(40)
        take_order_button.clicked.connect(lambda: self.take_order(order))
        layout.addWidget(take_order_button)

        # Кнопка закрыть
        close_button = QPushButton("Закрыть")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Стиль
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
        with open("Data\\session.json", "r") as f:
            session_json = json.load(f)
        session_json["orderId"] = order_id
        response = requests.post("http://localhost:8080/worker/startOrder", json=session_json)
        if response.status_code == 200:
            QMessageBox.information(self, "Заказ", f"Заказ {order_id} успешно взят")
        else:
            QMessageBox.information(self, "Заказ", response.text)
        orders_page.update_ui()


class ActiveOrderPopUp(QDialog):
    def __init__(self, order):
        super().__init__()
        self.setWindowTitle("Заказы")
        self.setFixedSize(500, 260)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Заголовок
        title = QLabel("Заказы")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текст уведомления
        text = (
            f"ID заказа: {order["_id"]["$oid"]}\n"
            f"Тип заказа: {order["type"]}\n"
            f"Комментарий: {order["comment"]}\n\n"
            f"Имя заказчика: {order["customerFirstName"]}\n"
            f"Фамилия заказчика: {order["customerLastName"]}\n"
            f"Номер телефона заказчика: {order["customerPhoneNum"]}"
        )
        message = QLabel(text)
        message.setWordWrap(True)
        message.setFont(QFont("Arial", 14))
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        complete_order_button = QPushButton("Завершить заказ")
        complete_order_button.setFixedHeight(40)
        complete_order_button.clicked.connect(lambda: self.complete_order(order))
        layout.addWidget(complete_order_button)

        # Кнопка закрыть
        close_button = QPushButton("Закрыть")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Стиль
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

    def complete_order(self, order):
        with open("Data\\session.json", "r") as f:
            session_token = json.load(f)["sessionToken"]
        data = {
            'username': user["username"],
            'sessionToken': session_token,
            'orderId': order["_id"]["$oid"],
        }
        response = requests.post(url="http://localhost:8080/worker/completeOrder", json=data)
        QMessageBox.information(self, "Заказ", response.text)
        orders_page.update_ui()


class CompletedOrderPopUp(QDialog):
    def __init__(self, order):
        super().__init__()
        self.setWindowTitle("Заказы")
        self.setFixedSize(500, 260)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Заголовок
        title = QLabel("Заказы")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Текст уведомления
        text = (
            f"ID заказа: {order["_id"]["$oid"]}\n"
            f"Тип заказа: {order["type"]}\n"
            f"Комментарий: {order["comment"]}\n\n"
            f"Имя заказчика: {order["customerFirstName"]}\n"
            f"Фамилия заказчика: {order["customerLastName"]}\n"
            f"Номер телефона заказчика: {order["customerPhoneNum"]}"
        )
        message = QLabel(text)
        message.setWordWrap(True)
        message.setFont(QFont("Arial", 14))
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        # Кнопка закрыть
        close_button = QPushButton("Закрыть")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Стиль
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


class FeedbacksPage(QWidget):
    def __init__(self):
        super().__init__()

        self.stack = stack
        self.setWindowTitle("Отзывы")
        self.setFixedSize(600, 500)

        self.create_layout()
        self.create_empty_label()
        self.create_feedbacks_list()
        self.create_back_button()
        self.apply_styles()

    # ----------------------------- UI -----------------------------

    def create_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def create_empty_label(self):
        self.empty_label = QLabel("Отзывов нет")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #1A3E6E; font-size: 18px;")
        self.empty_label.hide()
        self.layout.addWidget(self.empty_label)

    def create_feedbacks_list(self):
        self.feedbacks_list = QListWidget()
        self.layout.addWidget(self.feedbacks_list)

    def create_back_button(self):
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(main_page))
        self.back_button.setFixedHeight(40)
        self.layout.addWidget(self.back_button)  # пока не привязываем обработчик

    def apply_styles(self):
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
            #feedbackButton {
                background-color: #ffffff;
                color: #1A3E6E;
                border: 2px solid #C7D8F7;
                border-radius: 8px;
                padding: 10px;
                text-align: left;
            }
            #feedbackButton:hover {
                background-color: #E8F1FF;
            }
        """)

    # ----------------------------- UPDATE UI -----------------------------

    def update_ui(self):
        url = "http://localhost:8080/worker/getFeedbacksForUser"
        feedbacks = get_feedbacks(url, user["username"])

        self.feedbacks_list.clear()

        if not feedbacks:
            self.empty_label.show()
            return
        self.empty_label.hide()
        for feedback in feedbacks:
            self.add_feedback_item(feedback)

    # ----------------------------- ADD ONE ORDER -----------------------------

    def add_feedback_item(self, feedback):
        item = QListWidgetItem()
        widget = QWidget()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 5, 0, 5)

        button = QPushButton(
            f"Оценка: {feedback["rating"]}\n"
            f"Комментарий: {feedback["comment"]}"
        )
        button.setObjectName("feedbackButton")
        button.setFixedHeight(80)

        vbox.addWidget(button)
        widget.setLayout(vbox)

        item.setSizeHint(widget.sizeHint())
        self.feedbacks_list.addItem(item)
        self.feedbacks_list.setItemWidget(item, widget)


def check_user():
    if user:
        stack.setCurrentWidget(main_page)
    else:
        stack.setCurrentWidget(log_in_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    stack.setStyleSheet("background-color: #F7FAFF;")

    log_in_page = LoginPage()
    registration_page = RegistrationPage()
    main_page = MainPage()
    orders_page = OrdersPage()
    notifications_page = NotificationsPage()
    feedbacks_page = FeedbacksPage()

    stack.addWidget(log_in_page)
    stack.addWidget(registration_page)
    stack.addWidget(main_page)
    stack.addWidget(orders_page)
    stack.addWidget(notifications_page)
    stack.addWidget(feedbacks_page)

    check_user()

    stack.resize(360, 420)
    stack.show()
    sys.exit(app.exec())
