def get_log_in_data():
    username = input("Логин: ").lower()
    password = input("Пароль: ")

    return {"username": username, "password": password}