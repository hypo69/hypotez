# Модуль для взаимодействия с API XAI
==========================================

Модуль содержит класс `XAI`, который предоставляет интерфейс для взаимодействия с API XAI, включая отправку запросов на завершение чата и потоковую передачу ответов.

## Обзор

Модуль `grock.py` предназначен для упрощения взаимодействия с API XAI. Он предоставляет класс `XAI`, который инкапсулирует логику аутентификации и отправки запросов к API. Модуль поддерживает как непотоковые, так и потоковые запросы на завершение чата.

## Подробней

Этот модуль позволяет взаимодействовать с API XAI для получения ответов от модели Grok. Класс `XAI` предоставляет методы для отправки запросов и обработки ответов, включая потоковую передачу. Он использует библиотеку `requests` для отправки HTTP-запросов и `json` для обработки данных в формате JSON.

## Классы

### `XAI`

**Описание**: Класс для взаимодействия с API XAI.

**Принцип работы**: Класс инициализируется с API-ключом, который используется для аутентификации при каждом запросе. Он предоставляет методы для отправки запросов на завершение чата и потоковой передачи ответов. Класс использует библиотеку `requests` для отправки HTTP-запросов и `json` для обработки данных в формате JSON.

**Атрибуты**:
- `api_key` (str): Ключ API для аутентификации.
- `base_url` (str): Базовый URL API.
- `headers` (dict): Заголовки для HTTP-запросов, включая ключ API и тип контента.

**Методы**:
- `__init__(api_key)`: Инициализация класса XAI.
- `_send_request(method, endpoint, data=None)`: Отправка запроса к API x.ai.
- `chat_completion(messages, model="grok-beta", stream=False, temperature=0)`: Запрос на завершение чата.
- `stream_chat_completion(messages, model="grok-beta", temperature=0)`: Запрос на завершение чата с потоковой передачей.

### `__init__`

```python
    def __init__(self, api_key):
        """
        Инициализация класса XAI.

        :param api_key: Ключ API для аутентификации.
        """
```

**Назначение**: Инициализирует экземпляр класса `XAI` с заданным API-ключом.

**Параметры**:
- `api_key` (str): Ключ API для аутентификации.

**Как работает функция**:
1. Присваивает переданный `api_key` атрибуту `self.api_key`.
2. Устанавливает базовый URL API в атрибуте `self.base_url`.
3. Определяет заголовки HTTP-запроса, включая ключ API для аутентификации и указание типа контента как JSON.

```
A: Присвоение api_key
|
B: Определение base_url
|
C: Определение headers (включая api_key)
```

**Примеры**:

```python
api_key = "your_api_key_here"
xai = XAI(api_key)
```

### `_send_request`

```python
    def _send_request(self, method, endpoint, data=None):
        """
        Отправка запроса к API x.ai.

        :param method: Метод HTTP (GET, POST, PUT, DELETE).
        :param endpoint: Конечная точка API.
        :param data: Данные для отправки в теле запроса (для POST и PUT).
        :return: Ответ от API.
        """
```

**Назначение**: Отправляет HTTP-запрос к API XAI.

**Параметры**:
- `method` (str): Метод HTTP (GET, POST, PUT, DELETE).
- `endpoint` (str): Конечная точка API.
- `data` (dict, optional): Данные для отправки в теле запроса (для POST и PUT). По умолчанию `None`.

**Возвращает**:
- `dict`: Ответ от API в формате JSON.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если статус ответа не 2xx.

**Как работает функция**:
1. Формирует полный URL, объединяя `self.base_url` и `endpoint`.
2. Отправляет HTTP-запрос с использованием библиотеки `requests`.
3. Если передан параметр `data`, он включается в тело запроса в формате JSON.
4. Проверяет статус ответа и вызывает исключение `HTTPError`, если статус не 2xx.
5. Возвращает ответ от API в формате JSON.

```
A: Формирование URL
|
B: Отправка HTTP-запроса
|
C: Проверка статуса ответа
|
D: Возврат ответа в формате JSON
```

**Примеры**:

```python
api_key = "your_api_key_here"
xai = XAI(api_key)
endpoint = "chat/completions"
data = {"messages": [{"role": "user", "content": "Hello"}]}
response = xai._send_request("POST", endpoint, data)
print(response)
```

### `chat_completion`

```python
    def chat_completion(self, messages, model="grok-beta", stream=False, temperature=0):
        """
        Запрос на завершение чата.

        :param messages: Список сообщений для чата.
        :param model: Модель для использования.
        :param stream: Флаг для включения потоковой передачи.
        :param temperature: Температура для генерации ответа.
        :return: Ответ от API.
        """
```

**Назначение**: Отправляет запрос на завершение чата в API XAI.

**Параметры**:
- `messages` (list): Список сообщений для чата.
- `model` (str, optional): Модель для использования. По умолчанию "grok-beta".
- `stream` (bool, optional): Флаг для включения потоковой передачи. По умолчанию `False`.
- `temperature` (int, optional): Температура для генерации ответа. По умолчанию `0`.

**Возвращает**:
- `dict`: Ответ от API в формате JSON.

**Как работает функция**:
1. Определяет конечную точку API как "chat/completions".
2. Формирует данные запроса, включая сообщения, модель, флаг потоковой передачи и температуру.
3. Вызывает метод `_send_request` для отправки POST-запроса к API с сформированными данными.
4. Возвращает ответ от API.

```
A: Определение endpoint
|
B: Формирование данных запроса
|
C: Отправка POST-запроса
|
D: Возврат ответа
```

**Примеры**:

```python
api_key = "your_api_key_here"
xai = XAI(api_key)
messages = [{"role": "user", "content": "Hello"}]
response = xai.chat_completion(messages)
print(response)
```

### `stream_chat_completion`

```python
    def stream_chat_completion(self, messages, model="grok-beta", temperature=0):
        """
        Запрос на завершение чата с потоковой передачей.

        :param messages: Список сообщений для чата.
        :param model: Модель для использования.
        :param temperature: Температура для генерации ответа.
        :return: Поток ответов от API.
        """
```

**Назначение**: Отправляет запрос на завершение чата с потоковой передачей в API XAI.

**Параметры**:
- `messages` (list): Список сообщений для чата.
- `model` (str, optional): Модель для использования. По умолчанию "grok-beta".
- `temperature` (int, optional): Температура для генерации ответа. По умолчанию `0`.

**Возвращает**:
- `generator`: Поток ответов от API.

**Как работает функция**:
1. Определяет конечную точку API как "chat/completions".
2. Формирует данные запроса, включая сообщения, модель, флаг потоковой передачи (установлен в `True`) и температуру.
3. Формирует полный URL, объединяя `self.base_url` и `endpoint`.
4. Отправляет POST-запрос с использованием библиотеки `requests` с параметром `stream=True`.
5. Проверяет статус ответа и вызывает исключение, если статус не 2xx.
6. Возвращает итератор по строкам ответа.

```
A: Определение endpoint
|
B: Формирование данных запроса (stream=True)
|
C: Формирование URL
|
D: Отправка POST-запроса (stream=True)
|
E: Проверка статуса ответа
|
F: Возврат итератора по строкам ответа
```

**Примеры**:

```python
api_key = "your_api_key_here"
xai = XAI(api_key)
messages = [{"role": "user", "content": "Hello"}]
stream_response = xai.stream_chat_completion(messages)
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Функции

В данном модуле функции отсутствуют.

## Пример использования класса XAI

```python
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