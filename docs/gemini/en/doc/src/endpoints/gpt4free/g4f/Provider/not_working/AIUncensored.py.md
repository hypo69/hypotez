# Документация модуля AIUncensored

## Обзор

Модуль `AIUncensored` предоставляет асинхронный интерфейс для взаимодействия с сервисом AIUncensored.
Он позволяет генерировать текст на основе предоставленных сообщений, поддерживая как потоковую передачу данных, так и обычные запросы.

## Подробнее

Модуль предназначен для использования в проектах, требующих интеграции с AIUncensored для генерации текста.
Он включает в себя функции для расчета подписи запросов, выбора случайного URL сервера и создания асинхронного генератора для получения ответов.

## Классы

### `AIUncensored`

**Описание**:
Класс `AIUncensored` является асинхронным провайдером и миксином моделей, который обеспечивает взаимодействие с AIUncensored.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса AIUncensored.
- `api_key` (str): Ключ API для доступа к сервису.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Принцип работы**:
Класс использует `aiohttp` для выполнения асинхронных HTTP-запросов к сервису AIUncensored.
Он поддерживает потоковую передачу данных, что позволяет получать ответы по частям, а также обычные запросы, возвращающие полный ответ.
Для аутентификации запросов используется механизм подписи на основе HMAC-SHA256.

## Методы класса

### `calculate_signature`

```python
@staticmethod
def calculate_signature(timestamp: str, json_dict: dict) -> str:
    """ Вычисляет подпись для запроса к AIUncensored.

    Args:
        timestamp (str): Временная метка запроса.
        json_dict (dict): Словарь с данными запроса в формате JSON.

    Returns:
        str: Подпись запроса.

    Как работает:
        Функция принимает временную метку и словарь с данными запроса, объединяет их в строку,
        подписывает с использованием секретного ключа и возвращает полученную подпись в формате HEX.
    """
    ...
```

### `get_server_url`

```python
@staticmethod
def get_server_url() -> str:
    """ Возвращает случайный URL сервера AIUncensored.

    Returns:
        str: URL сервера.

    Как работает:
        Функция выбирает случайный URL из списка доступных серверов AIUncensored.
    """
    ...
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
    """ Создает асинхронный генератор для получения ответов от AIUncensored.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `False`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        api_key (str, optional): Ключ API. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от AIUncensored.

    Как работает:
        Функция создает и отправляет запрос к AIUncensored с использованием `aiohttp`.
        В зависимости от значения параметра `stream`, она либо возвращает асинхронный генератор для потоковой передачи данных,
        либо возвращает полный ответ после завершения запроса.
        Для аутентификации запроса используется функция `calculate_signature`.
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса AIUncensored.
- `api_key` (str): Ключ API для доступа к сервису.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider import AIUncensored
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    messages: Messages = [{"role": "user", "content": "Hello, AI!"}]
    model = "hermes3-70b"
    async for response in AIUncensored.create_async_generator(model=model, messages=messages, stream=True):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
from src.endpoints.gpt4free.g4f.Provider import AIUncensored
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    messages: Messages = [{"role": "user", "content": "Как дела?"}]
    model = "hermes3-70b"
    async for response in AIUncensored.create_async_generator(model=model, messages=messages, stream=True):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())