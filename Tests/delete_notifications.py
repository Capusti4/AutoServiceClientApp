from Services import requests_service

session = {
    "username": "capusti4",
    "sessionToken": "tpMVVNaFILHBblGSm2ynIB9SEmE6QF4j3HFYz0qld-Y"
}

response = requests_service.make_get_request(
    "http://localhost:8080/client/getNotifications",
    session
)

notifications = response.json()["notifications"]
for notification in notifications:
    response = requests_service.make_delete_request(
        f"http://localhost:8080/client/deleteNotification/{notification["_id"]}",
        session
    )
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(response.json()["error"])
