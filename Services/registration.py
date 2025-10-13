def get_registration_data():
    username = input("Логин: ").lower()
    password = input("Пароль: ")
    first_name = input("Имя: ").lower()
    last_name = input("Фамилия: ").lower()
    phone_num = input("Номер телефона: ")

    return {
        "username": username,
        "password": password,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNum": phone_num
    }
