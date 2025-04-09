# Модуль `Chatgpt4Online.py`

## Обзор

Модуль `Chatgpt4Online.py` предназначен для асинхронного взаимодействия с API `chatgpt4online.org`. Он предоставляет класс `Chatgpt4Online`, который позволяет отправлять запросы к API и получать ответы в режиме реального времени. Модуль использует `aiohttp` для асинхронных HTTP-запросов и поддерживает работу через прокси. Этот модуль является частью проекта `hypotez` и служит для обеспечения функциональности взаимодействия с GPT-4 через указанный онлайн-сервис.

## Подробней

Модуль содержит класс `Chatgpt4Online`, который наследуется от `AsyncGeneratorProvider`. Он предназначен для работы с API `chatgpt4online.org`, который предоставляет доступ к модели `gpt-4`. Класс использует асинхронные запросы для взаимодействия с API и возвращает ответы в виде асинхронного генератора.

Модуль выполняет следующие основные задачи:

1.  Получение `nonce` (одноразового ключа) для авторизации запросов.
2.  Форматирование запроса в нужном формате.
3.  Отправка запроса к API с использованием `aiohttp`.
4.  Получение ответа от API в режиме реального времени и его обработка.
5.  Возврат результата в виде асинхронного генератора.

## Классы

### `Chatgpt4Online`

**Описание**: Класс для асинхронного взаимодействия с API `chatgpt4online.org`.

**Наследует**:

*   `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных генераторов провайдеров.

**Атрибуты**:

*   `url` (str): URL сервиса `chatgpt4online.org`.
*   `api_endpoint` (str): Конечная точка API для отправки сообщений.
*   `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).
*   `default_model` (str): Модель по умолчанию (`gpt-4`).
*   `models` (list[str]): Список поддерживаемых моделей, содержащий только `default_model`.

**Методы**:

*   `get_nonce(headers: dict) -> str`: Асинхронно получает `nonce` для авторизации запросов.
*   `create_async_generator(model: str, messages: Messages, proxy: str = None, \*\*kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API.

## Функции

### `get_nonce`

```python
async def get_nonce(headers: dict) -> str:
    """ Асинхронно получает nonce для авторизации запросов.

    Args:
        headers (dict): Словарь HTTP-заголовков для запроса.

    Returns:
        str: Значение nonce, полученное из ответа API.
    """
    ...
```

**Назначение**: Функция `get_nonce` асинхронно получает одноразовый ключ (nonce) для авторизации запросов к API `chatgpt4online.org`.

**Параметры**:

*   `headers` (dict): Словарь HTTP-заголовков, которые будут отправлены в запросе.

**Возвращает**:

*   `str`: Значение nonce, полученное из ответа API в формате JSON.

**Как работает функция**:

1.  Функция создает асинхронную сессию `ClientSession` с переданными заголовками.
2.  Выполняет POST-запрос к адресу `https://chatgpt4online.org/wp-json/mwai/v1/start_session`.
3.  Получает JSON-ответ и извлекает значение ключа `restNonce`, которое и возвращает.

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

async def main():
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }
    nonce = await Chatgpt4Online.get_nonce(headers)
    print(f"Nonce: {nonce}")

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
    """ Создает асинхронный генератор для взаимодействия с API.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.
    """
    ...
```

**Назначение**: Функция `create_async_generator` создает асинхронный генератор, который используется для взаимодействия с API `chatgpt4online.org`.

**Параметры**:

*   `cls`: Ссылка на класс `Chatgpt4Online`.
*   `model` (str): Модель, которую необходимо использовать для генерации ответа (в данном случае всегда `gpt-4`).
*   `messages` (Messages): Список сообщений, которые будут отправлены в API.
*   `proxy` (str, optional): URL прокси-сервера, если необходимо использовать прокси. По умолчанию `None`.
*   `**kwargs`: Дополнительные параметры, которые могут быть переданы в функцию.

**Возвращает**:

*   `AsyncResult`: Асинхронный генератор, который возвращает ответы от API.

**Как работает функция**:

1.  Формирует заголовки HTTP-запроса, включая `x-wp-nonce`, полученный с помощью `get_nonce`.
2.  Использует `format_prompt` для форматирования списка сообщений в строку.
3.  Создает тело запроса в формате JSON, содержащее `botId`, отформатированное сообщение `newMessage` и флаг `stream`.
4.  Отправляет асинхронный POST-запрос к API `chatgpt4online.org` с использованием `aiohttp`.
5.  Получает ответ от API в виде потока чанков данных.
6.  Извлекает JSON-объекты из каждого чанка, декодирует их и накапливает полные ответы.
7.  Возвращает полные ответы через асинхронный генератор.

**Примеры**:

```python
import asyncio
from typing import List

async def main():
    messages = [{"role": "user", "content": "Hello, GPT-4!"}]
    async for response in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())