# Модуль для проверки ngrok

## Обзор

Модуль содержит пример кода для отправки POST-запроса к API, предположительно, работающему через ngrok. Он демонстрирует, как установить заголовки авторизации и отправить данные в формате JSON.

## Подробней

Этот код предназначен для тестирования или взаимодействия с API, которое временно доступно через ngrok. Ngrok создает временный туннель к локальному серверу, что позволяет получить доступ к нему извне. Этот код полезен для автоматизированной проверки доступности и корректной работы API.

## Функции

### Отправка POST-запроса

```python
response = requests.post(url, headers=headers, json=data)
```

**Назначение**: Отправляет POST-запрос на указанный URL с заданными заголовками и данными.

**Параметры**:
- `url` (str): URL API, к которому отправляется запрос.
- `headers` (dict): Словарь с HTTP-заголовками для запроса.
- `data` (dict): Словарь с данными, которые отправляются в формате JSON.

**Возвращает**:
- `response` (requests.Response): Объект ответа от сервера.

**Как работает функция**:
- Функция `requests.post` отправляет POST-запрос по указанному URL.
- В заголовках передается токен авторизации и указание на формат JSON.
- Данные преобразуются в формат JSON и отправляются в теле запроса.

**Примеры**:
```python
import requests

# URL API
url = "127.0.0.1:8443"

# Заголовки
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}

# Данные для отправки
data = {
    "key1": "value1",
    "key2": "value2"
}

# Отправка POST-запроса
response = requests.post(url, headers=headers, json=data)
```

### Обработка ответа

```python
if response.status_code == 200:
    print("Успешно:", response.json())
else:
    print("Ошибка:", response.status_code, response.text)
```

**Назначение**: Проверяет статус код ответа и выводит результат или информацию об ошибке.

**Параметры**:
- `response` (requests.Response): Объект ответа от сервера.

**Как работает функция**:
- Проверяется, равен ли статус код ответа 200 (успешный запрос).
- Если запрос успешен, выводится сообщение "Успешно" и JSON-ответ.
- Если статус код отличается от 200, выводится сообщение "Ошибка", статус код и текст ошибки.

**Примеры**:
```python
import requests

# URL API
url = "127.0.0.1:8443"

# Заголовки
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}

# Данные для отправки
data = {
    "key1": "value1",
    "key2": "value2"
}

# Отправка POST-запроса
response = requests.post(url, headers=headers, json=data)

# Обработка ответа
if response.status_code == 200:
    print("Успешно:", response.json())
else:
    print("Ошибка:", response.status_code, response.text)