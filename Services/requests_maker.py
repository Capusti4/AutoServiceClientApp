import json
import requests


def get_response_with_user_data(url, username):
    with open("Data\\session.json", "r") as f:
        session_token = json.load(f)["sessionToken"]
    data = {
        'username': username,
        'sessionToken': session_token
    }
    return requests.post(url=url, json=data)