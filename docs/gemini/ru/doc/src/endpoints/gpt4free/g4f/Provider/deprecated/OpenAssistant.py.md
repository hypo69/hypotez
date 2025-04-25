# Модуль OpenAssistant - deprecated

## Обзор

Модуль предоставляет класс `OpenAssistant`, который использовался для взаимодействия с моделью OpenAssistant.io, но в данный момент является устаревшим.

## Подробней

Класс `OpenAssistant` реализует асинхронный генератор для работы с моделью OpenAssistant.io. 
Он наследует базовый класс `AsyncGeneratorProvider` и предоставляет функции для отправки запросов, получения ответов и обработки 
результатов модели.
В данный момент, модуль является deprecated и не используется в проекте `hypotez`. 

## Классы

### `OpenAssistant`

**Описание**: Класс `OpenAssistant` реализует асинхронный генератор для работы с моделью OpenAssistant.io.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url` (str): Базовый URL для взаимодействия с OpenAssistant.io.
- `needs_auth` (bool): Флаг, указывающий, требуется ли авторизация для доступа к модели.
- `working` (bool): Флаг, указывающий, работает ли модель.
- `model` (str): Имя модели OpenAssistant.io.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: dict = None, **kwargs) -> AsyncResult`:
    - **Назначение**: Создает асинхронный генератор, который отправляет запросы к модели OpenAssistant.io, получает ответы и 
    -  обрабатывает результаты.
    - **Параметры**:
        - `model` (str): Имя модели OpenAssistant.io.
        - `messages` (Messages): Список сообщений, используемых для генерации ответа модели.
        - `proxy` (str, optional): Proxy-сервер для отправки запросов. По умолчанию `None`.
        - `cookies` (dict, optional): Словарь с cookies, используемыми для авторизации. По умолчанию `None`.
    - **Возвращает**:
        - `AsyncResult`: Асинхронный результат, который содержит ответы модели.
    - **Вызывает исключения**:
        - `RuntimeError`: Если произошла ошибка во время обработки запроса.
    - **Как работает**:
        - Внутри функции `create_async_generator` отправляется POST-запрос на сервер OpenAssistant.io для получения 
        - `chat_id` и `parent_id`.
        - Далее отправляется второй POST-запрос с данными, которые включают `chat_id`, `parent_id`, `model_config_name`, 
        - `sampling_parameters` и `plugins`. 
        - После получения ответа, генерируется `message_id` для отслеживания запроса.
        - Затем отправляется POST-запрос на `/api/chat/events` для получения ответов модели в реальном времени.
        - Ответы модели обрабатываются в виде токенов, которые отправляются в `yield line['text']` для последующей 
        - обработки.
        - В конце функции выполняется DELETE-запрос на `/api/chat` для удаления чата.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.OpenAssistant import OpenAssistant
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.helper import format_prompt

messages = Messages([
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя?"},
    {"role": "user", "content": "Тоже неплохо. Можешь рассказать мне анекдот?"}
])

async def main():
    model = "OA_SFT_Llama_30B_6"
    async for text in OpenAssistant.create_async_generator(model=model, messages=messages):
        print(text)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Внутренние функции

- `format_prompt(messages: Messages) -> str`:
    - **Назначение**: Форматирует список сообщений в строку для отправки в модель OpenAssistant.io.
    - **Параметры**:
        - `messages` (Messages): Список сообщений.
    - **Возвращает**:
        - `str`: Строка с отформатированными сообщениями.

- `get_cookies(domain: str) -> dict`:
    - **Назначение**: Получает cookies для авторизации в OpenAssistant.io.
    - **Параметры**:
        - `domain` (str): Домен для получения cookies.
    - **Возвращает**:
        - `dict`: Словарь с cookies.