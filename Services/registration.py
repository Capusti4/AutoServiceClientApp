import requests


def register(app):
    url = f"http://localhost:8080/{app}/register"

    username = input("Логин: ").lower()
    password = input("Пароль: ")
    first_name = input("Имя: ").lower()
    last_name = input("Фамилия: ").lower()
    phone_num = input("Номер телефона: ")

    json = {
        "username": username,
        "password": password,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNum": phone_num
    }

    return requests.post(url=url, json=json)

