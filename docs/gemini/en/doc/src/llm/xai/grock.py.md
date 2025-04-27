# hypotez/src/llm/xai/grock.py

## Overview

Модуль для работы с моделью Grok (ChatGPT-подобная) через API x.ai.

## Details

Модуль предоставляет класс `XAI`, который используется для взаимодействия с API x.ai и отправки запросов к модели Grok для получения ответов. 

## Classes

### `XAI`

**Описание**: Класс для взаимодействия с API x.ai и использования модели Grok для чата. 

**Атрибуты**:

 - `api_key` (str): Ключ API для аутентификации. 
 - `base_url` (str): Базовый URL API x.ai. 
 - `headers` (dict): Заголовки для запросов к API x.ai. 

**Методы**:

 - `_send_request(method, endpoint, data=None)`: Отправка запроса к API x.ai.
 - `chat_completion(messages, model="grok-beta", stream=False, temperature=0)`: Отправка запроса на завершение чата к модели Grok.
 - `stream_chat_completion(messages, model="grok-beta", temperature=0)`: Отправка запроса на завершение чата к модели Grok с потоковой передачей.

## Functions

### `_send_request(method, endpoint, data=None)`

**Описание**: Функция отправки запроса к API x.ai.

**Параметры**:

 - `method` (str): HTTP-метод (GET, POST, PUT, DELETE).
 - `endpoint` (str): Конечная точка API.
 - `data` (dict): Данные для отправки в теле запроса (для POST и PUT).

**Возвращает**:

 - `dict`: Ответ от API.

**Raises Exceptions**:

 - `requests.exceptions.HTTPError`: Если статус ответа не 2xx.

**Как работает функция**:

 1. Формирует полный URL для запроса.
 2. Отправляет запрос к API с использованием `requests.request`.
 3. Проверяет статус ответа и выбрасывает исключение `requests.exceptions.HTTPError`, если статус не 2xx.
 4. Возвращает ответ в формате JSON.

### `chat_completion(messages, model="grok-beta", stream=False, temperature=0)`

**Описание**: Функция отправки запроса на завершение чата к модели Grok.

**Параметры**:

 - `messages` (list): Список сообщений для чата.
 - `model` (str, optional): Модель для использования. По умолчанию 'grok-beta'.
 - `stream` (bool, optional): Флаг для включения потоковой передачи. По умолчанию False.
 - `temperature` (float, optional): Температура для генерации ответа. По умолчанию 0.

**Возвращает**:

 - `dict`: Ответ от API.

**Как работает функция**:

 1. Формирует данные для отправки в теле запроса.
 2. Вызывает функцию `_send_request` для отправки запроса к API с использованием метода POST.
 3. Возвращает ответ в формате JSON.

### `stream_chat_completion(messages, model="grok-beta", temperature=0)`

**Описание**: Функция отправки запроса на завершение чата к модели Grok с потоковой передачей.

**Параметры**:

 - `messages` (list): Список сообщений для чата.
 - `model` (str, optional): Модель для использования. По умолчанию 'grok-beta'.
 - `temperature` (float, optional): Температура для генерации ответа. По умолчанию 0.

**Возвращает**:

 - `Generator[str, None, None]`: Генератор строк, содержащих части ответа от API.

**Как работает функция**:

 1. Формирует данные для отправки в теле запроса, включая флаг `stream = True`.
 2. Отправляет запрос к API с использованием метода POST и параметром `stream = True`.
 3. Возвращает генератор строк, который позволяет получать части ответа по мере их поступления от API. 

## Parameter Details

 - `messages` (list): Список сообщений для чата. Состоит из словарей с ключами `role` (строка, например "system" или "user") и `content` (строка, содержащая текст сообщения).

 - `model` (str, optional): Имя модели Grok для использования. По умолчанию 'grok-beta'.

 - `stream` (bool, optional): Флаг для включения потоковой передачи. По умолчанию False.

 - `temperature` (float, optional): Температура для генерации ответа. Чем выше температура, тем более креативным будет ответ. По умолчанию 0.

## Examples

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