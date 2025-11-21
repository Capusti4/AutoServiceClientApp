import json

import requests

from Services.feedbacks import ask_about_feedback
from Services.requests_maker import get_response_with_user_data


def notifications_menu(user_info, app):
    url = f"http://localhost:8080/{app}/getNotifications"
    response = get_response_with_user_data(url, user_info["username"])
    if response.status_code != 200:
        print(response.text)
    else:
        notifications = response.json()
        show_notifications(notifications, user_info, app)


def show_notifications(notifications, user_info, app):
    if not notifications:
        print("Уведомлений пока нет")
    else:
        print_notifications(notifications)
        print("Если хотите открыть уведомление - введите его номер")
        print("0 - чтобы выйти")
        choice = int(input()) - 1
        if choice != -1:
            notification = notifications[choice]
            open_notification(notification, user_info, app)


def print_notifications(notifications):
    print("---")
    for i, notification in enumerate(notifications):
        type_id = notification["typeId"]
        text = ""
        match type_id:
            case 1:
                text = f"{i + 1}. Важное уведомление"
            case 2:
                text = f"{i + 1}. Ваш заказ взят в работу"
            case 3:
                text = f"{i + 1}. Ваш заказ завершен"
            case 4:
                text = f"{i + 1}. Вам оставили отзыв"
            case 5:
                text = f"{i + 1}. Вы завершили заказ, оставьте отзыв о клиенте"
        if not notification["isRead"]:
            text += " !"
        print(text)
        print("---")


def open_notification(notification, user_info, app):
    print(notification["text"])
    read_notification(notification, user_info["username"], app)
    if notification["typeId"] == (3 or 5) and not notification["isRead"]:
        ask_about_feedback(notification, user_info, app)


def read_notification(notification, username, app):
    url = f"http://localhost:8080/{app}/readNotification"
    with open("Data\\session.json", "r") as f:
        session_token = json.load(f)["sessionToken"]
    data = {
        'username': username,
        'sessionToken': session_token,
        'notificationId': notification["_id"]["$oid"],
    }
    response = requests.post(url=url, json=data)
    if response.status_code != 200:
        print(response.text)