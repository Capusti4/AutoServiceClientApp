import json
import requests

from Services.responses import get_response_with_user_data


def notifications_menu(username, app):
    url = f"http://localhost:8080/{app}/getNotifications"
    response = get_response_with_user_data(url, username)
    if response.status_code != 200:
        print(response.text)
    else:
        notifications = response.json()
        show_notifications(notifications, username, app)


def show_notifications(notifications, username, app):
    if not notifications:
        print("Уведомлений пока нет")
    else:
        print_notifications(notifications)
        print("Если хотите открыть уведомление - введите его номер")
        print("Если хотите прочитать все - введите -1")
        print("0 - чтобы выйти")
        choice = int(input()) - 1
        if choice == -2:
            url = f"http://localhost:8080/{app}/readAllNotifications"
            response = get_response_with_user_data(url, username)
            print(response.text)
        elif choice != -1:
            notification = notifications[choice]
            open_notification(notification, username, app)


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


def open_notification(notification, username, app):
    print(notification["text"])
    read_notification(notification, username, app)


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