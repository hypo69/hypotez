# Модуль для работы с H2o API
=================================================

Модуль содержит класс `H2o`, который используется для взаимодействия с H2o AI API для генерации текста.

## Обзор

Модуль `H2o` предоставляет асинхронный интерфейс для взаимодействия с API H2o AI. Он позволяет отправлять запросы на генерацию текста и получать результаты в виде асинхронного генератора. Этот модуль предназначен для интеграции в системы, требующие асинхронной обработки данных и взаимодействия с API H2o AI.

## Подробнее

Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов к API H2o AI. Он поддерживает настройку прокси-сервера и передачу дополнительных параметров в запросе.

## Классы

### `H2o`

**Описание**: Класс `H2o` предоставляет асинхронный интерфейс для взаимодействия с API H2o AI.

**Наследует**:
- `AsyncGeneratorProvider`: Класс наследует функциональность асинхронного генератора от `AsyncGeneratorProvider`.

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с H2o AI API.

    Args:
        model (str): Название модели, используемой для генерации текста.
        messages (Messages): Список сообщений, передаваемых в запросе.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры, передаваемые в запросе.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий сгенерированный текст.

    Raises:
        aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.

    Внутренние функции:
        Нет внутренних функций
    """
```

**Параметры**:

-   `cls`: Ссылка на класс.
-   `model` (`str`): Название модели, используемой для генерации текста.
-   `messages` (`Messages`): Список сообщений, передаваемых в запросе.
-   `proxy` (`str`, `Optional`): Адрес прокси-сервера. По умолчанию `None`.
-   `**kwargs`: Дополнительные параметры, передаваемые в запросе.

**Возвращает**:

-   `AsyncResult`: Асинхронный генератор, выдающий сгенерированный текст.

**Вызывает исключения**:

-   `aiohttp.ClientResponseError`: Если возникает ошибка при выполнении HTTP-запроса.

**Как работает функция**:

1.  **Инициализация**: Функция принимает параметры модели, сообщения, прокси и дополнительные аргументы.
2.  **Формирование заголовков**: Создаются заголовки, включающие Referer для запроса.
3.  **Создание сессии**: Используется `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
4.  **Настройка параметров**: Формируется словарь `data` с параметрами, необходимыми для запроса к API.
5.  **Отправка запроса на настройку**: Отправляется POST-запрос к `/settings` для установки параметров.
6.  **Отправка запроса на создание разговора**: Отправляется POST-запрос к `/conversation` для создания нового разговора. Полученный `conversationId` используется в последующих запросах.
7.  **Формирование данных для запроса**: Формируется словарь `data` с входными данными, параметрами генерации и опциями.
8.  **Отправка запроса на генерацию текста**: Отправляется POST-запрос к `/conversation/{conversationId}` для генерации текста.
9.  **Обработка потока данных**: Полученные данные обрабатываются построчно, извлекается текст из JSON-ответов и выдается через генератор.
10. **Удаление разговора**: После завершения генерации текста отправляется DELETE-запрос к `/conversation/{conversationId}` для удаления разговора.

**Примеры**:

```python
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from aiohttp import ClientSession

# Предположим, что Messages это List[Dict[str, str]]
Messages = List[Dict[str, str]]
AsyncResult = AsyncGenerator[str, None]

class H2o:
    url = "https://gpt-gm.h2o.ai"
    model = "h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1"

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        **kwargs
    ) -> AsyncResult:
        model = model if model else cls.model
        headers = {"Referer": f"{cls.url}/"}

        async with ClientSession(
            headers=headers
        ) as session:
            data = {
                "ethicsModalAccepted": "true",
                "shareConversationsWithModelAuthors": "true",
                "ethicsModalAcceptedAt": "",
                "activeModel": model,
                "searchEnabled": "true",
            }
            async with session.post(
                f"{cls.url}/settings",
                proxy=proxy,
                data=data
            ) as response:
                response.raise_for_status()

            async with session.post(
                f"{cls.url}/conversation",
                proxy=proxy,
                json={"model": model},
            ) as response:
                response.raise_for_status()
                conversationId = (await response.json())["conversationId"]

            data = {
                "inputs": format_prompt(messages),
                "parameters": {
                    "temperature": 0.4,
                    "truncate": 2048,
                    "max_new_tokens": 1024,
                    "do_sample":  True,
                    "repetition_penalty": 1.2,
                    "return_full_text": False,
                    **kwargs
                },
                "stream": True,
                "options": {
                    "id": str(uuid.uuid4()),
                    "response_id": str(uuid.uuid4()),
                    "is_retry": False,
                    "use_cache": False,
                    "web_search_id": "",
                },
            }
            async with session.post(
                f"{cls.url}/conversation/{conversationId}",
                proxy=proxy,
                json=data
             ) as response:
                start = "data:"
                async for line in response.content:
                    line = line.decode("utf-8")
                    if line and line.startswith(start):
                        line = json.loads(line[len(start):-1])
                        if not line["token"]["special"]:
                            yield line["token"]["text"]

            async with session.delete(
                f"{cls.url}/conversation/{conversationId}",
                proxy=proxy,
            ) as response:
                response.raise_for_status()

async def format_prompt(messages: Messages) -> str:
    """
    Форматирует список сообщений в строку для отправки в API.

    Args:
        messages (Messages): Список сообщений для форматирования.

    Returns:
        str: Отформатированная строка.
    """
    return "\\n".join([message["content"] for message in messages])


async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for token in H2o.create_async_generator(model="h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1", messages=messages):
        print(token, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

**ASCII Flowchart**:

```
Начало
│
ClientSession - Создание асинхронной сессии
│
POST /settings - Отправка запроса на настройку
│
POST /conversation - Создание нового conversationId
│
POST /conversation/{conversationId} - Отправка запроса на генерацию текста
│
Обработка потока данных (JSON) - Извлечение текста из ответов
│
DELETE /conversation/{conversationId} - Удаление разговора
│
Конец