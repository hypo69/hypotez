# Myshell.py

## Обзор

Этот модуль предоставляет класс `Myshell`, который реализует асинхронный генератор для взаимодействия с API сервиса Myshell.ai. 

Myshell.ai - это платформа для взаимодействия с различными AI-моделями, включая GPT-3.5-turbo и GPT-4. 

`Myshell` использует WebSocket-соединение для отправки запросов и получения ответов от сервера Myshell.ai.  

## Подробей

`Myshell` предоставляет метод `create_async_generator` для отправки запросов к API Myshell.ai. Этот метод принимает параметры, такие как модель, список сообщений, прокси-сервер и таймаут. 

Метод `create_async_generator` возвращает асинхронный генератор, который позволяет получить ответы от модели Myshell.ai в виде потока текста. 

## Классы

### `class Myshell(AsyncGeneratorProvider)`

**Описание**: Класс, реализующий асинхронный генератор для взаимодействия с сервисом Myshell.ai.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес API Myshell.ai.
- `working` (bool): Флаг, указывающий на то, работает ли генератор в данный момент.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на то, поддерживает ли генератор модель GPT-3.5-turbo.
- `supports_gpt_4` (bool): Флаг, указывающий на то, поддерживает ли генератор модель GPT-4.

**Методы**:
- `create_async_generator()`:  Асинхронный метод, который создает асинхронный генератор для взаимодействия с API Myshell.ai.

## Методы класса

### `def create_async_generator(cls, model: str, messages: Messages, proxy: str = None, timeout: int = 90, **kwargs) -> AsyncResult:`

**Назначение**: Метод создает асинхронный генератор для взаимодействия с API Myshell.ai.

**Параметры**:
- `model` (str): Имя модели, с которой требуется взаимодействовать. 
- `messages` (Messages): Список сообщений, которые будут переданы модели.
- `proxy` (str, optional): Прокси-сервер для подключения. По умолчанию `None`.
- `timeout` (int, optional): Таймаут для соединения. По умолчанию 90 секунд.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который позволяет получать ответы от модели Myshell.ai в виде потока текста.

**Вызывает исключения**:
- `ValueError`: Если указана неподдерживаемая модель.

**Как работает функция**:
- Проверяет, указана ли модель. Если нет, то используется модель `samantha` по умолчанию.
- Проверяет, поддерживается ли указанная модель.
- Генерирует уникальный идентификатор посетителя.
- Открывает WebSocket-соединение с сервером Myshell.ai.
- Отправляет и получает приветственное сообщение.
- Отправляет сообщение с запросом на выполнение задачи.
- Получает ответы от модели Myshell.ai в виде потока текста.
- Возвращает асинхронный генератор, который позволяет получить ответы от модели Myshell.ai в виде потока текста.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Myshell import Myshell
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages(
    [
        {
            "role": "user",
            "content": "Привет, как дела?",
        },
    ]
)
async_generator = await Myshell.create_async_generator(
    model="samantha",
    messages=messages,
)
async for response in async_generator:
    print(response)
```

## Внутренние функции

### `def generate_timestamp() -> str:`

**Назначение**:  Генерирует временную метку в формате, используемом сервисом Myshell.ai.

**Параметры**:
-  Отсутствуют.

**Возвращает**:
- `str`: Временная метка.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Myshell import generate_timestamp
timestamp = generate_timestamp()
print(timestamp)
```

### `def generate_signature(text: str) -> dict:`

**Назначение**:  Генерирует подпись для сообщения, используемую сервисом Myshell.ai.

**Параметры**:
- `text` (str): Текст сообщения.

**Возвращает**:
- `dict`: Словарь, содержащий подпись, временную метку и версию.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Myshell import generate_signature
signature = generate_signature("Hello, world!")
print(signature)
```

### `def xor_hash(B: str) -> str:`

**Назначение**: Вычисляет хеш-значение строки.

**Параметры**:
- `B` (str): Строка для вычисления хеша.

**Возвращает**:
- `str`: Хеш-значение строки в шестнадцатеричном формате.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Myshell import xor_hash
hash_value = xor_hash("Hello, world!")
print(hash_value)
```

### `def performance() -> str:`

**Назначение**:  Измеряет производительность системы.

**Параметры**:
-  Отсутствуют.

**Возвращает**:
- `str`: Строка, представляющая производительность системы.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Myshell import performance
performance_value = performance()
print(performance_value)
```

### `def generate_visitor_id(user_agent: str) -> str:`

**Назначение**:  Генерирует уникальный идентификатор посетителя.

**Параметры**:
- `user_agent` (str): User-Agent браузера.

**Возвращает**:
- `str`: Уникальный идентификатор посетителя.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Myshell import generate_visitor_id
visitor_id = generate_visitor_id("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
print(visitor_id)
```