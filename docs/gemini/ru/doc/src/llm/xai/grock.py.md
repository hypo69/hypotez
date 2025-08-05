# Модуль `grock.py`

## Обзор

Модуль `grock.py` предоставляет класс `XAI`, который позволяет взаимодействовать с API x.ai для работы с моделями искусственного интеллекта, такими как Grok. 

## Подробнее

Модуль `grock.py` реализует класс `XAI`, который предоставляет методы для отправки запросов к API x.ai для генерации ответов от моделей ИИ, таких как Grok. Класс `XAI` поддерживает как потоковую, так и непотоковую генерацию ответов.

## Классы

### `XAI`

**Описание**: Класс `XAI` обеспечивает взаимодействие с API x.ai для работы с моделями ИИ.

**Атрибуты**:
- `api_key` (str): Ключ API для аутентификации.
- `base_url` (str): Базовый URL API x.ai.
- `headers` (dict): Заголовки HTTP-запросов.

**Методы**:
- `_send_request(method, endpoint, data=None)`: Отправляет HTTP-запрос к API x.ai.
- `chat_completion(messages, model="grok-beta", stream=False, temperature=0)`: Выполняет запрос на завершение чата.
- `stream_chat_completion(messages, model="grok-beta", temperature=0)`: Выполняет запрос на завершение чата с потоковой передачей.

#### `_send_request(method, endpoint, data=None)`

**Назначение**: Отправляет HTTP-запрос к API x.ai.

**Параметры**:
- `method` (str): Метод HTTP (GET, POST, PUT, DELETE).
- `endpoint` (str): Конечная точка API.
- `data` (dict, optional): Данные для отправки в теле запроса (для POST и PUT). По умолчанию `None`.

**Возвращает**:
- `dict`: Ответ от API в формате JSON.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: В случае ошибки при отправке запроса.

#### `chat_completion(messages, model="grok-beta", stream=False, temperature=0)`

**Назначение**: Выполняет запрос на завершение чата с использованием модели Grok.

**Параметры**:
- `messages` (list): Список сообщений для чата.
- `model` (str, optional): Модель для использования. По умолчанию "grok-beta".
- `stream` (bool, optional): Флаг для включения потоковой передачи. По умолчанию `False`.
- `temperature` (float, optional): Температура для генерации ответа. По умолчанию `0`.

**Возвращает**:
- `dict`: Ответ от API в формате JSON.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: В случае ошибки при отправке запроса.

#### `stream_chat_completion(messages, model="grok-beta", temperature=0)`

**Назначение**: Выполняет запрос на завершение чата с использованием модели Grok с потоковой передачей.

**Параметры**:
- `messages` (list): Список сообщений для чата.
- `model` (str, optional): Модель для использования. По умолчанию "grok-beta".
- `temperature` (float, optional): Температура для генерации ответа. По умолчанию `0`.

**Возвращает**:
- `generator`: Поток ответов от API.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: В случае ошибки при отправке запроса.

## Примеры

```python
# Пример использования класса XAI
if __name__ == "__main__":
    api_key = "your_api_key_here"  # Замените на ваш реальный API-ключ
    xai = XAI(api_key)

    messages = [
        {
            "role": "system",
            "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
        },
        {
            "role": "user",
            "content": "What is the answer to life and universe?"
        }
    ]

    # Непотоковый запрос
    completion_response = xai.chat_completion(messages)
    print("Non-streaming response:", completion_response)

    # Потоковый запрос
    stream_response = xai.stream_chat_completion(messages)
    print("Streaming response:")
    for line in stream_response:
        if line.strip():
            print(json.loads(line))
```