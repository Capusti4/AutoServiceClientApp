import requests

from Services.log_in import log_in
from Services.notification_opener import open_notification
from Services.notification_printer import print_notifications
from Services.order_creator import create_order_data
from Services.registration import register
from Services.requests_maker import get_response_with_user_data
from Services.response_parser import get_user_info
from Services.sessions import delete_session, check_session

user_info: dict


def main():
    global user_info
    print("Добрый день")
    try:
        user_info = check_session("client")
        if not user_info:
            start_menu()
        else:
            main_menu()
    except FileNotFoundError:
        start_menu()


def start_menu():
    global user_info
    print("1. Регистрация")
    print("2. Вход")
    choice = int(input())
    if choice == 1:
        response = register("client")
    elif choice == 2:
        response = log_in("client")
    else:
        exit()

    user_info = get_user_info(response)
    if user_info:
        main_menu()


def main_menu():
    global user_info
    response = get_response_with_user_data("http://localhost:8080/client/getNotificationsAmount", user_info["username"])
    try:
        amount = response.json()
    except Exception as e:
        print(f"Неизвестная ошибка {e}")
        print("Сообщите о ней в поддержку")
        exit()
    print("Че дел?")
    print("1. Сделать заказ")
    if amount > 0:
        print(f"2. Посмотреть уведомления ({amount})")
    else:
        print(f"2. Посмотреть уведомления")
    print("3. Выйти из аккаунта")
    print("4. Закрыть приложение")
    choice = int(input())
    if choice == 1:
        data = create_order_data()
        response = requests.post(url="http://localhost:8080/client/createOrder", json=data)
        print(response.text)
        main_menu()
    elif choice == 2:
        notifications_menu()
        main_menu()
    elif choice == 3:
        exit_from_account()
    elif choice == 4:
        exit()


def notifications_menu():
    url = "http://localhost:8080/client/getNotifications"
    response = get_response_with_user_data(url, user_info["username"])
    if response.status_code != 200:
        print(response.text)
    else:
        notifications = response.json()
        show_notifications(notifications)


def show_notifications(notifications):
    if not notifications:
        print("Уведомлений пока нет")
    else:
        print_notifications(notifications)
        print("Если хотите открыть уведомление - введите его номер")
        print("0 - чтобы выйти")
        choice = int(input())
        if choice != 0:
            open_notification(notifications[choice - 1], user_info["username"])


def exit_from_account():
    response = delete_session("client")
    if response.status_code == 200:
        start_menu()
    else:
        print(response.text)


if __name__ == "__main__":
    main()
