# Модуль Cromicle

## Обзор

Модуль `Cromicle` предоставляет класс `Cromicle`, который представляет собой асинхронный генератор для работы с API сервиса `Cromicle.top`.

## Подробней

Класс `Cromicle` наследует от класса `AsyncGeneratorProvider`, который определен в модуле `hypotez/src/endpoints/gpt4free/g4f/Provider/base_provider.py`.  

Класс `Cromicle` использует API сервиса `Cromicle.top` для генерации текста, перевода и выполнения других задач, связанных с обработкой естественного языка. 

## Классы

### `class Cromicle`

**Описание**: Класс `Cromicle` реализует асинхронный генератор для взаимодействия с API сервиса `Cromicle.top`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url` (str): URL-адрес API сервиса.
- `working` (bool): Флаг, указывающий на доступность сервиса.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для выполнения запроса к API сервиса.

**Принцип работы**: 

Класс `Cromicle` использует асинхронный клиент HTTP `ClientSession` для отправки запросов к API сервиса. 

- В методе `create_async_generator` создается асинхронный генератор, который используется для получения потоковых ответов от API сервиса. 
-  В методе `create_async_generator`  используется функция `format_prompt` из модуля `hypotez/src/endpoints/gpt4free/g4f/Provider/helper.py`, которая  преобразует  входящие сообщения `messages` в формат, подходящий для API сервиса.
-  В методе `create_async_generator`  используется функция `_create_header`, которая формирует заголовки HTTP-запроса.
-  В методе `create_async_generator`  используется функция `_create_payload`, которая формирует тело HTTP-запроса. 
-  Метод `create_async_generator` использует `sha256` для хеширования запросов.
-  Метод `create_async_generator` использует  `response.content.iter_any()` для получения потоковых ответов от API сервиса.

## Функции

### `_create_header()`

**Назначение**: Функция `_create_header` формирует заголовки HTTP-запроса для API сервиса.

**Параметры**: 

- Нет параметров.

**Возвращает**:

- `Dict[str, str]`: Словарь заголовков HTTP-запроса.

**Как работает функция**:

- Функция `_create_header` формирует словарь заголовков HTTP-запроса, включая `accept` и `content-type`.

### `_create_payload()`

**Назначение**: Функция `_create_payload` формирует тело HTTP-запроса для API сервиса.

**Параметры**: 

- `message` (str): Текст сообщения.

**Возвращает**:

- `Dict[str, str]`: Словарь данных для тела HTTP-запроса.

**Как работает функция**:

- Функция `_create_payload` формирует словарь данных для тела HTTP-запроса,  включая текст сообщения, токен `token` и хэш запроса `hash`.
- `hash` генерируется с использованием функции `sha256` для хеширования строки, которая состоит из токена `token` и текста сообщения.

**Примеры**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Cromicle import _create_payload
>>> message = "Hello world!"
>>> _create_payload(message)
{'message': 'Hello world!', 'token': 'abc', 'hash': '439a6d8247d2b45c4923d845c45b02e001d8a49eb1446d014ef818752c8f715a'}
```

## Параметры класса

- `url` (str):  URL-адрес API сервиса.
- `working` (bool): Флаг, указывающий на доступность сервиса.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.


## Примеры

```python
# Пример использования класса `Cromicle`

from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Cromicle import Cromicle
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Привет!'}
]
async def main():
    async for stream in Cromicle.create_async_generator(model='gpt-3.5-turbo', messages=messages):
        print(stream)
```
```python
# Пример использования функции `_create_header()`

from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Cromicle import _create_header

headers = _create_header()
print(headers)

# Вывод:
{'accept': '*/*', 'content-type': 'application/json'}
```

```python
# Пример использования функции `_create_payload()`

from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Cromicle import _create_payload

message = "Hello world!"
payload = _create_payload(message)
print(payload)

# Вывод:
{'message': 'Hello world!', 'token': 'abc', 'hash': '439a6d8247d2b45c4923d845c45b02e001d8a49eb1446d014ef818752c8f715a'}
```
```python
# Пример использования функции `sha256`

from hashlib import sha256

message = "Hello world!"
token = 'abc'
hash = sha256(token.encode() + message.encode()).hexdigest()
print(hash)

# Вывод:
439a6d8247d2b45c4923d845c45b02e001d8a49eb1446d014ef818752c8f715a