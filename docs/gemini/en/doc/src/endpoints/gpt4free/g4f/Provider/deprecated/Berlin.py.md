# Module `Berlin.py`

## Обзор

Модуль `Berlin.py` предоставляет асинхронный генератор для взаимодействия с API Berlin, используемым для получения ответов от языковой модели GPT-3.5 Turbo. Он включает в себя аутентификацию, форматирование запросов и обработку ответов в режиме реального времени.

## Более подробно

Модуль предназначен для работы с API Berlin для получения ответов от языковой модели GPT-3.5 Turbo. Он выполняет аутентификацию, форматирует запросы и обрабатывает ответы в режиме реального времени. Класс `Berlin` является подклассом `AsyncGeneratorProvider` и реализует метод `create_async_generator`, который создает асинхронный генератор для получения ответов от API.

## Classes

### `Berlin`

**Описание**: Класс `Berlin` является асинхронным провайдером генератора, который взаимодействует с API Berlin для получения ответов от языковой модели GPT-3.5 Turbo.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров генераторов.

**Атрибуты**:
- `url` (str): URL-адрес API Berlin (`https://ai.berlin4h.top`).
- `working` (bool): Флаг, указывающий, работает ли провайдер (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель GPT-3.5 Turbo (по умолчанию `True`).
- `_token` (str | None): Токен аутентификации, используемый для доступа к API (изначально `None`).

**Принцип работы**:
Класс `Berlin` использует асинхронный генератор для взаимодействия с API Berlin. Он выполняет аутентификацию, форматирует запросы и обрабатывает ответы в режиме реального времени. Класс `Berlin` является подклассом `AsyncGeneratorProvider` и реализует метод `create_async_generator`, который создает асинхронный генератор для получения ответов от API.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API Berlin.

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
    """ Создает асинхронный генератор для получения ответов от API Berlin.
    Args:
        cls (Berlin): Ссылка на класс `Berlin`.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.

    Raises:
        RuntimeError: Если возникает ошибка при обработке ответа от API.

    """
    ...
```

**Параметры**:
- `cls` (Berlin): Ссылка на класс `Berlin`.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в API.

**Как работает функция**:
1. Функция `create_async_generator` является классовым методом, который создает асинхронный генератор для получения ответов от API Berlin.
2. Если модель не указана, используется `gpt-3.5-turbo`.
3. Формируются заголовки запроса, включающие `User-Agent`, `Accept`, `Accept-Language`, `Content-Type`, `Origin` и другие необходимые параметры.
4. Создается асинхронная сессия с использованием `aiohttp.ClientSession` и переданных заголовков.
5. Проверяется наличие токена аутентификации `cls._token`. Если токен отсутствует, выполняется запрос к API для его получения. Для этого отправляются данные учетной записи (`account` и `password`) на URL `/api/login`.
6. После успешной аутентификации токен сохраняется в `cls._token`.
7. Если токен уже существует, он используется для дальнейших запросов.
8. Формируется запрос к API Berlin с использованием метода `format_prompt` для форматирования сообщений.
9. Создается словарь `data`, содержащий параметры запроса, такие как `prompt`, `parentMessageId` (сгенерированный с помощью `uuid.uuid4()`) и `options`. В `options` включаются параметры модели, такие как `model`, `temperature`, `presence_penalty`, `frequency_penalty`, `max_tokens` и дополнительные аргументы `kwargs`.
10. Отправляется POST-запрос к API Berlin (`/api/chat/completions`) с использованием асинхронной сессии, данных запроса, прокси-сервера (если указан) и заголовков, включающих токен аутентификации.
11. Обрабатывается ответ от API в асинхронном режиме. Ответ разбивается на чанки, и каждый чанк преобразуется в JSON.
12. Извлекается содержимое (`content`) из каждого JSON-чанка и передается через генератор `yield`.
13. В случае ошибки при обработке ответа генерируется исключение `RuntimeError` с информацией об ошибке.

**Примеры**:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Berlin import Berlin
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [
        {"role": "user", "content": "Hello, Berlin!"}
    ]
    async for response in Berlin.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Berlin import Berlin
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [
        {"role": "user", "content": "Как дела?"}
    ]
    async for response in Berlin.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())