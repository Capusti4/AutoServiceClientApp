import requests

body = {
    "username": "userna",
    "password": "password",
    "firstName": "Имя",
    "lastName": "Фамилия",
    "phoneNumber": "88005553532"
}

response = requests.post(
    "http://localhost:8080/client/register",
    json=body
)
print(response.json())
