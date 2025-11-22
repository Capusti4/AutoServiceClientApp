import json

orders = {
    1: "Покраска авто",
    2: "Замена шин",
    3: "Замена внешней детали",
    4: "Замена внутренней детали",
    5: "Ремонт внешней детали",
    6: "Ремонт внутренней детали",
}


def print_order(order, app):
    print("---")
    print(f"ID заказа: {order["_id"]["$oid"]}")
    print(f"Тип заказа: {order["type"]}")
    print(f"Комментарий: {order["comment"]}")
    if app == "worker":
        print()
        print(f"Имя заказчика: {order["customerFirstName"]}")
        print(f"Фамилия заказчика: {order["customerLastName"]}")
        print(f"Номер телефона заказчика: {order["customerPhoneNum"]}")


def create_order_data():
    print("Выберите какой тип заказа вам нужен")
    for key, value in orders.items():
        print(f"{key}: {value}")
    print("0: Свой тип заказа")
    type_id = int(input())
    if type_id == "0":
        print("Введите тип вашего заказа:")
        order_type = input()
    else:
        order_type = None
    print("Введите комментарий для работника:")
    comment = input()
    with open("Data\\session.json", "r") as f:
        user_session_info = json.load(f)
    return {
        "orderTypeId": type_id,
        "orderType": order_type,
        "userSessionInfo": user_session_info,
        "comment": comment,
    }
