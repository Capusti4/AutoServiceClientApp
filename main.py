from pathlib import Path

import requests

from Services.log_in import get_log_in_data
from Services.registration import get_registration_data

def start_menu():
    if Path("Data\\user_info.txt").exists():
        main_menu()
        return

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
        user_info = response.json()["userInfo"]
        with open("Data\\session.txt", "a", encoding="utf-8") as f:
            f.write(response.json()["sessionToken"])
        # print(user_info)
        main_menu()
    else:
        print(response.text)
        print(response.status_code)


def main_menu():
    print("Че дел?")
    print("1. Оформить заказ")
    choice = int(input())
    if choice == 1:
        print()


print("Васап ма бой")
start_menu()