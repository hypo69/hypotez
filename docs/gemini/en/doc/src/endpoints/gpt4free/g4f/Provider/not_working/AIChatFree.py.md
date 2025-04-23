# Документация для модуля `AIChatFree.py`

## Обзор

Модуль `AIChatFree.py` предоставляет асинхронный генератор для взаимодействия с сервисом AIChatFree. Он позволяет отправлять запросы к модели `gemini-1.5-pro` и получать ответы в виде асинхронного потока. Модуль также включает в себя функцию для генерации подписи запроса, необходимой для аутентификации.

## Подробнее

Этот модуль используется для интеграции с сервисом AIChatFree, который предоставляет API для работы с моделью `gemini-1.5-pro`. Он особенно полезен в случаях, когда требуется асинхронное взаимодействие с сервисом, например, в веб-приложениях. В коде реализована поддержка прокси и обработка ошибок, связанных с ограничением скорости запросов.

## Классы

### `AIChatFree`

**Описание**: Класс `AIChatFree` предоставляет методы для асинхронного взаимодействия с сервисом AIChatFree.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса AIChatFree (`"https://aichatfree.info"`).
- `working` (bool): Указывает, работает ли провайдер (по умолчанию `False`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (по умолчанию `True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (по умолчанию `True`).
- `default_model` (str): Модель, используемая по умолчанию (`"gemini-1.5-pro"`).

**Принцип работы**:
Класс использует `aiohttp` для отправки асинхронных запросов к сервису AIChatFree. Он генерирует подпись для каждого запроса с помощью функции `generate_signature` и обрабатывает возможные ошибки, такие как превышение лимита запросов.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    connector: BaseConnector = None,
    **kwargs,
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с сервисом AIChatFree.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. Defaults to None.
        connector (BaseConnector, optional): Aiohttp коннектор. Defaults to None.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от сервиса.

    Raises:
        RateLimitError: Если достигнут лимит запросов.
        Exception: При других ошибках во время запроса.
    """
    ...
```

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Как работает функция**:
- Функция создает заголовки запроса, включая User-Agent, Accept и Content-Type.
- Генерирует timestamp и подпись запроса с использованием функции `generate_signature`.
- Формирует данные запроса, включая сообщения, timestamp и подпись.
- Отправляет POST-запрос к сервису AIChatFree с использованием `aiohttp`.
- Обрабатывает возможные ошибки, такие как превышение лимита запросов (RateLimitError).
- Возвращает асинхронный генератор, который выдает ответы от сервиса по частям.

**Примеры**:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.AIChatFree import AIChatFree
from typing import List, Dict

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "У меня все хорошо, спасибо!"},
        {"role": "user", "content": "Что ты умеешь?"}
    ]
    async for response in AIChatFree.create_async_generator(model="gemini-1.5-pro", messages=messages):
        print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `generate_signature`

```python
def generate_signature(time: int, text: str, secret: str = ""):
    """Генерирует подпись для запроса к сервису AIChatFree.

    Args:
        time (int): Timestamp запроса.
        text (str): Текст сообщения.
        secret (str, optional): Секретный ключ. Defaults to "".

    Returns:
        str: Подпись запроса в виде SHA256 хеша.
    """
    ...
```

**Параметры**:
- `time` (int): Timestamp запроса.
- `text` (str): Текст сообщения.
- `secret` (str, optional): Секретный ключ. По умолчанию `""`.

**Как работает функция**:
- Функция создает строку сообщения, объединяя timestamp, текст сообщения и секретный ключ.
- Вычисляет SHA256 хеш от этой строки.
- Возвращает хеш в шестнадцатеричном формате.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.Provider.not_working.AIChatFree import generate_signature

time = 1678886400
text = "Привет, как дела?"
signature = generate_signature(time, text)
print(signature)
```