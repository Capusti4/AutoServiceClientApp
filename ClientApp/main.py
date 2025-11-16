import requests

from Services.log_in import log_in
from Services.order_creator import create_order_data
from Services.registration import register
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
    print("Че дел?")
    print("1. Сделать заказ")
    print("2. Выйти из аккаунта")
    print("3. Закрыть приложение")
    choice = int(input())
    if choice == 1:
        data = create_order_data()
        response = requests.post(url="http://localhost:8080/client/createOrder", json=data)
        print(response.text)
        main_menu()
    elif choice == 2:
        exit_from_account()
    elif choice == 3:
        exit()


def exit_from_account():
    response = delete_session("client")
    if response.status_code == 200:
        start_menu()
    else:
        print(response.text)


if __name__ == "__main__":
    main()
