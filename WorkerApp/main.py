import json
import requests
from time import sleep

from Services.feedbacks import send_feedback, show_feedbacks
from Services.log_in import log_in
from Services.notifications import notifications_menu
from Services.orders import print_order
from Services.registration import register
from Services.responses import get_user_info, get_response_with_user_data
from Services.sessions import delete_session, check_session

user_info: dict


def main():
    global user_info
    print("Сапчик")
    try:
        user_info = check_session("worker")
        if not user_info:
            start_menu()
        else:
            main_menu()
    except FileNotFoundError:
        start_menu()
    except requests.ConnectionError or requests.Timeout:
        try_restart_app()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        unknown_exception(e)


def try_restart_app():
    print(
        "Ошибка соединения, пробуем подключится еще раз, "
        "если ошибка повторяется - проверьте подключение к интернету или обратитесь в поддержку"
    )
    sleep(3)
    main()


def unknown_exception(e):
    print(f"Неизвестная ошибка {e}")
    print("Сообщите о ней в поддержку")
    exit()


def start_menu():
    global user_info
    print("1. Регистрация")
    print("2. Вход")
    choice = int(input())
    if choice == 1:
        response = register("worker")
    elif choice == 2:
        response = log_in("worker")
    else:
        exit()
    user_info = get_user_info(response)
    if user_info:
        main_menu()


def main_menu():
    response = get_response_with_user_data("http://localhost:8080/worker/getNotificationsAmount", user_info["username"])
    try:
        print_main_menu(response.json())
        match_main_menu_choice()
    except Exception as e:
        unknown_exception(e)


def print_main_menu(amount):
    print("Че дел?")
    print("1. Посмотреть заказы")
    if amount > 0:
        print(f"2. Посмотреть уведомления ({amount})")
    else:
        print(f"2. Посмотреть уведомления")
    print("3. Посмотреть свои отзывы")
    print("4. Выйти из аккаунта")
    print("5. Закрыть приложение")


def match_main_menu_choice():
    match int(input()):
        case 1:
            orders_menu()
            main_menu()
        case 2:
            notifications_menu(user_info, "worker")
            main_menu()
        case 3:
            show_feedbacks(user_info["username"], "worker")
            main_menu()
        case 4:
            exit_from_account()
        case 5:
            exit()


def orders_menu():
    print("1. Посмотреть новые заказы")
    print("2. Посмотреть заказы в процессе")
    print("3. Посмотреть завершенные заказы")
    print("4. Назад")
    match_orders_menu_choice(int(input()))


def match_orders_menu_choice(choice):
    match choice:
        case 1:
            show_new_orders()
            orders_menu()
        case 2:
            show_active_orders()
            orders_menu()
        case 3:
            show_completed_orders()
            orders_menu()
        case 4:
            main_menu()


def show_new_orders():
    url = "http://localhost:8080/worker/getNewOrders"
    response = get_response_with_user_data(url, user_info["username"])
    orders = response.json()["orders"]

    if not orders:
        print("Пока заказов нет")
    else:
        print("Новые заказы:")
        print("---")
        for order in orders:
            print_order(order, "worker")
        take_order(orders)


def take_order(orders):
    print("Хотите взять какой-то из заказов?")
    print("1. Да")
    print("2. Нет")
    if input() != "1": return

    print(f"Введите номер заказа (1-{len(orders)})")
    order_id = orders[int(input()) - 1]["_id"]
    with open("Data\\session.json", "r") as f:
        session_json = json.load(f)
    session_json["orderId"] = order_id
    response = requests.post("http://localhost:8080/worker/startOrder", json=session_json)
    if response.status_code == 200:
        print(f"Заказ {order_id["$oid"]} успешно взят")
    else:
        print(response.text)


def show_active_orders():
    url = "http://localhost:8080/worker/getActiveOrders"
    response = get_response_with_user_data(url, user_info["username"])
    orders = response.json()
    if response.status_code != 200:
        print(response.text)
    elif not orders:
        print("Активных заказов нет")
    else:
        print_active_orders(orders)


def print_active_orders(orders):
    print("Ваши активные заказы:")
    for order in orders:
        print_order(order, "worker")
    print(f"Если хотите завершить заказ - введите его номер (1-{len(orders)})")
    print("Чтобы выйти, введите 0")
    choice = int(input()) - 1
    if choice == -1: return
    order = orders[choice]
    with open("Data\\session.json", "r") as f:
        session_token = json.load(f)["sessionToken"]
    data = {
        'username': user_info["username"],
        'sessionToken': session_token,
        'orderId': order["_id"]["$oid"],
    }
    response = requests.post(url="http://localhost:8080/worker/completeOrder", json=data)
    print(response.text)


def show_completed_orders():
    url = "http://localhost:8080/worker/getCompletedOrders"
    response = get_response_with_user_data(url, user_info["username"])
    orders = response.json()["orders"]
    if not orders:
        print("Пока заказов нет")
    else:
        print_completed_orders(orders)


def print_completed_orders(orders):
    orders_without_feedback = []
    print("Ваши завершенные заказы:")
    for order in orders:
        print_order(order, "worker")
        if not order["hasWorkerFeedback"]: orders_without_feedback.append(order)
    print("---")
    if orders_without_feedback:
        print_orders_without_feedback(orders_without_feedback)


def print_orders_without_feedback(orders_without_feedback):
    print("У данных заказов нет отзыва:")
    for i, order in enumerate(orders_without_feedback):
        print(f"{i + 1}. {order["_id"]["$oid"]}")
    print("Чтобы оставить отзыв на один из них, напишите его номер")
    print("Чтобы выйти напишите 0")
    choice = int(input()) - 1
    if choice != -1:
        send_feedback(orders_without_feedback[choice], user_info, "worker")


def exit_from_account():
    response = delete_session("worker")
    if response.status_code == 200:
        start_menu()
    else:
        print(response.text)


if __name__ == "__main__":
    main()
