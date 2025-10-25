import requests


def log_in(app):
    url = f"http://localhost:8080/{app}/logIn"

    username = input("Логин: ").lower()
    password = input("Пароль: ")

    json = {"username": username, "password": password}

    return requests.post(url, json=json)
