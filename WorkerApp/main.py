import json
from http.client import responses

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
    print("1. Просмотреть заказы")
    print("2. Выйти из аккаунта")
    print("3. Закрыть приложение")
    choice = int(input())
    if choice == 1:
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
                print(f"Тип заказа: {order["type"]}")
                print(f"Комментарий: {order["comment"]}")
                print()
                print(f"Имя заказчика: {order["customerFirstName"]}")
                print(f"Фамилия заказчика: {order["customerLastName"]}")
                print(f"Номер телефона заказчика: {order["customerPhoneNum"]}")
                print("---")
        main_menu()
    elif choice == 2:
        response = delete_session("worker")
        if response.status_code == 200:
            start_menu()
        else:
            print(response.text)
    elif choice == 3:
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
