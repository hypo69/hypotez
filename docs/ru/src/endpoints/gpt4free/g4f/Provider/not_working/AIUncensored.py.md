# Модуль AIUncensored

## Обзор

Модуль `AIUncensored` предоставляет асинхронный интерфейс для взаимодействия с сервисом AIUncensored. Этот модуль позволяет отправлять запросы к моделям AIUncensored и получать ответы в виде асинхронного генератора. Поддерживается потоковая передача данных (streaming) и работа с историей сообщений.

## Подробней

Модуль предназначен для использования в асинхронных приложениях, требующих взаимодействия с AI-моделями через API AIUncensored. Он обеспечивает удобный способ отправки запросов и обработки ответов, поддерживая как потоковый, так и не потоковый режимы работы. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и включает функциональность для вычисления подписи запросов, что необходимо для аутентификации.

## Классы

### `AIUncensored`

**Описание**: Класс `AIUncensored` предоставляет методы для взаимодействия с AI-моделями AIUncensored.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к API AIUncensored.
- `api_key` (str): API-ключ для аутентификации.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Поддерживает ли потоковую передачу данных.
- `supports_system_message` (bool): Поддерживает ли системные сообщения.
- `supports_message_history` (bool): Поддерживает ли историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Псевдонимы моделей.

**Методы**:
- `calculate_signature(timestamp: str, json_dict: dict) -> str`: Вычисляет подпись запроса.
- `get_server_url() -> str`: Возвращает случайный URL сервера.
- `create_async_generator(model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от AIUncensored.

## Функции

### `calculate_signature`

```python
@staticmethod
def calculate_signature(timestamp: str, json_dict: dict) -> str:
    """Вычисляет подпись для запроса к AIUncensored.

    Args:
        timestamp (str): Временная метка запроса.
        json_dict (dict): Словарь с данными запроса в формате JSON.

    Returns:
        str: Подпись запроса.

    Как работает функция:
    1. Формирует строку сообщения, объединяя временную метку и JSON-представление данных запроса.
    2. Использует секретный ключ для создания HMAC-подписи на основе SHA256.
    3. Возвращает вычисленную подпись в шестнадцатеричном формате.

    ASCII flowchart:

    Сформировать строку сообщения (timestamp + json_dict)
    ↓
    Вычислить HMAC-подпись с использованием секретного ключа и SHA256
    ↓
    Вернуть подпись в шестнадцатеричном формате
    """
```

**Назначение**: Вычисление подписи для запроса к AIUncensored.

**Параметры**:
- `timestamp` (str): Временная метка запроса.
- `json_dict` (dict): Словарь с данными запроса в формате JSON.

**Возвращает**:
- `str`: Подпись запроса.

**Примеры**:

```python
timestamp = "1678886400"
json_data = {"messages": [{"role": "user", "content": "Hello"}]}
signature = AIUncensored.calculate_signature(timestamp, json_data)
print(signature)
```

### `get_server_url`

```python
@staticmethod
def get_server_url() -> str:
    """Возвращает случайный URL сервера из списка доступных серверов.

    Returns:
        str: URL сервера.

    Как работает функция:
    1. Определяет список доступных URL серверов.
    2. Выбирает случайный URL из списка.
    3. Возвращает выбранный URL.

    ASCII flowchart:

    Определить список доступных URL серверов
    ↓
    Выбрать случайный URL из списка
    ↓
    Вернуть выбранный URL
    """
```

**Назначение**: Возвращает случайный URL сервера из списка доступных серверов.

**Возвращает**:
- `str`: URL сервера.

**Примеры**:

```python
url = AIUncensored.get_server_url()
print(url)
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    proxy: str = None,
    api_key: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от AIUncensored.

    Args:
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Включает ли потоковый режим. По умолчанию False.
        proxy (str, optional): URL прокси-сервера. По умолчанию None.
        api_key (str, optional): API-ключ. По умолчанию None.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от AIUncensored.

    Как работает функция:
    1. Получает название модели, используя `cls.get_model(model)`.
    2. Генерирует временную метку.
    3. Формирует словарь `json_dict` с данными запроса, включая сообщения, модель и флаг потоковой передачи.
    4. Вычисляет подпись запроса с использованием `cls.calculate_signature(timestamp, json_dict)`.
    5. Формирует заголовки запроса, включая API-ключ, временную метку и подпись.
    6. Получает URL сервера с помощью `cls.get_server_url()`.
    7. Отправляет асинхронный POST-запрос к API с использованием `aiohttp.ClientSession`.
    8. Если включен потоковый режим, обрабатывает ответы построчно, извлекая данные JSON и выдавая их через генератор.
    9. Если потоковый режим выключен, ожидает полный ответ в формате JSON и выдает содержимое через генератор.

    ASCII flowchart:

    Получить название модели
    ↓
    Сгенерировать временную метку
    ↓
    Сформировать словарь json_dict с данными запроса
    ↓
    Вычислить подпись запроса
    ↓
    Сформировать заголовки запроса
    ↓
    Получить URL сервера
    ↓
    Отправить асинхронный POST-запрос
    ↓
    Обработать потоковые или не потоковые ответы
    ↓
    Выдать ответы через генератор
    """
```

**Назначение**: Создает асинхронный генератор для получения ответов от AIUncensored.

**Параметры**:
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool, optional): Включает ли потоковый режим. По умолчанию `False`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `api_key` (str, optional): API-ключ. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от AIUncensored.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, AI!"}]
async def main():
    async for message in AIUncensored.create_async_generator(model="hermes3-70b", messages=messages, stream=True):
        print(message)

import asyncio
asyncio.run(main())