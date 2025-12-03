import json

import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox


class NotificationPopUp(QDialog):
    def __init__(self, notification, router):
        super().__init__()
        self.router = router
        self.setWindowTitle("Уведомление")
        self.setFixedSize(380, 260)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.create_tittle()
        self.create_notification_label(notification)
        self.create_buttons(notification)

        self.setLayout(self.layout)
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

    def create_tittle(self):
        title = QLabel("Уведомление")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

    def create_notification_label(self, notification):
        label = QLabel(notification["text"])
        label.setWordWrap(True)
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

    def create_buttons(self, notification):
        delete_button = QPushButton("Удалить")
        delete_button.setFixedHeight(40)
        delete_button.clicked.connect(lambda: self.delete_notification(notification))
        close_button = QPushButton("Закрыть")
        close_button.setFixedHeight(40)
        close_button.clicked.connect(self.close)
        self.layout.addWidget(delete_button)
        self.layout.addWidget(close_button)

    def delete_notification(self, notification):
        notification_id = notification["_id"]["$oid"]
        url = "http://localhost:8080/worker/deleteNotification"
        with open("Data\\session.json", "r") as f:
            session_token = json.load(f)["sessionToken"]
        data = {
            'username': self.router.user["username"],
            'sessionToken': session_token,
            'notificationId': notification_id,
        }
        response = requests.post(url=url, json=data)
        QMessageBox.information(self, "Уведомление", response.text)
        self.router.notifications_page.update_ui()
        self.close()