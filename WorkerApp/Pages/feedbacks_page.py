from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem

from Services.feedbacks import get_feedbacks


class FeedbacksPage(QWidget):
    def __init__(self, router):
        super().__init__()

        self.router = router
        self.setWindowTitle("Отзывы")
        self.setFixedSize(600, 500)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.empty_label = QLabel("Отзывов нет")
        self.feedbacks_list = QListWidget()
        self.back_button = QPushButton("Назад")

        self.modify_empty_label()
        self.layout.addWidget(self.feedbacks_list)
        self.modify_back_button()
        self.set_styles_sheet()

    def modify_empty_label(self):
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #1A3E6E; font-size: 18px;")
        self.empty_label.hide()
        self.layout.addWidget(self.empty_label)

    def modify_back_button(self):
        self.back_button.clicked.connect(self.router.open_main_page)
        self.back_button.setFixedHeight(40)
        self.layout.addWidget(self.back_button)

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

    def update_ui(self):
        url = "http://localhost:8080/worker/getFeedbacksForUser"
        feedbacks = get_feedbacks(url, self.router.user["username"])

        self.feedbacks_list.clear()

        if not feedbacks:
            self.empty_label.show()
            return
        self.empty_label.hide()
        for feedback in feedbacks:
            self.add_feedback_item(feedback)

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
