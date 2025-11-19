import json
import requests


def open_notification(notification, username):
    print(notification["text"])
    url = "http://localhost:8080/client/readNotification"
    with open("Data\\session.json", "r") as f:
        session_token = json.load(f)["sessionToken"]
    data = {
        'username': username,
        'sessionToken': session_token,
        'notificationId': notification["_id"]["$oid"],
    }
    response = requests.post(url=url, json=data)
    if response.status_code != 200:
        print(response.text)