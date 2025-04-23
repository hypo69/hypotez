# Модуль AiChatOnline

## Обзор

Модуль `AiChatOnline` предназначен для асинхронного взаимодействия с сервисом AiChatOnline для генерации текста на основе предоставленных сообщений. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для получения уникального идентификатора пользователя и форматирования запроса. Модуль наследует базовые классы `AsyncGeneratorProvider` и `ProviderModelMixin` и предназначен для работы с API AiChatOnline.

## Подробнее

Модуль `AiChatOnline` является частью проекта `hypotez` и предназначен для интеграции с сервисом AiChatOnline, предоставляющим API для взаимодействия с моделями генерации текста. Он асинхронно отправляет запросы к API, используя `aiohttp`, и генерирует текст на основе предоставленных сообщений. Модуль также включает в себя методы для получения уникального идентификатора пользователя и форматирования запросов.

## Классы

### `AiChatOnline`

**Описание**: Класс `AiChatOnline` реализует асинхронное взаимодействие с сервисом AiChatOnline для генерации текста на основе предоставленных сообщений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `site_url` (str): URL сайта AiChatOnline.
- `url` (str): Базовый URL API AiChatOnline.
- `api_endpoint` (str): Endpoint API для отправки сообщений.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).

**Методы**:
- `grab_token`: Асинхронно получает уникальный идентификатор пользователя.
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API AiChatOnline.

## Методы класса

### `grab_token`

```python
    @classmethod
    async def grab_token(
        cls,
        session: ClientSession,
        proxy: str
    ) -> str:
        """
        Асинхронно получает уникальный идентификатор пользователя.

        Args:
            session (ClientSession): Асинхронная HTTP-сессия для выполнения запросов.
            proxy (str): URL прокси-сервера для использования при выполнении запросов.

        Returns:
            str: Уникальный идентификатор пользователя, полученный из API.

        Raises:
            aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

        
        - Отправляет GET-запрос к API для получения уникального идентификатора пользователя.
        - Извлекает и возвращает значение 'data' из JSON-ответа.
        """
```

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        token = await AiChatOnline.grab_token(session, 'http://proxy.example.com')
        print(token)

if __name__ == "__main__":
    asyncio.run(main())
```

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
        """
        Создает асинхронный генератор для получения ответов от API AiChatOnline.

        Args:
            model (str): Модель, используемая для генерации текста.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера для использования при выполнении запросов. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Yields:
            str: Части сгенерированного текста, полученные от API.

        Raises:
            aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

        
        - Формирует заголовки для HTTP-запроса, включая User-Agent, Referer и Content-Type.
        - Создает асинхронную HTTP-сессию с заданными заголовками.
        - Формирует данные запроса, включая conversationId и prompt (отформатированные сообщения).
        - Получает уникальный идентификатор пользователя с помощью метода `grab_token`.
        - Отправляет POST-запрос к API с заголовками и данными.
        - Получает чанки данных из ответа и извлекает сгенерированный текст из JSON-ответа.
        - Возвращает сгенерированный текст через yield.
        """
```

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for chunk in AiChatOnline.create_async_generator('gpt-4o-mini', messages, proxy='http://proxy.example.com'):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())