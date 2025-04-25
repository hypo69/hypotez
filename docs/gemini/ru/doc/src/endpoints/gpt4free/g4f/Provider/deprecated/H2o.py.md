# Модуль H2o

## Обзор

Модуль предоставляет класс `H2o`, который реализует асинхронный генератор ответов от модели `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1` на платформе `gpt-gm.h2o.ai`.

## Подробней

Класс `H2o` наследует от `AsyncGeneratorProvider`, который, в свою очередь, предоставляет базовый функционал для работы с асинхронными генераторами ответов от различных моделей.

`H2o` реализует метод `create_async_generator`, который принимает в качестве входных данных модель, сообщения, прокси-сервер и дополнительные параметры. Метод выполняет следующие действия:

1.  **Установка заголовков**: Устанавливает заголовок `Referer` для запросов к `gpt-gm.h2o.ai`.
2.  **Настройка параметров**: Устанавливает базовые параметры для модели, такие как `temperature`, `truncate`, `max_new_tokens`, `do_sample`, `repetition_penalty`, `return_full_text` и добавляет дополнительные параметры, переданные в качестве аргументов.
3.  **Создание сессии**: Создает асинхронную сессию HTTP-клиента `ClientSession` с установленными заголовками.
4.  **Установка настроек**: Делает POST-запрос к `/settings` для установки настроек модели, таких как `ethicsModalAccepted`, `shareConversationsWithModelAuthors`, `ethicsModalAcceptedAt`, `activeModel` и `searchEnabled`.
5.  **Инициализация разговора**: Делает POST-запрос к `/conversation` для инициализации нового разговора с моделью.
6.  **Отправка запроса**: Делает POST-запрос к `/conversation/{conversationId}` с текстом запроса и установленным параметром `stream=True`.
7.  **Получение ответа**: Использует `async for` для обработки ответа по частям. 
    - Выполняет декодировку каждой части.
    - Проверяет, начинается ли строка с `data:`.
    - Если да, то парсит JSON-объект и проверяет, является ли токен `special`. 
    - Если токен не `special`, то добавляет текст токена к результату.
8.  **Удаление разговора**: Делает DELETE-запрос к `/conversation/{conversationId}` для удаления разговора с сервера.

## Классы

### `class H2o`

**Описание**:  Реализует асинхронный генератор ответов от модели `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1` на платформе `gpt-gm.h2o.ai`.

**Наследует**: `AsyncGeneratorProvider`.

**Атрибуты**:

-   `url`: URL-адрес платформы `gpt-gm.h2o.ai`.
-   `model`: Имя модели `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1`.

**Методы**:

-   `create_async_generator()`:  Создает асинхронный генератор ответов от модели `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1` на платформе `gpt-gm.h2o.ai`.

## Методы класса

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
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
```

**Назначение**: Создает асинхронный генератор ответов от модели `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1`.

**Параметры**:

-   `model` (`str`): Имя модели. По умолчанию `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1`.
-   `messages` (`Messages`): Список сообщений для отправки модели.
-   `proxy` (`str`, optional): Прокси-сервер. По умолчанию `None`.
-   `kwargs` (`dict`, optional): Дополнительные параметры для модели.

**Возвращает**: `AsyncResult` - объект с результатом. 

**Примеры**:
```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.H2o import H2o
from src.endpoints.gpt4free.g4f.typing import Messages
from src.utils.string import format_prompt

messages: Messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "<инструкция для модели gemini:Загрузка описаний продуктов в PrestaShop.>"}
]

async def main():
    async for token in await H2o.create_async_generator(model="h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1", messages=messages):
        print(token, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Как работает функция**:

- **Определение модели**: Определяет модель, которую нужно использовать, если она не задана пользователем. 
- **Формирование заголовков**: Формирует заголовки для запросов к серверу, устанавливая `Referer` для запросов.
- **Создание сессии**: Создает асинхронную сессию HTTP-клиента `ClientSession` с установленными заголовками.
- **Установка настроек**: Делает POST-запрос к `/settings` для установки настроек модели, таких как `ethicsModalAccepted`, `shareConversationsWithModelAuthors`, `ethicsModalAcceptedAt`, `activeModel` и `searchEnabled`.
- **Инициализация разговора**: Делает POST-запрос к `/conversation` для инициализации нового разговора с моделью.
- **Отправка запроса**: Делает POST-запрос к `/conversation/{conversationId}` с текстом запроса и установленным параметром `stream=True`.
- **Получение ответа**: Использует `async for` для обработки ответа по частям.
    - Выполняет декодировку каждой части.
    - Проверяет, начинается ли строка с `data:`.
    - Если да, то парсит JSON-объект и проверяет, является ли токен `special`.
    - Если токен не `special`, то добавляет текст токена к результату.
- **Удаление разговора**: Делает DELETE-запрос к `/conversation/{conversationId}` для удаления разговора с сервера.

## Параметры класса

-   `url` (`str`): URL-адрес платформы `gpt-gm.h2o.ai`. 
-   `model` (`str`): Имя модели `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1`.

## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.H2o import H2o
from src.endpoints.gpt4free.g4f.typing import Messages
from src.utils.string import format_prompt

messages: Messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "<инструкция для модели gemini:Загрузка описаний продуктов в PrestaShop.>"}
]

async def main():
    async for token in await H2o.create_async_generator(model="h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1", messages=messages):
        print(token, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Примеры вызова функции**

-   ```python
    async for token in await H2o.create_async_generator(messages=messages):
        print(token, end="")
    ```
-   ```python
    async for token in await H2o.create_async_generator(model='h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1', messages=messages):
        print(token, end="")
    ```
-   ```python
    async for token in await H2o.create_async_generator(model='h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1', messages=messages, proxy='http://proxy.server:8080'):
        print(token, end="")
    ```