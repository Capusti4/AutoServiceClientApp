import json

import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt

from Services.responses import get_response_with_user_data
from WorkerApp.popups.notification_popup import NotificationPopUp


class NotificationsPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.setWindowTitle("Уведомления")
        self.setFixedSize(600, 400)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.create_buttons()
        self.set_style_sheet()

    def create_buttons(self):
        read_all_notifications_button = QPushButton("Прочитать все")
        back_button = QPushButton("Назад")
        hbox = QHBoxLayout()
        hbox.addStretch()
        read_all_notifications_button.clicked.connect(self.read_all_notifications)
        read_all_notifications_button.setFixedSize(150, 40)
        back_button.clicked.connect(self.router.open_main_page)
        back_button.setFixedSize(70, 40)
        hbox.addWidget(read_all_notifications_button)
        hbox.addWidget(back_button)
        hbox.addStretch()
        self.layout.addLayout(hbox)

    def read_all_notifications(self):
        url = "http://localhost:8080/worker/readAllNotifications"
        response = get_response_with_user_data(url, self.router.user["username"])
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
        response = get_response_with_user_data(url, self.router.user["username"])
        if response.status_code != 200:
            QMessageBox.information(self, "Ошибка", response.text)
            self.router.open_log_in_page()
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
        notification_button.clicked.connect(lambda: self.open_notification(notification, self.router.user["username"], "worker"))
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
            popup = NotificationPopUp(response.text, self.router)
        else:
            popup = NotificationPopUp(notification, self.router)
        self.update_ui()
        popup.exec()