import requests

LOGIN_URL = "http://127.0.0.1:5000/login"

data = {
    "username": "admin",
    "password": "wrongpassword"
}

headers = {
    "User-Agent": "BotScanner/1.0",
    "X-Forwarded-For": "192.168.1.250"
}

response = requests.post(LOGIN_URL, data=data, headers=headers)

print("Status Code:", response.status_code)
print("Response Text:", response.text[:200])