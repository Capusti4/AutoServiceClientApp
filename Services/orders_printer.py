def print_order(order):
    print(f"ID заказа: {order["_id"]["$oid"]}")
    print(f"Тип заказа: {order["type"]}")
    print(f"Комментарий: {order["comment"]}")
    print()
    print(f"Имя заказчика: {order["customerFirstName"]}")
    print(f"Фамилия заказчика: {order["customerLastName"]}")
    print(f"Номер телефона заказчика: {order["customerPhoneNum"]}")
    print("---")