import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QStackedWidget, QListWidget, QListWidgetItem
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys

from Services.responses import get_user_info, get_response_with_user_data
from Services.sessions import check_session

user_info = check_session("worker")


class LoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setWindowTitle("Вход")
        self.setFixedSize(360, 420)

        # --- Основной контейнер ---
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # --- Заголовок ---
        title = QLabel("Вход")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- Форма ---
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        self.username_text_box = QLineEdit()
        self.username_text_box.setPlaceholderText("Логин")

        self.password_text_box = QLineEdit()
        self.password_text_box.setPlaceholderText("Пароль")
        self.password_text_box.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Логин:", self.username_text_box)
        form_layout.addRow("Пароль:", self.password_text_box)

        layout.addLayout(form_layout)

        # --- Кнопка входа ---
        self.login_btn = QPushButton("Войти")
        self.login_btn.setFixedHeight(45)
        self.login_btn.clicked.connect(self.log_in)

        # --- Кнопка регистрации ---
        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.setFixedHeight(45)
        self.register_btn.clicked.connect(self.open_registration_page)

        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        # --- Стиль ---
        self.setStyleSheet("""
            QWidget {
                background-color: #F7FAFF;
            }
            QLabel {
                color: #1A3E6E;
            }
            /* Тёмный текст внутри полей ввода */
            QLineEdit {
                color: #000000;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #C7D8F7;
                background: #ffffff;
            }
            /* Светлый плейсхолдер (смягчает визуал) */
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

    def log_in(self):
        global user_info
        username = self.username_text_box.text().lower()
        password = self.password_text_box.text()
        url = "http://localhost:8080/worker/logIn"
        json = {"username": username, "password": password}
        response = requests.post(url, json=json)
        if response.status_code != 200:
            QMessageBox.information(self, "Вход", response.text)
        else:
            user_info = get_user_info(response)
            self.stack.setCurrentWidget(main_page)

    def open_registration_page(self):
        self.stack.setCurrentWidget(registration_page)


class RegistrationPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack
        self.setWindowTitle("Регистрация")
        self.setFixedSize(360, 420)

        # --- Основной контейнер ---
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # --- Заголовок ---
        title = QLabel("Регистрация")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- Форма ---
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        self.username_text_box = QLineEdit()
        self.username_text_box.setPlaceholderText("Логин")

        self.password_text_box = QLineEdit()
        self.password_text_box.setPlaceholderText("Пароль")
        self.password_text_box.setEchoMode(QLineEdit.Password)

        self.firstname_text_box = QLineEdit()
        self.firstname_text_box.setPlaceholderText("Имя")

        self.lastname_text_box = QLineEdit()
        self.lastname_text_box.setPlaceholderText("Фамилия")

        self.phone_number_text_box = QLineEdit()
        self.phone_number_text_box.setPlaceholderText("Номер телефона")

        form_layout.addRow("Логин:", self.username_text_box)
        form_layout.addRow("Пароль:", self.password_text_box)
        form_layout.addRow("Имя:", self.firstname_text_box)
        form_layout.addRow("Фамилия:", self.lastname_text_box)
        form_layout.addRow("Номер телефона:", self.phone_number_text_box)

        layout.addLayout(form_layout)

        # --- Кнопка регистрации ---
        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.setFixedHeight(45)
        self.register_btn.clicked.connect(self.register)

        # --- Кнопка входа ---
        self.login_btn = QPushButton("Войти")
        self.login_btn.setFixedHeight(45)
        self.login_btn.clicked.connect(self.open_log_in_page)

        layout.addWidget(self.register_btn)
        layout.addWidget(self.login_btn)

        # --- Стиль ---
        self.setStyleSheet("""
                    QLabel {
                        color: #1A3E6E;
                    }
                    /* Тёмный текст внутри полей ввода */
                    QLineEdit {
                        color: #000000;
                        padding: 10px;
                        border-radius: 8px;
                        border: 2px solid #C7D8F7;
                        background: #ffffff;
                    }
                    /* Светлый плейсхолдер (смягчает визуал) */
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
        global user_info
        username = self.username_text_box.text().lower()
        password = self.password_text_box.text()
        firstname = self.firstname_text_box.text().lower()
        lastname = self.lastname_text_box.text().lower()
        phone_number = self.phone_number_text_box.text()
        url = "http://localhost:8080/worker/register"
        json = {
            "username": username,
            "password": password,
            "firstName": firstname,
            "lastName": lastname,
            "phoneNum": phone_number
        }
        response = requests.post(url, json=json)
        if response.status_code != 201:
            QMessageBox.information(self, "Регистрация", response.text)
        else:
            user_info = get_user_info(response)
            self.stack.setCurrentWidget(main_page)

    def open_log_in_page(self):
        self.stack.setCurrentWidget(log_in_page)


class MainPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setWindowTitle("Главное меню")
        self.setFixedSize(360, 420)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Заголовок
        title = QLabel("Главное меню")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Кнопки меню
        self.orders_btn = QPushButton("Посмотреть заказы")
        self.notifications_btn = QPushButton("Посмотреть уведомления")
        self.notifications_btn.clicked.connect(self.open_notifications_menu)
        self.reviews_btn = QPushButton("Открыть меню отзывов")
        self.logout_btn = QPushButton("Выйти из аккаунта")

        for btn in [self.orders_btn, self.notifications_btn, self.reviews_btn, self.logout_btn]:
            btn.setFixedHeight(45)
            layout.addWidget(btn)

        self.setLayout(layout)

        # Стиль
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

    def open_notifications_menu(self):
        self.stack.setCurrentWidget(notifications_page)


class NotificationsPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setWindowTitle("Уведомления")
        self.setFixedSize(600, 400)
        layout = QVBoxLayout(self)

        list_widget = QListWidget()

        url = "http://localhost:8080/worker/getNotifications"
        response = get_response_with_user_data(url, user_info["username"])
        if response.status_code != 200:
            QMessageBox.information(self, "Ошибка", response.text)
            self.stack.setCurrentWidget(log_in_page)
            return
        else:
            notifications = response.json()

        for notification in notifications:
            item = QListWidgetItem()
            widget = QWidget()
            vbox = QVBoxLayout()
            vbox.setSpacing(2)
            type_id = notification["typeId"]
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

            vbox.addWidget(QPushButton(text))

            widget.setLayout(vbox)
            item.setSizeHint(widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)

        layout.addWidget(list_widget)

        self.setStyleSheet("""
                    QWidget {
                        background-color: #F7FAFF;
                    }
                    QPushButton {
                        color: #1A3E6E;
                        background-color: #ffffff;
                        border: 2px solid #C7D8F7;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #fff000;
                    }
                    QPushButton:pressed {
                        background-color: #4C82D1;
                    }
                """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    stack.setStyleSheet("background-color: #F7FAFF;")

    log_in_page = LoginPage(stack)
    registration_page = RegistrationPage(stack)
    main_page = MainPage(stack)
    notifications_page = NotificationsPage(stack)

    stack.addWidget(log_in_page)
    stack.addWidget(registration_page)
    stack.addWidget(main_page)
    stack.addWidget(notifications_page)

    if user_info:
        stack.setCurrentWidget(main_page)
    else:
        stack.setCurrentWidget(log_in_page)

    stack.resize(360, 420)
    stack.show()
    sys.exit(app.exec())
