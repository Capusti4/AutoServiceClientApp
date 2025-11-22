import json
import requests

from Services.responses import get_response_with_user_data


def send_feedback(order, user_info, app):
    if app == "client":
        text = "Оцените услугу от 1 до 5: "
        target_id = order["workerId"]["$oid"]
    elif app == "worker":
        text = "Оцените клиента от 1 до 5: "
        target_id = order["customerId"]["$oid"]
    else:
        raise Exception("Не то приложение")
    author_id = user_info["_id"]["$oid"]
    rating = int(input(text))
    print("Оставьте комментарий по желанию:")
    comment = input()
    if comment.strip() == "": comment = None
    url = f"http://localhost:8080/{app}/sendFeedback"
    with open("Data\\session.json", "r") as f:
        session_token = json.load(f)["sessionToken"]
    data = {
        'username': user_info["username"],
        'sessionToken': session_token,
        'authorId': author_id,
        'targetId': target_id,
        'orderId': order["_id"]["$oid"],
        'rating': rating,
        'comment': comment
    }
    response = requests.post(url=url, json=data)
    print(response.text)


def show_feedbacks(username, app):
    url = f"http://localhost:8080/{app}/getFeedbacks"
    response = get_response_with_user_data(url, username)
    if response.status_code == 200:
        feedbacks = response.json()["feedbacks"]
        if feedbacks:
            print("Ваши отзывы:")
            for feedback in feedbacks:
                print("---")
                print(f"Оценка: {feedback["rating"]}")
                print(f"Комментарий: {feedback["comment"]}")
            print("---")
        else:
            print("Отзывов нет")
    else:
        print(response.text)