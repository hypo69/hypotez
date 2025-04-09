# Модуль для работы с провайдером AutonomousAI
=================================================

Модуль содержит класс `AutonomousAI`, который используется для взаимодействия с AI-моделями через API AutonomousAI.
Поддерживает стриминг, системные сообщения и историю сообщений.

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с различными AI-моделями, предоставляемыми AutonomousAI.
Он включает поддержку стриминга ответов, передачи системных сообщений и сохранения истории сообщений.
Модуль использует `aiohttp` для асинхронных HTTP-запросов и `base64` для кодирования сообщений.

## Подробнее

Этот модуль предназначен для использования в проекте `hypotez` в качестве одного из провайдеров для работы с AI-моделями.
Он позволяет отправлять запросы к API AutonomousAI и получать ответы в асинхронном режиме, поддерживая различные модели и параметры.

## Классы

### `AutonomousAI`

**Описание**: Класс для взаимодействия с AI-моделями через API AutonomousAI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL главной страницы AutonomousAI.
- `api_endpoints` (dict): Словарь с URL для различных моделей AI.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер стриминг ответов.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от AI-модели.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    stream: bool = False,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от AI-модели.

    Args:
        cls (AutonomousAI): Класс AutonomousAI.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        stream (bool, optional): Включает ли стриминг ответов. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от AI-модели.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    """
    ...
```

**Назначение**:
Создает асинхронный генератор для получения ответов от AI-модели, используя API AutonomousAI.

**Параметры**:
- `cls` (AutonomousAI): Класс AutonomousAI.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `stream` (bool, optional): Включает ли стриминг ответов. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от AI-модели.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при отправке запроса или обработке ответа.

**Как работает функция**:

1. **Определение endpoint**: Определяется URL API для запрошенной модели AI.
2. **Формирование заголовков**: Создаются заголовки HTTP-запроса, включая информацию о типе контента, стране, часовом поясе и User-Agent.
3. **Создание сессии aiohttp**: Создается асинхронная сессия `aiohttp` с заданными заголовками.
4. **Кодирование сообщений**: Список сообщений преобразуется в JSON-формат и кодируется в base64.
5. **Формирование данных запроса**: Создается словарь с данными для отправки, включая закодированное сообщение, ID потока, флаг стриминга и название AI-агента.
6. **Отправка POST-запроса**: Отправляется асинхронный POST-запрос к API endpoint с данными и прокси (если указан).
7. **Обработка ответа**:
   - Проверяется статус ответа с помощью `raise_for_status`.
   - Читаются чанки из ответа в асинхронном режиме.
   - Если чанк содержит `data: [DONE]`, он пропускается.
   - Извлекается JSON из чанка, удаляя префикс `data: `.
   - Извлекается содержимое (`content`) из поля `delta` в `choices`.
   - Если присутствует `finish_reason`, он также извлекается и возвращается.
   - В случае ошибки JSONDecodeError, чанк пропускается.

**Внутренние функции**: Нет.

**ASCII flowchart**:

```
A [Определение endpoint и заголовков]
|
B [Создание асинхронной сессии aiohttp]
|
C [Кодирование сообщений в base64]
|
D [Отправка POST-запроса к API]
|
E [Обработка стримингового ответа]
|
F [Извлечение и выдача контента или причины завершения]
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator

async def main():
    model = "llama"
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    proxy = None
    stream = True

    async def consume_generator(generator: AsyncGenerator[str, None]) -> None:
        async for message in generator:
            print(message, end="")

    generator = AutonomousAI.create_async_generator(
        model=model, messages=messages, proxy=proxy, stream=stream
    )
    if generator:
        await consume_generator(generator)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator с указанием proxy
import asyncio
from typing import List, Dict, AsyncGenerator

async def main():
    model = "llama"
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    proxy = "http://your_proxy:8080"  # Замените на ваш прокси
    stream = True

    async def consume_generator(generator: AsyncGenerator[str, None]) -> None:
        async for message in generator:
            print(message, end="")

    generator = AutonomousAI.create_async_generator(
        model=model, messages=messages, proxy=proxy, stream=stream
    )
    if generator:
        await consume_generator(generator)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator без стриминга
import asyncio
from typing import List, Dict, AsyncGenerator

async def main():
    model = "llama"
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    proxy = None
    stream = False

    async def consume_generator(generator: AsyncGenerator[str, None]) -> None:
        async for message in generator:
            print(message, end="")

    generator = AutonomousAI.create_async_generator(
        model=model, messages=messages, proxy=proxy, stream=stream
    )
    if generator:
        await consume_generator(generator)

if __name__ == "__main__":
    asyncio.run(main())