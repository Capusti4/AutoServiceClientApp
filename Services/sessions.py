import json
from pathlib import Path
import requests


def check_session(name):
    try:
        with open("Data\\session.json", "r") as f:
            session_json = json.load(f)
        url = f"http://localhost:8080/{name}/checkSession"
        response = requests.post(url=url, json=session_json)
        if response.status_code == 200:
            user_info = response.json()["userData"]
        else:
            user_info = None
        return user_info
    except FileNotFoundError:
        return None

def delete_session(app):
    with open("Data\\session.json", "r", encoding="utf-8") as f:
        user_json = json.load(f)
    Path("Data\\session.json").unlink()
    url = f"http://localhost:8080/{app}/deleteSession"
    return requests.post(url=url, json=user_json)
