# Модуль `FreeGpt.py`

## Обзор

Модуль `FreeGpt.py` предоставляет класс `FreeGpt`, который является асинхронным генератором для взаимодействия с API FreeGpt. Он позволяет получать ответы от моделей Gemini 1.5 Pro и Gemini 1.5 Flash, поддерживая историю сообщений и системные сообщения.

## Подробней

Модуль предназначен для интеграции с другими частями проекта `hypotez`, обеспечивая возможность использования бесплатных моделей GPT для генерации текста. Модуль включает в себя функциональность для обхода ограничений скорости и выбора случайного домена для запросов.

## Классы

### `FreeGpt`

**Описание**: Класс `FreeGpt` предоставляет асинхронный генератор для взаимодействия с API FreeGpt.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность асинхронного генератора.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к API FreeGpt (`https://freegptsnav.aifree.site`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (всегда `True`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (всегда `True`).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (list): Список поддерживаемых моделей (`[default_model, 'gemini-1.5-flash']`).

**Принцип работы**:
Класс использует асинхронный генератор для отправки запросов к API FreeGpt и получения ответов. Он обрабатывает возможные ошибки, такие как достижение лимита запросов, и возвращает сгенерированный текст.

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от API FreeGpt.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: Optional[str] = None,
    timeout: int = 120,
    **kwargs: Any
) -> AsyncGenerator[str, None]:
    """Создает асинхронный генератор для получения ответов от API FreeGpt.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса. По умолчанию 120.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        AsyncGenerator[str, None]: Асинхронный генератор, возвращающий текст ответа.

    Raises:
        RateLimitError: Если достигнут лимит запросов.
        Exception: Если возникает ошибка при выполнении запроса.
    """
```

**Назначение**: Создает асинхронный генератор, который отправляет запросы к API FreeGpt и возвращает ответы.

**Параметры**:
- `cls` (FreeGpt): Ссылка на класс `FreeGpt`.
- `model` (str): Модель для использования (например, `gemini-1.5-pro`).
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию 120.
- `**kwargs` (Any): Дополнительные параметры, которые могут быть переданы в API.

**Как работает функция**:
1. Извлекает последний `prompt` (сообщение) из списка `messages`.
2. Генерирует временную метку (`timestamp`) текущего времени.
3. Вызывает метод `_build_request_data` для формирования данных запроса.
4. Выбирает случайный домен из списка `DOMAINS`.
5. Использует `StreamSession` для отправки асинхронного POST-запроса к API.
6. Обрабатывает ответ, проверяя наличие ошибки лимита запросов (`RATE_LIMIT_ERROR_MESSAGE`).
7. Возвращает асинхронный генератор, который выдает части ответа.

**Примеры**:

```python
import asyncio
from typing import List, Dict

async def main():
    model = "gemini-1.5-pro"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Напиши короткий стих."}]

    generator = FreeGpt.create_async_generator(model=model, messages=messages)
    
    async for chunk in await generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

### `_build_request_data`

```python
@staticmethod
def _build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]:
    """Создает словарь с данными для запроса к API FreeGpt.

    Args:
        messages (Messages): Список сообщений для отправки.
        prompt (str): Последнее сообщение пользователя.
        timestamp (int): Временная метка запроса.
        secret (str, optional): Секретный ключ для подписи запроса. По умолчанию "".

    Returns:
        Dict[str, Any]: Словарь с данными для запроса.
    """
```

**Назначение**: Формирует словарь с данными для отправки запроса к API FreeGpt.

**Параметры**:
- `messages` (Messages): Список сообщений для отправки.
- `prompt` (str): Последнее сообщение пользователя.
- `timestamp` (int): Временная метка запроса.
- `secret` (str, optional): Секретный ключ для подписи запроса. По умолчанию пустая строка.

**Как работает функция**:
Создает словарь, содержащий сообщения, временную метку, `pass` (установлен в `None`) и подпись запроса, сгенерированную функцией `generate_signature`.

**Примеры**:

```python
messages = [{"role": "user", "content": "Привет!"}]
prompt = "Привет!"
timestamp = int(time.time())
data = FreeGpt._build_request_data(messages, prompt, timestamp)
print(data)
```

## Функции

### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "") -> str:
    """Генерирует подпись для запроса к API FreeGpt.

    Args:
        timestamp (int): Временная метка запроса.
        message (str): Сообщение для подписи.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: Подпись запроса в виде шестнадцатеричной строки.
    """
```

**Назначение**: Генерирует подпись для запроса к API FreeGpt, используя алгоритм SHA256.

**Параметры**:
- `timestamp` (int): Временная метка запроса.
- `message` (str): Сообщение для подписи.
- `secret` (str, optional): Секретный ключ. По умолчанию "".

**Как работает функция**:
1. Формирует строку данных, объединяя временную метку, сообщение и секретный ключ через двоеточие.
2. Вычисляет SHA256-хеш от этой строки.
3. Возвращает хеш в виде шестнадцатеричной строки.

**Примеры**:

```python
timestamp = int(time.time())
message = "Привет!"
signature = generate_signature(timestamp, message)
print(signature)