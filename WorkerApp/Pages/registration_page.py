import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QFormLayout, QPushButton, QMessageBox

from Services.responses import get_user_info


class RegistrationPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.username_textbox = QLineEdit("Логин")
        self.password_textbox = QLineEdit("Пароль")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        self.firstname_textbox = QLineEdit("Имя")
        self.lastname_textbox = QLineEdit("Фамилия")
        self.phone_number_textbox = QLineEdit("Номер телефона")

        self.setWindowTitle("Регистрация")
        self.setFixedSize(360, 420)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.create_tittle()
        self.create_form_layout()
        self.create_buttons()
        self.set_style_sheet()

    def create_tittle(self):
        title = QLabel("Регистрация")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

    def create_form_layout(self):
        form_layout = QFormLayout()
        form_layout.addRow("Логин:", self.username_textbox)
        form_layout.addRow("Пароль:", self.password_textbox)
        form_layout.addRow("Имя:", self.firstname_textbox)
        form_layout.addRow("Фамилия:", self.lastname_textbox)
        form_layout.addRow("Номер телефона:", self.phone_number_textbox)
        self.layout.addLayout(form_layout)

    def create_buttons(self):
        register_button = QPushButton("Зарегистрироваться")
        register_button.setFixedHeight(45)
        register_button.clicked.connect(self.register)
        login_button = QPushButton("Войти")
        login_button.setFixedHeight(45)
        login_button.clicked.connect(self.router.open_login_page)
        self.layout.addWidget(register_button)
        self.layout.addWidget(login_button)

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
        if response.status_code != 201:
            QMessageBox.information(self, "Регистрация", response.text)
        else:
            self.router.user = get_user_info(response)
            self.router.open_main_page()
