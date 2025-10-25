orders = {
    1: "Покраска авто",
    2: "Замена шин",
    3: "Замена внешней детали",
    4: "Замена внутренней детали",
    5: "Ремонт внешней детали",
    6: "Ремонт внутренней детали",
}

def create_order_data(user_info):
    print("Выберите какой тип заказа вам нужен")
    for key, value in orders.items():
        print(f"{key}: {value}")
    print("0. Свой тип заказа")
    type_id = input()
    if type_id == "0":
        print("Введите тип вашего заказа:")
        order_type = input()
    else:
        order_type = None
    print("Введите комментарий для работника")
    comment = input()
    return {
        "orderTypeId": type_id,
        "orderType": order_type,
        "userInfo": user_info,
        "comment": comment,
    }