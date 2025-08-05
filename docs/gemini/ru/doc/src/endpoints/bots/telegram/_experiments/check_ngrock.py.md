# Проверка доступности ngrok-туннеля

## Обзор

Этот файл содержит код, который проверяет доступность ngrok-туннеля, отправляя POST-запрос на его URL. 

## Подробней

Файл используется для отладки и проверки работоспособности ngrok-туннеля. Он определяет URL API, заголовки запроса и данные для отправки. 
Затем отправляет POST-запрос на URL API и анализирует ответ, выводя сообщение об успехе или ошибке.

## Функции

### `check_ngrok`

**Назначение**: Проверяет доступность ngrok-туннеля.

**Параметры**:
- `url` (str): URL ngrok-туннеля.
- `headers` (dict): Заголовки запроса.
- `data` (dict): Данные для отправки в запросе.

**Возвращает**:
- `bool`: Возвращает `True` если запрос был успешным, иначе `False`.

**Как работает**:

1. Функция `check_ngrok` создает запрос с помощью `requests.post`.
2. Она использует URL туннеля, заголовки и данные, которые были предоставлены в качестве аргументов.
3. После получения ответа от сервера функция проверяет код статуса ответа.
4. Если код статуса равен 200 (успех), функция возвращает `True`.
5. В противном случае функция возвращает `False`.

**Примеры**:
```python
# Пример вызова функции с корректным URL, заголовками и данными
result = check_ngrok(url='https://example.ngrok.io', headers={'Authorization': 'Bearer YOUR_API_TOKEN'}, data={'key1': 'value1'})
if result:
    print('ngrok-туннель доступен')
else:
    print('ngrok-туннель недоступен')

# Пример вызова функции с некорректным URL
result = check_ngrok(url='https://invalid.url', headers={'Authorization': 'Bearer YOUR_API_TOKEN'}, data={'key1': 'value1'})
if result:
    print('ngrok-туннель доступен')
else:
    print('ngrok-туннель недоступен')
```
```python
def check_ngrok(url: str, headers: dict, data: dict) -> bool:
    """
    Проверяет доступность ngrok-туннеля, отправляя POST-запрос на его URL.

    Args:
        url (str): URL ngrok-туннеля.
        headers (dict): Заголовки запроса.
        data (dict): Данные для отправки в запросе.

    Returns:
        bool: Возвращает `True` если запрос был успешным, иначе `False`.
    """
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False
```
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
```

## Примеры

```python
# Пример использования функции `check_ngrok`
from hypotez.src.endpoints.bots.telegram._experiments.check_ngrock import check_ngrok

# Определение URL ngrok-туннеля, заголовков и данных
url = 'https://example.ngrok.io'
headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
data = {'key1': 'value1'}

# Вызов функции `check_ngrok`
result = check_ngrok(url, headers, data)

# Вывод результата
if result:
    print('ngrok-туннель доступен')
else:
    print('ngrok-туннель недоступен')
```
```python
# Пример использования функции `check_ngrok` с некорректным URL
from hypotez.src.endpoints.bots.telegram._experiments.check_ngrock import check_ngrok

# Определение URL ngrok-туннеля, заголовков и данных
url = 'https://invalid.url'
headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
data = {'key1': 'value1'}

# Вызов функции `check_ngrok`
result = check_ngrok(url, headers, data)

# Вывод результата
if result:
    print('ngrok-туннель доступен')
else:
    print('ngrok-туннель недоступен')
```
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