import requests

body = {
    "username": "username",
    "password": "password"
}

response = requests.post('http://localhost:8080/client/login', json=body)
print(response.json()["answer"])
print(response.json())