import json

import requests
from Services import requests_service, notifications_service


class Order:
    def __init__(self, order_type_id: int, order_type: str, comment: str):
        self.order_type_id = order_type_id
        self.order_type = order_type
        self.comment = comment


class App:
    def __init__(self):
        self.user = self.get_user()
        if self.user:
            self.main_menu()
        else:
            self.start_menu()

    @staticmethod
    def get_user() -> dict:
        with open("Data\\session.json", "r") as f:
            session = json.load(f)
            response = requests_service.make_get_request("http://localhost:8080/client/getUser", session)
            if response.status_code == 200:
                return response.json()

    def start_menu(self):
        print("-----")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")
        print("-----")
        choice = int(input("Ваш выбор: "))
        match choice:
            case 1:
                self.register()
            case 2:
                self.login()
            case 3:
                exit()

    def main_menu(self):
        print("-----")
        print("1. Сделать заказ")
        print("2. Посмотреть уведомления")
        print("3. Посмотреть отзывы")
        print("4. Посмотреть свои заказы")
        print("-----")
        choice = int(input())
        match choice:
            case 1:
                self.make_order()
            case 2:
                self.show_notifications()
            case 3:
                self.show_feedbacks()
            case 4:
                self.show_orders()

    def make_order(self):
        username = self.user["username"]
        session_token = self.user["session"]["sessionToken"]

        order = self.input_order()

        response = requests.post(
            "http://localhost:8080/client/makeOrder",
            json={
                "username": username,
                "sessionToken": session_token,
                "orderType": order.order_type,
                "orderTypeId": order.order_type_id,
                "comment": order.comment
            }
        )
        if response.status_code == 201:
            print(response.json()["message"])
        else:
            print(response.json()["error"])
        self.main_menu()

    @staticmethod
    def input_order() -> Order:
        orders = [
            "Покраска авто",
            "Замена шин",
            "Замена внешней детали",
            "Замена внутренней детали",
            "Ремонт внешней детали",
            "Ремонт внутренней детали",
        ]

        print("Выберите тип заказа:")
        for i, order_type in enumerate(orders):
            print(f"{i + 1}. {order_type}")
        print(f"0. Свой тип")

        order_type_id = int(input())
        if order_type_id == 0:
            order_type = input("Ваш тип заказа: ")
        else:
            order_type = orders[order_type_id - 1]
        comment = input("Комментарий к заказу: ")

        return Order(order_type_id, order_type, comment)

    def show_notifications(self):
        response = requests_service.make_get_request("http://localhost:8080/client/getNotifications",
                                                     self.user["session"])
        if response.status_code == 200:
            notifications = response.json()["notifications"]
            if not notifications:
                print("Уведомлений пока нет")
                return self.main_menu()

            notifications_service.print_notifications(notifications)
            choice = int(input("Введите номер уведомления: ")) - 1
            if choice != -1:
                notification = notifications[choice]
                print(notification["text"])
                url = f"http://localhost:8080/client/readNotification/{notification["_id"]}"
                session = self.user["session"]
                response = requests_service.make_patch_request(url, session)

                if response.status_code != 200:
                    print(response.json()["error"])
                    return self.main_menu()

                print("1. Отметить непрочитанным")
                print("2. Удалить")
                choice = int(input())
                if choice == 1:
                    url = f"http://localhost:8080/client/unreadNotification/{notification["_id"]}"
                    response = requests_service.make_patch_request(url, session)

                    if response.status_code == 200:
                        print(response.json()["message"])
                    else:
                        print(response.json()["error"])
                    self.main_menu()
                elif choice == 2:
                    url = f"http://localhost:8080/client/deleteNotification/{notification["_id"]}"
                    response = requests_service.make_delete_request(url, session)

                    if response.status_code == 200:
                        print(response.json()["message"])
                    else:
                        print(response.json()["error"])
                    self.main_menu()

        else:
            print(response.json()["error"])

    def register(self):
        username = input("Юзернейм: ")
        password = input("Пароль: ")
        first_name = input("Имя: ")
        last_name = input("Фамилия: ")
        phone_number = input("Номер телефона: ")

        body = {
            "username": username,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "phoneNumber": phone_number
        }
        response = requests.post(
            "http://localhost:8080/client/register",
            json=body
        )
        self.check_response(response)

    def login(self):
        username = input("Юзернейм: ")
        password = input("Пароль: ")

        body = {
            "username": username,
            "password": password
        }
        response = requests.post('http://localhost:8080/client/login', json=body)
        self.check_response(response)

    def check_response(self, response: requests.Response):
        if response.status_code == 201:
            print(response.json()["answer"])
            with open("Data\\session.json", "w") as f:
                json.dump(response.json()["session"], f)
            self.main_menu()
        else:
            print(response.json()["error"])
            self.start_menu()

    def show_feedbacks(self):
        print("Отзывы про Вас:")
        print("-----")
        response = requests_service.make_get_request(
            "http://localhost:8080/client/getFeedbacksForUser",
            self.user["session"]
        )
        if response.status_code == 200:
            feedbacks = response.json()["feedbacks"]
            if not feedbacks:
                print("Нету :(")
            else:
                for feedback in feedbacks:
                    print(f"Оценка: {feedback["rating"]}")
                    if feedback["comment"]:
                        print(f"Комментарий: {feedback["comment"]}")
                    print()
        else:
            print(response.json()["error"])
            return self.main_menu()

        print("Отзывы от Вас:")
        print("-----")
        response = requests_service.make_get_request(
            "http://localhost:8080/client/getFeedbacksByUser",
            self.user["session"]
        )
        if response.status_code == 200:
            feedbacks = response.json()["feedbacks"]
            if not feedbacks:
                print("Нету :(")
            else:
                for feedback in feedbacks:
                    print(f"Оценка: {feedback["rating"]}")
                    if feedback["comment"]:
                        print(f"Комментарий: {feedback["comment"]}")
                    print()
        else:
            print(response.json()["error"])
        self.main_menu()

    def show_orders(self):
        response = requests_service.make_get_request(
            "http://localhost:8080/client/getOrders",
            self.user["session"]
        )
        if response.status_code == 200:
            orders = response.json()["orders"]
            for order in orders:
                print("-----")
                print(f"Тип: {order["type"]}")
                if order["status"] == "new":
                    print("Статус: в ожидании")
                elif order["status"] == "active":
                    print("Статус: взят в работу")
                elif order["status"] == "completed":
                    print("Статус: выполнен")
                if order["comment"] is not None:
                    print(f"Комментарий: {order["comment"]}")
                if order["status"] == "completed" and not order["hasCustomerFeedback"]:
                    rating = int(input("Оцените работу от 1 до 5: "))
                    comment = input("Оставьте отзыв по желанию: ")

                    response = requests.post(
                        "http://localhost:8080/client/sendFeedback",
                        json={
                            'username': self.user["username"],
                            'sessionToken': self.user["session"]["sessionToken"],
                            'authorId': order["customerId"],
                            'targetId': order["workerId"],
                            'orderId': order["id"],
                            'rating': rating,
                            'comment': comment
                        }
                    )
                    print()
                    if response.status_code == 201:
                        print(response.json()["message"])
                    else:
                        print(response.json()["error"])
                    print()
        else:
            print(response.json()["error"])
        self.main_menu()


if __name__ == "__main__":
    app = App()
