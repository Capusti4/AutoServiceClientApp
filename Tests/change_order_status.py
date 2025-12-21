import requests

username = "capusti4"
session_token = "kpKuOZmrbUh59vjXOqjAv-yD-eM4XrUFSqrsmUAwIZs"

response = requests.patch(
    "http://localhost:8080/worker/startOrder/69481484ff43290796dc7b12",
    headers={
        "Username": username,
        "Session-Token": session_token
    }
)

if response.status_code == 200:
    print(response.json()["message"])
else:
    print(response.json()["error"])

response = requests.patch(
    "http://localhost:8080/worker/startOrder/69481484ff43290796dc7b12",
    headers={
        "Username": username,
        "Session-Token": session_token
    }
)

if response.status_code == 200:
    print(response.json()["message"])
else:
    print(response.json()["error"])

response = requests.patch(
    "http://localhost:8080/worker/completeOrder/69481484ff43290796dc7b12",
    headers={
        "Username": username,
        "Session-Token": session_token
    }
)

if response.status_code == 200:
    print(response.json()["message"])
else:
    print(response.json()["error"])

response = requests.patch(
    "http://localhost:8080/worker/completeOrder/69481484ff43290796dc7b12",
    headers={
        "Username": username,
        "Session-Token": session_token
    }
)

if response.status_code == 200:
    print(response.json()["message"])
else:
    print(response.json()["error"])
