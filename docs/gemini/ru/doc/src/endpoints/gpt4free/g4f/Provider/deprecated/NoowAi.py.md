# Модуль NoowAi
## Обзор

Модуль `NoowAi` - это класс, предоставляющий асинхронный генератор для работы с API NoowAi. Он реализует интерфейс `AsyncGeneratorProvider` и обеспечивает асинхронную генерацию ответов от модели NoowAi.

## Подробности

Модуль использует библиотеку `aiohttp` для асинхронного взаимодействия с API NoowAi. Он отправляет запросы с использованием метода `POST` на URL `/wp-json/mwai-ui/v1/chats/submit`. В запросе передаются:

- `botId`: Идентификатор бота.
- `customId`: Идентификатор пользователя.
- `session`: Идентификатор сессии.
- `chatId`: Случайно сгенерированный идентификатор чата.
- `contextId`: Идентификатор контекста.
- `messages`: Список сообщений, включая текущее сообщение.
- `newMessage`: Текст последнего сообщения.
- `stream`: Флаг, указывающий на то, что требуется потоковая передача ответов.

API NoowAi возвращает ответы в виде потока данных, который парсится модулем. Ответы с типом `live` содержат части ответа от модели NoowAi. Ответы с типом `end` сигнализируют о завершении генерации ответа. Ответы с типом `error` указывают на ошибку во время генерации ответа.

## Классы

### `class NoowAi`

**Описание**: Класс, предоставляющий асинхронный генератор для работы с API NoowAi.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url (str)`: URL API NoowAi.
- `supports_message_history (bool)`: Флаг, указывающий на то, поддерживает ли API NoowAi историю сообщений.
- `supports_gpt_35_turbo (bool)`: Флаг, указывающий на то, поддерживает ли API NoowAi модель GPT-3.5 Turbo.
- `working (bool)`: Флаг, указывающий на то, работает ли API NoowAi.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для работы с API NoowAi.

**Параметры**:

- `model (str)`: Название модели NoowAi.
- `messages (Messages)`: Список сообщений.
- `proxy (str, optional)`: Прокси-сервер для использования с запросами. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для запросов к API.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который генерирует ответы от модели NoowAi.

**Вызывает исключения**:

- `RuntimeError`: Возникает в случае, если API NoowAi возвращает ошибку.


## Функции

### `create_async_generator`

**Назначение**: Создает асинхронный генератор для работы с API NoowAi.

**Параметры**:

- `model (str)`: Название модели NoowAi.
- `messages (Messages)`: Список сообщений.
- `proxy (str, optional)`: Прокси-сервер для использования с запросами. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для запросов к API.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который генерирует ответы от модели NoowAi.

**Вызывает исключения**:

- `RuntimeError`: Возникает в случае, если API NoowAi возвращает ошибку.

**Как работает функция**:

- Функция создает асинхронную сессию `ClientSession` с заданными заголовками HTTP.
- Она отправляет POST-запрос на URL API NoowAi с данными, содержащими информацию о боте, сессии, чате, сообщениях и флагами, указывающими на потоковую передачу ответа.
- После получения ответа от API, функция генерирует ответы с типом `live`, если они доступны.
- Если получен ответ с типом `end`, функция завершает генерацию.
- Если получен ответ с типом `error`, функция вызывает исключение `RuntimeError`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.NoowAi import NoowAi
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет!"}
]

async def main():
    async for response in NoowAi.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
```markdown