# Модуль для взаимодействия с API XAI Grok

## Обзор

Модуль предоставляет класс `XAI` для взаимодействия с API XAI Grok. Он позволяет отправлять запросы на завершение чата, как в обычном, так и в потоковом режиме.

## Подробнее

Модуль предназначен для упрощения работы с API XAI Grok. Он предоставляет удобный интерфейс для отправки запросов и обработки ответов. Для работы с API требуется ключ API, который передается при инициализации класса `XAI`.

## Классы

### `XAI`

**Описание**: Класс для взаимодействия с API XAI Grok.

**Атрибуты**:

- `api_key` (str): Ключ API для аутентификации.
- `base_url` (str): Базовый URL API (по умолчанию "https://api.x.ai/v1").
- `headers` (dict): Заголовки для HTTP-запросов, включая авторизацию и тип контента.

**Методы**:

- `__init__(api_key)`: Инициализация класса XAI.
- `_send_request(method, endpoint, data=None)`: Отправка запроса к API x.ai.
- `chat_completion(messages, model="grok-beta", stream=False, temperature=0)`: Запрос на завершение чата.
- `stream_chat_completion(messages, model="grok-beta", temperature=0)`: Запрос на завершение чата с потоковой передачей.

#### `__init__(self, api_key: str)`

**Назначение**: Инициализация экземпляра класса `XAI`.

**Параметры**:

- `api_key` (str): Ключ API для аутентификации в API XAI.

**Как работает функция**:

- Функция инициализирует класс `XAI`, сохраняя API-ключ в атрибуте `self.api_key`.
- Устанавливает базовый URL API в атрибуте `self.base_url` (https://api.x.ai/v1).
- Формирует заголовки HTTP-запроса, включая ключ авторизации и тип контента (`application/json`), и сохраняет их в атрибуте `self.headers`.

#### `_send_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict`

**Назначение**: Отправка HTTP-запроса к API XAI.

**Параметры**:

- `method` (str): HTTP-метод запроса (например, "GET", "POST", "PUT", "DELETE").
- `endpoint` (str): Конечная точка API, к которой будет отправлен запрос.
- `data` (Optional[dict], optional): Данные, которые будут отправлены в теле запроса в формате JSON. По умолчанию `None`.

**Возвращает**:

- `dict`: JSON-ответ от API.

**Вызывает исключения**:

- `requests.exceptions.HTTPError`: Если статус ответа не 2xx.

**Как работает функция**:

- Функция формирует полный URL, объединяя `self.base_url` и `endpoint`.
- Выполняет HTTP-запрос с использованием библиотеки `requests`.
- Устанавливает необходимые заголовки, включая авторизацию и тип контента.
- Если предоставлены данные (`data`), они сериализуются в JSON и отправляются в теле запроса.
- Функция проверяет статус ответа и вызывает исключение `HTTPError`, если статус не указывает на успешное выполнение (не 2xx).
- Возвращает JSON-ответ от API.

#### `chat_completion(self, messages: List[dict], model: str = "grok-beta", stream: bool = False, temperature: int = 0) -> dict`

**Назначение**: Отправка запроса на завершение чата к API XAI.

**Параметры**:

- `messages` (List[dict]): Список сообщений для чата, где каждое сообщение - это словарь с ключами "role" и "content".
- `model` (str, optional): Модель, которая будет использоваться для генерации ответа. По умолчанию "grok-beta".
- `stream` (bool, optional): Флаг, указывающий, будет ли ответ возвращаться в потоковом режиме. По умолчанию `False`.
- `temperature` (int, optional): Температура генерации, которая влияет на случайность ответа. По умолчанию 0.

**Возвращает**:

- `dict`: JSON-ответ от API с завершением чата.

**Как работает функция**:

- Функция формирует данные для запроса, включая сообщения, модель, флаг потоковой передачи и температуру.
- Вызывает метод `self._send_request` для отправки POST-запроса к конечной точке "chat/completions".
- Возвращает JSON-ответ, полученный от API.

#### `stream_chat_completion(self, messages: List[dict], model: str = "grok-beta", temperature: int = 0) -> Generator[str, None, None]`

**Назначение**: Отправка запроса на завершение чата с потоковой передачей ответов от API XAI.

**Параметры**:

- `messages` (List[dict]): Список сообщений для чата, где каждое сообщение - это словарь с ключами "role" и "content".
- `model` (str, optional): Модель, которая будет использоваться для генерации ответа. По умолчанию "grok-beta".
- `temperature` (int, optional): Температура генерации, которая влияет на случайность ответа. По умолчанию 0.

**Возвращает**:

- `Generator[str, None, None]`: Генератор строк, представляющих собой отдельные строки потокового ответа от API.

**Как работает функция**:

- Функция формирует данные для запроса, включая сообщения, модель и температуру. Устанавливает параметр `stream` в `True` для включения потоковой передачи.
- Формирует URL запроса, объединяя `self.base_url` и "chat/completions".
- Отправляет POST-запрос к API с использованием библиотеки `requests` и параметром `stream=True`.
- Проверяет статус ответа и вызывает исключение `HTTPError`, если статус не указывает на успешное выполнение (не 2xx).
- Возвращает генератор, который итерируется по строкам ответа, декодируя их в Unicode.

## Пример использования

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
```