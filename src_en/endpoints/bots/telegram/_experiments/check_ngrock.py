import requests

# URL API
url = "127.0.0.1:8443"

# Headers
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}

# Data for sending
data = {
    "key1": "value1",
    "key2": "value2"
}

# Sending Post-request
response = requests.post(url, headers=headers, json=data)

# Response processing
if response.status_code == 200:
    print("Успешно:", response.json())
else:
    print("Ошибка:", response.status_code, response.text)
