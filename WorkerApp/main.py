import json

import requests

from Services.log_in import log_in
from Services.registration import register
from Services.response_parser import get_user_info
from Services.sessions import delete_session, check_session

user_info: dict


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
            print("1. Посмотреть новые заказы")
            print("2. Посмотреть заказы в процессе")
            print("3. Посмотреть завершенные заказы")
            print("4. Назад")
            match int(input()):
                case 1:
                    url = "http://localhost:8080/worker/getOrdersList"
                    with open("Data\\session.json", "r") as f:
                        session_token = json.load(f)["sessionToken"]
                    data = {
                        'username': user_info['username'],
                        'sessionToken': session_token
                    }
                    response = requests.post(url=url, json=data)
                    orders = response.json()["orders"]
                    if not orders:
                        print("Пока заказов нет")
                    else:
                        print("Заказы:")
                        print("---")
                        for order in orders:
                            print(f"ID заказа: {order["_id"]["$oid"]}")
                            print(f"Тип заказа: {order["type"]}")
                            print(f"Комментарий: {order["comment"]}")
                            print()
                            print(f"Имя заказчика: {order["customerFirstName"]}")
                            print(f"Фамилия заказчика: {order["customerLastName"]}")
                            print(f"Номер телефона заказчика: {order["customerPhoneNum"]}")
                            print("---")
                        print("Хотите взять какой-то из заказов?")
                        print("1. Да")
                        print("2. Нет")
                        if input() == "1":
                            print(f"Введите номер заказа (1-{len(orders)})")
                            order_id = orders[int(input()) - 1]["_id"]
                            with open("Data\\session.json", "r") as f:
                                session_json = json.load(f)
                            session_json["orderId"] = order_id
                            response = requests.post("http://localhost:8080/worker/startOrder", json=session_json)
                            print(response.text)
                            print(response.status_code)
                    main_menu()
                case 2:
                    print()
                case 3:
                    print()
            main_menu()
        case 2:
            response = delete_session("worker")
            if response.status_code == 200:
                start_menu()
            else:
                print(response.text)
        case 3:
            exit()


print("Сапчик")
try:
    user_info = check_session("worker")
    if user_info:
        main_menu()
    else:
        start_menu()
except FileNotFoundError:
    start_menu()
