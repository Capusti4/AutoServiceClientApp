from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from Services.sessions import delete_session


class MainPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.layout = QVBoxLayout()
        self.router = router
        self.orders_button = QPushButton("Посмотреть заказы")
        self.reviews_button = QPushButton("Открыть меню отзывов")
        self.notifications_button = QPushButton("Открыть уведомления")
        self.logout_button = QPushButton("Выйти из аккаунта")

        self.setWindowTitle("Главное меню")
        self.setFixedSize(360, 420)

        self.modify_layout()
        self.create_tittle()
        self.modify_buttons()
        self.set_style_sheet()

    def modify_layout(self):
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

    def create_tittle(self):
        title = QLabel("Главное меню")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

    def modify_buttons(self):
        self.orders_button.clicked.connect(self.router.open_orders_page)
        self.notifications_button.clicked.connect(self.router.open_notifications_page)
        self.reviews_button.clicked.connect(self.router.open_feedbacks_page)
        self.logout_button.clicked.connect(self.exit_from_account)
        for button in [self.orders_button, self.notifications_button, self.reviews_button, self.logout_button]:
            button.setFixedHeight(45)
            self.layout.addWidget(button)

    def exit_from_account(self):
        response = delete_session("worker")
        if response.status_code != 200:
            QMessageBox.information(self, "Ошибка", response.text)
        else:
            QMessageBox.information(self, "Выход", response.text)
            self.router.open_login_page()

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
