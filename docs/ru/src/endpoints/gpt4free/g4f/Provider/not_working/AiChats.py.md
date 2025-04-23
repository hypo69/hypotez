# Модуль AiChats

## Обзор

Модуль `AiChats` предоставляет асинхронный интерфейс для взаимодействия с сервисом ai-chats.org. Он поддерживает как текстовые запросы через модель `gpt-4`, так и запросы на генерацию изображений через модель `dalle`. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для работы с прокси.

## Подробнее

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется взаимодействие с AI-моделями для генерации текста или изображений. Он предоставляет удобный интерфейс для отправки запросов и обработки ответов от сервиса ai-chats.org.

## Классы

### `AiChats`

**Описание**: Класс `AiChats` предоставляет методы для асинхронного взаимодействия с сервисом ai-chats.org.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общую функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL сервиса ai-chats.org.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер в данный момент (по умолчанию `False`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (по умолчанию `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (List[str]): Список поддерживаемых моделей (`gpt-4`, `dalle`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от сервиса.
- `create_async`: Отправляет запрос и возвращает ответ в виде строки или изображения.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от сервиса ai-chats.org.

    Args:
        cls (AiChats): Ссылка на класс.
        model (str): Модель для использования (`gpt-4` или `dalle`).
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от сервиса.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    Как работает функция:
    - Функция принимает модель, список сообщений и прокси (опционально).
    - Формирует заголовки для HTTP-запроса.
    - В зависимости от модели (`gpt-4` или `dalle`) формирует запрос.
    - Отправляет POST-запрос к `cls.api_endpoint` с использованием `aiohttp.ClientSession`.
    - Для модели `dalle` обрабатывает JSON-ответ, извлекает URL изображения, загружает изображение и кодирует его в base64.
    - Для модели `gpt-4` обрабатывает текстовый ответ, извлекая сообщения из строк, начинающихся с `data: `.
    - В случае ошибки возвращает сообщение об ошибке.

    Внутренние функции:
        - Отсутствуют.
    """
```

### `create_async`

```python
    @classmethod
    async def create_async(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> str:
        """Отправляет запрос и возвращает ответ в виде строки или изображения.

        Args:
            cls (AiChats): Ссылка на класс.
            model (str): Модель для использования (`gpt-4` или `dalle`).
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Ответ от сервиса в виде строки или URL изображения.

        Как работает функция:
        - Функция принимает модель, список сообщений и прокси (опционально).
        - Вызывает `cls.create_async_generator` для получения асинхронного генератора ответов.
        - Перебирает ответы, возвращаемые генератором.
        - Если ответ является экземпляром `ImageResponse`, возвращает URL изображения.
        - В противном случае возвращает ответ в виде строки.

        Внутренние функции:
            - Отсутствуют.
        """
```

## Примеры

### Пример использования `create_async_generator`

```python
import asyncio
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Нарисуй котика"}]
    async for response in AiChats.create_async_generator(model='dalle', messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### Пример использования `create_async`

```python
import asyncio
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Привет, как дела?"}]
    response = await AiChats.create_async(model='gpt-4', messages=messages)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())