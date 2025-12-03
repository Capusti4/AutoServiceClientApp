import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QFormLayout, QPushButton, QMessageBox

from Services.responses import get_user_info


class LoginPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.username_textbox = QLineEdit("Логин")
        self.password_textbox = QLineEdit("Пароль")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)

        self.setWindowTitle("Вход")
        self.setFixedSize(360, 420)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.create_tittle()
        self.create_form_layout()
        self.create_buttons()
        self.set_style_sheet()

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
        login_button = QPushButton("Войти")
        login_button.setFixedHeight(45)
        login_button.clicked.connect(self.log_in)
        self.layout.addWidget(login_button)

        register_button = QPushButton("Зарегистрироваться")
        register_button.setFixedHeight(45)
        register_button.clicked.connect(self.router.open_registration_page)
        self.layout.addWidget(register_button)

    def log_in(self):
        username = self.username_textbox.text().lower()
        password = self.password_textbox.text()
        url = "http://localhost:8080/worker/logIn"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            QMessageBox.information(self, "Вход", response.text)
        else:
            self.router.user = get_user_info(response)
            self.router.open_main_menu()

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
