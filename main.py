import json
from pathlib import Path

import requests

from Services.log_in import get_log_in_data
from Services.registration import get_registration_data

def start_menu():
    try:
        if check_session():
            return
    except FileNotFoundError:
        print("Файл сессии не найден")

    print("1. Регистрация")
    print("2. Вход")
    choice = int(input())
    if choice == 1:
        url = "http://localhost:8080/client/register"
        data: dict = get_registration_data()
    elif choice == 2:
        url = "http://localhost:8080/client/logIn"
        data: dict = get_log_in_data()
    else:
        exit()

    response = requests.post(url=url, json=data)

    if response.status_code == 200 or response.status_code == 201:
        user_info = response.json()["userData"]
        with open("Data\\session.json", "w", encoding="utf-8") as f:
            json.dump(response.json()["sessionInfo"], f, indent=4, ensure_ascii=False)
        main_menu()
    else:
        print(response.text)
        print(response.status_code)

def main_menu():
    print("Че дел?")
    print("1. Оформить заказ")
    print("2. Выйти из аккаунта")
    print("3. Закрыть приложение")
    choice = int(input())
    if choice == 1:
        print("Много хочешь")
    elif choice == 2:
        with open("Data\\session.json", "r", encoding="utf-8") as f:
            user_json = json.load(f)
        Path("Data\\session.json").unlink()
        url = "http://localhost:8080/client/deleteSession"
        response = requests.post(url=url, json=user_json)
        print(response.text)
        start_menu()
    elif choice == 3:
        exit()

def check_session():
    with open("Data\\session.json", "r") as f:
        session_json = json.load(f)
    url = "http://localhost:8080/client/checkSession"
    response = requests.post(url=url, json=session_json)
    if response.status_code == 200:
        user_info = response.json()["userData"]
        print(f"Сапчик, {user_info["username"]}")
        main_menu()
        return True
    else:
        print(response.text)


print("Васап ма бой")
start_menu()