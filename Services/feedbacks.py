import json
import requests


def ask_about_feedback(notification, user_info, app):
    print("Оставить отзыв? Y/N")
    if input().lower() == "y":
        send_feedback(notification, user_info, app)


def send_feedback(notification, user_info, app):
    rating = int(input("Оцените услугу от 1 до 5: "))
    print("Оставьте комментарий по желанию:")
    comment = input()
    if comment.strip() == "": comment = None
    print(rating, comment)
    worker_id = notification["workerId"]["$oid"]
    url = f"http://localhost:8080/{app}/sendFeedback"
    with open("Data\\session.json", "r") as f:
        session_token = json.load(f)["sessionToken"]
    data = {
        'username': user_info["username"],
        'sessionToken': session_token,
        'authorId': user_info["_id"]["$oid"],
        'targetId': worker_id,
        "rating": rating,
        "comment": comment
    }
    response = requests.post(url=url, json=data)
    print(response.text)