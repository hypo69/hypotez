# Модуль AIUncensored
## Обзор

Модуль `AIUncensored` предоставляет асинхронный интерфейс для взаимодействия с AI-моделями через API AIUncensored.info. Он поддерживает потоковую передачу данных, использование системных сообщений и истории сообщений. Модуль предназначен для генерации текста с использованием различных AI-моделей.

## Подробней

Модуль использует `aiohttp` для асинхронных HTTP-запросов и предоставляет класс `AIUncensored`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он включает в себя методы для расчета подписи запроса, выбора URL сервера и создания асинхронного генератора для получения ответов от API. Модуль также обрабатывает потоковые и не потоковые ответы, возвращая результаты генерации текста.

## Классы

### `AIUncensored`

**Описание**: Класс для взаимодействия с AI-моделями через API AIUncensored.info.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL API AIUncensored.info.
- `api_key` (str): Ключ API для доступа к AIUncensored.info.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.

**Методы**:
- `calculate_signature(timestamp: str, json_dict: dict) -> str`: Вычисляет подпись для запроса к API.
- `get_server_url() -> str`: Возвращает случайный URL сервера из списка доступных.
- `create_async_generator(model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

### `calculate_signature`

```python
@staticmethod
def calculate_signature(timestamp: str, json_dict: dict) -> str:
    """
    Вычисляет подпись для запроса к API.

    Args:
        timestamp (str): Временная метка запроса.
        json_dict (dict): Словарь с данными запроса в формате JSON.

    Returns:
        str: Подпись запроса.

    Как работает функция:
    - Формирует сообщение для подписи, объединяя временную метку и JSON-представление данных запроса.
    - Использует секретный ключ для создания HMAC-подписи с использованием алгоритма SHA256.
    - Возвращает вычисленную подпись в виде шестнадцатеричной строки.

    Пример:
        >>> timestamp = '1678886400'
        >>> json_dict = {'messages': [{'role': 'user', 'content': 'Hello'}]}
        >>> AIUncensored.calculate_signature(timestamp, json_dict)
        'e5b7b3b2b4a2a1a0a9a8a7a6a5a4a3a2a1a0a9a8a7a6a5a4a3a2a1a0a9a8a7a6'
    """
    ...
```

### `get_server_url`

```python
@staticmethod
def get_server_url() -> str:
    """
    Возвращает случайный URL сервера из списка доступных.

    Returns:
        str: Случайный URL сервера.

    Как работает функция:
    - Определяет список доступных серверов.
    - Выбирает случайный URL из списка.
    - Возвращает выбранный URL.

    Пример:
        >>> AIUncensored.get_server_url()
        'https://llm-server-nov24-ibak.onrender.com'
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
    """
    Создает асинхронный генератор для получения ответов от API.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool, optional): Указывает, использовать ли потоковую передачу данных. По умолчанию `False`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        api_key (str, optional): Ключ API. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Как работает функция:
    - Получает модель, используя `cls.get_model(model)`.
    - Генерирует временную метку.
    - Формирует словарь `json_dict` с сообщениями, моделью и параметром потоковой передачи.
        - Преобразует сообщения в формат, требуемый API, с использованием `format_prompt(messages)`.
    - Вычисляет подпись запроса с использованием `cls.calculate_signature(timestamp, json_dict)`.
    - Устанавливает заголовки запроса, включая ключ API, временную метку и подпись.
    - Отправляет асинхронный POST-запрос к API.
        - Если `stream` равен `True`:
            - Получает данные потоком и обрабатывает каждую строку.
            - Извлекает JSON-данные из каждой строки и возвращает их.
            - Если встречает `[DONE]`, завершает генерацию.
        - Если `stream` равен `False`:
            - Получает JSON-ответ и возвращает содержимое поля `content`.

    Пример:
        >>> model = 'hermes3-70b'
        >>> messages = [{'role': 'user', 'content': 'Hello'}]
        >>> async for message in AIUncensored.create_async_generator(model, messages, stream=True):
        ...     print(message)
        ...
        Hello
    """
    ...
```

## Параметры класса

- `url` (str): URL API AIUncensored.info.
- `api_key` (str): Ключ API для доступа к AIUncensored.info.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.

## Примеры

Пример использования класса `AIUncensored` для получения ответа от API:

```python
import asyncio

from src.endpoints.gpt4free.g4f.Provider.not_working import AIUncensored
from src.endpoints.gpt4free.g4f.typing import Messages, AsyncResult
from src.endpoints.gpt4free.g4f.providers.response import FinishReason

async def main():
    model: str = 'hermes3-70b'
    messages: Messages = [{'role': 'user', 'content': 'Hello'}]
    generator: AsyncResult = AIUncensored.create_async_generator(model, messages, stream=True)
    
    async for message in generator:
        if isinstance(message, FinishReason):
            print(f"Завершено с причиной: {message}")
        else:
            print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())