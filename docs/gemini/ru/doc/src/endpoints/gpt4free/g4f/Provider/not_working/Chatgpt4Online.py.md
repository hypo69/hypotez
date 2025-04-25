# Модуль Chatgpt4Online 

## Обзор 

Этот модуль предоставляет класс `Chatgpt4Online`, который реализует асинхронный генератор для взаимодействия с API-платформы Chatgpt4Online.org.

## Подробности

**Назначение**:
- Предоставление асинхронного генератора для получения ответов от ChatGPT4Online.org,  основанного на модели gpt-4.
- Содержит методы для формирования запросов к API, обработки ответов и управления сессиями.

**Пример использования**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Chatgpt4Online import Chatgpt4Online
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages = Messages(
        [
            {"role": "user", "content": "Привет! Как дела?"},
        ]
    )
    async for response in Chatgpt4Online.create_async_generator(model='gpt-4', messages=messages):
        print(f'Ответ: {response}')
```

## Классы

### `class Chatgpt4Online`

**Описание**:
- Класс `Chatgpt4Online` наследует от класса `AsyncGeneratorProvider` и обеспечивает асинхронную генерацию ответов от модели gpt-4, доступной на платформе Chatgpt4Online.org.

**Наследует**:
- `AsyncGeneratorProvider`

**Атрибуты**:
- `url`: URL-адрес основного сайта Chatgpt4Online.org
- `api_endpoint`: URL-адрес конечной точки API для отправки запросов к API.
- `working`: Текущий статус работы сервиса (True - работает, False - не работает).
- `default_model`:  Стандартная модель, которая используется по умолчанию (gpt-4).
- `models`: Список поддерживаемых моделей (включает только `default_model`).

**Методы**:

- `get_nonce(headers: dict) -> str`:
    - **Назначение**: Возвращает  nonce-токен, необходимый для авторизации в API Chatgpt4Online.org.
    - **Параметры**:
        - `headers (dict)`: Словарь заголовков HTTP-запроса.
    - **Возвращает**:
        - `str`: Номер nonce-токена.

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:
    - **Назначение**:  Создает асинхронный генератор для получения ответов от модели gpt-4 на заданные сообщения.
    - **Параметры**:
        - `model (str)`: Название модели, которую нужно использовать.
        - `messages (Messages)`: Список сообщений для модели gpt-4.
        - `proxy (str, optional)`: Прокси-сервер для отправки запросов, по умолчанию `None`.
    - **Возвращает**:
        - `AsyncResult`: Асинхронный генератор ответов от модели gpt-4.
    - **Как работает**:
        - Формирует HTTP-запрос с данными о модели, сообщениями и nonce-токеном.
        - Отправляет запрос на API Chatgpt4Online.org и обрабатывает ответ.
        - Асинхронно генерирует части ответов от модели gpt-4 по мере их поступления.
    - **Примеры**:
        ```python
        messages = Messages(
            [
                {"role": "user", "content": "Привет! Как дела?"},
            ]
        )
        async for response in Chatgpt4Online.create_async_generator(model='gpt-4', messages=messages):
            print(f'Ответ: {response}')
        ```

## Внутренние функции

- **`format_prompt(messages: Messages) -> str`**:
    - **Назначение**: Формирует строку запроса (prompt) для модели gpt-4, основываясь на списке сообщений.
    - **Параметры**:
        - `messages (Messages)`: Список сообщений.
    - **Возвращает**:
        - `str`: Строка запроса (prompt) для модели gpt-4.

## Примеры
- **Пример использования Chatgpt4Online**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Chatgpt4Online import Chatgpt4Online
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages = Messages(
        [
            {"role": "user", "content": "Привет! Как дела?"},
        ]
    )
    async for response in Chatgpt4Online.create_async_generator(model='gpt-4', messages=messages):
        print(f'Ответ: {response}')

asyncio.run(main())
```