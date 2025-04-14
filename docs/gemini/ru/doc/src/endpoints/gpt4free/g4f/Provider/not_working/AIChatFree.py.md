# Модуль `AIChatFree.py`

## Обзор

Модуль предоставляет асинхронный класс `AIChatFree`, который позволяет взаимодействовать с сервисом aichatfree.info для генерации текста на основе предоставленных сообщений. Он поддерживает потоковую передачу данных и сохранение истории сообщений.

## Подробней

Модуль предназначен для использования в асинхронных приложениях, где требуется взаимодействие с AI для генерации текста. Он использует `aiohttp` для выполнения HTTP-запросов и предоставляет методы для создания асинхронных генераторов, которые возвращают чанки сгенерированного текста.

## Классы

### `AIChatFree`

**Описание**: Асинхронный класс, реализующий взаимодействие с сервисом aichatfree.info.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров, генерирующих данные.
- `ProviderModelMixin`: Миксин для добавления поддержки выбора модели.

**Атрибуты**:
- `url` (str): URL сервиса aichatfree.info.
- `working` (bool): Указывает, работает ли провайдер (в данном случае всегда `False`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (`True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер сохранение истории сообщений (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).

**Методы**:

- `create_async_generator`: Статический асинхронный метод для создания асинхронного генератора, который отправляет запросы к сервису и возвращает чанки сгенерированного текста.

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
    """
    Создает асинхронный генератор для взаимодействия с сервисом aichatfree.info.

    Args:
        cls (AIChatFree): Ссылка на класс `AIChatFree`.
        model (str): Название модели, которую необходимо использовать.
        messages (Messages): Список сообщений для отправки в сервис.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        connector (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки сгенерированного текста.

    Raises:
        RateLimitError: Если достигнут лимит запросов.
        Exception: Если возникает ошибка при выполнении запроса.

    """
    ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с сервисом aichatfree.info.

**Параметры**:
- `cls` (AIChatFree): Ссылка на класс `AIChatFree`.
- `model` (str): Название модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений для отправки в сервис.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий чанки сгенерированного текста.

**Вызывает исключения**:
- `RateLimitError`: Если достигнут лимит запросов.
- `Exception`: Если возникает ошибка при выполнении запроса.

**Как работает функция**:
1. Формирует заголовки запроса, включая User-Agent, Accept, Content-Type и Referer.
2. Создает `aiohttp.ClientSession` с использованием предоставленного коннектора или прокси.
3. Формирует данные запроса, включая сообщения, временную метку и подпись.
4. Отправляет POST-запрос к сервису `aichatfree.info/api/generate`.
5. Обрабатывает возможные ошибки, такие как `RateLimitError` (если достигнут лимит запросов) или другие исключения.
6. Возвращает асинхронный генератор, который возвращает чанки сгенерированного текста.

**Примеры**:

```python
import asyncio
from typing import List, Dict

async def main():
    model = "gemini-1.5-pro"
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Привет!"},
        {"role": "assistant", "content": "Здравствуйте!"}
    ]
    
    generator = AIChatFree.create_async_generator(model=model, messages=messages)
    
    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `generate_signature`

```python
def generate_signature(time: int, text: str, secret: str = ""):
    """
    Генерирует подпись для запроса.

    Args:
        time (int): Временная метка.
        text (str): Текст сообщения.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: Подпись в виде hexdigest.
    """
    ...
```

**Назначение**: Генерирует подпись для запроса, используя алгоритм SHA256.

**Параметры**:
- `time` (int): Временная метка.
- `text` (str): Текст сообщения.
- `secret` (str, optional): Секретный ключ. По умолчанию "".

**Возвращает**:
- `str`: Подпись в виде hexdigest.

**Как работает функция**:
1. Формирует строку сообщения, объединяя временную метку, текст сообщения и секретный ключ.
2. Кодирует строку сообщения в байты.
3. Вычисляет SHA256 хэш от байтовой строки.
4. Возвращает хэш в виде hexdigest.

**Примеры**:

```python
timestamp = int(time.time() * 1e3)
text = "Привет!"
signature = generate_signature(timestamp, text)
print(signature)