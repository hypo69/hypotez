# Модуль для работы с API XAI (Grok)
=======================================

Модуль содержит класс `XAI`, который предоставляет интерфейс для взаимодействия с API XAI, включая запросы на завершение чата (chat completion) в потоковом и непотоковом режимах.

## Обзор

Этот модуль предназначен для упрощения работы с API XAI, предоставляя методы для отправки запросов и обработки ответов. Он включает в себя функциональность для установки соединения с API, отправки запросов на завершение чата и обработки потоковых ответов.

## Подробней

Модуль `grock.py` предоставляет класс `XAI`, который инкапсулирует логику взаимодействия с API XAI. Этот класс позволяет отправлять запросы на завершение чата, как в обычном, так и в потоковом режиме, что позволяет получать ответы в реальном времени. Модуль использует библиотеку `requests` для отправки HTTP-запросов и библиотеку `json` для обработки данных в формате JSON.
Внутри модуля определены методы для аутентификации, формирования запросов и обработки ответов от API.

## Классы

### `XAI`

**Описание**: Класс для взаимодействия с API XAI.

**Атрибуты**:
- `api_key` (str): Ключ API для аутентификации.
- `base_url` (str): Базовый URL API (по умолчанию "https://api.x.ai/v1").
- `headers` (dict): Заголовки для HTTP-запросов, включая авторизацию и тип контента.

**Методы**:
- `__init__(self, api_key)`: Инициализирует экземпляр класса `XAI` с заданным ключом API.
- `_send_request(self, method, endpoint, data=None)`: Отправляет HTTP-запрос к API XAI.
- `chat_completion(self, messages, model="grok-beta", stream=False, temperature=0)`: Отправляет запрос на завершение чата.
- `stream_chat_completion(self, messages, model="grok-beta", temperature=0)`: Отправляет запрос на завершение чата с потоковой передачей.

**Принцип работы**:
1. Класс `XAI` инициализируется с ключом API, который используется для аутентификации при отправке запросов.
2. Метод `_send_request` отправляет HTTP-запрос к API XAI с указанными параметрами (метод, конечная точка, данные).
3. Методы `chat_completion` и `stream_chat_completion` используют `_send_request` для отправки запросов на завершение чата, соответственно в непотоковом и потоковом режимах.
4. Ответы от API возвращаются в формате JSON.

## Методы класса

### `__init__`

```python
def __init__(self, api_key):
    """
    Инициализация класса XAI.

    Args:
        api_key: Ключ API для аутентификации.
    """
    self.api_key = api_key
    self.base_url = "https://api.x.ai/v1"  # Базовый URL API
    self.headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }
```

**Назначение**: Инициализирует экземпляр класса `XAI` с заданным ключом API, базовым URL и заголовками для HTTP-запросов.

**Параметры**:
- `api_key` (str): Ключ API для аутентификации.

**Как работает функция**:
- Принимает ключ API и сохраняет его в атрибуте `api_key`.
- Устанавливает базовый URL API в атрибуте `base_url`.
- Формирует словарь с заголовками, включающий ключ API для авторизации, и сохраняет его в атрибуте `headers`.

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

    Args:
        method: Метод HTTP (GET, POST, PUT, DELETE).
        endpoint: Конечная точка API.
        data: Данные для отправки в теле запроса (для POST и PUT).
    Returns:
        Ответ от API.
    Raises:
        requests.exceptions.HTTPError: Если статус ответа не 2xx
    """
    url = f"{self.base_url}/{endpoint}"
    response = requests.request(method, url, headers=self.headers, json=data)
    response.raise_for_status()  # Выбрасывает исключение, если статус ответа не 2xx
    return response.json()
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
- Формирует URL на основе базового URL и конечной точки.
- Отправляет HTTP-запрос с использованием библиотеки `requests`.
- Вызывает исключение, если статус ответа не 2xx.
- Возвращает ответ от API в формате JSON.

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

    Args:
        messages: Список сообщений для чата.
        model: Модель для использования.
        stream: Флаг для включения потоковой передачи.
        temperature: Температура для генерации ответа.
    Returns:
        Ответ от API.
    """
    endpoint = "chat/completions"
    data = {
        "messages": messages,
        "model": model,
        "stream": stream,
        "temperature": temperature
    }
    response = self._send_request("POST", endpoint, data)
    return response
```

**Назначение**: Отправляет запрос на завершение чата.

**Параметры**:
- `messages` (list): Список сообщений для чата.
- `model` (str, optional): Модель для использования. По умолчанию "grok-beta".
- `stream` (bool, optional): Флаг для включения потоковой передачи. По умолчанию `False`.
- `temperature` (int, optional): Температура для генерации ответа. По умолчанию `0`.

**Возвращает**:
- `dict`: Ответ от API в формате JSON.

**Как работает функция**:
- Формирует данные для запроса, включающие сообщения, модель, флаг потоковой передачи и температуру.
- Отправляет POST-запрос к конечной точке "chat/completions" с сформированными данными.
- Возвращает ответ от API в формате JSON.

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

    Args:
        messages: Список сообщений для чата.
        model: Модель для использования.
        temperature: Температура для генерации ответа.

    Returns:
        Поток ответов от API.
    Raises:
        requests.exceptions.HTTPError: Если статус ответа не 2хх
    """
    endpoint = "chat/completions"
    data = {
        "messages": messages,
        "model": model,
        "stream": True,
        "temperature": temperature
    }
    url = f"{self.base_url}/{endpoint}"
    response = requests.post(url, headers=self.headers, json=data, stream=True)
    response.raise_for_status()
    return response.iter_lines(decode_unicode=True)
```

**Назначение**: Отправляет запрос на завершение чата с потоковой передачей.

**Параметры**:
- `messages` (list): Список сообщений для чата.
- `model` (str, optional): Модель для использования. По умолчанию "grok-beta".
- `temperature` (int, optional): Температура для генерации ответа. По умолчанию `0`.

**Возвращает**:
- `generator`: Поток ответов от API.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если статус ответа не 2xx

**Как работает функция**:
- Формирует данные для запроса, включающие сообщения, модель, флаг потоковой передачи (установлен в `True`) и температуру.
- Отправляет POST-запрос к конечной точке "chat/completions" с сформированными данными и параметром `stream=True`.
- Возвращает поток ответов от API, который можно итерировать для получения каждого ответа.

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