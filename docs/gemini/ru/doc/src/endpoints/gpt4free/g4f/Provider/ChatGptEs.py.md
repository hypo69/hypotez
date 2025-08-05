# Модуль `ChatGptEs`

## Обзор

Этот модуль предоставляет класс `ChatGptEs`, который позволяет использовать модель ChatGPT от `chatgpt.es` для генерации ответов на основе предоставленного текста. 

## Подробней

Модуль `ChatGptEs` использует библиотеку `curl_cffi` для отправки запросов к API `chatgpt.es`.  Класс `ChatGptEs` наследует от классов `AsyncGeneratorProvider` и `ProviderModelMixin`.

`ChatGptEs` обеспечивает асинхронную генерацию текста. Он поддерживает потоковую передачу данных, но не поддерживает системные сообщения и историю сообщений.

## Классы

### `class ChatGptEs`

**Описание**: Класс `ChatGptEs` реализует асинхронный генератор для получения текста от модели ChatGPT, работающей на платформе `chatgpt.es`.

**Наследует**:
- `AsyncGeneratorProvider`:  Предоставляет базовый функционал для асинхронной генерации текста.
- `ProviderModelMixin`: Предоставляет методы для работы с различными моделями ChatGPT.

**Атрибуты**:

- `url (str)`: Базовый URL платформы `chatgpt.es`.
- `api_endpoint (str)`: URL конечной точки API для отправки запросов.
- `working (bool)`:  Флаг, указывающий, доступен ли данный провайдер (в данном случае `chatgpt.es`).
- `supports_stream (bool)`: Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message (bool)`: Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history (bool)`: Указывает, поддерживает ли провайдер историю сообщений.
- `default_model (str)`:  Название модели по умолчанию для данного провайдера.
- `models (list)`:  Список доступных моделей ChatGPT для данного провайдера.
- `SYSTEM_PROMPT (str)`:  Системный запрос, который отправляется в API вместе с пользователемским текстом.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:  Асинхронный генератор для получения текста от модели ChatGPT на `chatgpt.es`.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ChatGptEs import ChatGptEs

async def main():
    provider = ChatGptEs()
    messages = [
        {"role": "user", "content": "Привет! Как дела?"},
        {"role": "assistant", "content": "Привет! У меня все хорошо, спасибо за вопрос. А у тебя как дела?"},
        {"role": "user", "content": "Хорошо, спасибо!"},
    ]
    async for response in provider.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```


#### `create_async_generator`

**Назначение**:  Асинхронный генератор для получения текста от модели ChatGPT на `chatgpt.es`.

**Параметры**:

- `model (str)`:  Название модели ChatGPT, которую нужно использовать.
- `messages (Messages)`:  Список сообщений, которые будут отправлены в API.
- `proxy (str, optional)`:  Прокси-сервер, который будет использоваться для отправки запросов. По умолчанию `None`.
- `**kwargs`:  Дополнительные аргументы, которые могут быть переданы в API.

**Возвращает**:

- `AsyncResult`:  Объект `AsyncResult`, который содержит результат асинхронного запроса к API.

**Как работает функция**:

1.  Проверяет, установлена ли библиотека `curl_cffi`.
2.  Определяет модель ChatGPT, используя метод `get_model()`.
3.  Форматирует текст сообщений для отправки в API, используя функцию `format_prompt()`.
4.  Создает сеанс `Session` с использованием `curl_cffi`.
5.  Задает заголовки запроса.
6.  Устанавливает прокси-сервер, если он был указан.
7.  Выполняет GET-запрос к `chatgpt.es` для получения `nonce` и `post_id`.
8.  Использует регулярные выражения для извлечения `nonce` и `post_id` из ответа сервера.
9.  Генерирует случайный `client_id`.
10.  Подготавливает данные для отправки в POST-запрос.
11.  Выполняет POST-запрос к API.
12.  Проверяет код ответа сервера.
13.  Если код ответа равен 200, преобразует ответ в JSON и возвращает генератор, который выдает текст от модели ChatGPT.
14.  Если код ответа отличается от 200, выдает ошибку.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ChatGptEs import ChatGptEs

messages = [
    {"role": "user", "content": "Привет! Как дела?"},
]

async def main():
    provider = ChatGptEs()
    async for response in provider.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```


## Параметры класса

- `model (str)`:  Название модели ChatGPT, которая будет использоваться. По умолчанию `gpt-4o`.
- `proxy (str)`:  Прокси-сервер, который будет использоваться для отправки запросов. По умолчанию `None`.


## Примеры

**Пример 1:  Получение текста от модели ChatGPT**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ChatGptEs import ChatGptEs

messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Привет! У меня все хорошо, спасибо за вопрос. А у тебя как дела?"},
    {"role": "user", "content": "Хорошо, спасибо!"},
]

async def main():
    provider = ChatGptEs()
    async for response in provider.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

**Пример 2: Использование прокси-сервера**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ChatGptEs import ChatGptEs

messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Привет! У меня все хорошо, спасибо за вопрос. А у тебя как дела?"},
    {"role": "user", "content": "Хорошо, спасибо!"},
]

proxy = "http://user:password@proxy.example.com:8080"

async def main():
    provider = ChatGptEs()
    async for response in provider.create_async_generator(model="gpt-4", messages=messages, proxy=proxy):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```