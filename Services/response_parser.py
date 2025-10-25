import json


def get_user_info(response):
    if response.status_code == 200 or response.status_code == 201:
        user_info = response.json()["userData"]
        with open("Data\\session.json", "w", encoding="utf-8") as f:
            json.dump(response.json()["sessionInfo"], f, indent=4, ensure_ascii=False)
    else:
        user_info = None
        print(response.text)
        print(response.status_code)
    return user_info
