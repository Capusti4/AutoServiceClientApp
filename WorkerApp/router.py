from PySide6.QtWidgets import QStackedWidget

from Services import sessions
from WorkerApp.Pages.feedbacks_page import FeedbacksPage
from WorkerApp.Pages.login_page import LoginPage
from WorkerApp.Pages.main_page import MainPage
from WorkerApp.Pages.notifications_page import NotificationsPage
from WorkerApp.Pages.orders_page import OrdersPage
from WorkerApp.Pages.registration_page import RegistrationPage


class Router:
    def __init__(self):
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #F7FAFF;")
        self.user = sessions.check_session("worker")

        self.registration_page = RegistrationPage(self)
        self.login_page = LoginPage(self)
        self.main_page = MainPage(self)
        self.orders_page = OrdersPage(self)
        self.feedbacks_page = FeedbacksPage(self)
        self.notifications_page = NotificationsPage(self)
        self.add_widgets()

    def add_widgets(self):
        self.stack.addWidget(self.registration_page)
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.orders_page)
        self.stack.addWidget(self.feedbacks_page)
        self.stack.addWidget(self.notifications_page)

    def show(self):
        if self.user:
            self.stack.setCurrentWidget(self.main_page)
        else:
            self.stack.setCurrentWidget(self.login_page)
        self.stack.show()

    def open_login_page(self):
        self.stack.setCurrentWidget(self.login_page)

    def open_registration_page(self):
        self.stack.setCurrentWidget(self.registration_page)

    def open_orders_page(self):
        self.orders_page.update_ui()
        self.stack.setCurrentWidget(self.orders_page)

    def open_notifications_page(self):
        self.notifications_page.update_ui()
        self.stack.setCurrentWidget(self.notifications_page)

    def open_feedbacks_page(self):
        self.feedbacks_page.update_ui()
        self.stack.setCurrentWidget(self.feedbacks_page)

    def open_main_page(self):
        self.stack.setCurrentWidget(self.main_page)
