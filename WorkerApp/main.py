import json

import requests

from Services.log_in import log_in
from Services.orders_printer import print_order
from Services.registration import register
from Services.requests_maker import get_response_with_user_data
from Services.response_parser import get_user_info
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
    print("Че дел?")
    print("1. Открыть заказы")
    print("2. Выйти из аккаунта")
    print("3. Закрыть приложение")
    match int(input()):
        case 1:
            orders_menu()
            main_menu()
        case 2:
            exit_from_account()
        case 3:
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
        case 4:
            main_menu()


def show_new_orders():
    url = "http://localhost:8080/worker/getNewOrdersList"
    response = get_response_with_user_data(url, user_info["username"])
    orders = response.json()["orders"]

    if not orders:
        print("Пока заказов нет")
    else:
        print("Заказы:")
        print("---")
        for order in orders:
            print_order(order)
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
    url = "http://localhost:8080/worker/getActiveOrdersList"
    response = get_response_with_user_data(url, user_info["username"])
    orders = response.json()
    if response.status_code != 200 or not orders:
        print(response.text)
        orders_menu()
        return
    for order in orders:
        print_order(order)


def exit_from_account():
    response = delete_session("worker")
    if response.status_code == 200:
        start_menu()
    else:
        print(response.text)


if __name__ == "__main__":
    main()
