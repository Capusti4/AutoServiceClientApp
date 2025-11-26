import requests
from time import sleep
from requests.exceptions import ConnectionError, Timeout

from Services.feedbacks import send_feedback, feedbacks_menu
from Services.log_in import log_in
from Services.notifications import notifications_menu
from Services.orders import create_order_data, print_order
from Services.registration import register
from Services.responses import get_user_info, get_response_with_user_data
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
    except ConnectionError or Timeout:
        try_restart_app()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("Произошла ошибка, пожалуйста, отправьте ее в поддержку:\n", e)


def try_restart_app():
    print(
        "Ошибка соединения, пробуем подключится еще раз, "
        "если ошибка повторяется - проверьте подключение к интернету или обратитесь в поддержку"
    )
    sleep(3)
    main()


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
    response = get_response_with_user_data("http://localhost:8080/client/getNotificationsAmount",
                                           user_info["username"])
    try:
        print_main_menu(response.json())
        match_main_menu_choice(int(input()))
    except Exception as e:
        unknown_exception(e)


def print_main_menu(amount):
    print("Че дел?")
    print("1. Сделать заказ")
    print("2. Посмотреть завершенные заказы")
    if amount > 0:
        print(f"3. Посмотреть уведомления ({amount})")
    else:
        print(f"3. Посмотреть уведомления")
    print("4. Открыть меню отзывов")
    print("5. Выйти из аккаунта")
    print("6. Закрыть приложение")


def match_main_menu_choice(choice):
    if choice == 1:
        create_order()
        main_menu()
    elif choice == 2:
        show_completed_orders()
        main_menu()
    elif choice == 3:
        notifications_menu(user_info["username"], "client")
        main_menu()
    elif choice == 4:
        feedbacks_menu(user_info["username"], "client")
        main_menu()
    elif choice == 5:
        exit_from_account()
    elif choice == 6:
        exit()


def create_order():
    data = create_order_data()
    response = requests.post(url="http://localhost:8080/client/createOrder", json=data)
    print(response.text)


def show_completed_orders():
    response = get_response_with_user_data(
        "http://localhost:8080/client/getCompletedOrders",
        user_info["username"]
    )
    if response.status_code == 200:
        orders_without_feedback = []
        orders = response.json()['orders']
        print_completed_orders(orders, orders_without_feedback)
    else:
        print(response.text)


def print_completed_orders(orders, orders_without_feedback):
    if not orders:
        print("Завершенных заказов нет")
        return
    print("Ваши завершенные заказы:")
    for order in orders:
        print_order(order, "client")
        if not order["hasCustomerFeedback"]:
            orders_without_feedback.append(order)
    print("---")
    if orders_without_feedback:
        print_orders_without_feedback(orders_without_feedback)


def print_orders_without_feedback(orders_without_feedback):
    print("У вас есть заказы без отзыва:")
    for i, order in enumerate(orders_without_feedback):
        print(f"{i + 1}. {order['_id']['$oid']}")
    print(f"Если хотите оставить отзыв - введите его номер (1-{len(orders_without_feedback)})")
    print("Введите 0 - если хотите выйти")
    choice = int(input()) - 1
    if choice != -1:
        send_feedback(orders_without_feedback[choice], user_info, "client")


def unknown_exception(e):
    print(f"Неизвестная ошибка {e}")
    print("Сообщите о ней в поддержку")
    exit()


def exit_from_account():
    response = delete_session("client")
    if response.status_code == 200:
        start_menu()
    else:
        print(response.text)


if __name__ == "__main__":
    main()
