# Модуль `Wewordle.py`

## Обзор

Модуль предоставляет асинхронный класс `Wewordle`, предназначенный для взаимодействия с API `wewordle.org`. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предназначен для работы с моделью `gpt-3.5-turbo`.

## Подробнее

Этот модуль является частью набора провайдеров, используемых для доступа к различным языковым моделям. Он предоставляет асинхронный интерфейс для отправки запросов к API `wewordle.org` и получения ответов. Модуль генерирует случайные идентификаторы пользователя и приложения, формирует данные запроса в формате JSON и отправляет их на сервер.

## Классы

### `Wewordle`

**Описание**: Асинхронный провайдер для взаимодействия с API `wewordle.org`.

**Принцип работы**:
Класс использует библиотеку `aiohttp` для асинхронного выполнения HTTP-запросов. Он генерирует случайные идентификаторы пользователя и приложения, формирует JSON-данные запроса и отправляет их на сервер `wewordle.org`. Полученный ответ извлекается и возвращается.

**Атрибуты**:
- `url` (str): URL-адрес API `wewordle.org`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.

## Функции

### `create_async`

```python
@classmethod
async def create_async(
    cls,
    model: str,
    messages: list[dict[str, str]],
    proxy: str = None,
    **kwargs
) -> str:
    """
    Асинхронно создает запрос к API wewordle.org и возвращает ответ.

    Args:
        cls (Wewordle): Класс Wewordle.
        model (str): Имя модели для использования.
        messages (list[dict[str, str]]): Список сообщений для отправки в запросе.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Содержимое ответа от API.

    Raises:
        aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

    Внутренние функции:
        Нет

    Как работает функция:
    1. Устанавливает заголовки для HTTP-запроса.
    2. Генерирует случайные идентификаторы пользователя (_user_id) и приложения (_app_id).
    3. Формирует дату запроса (_request_date) в формате UTC.
    4. Создает структуру данных запроса, включая информацию о пользователе, сообщения и данные о подписке.
    5. Отправляет POST-запрос к API wewordle.org с использованием aiohttp.
    6. Извлекает содержимое ответа из JSON-формата и возвращает его.

    ASCII flowchart:

    Установка заголовков -> Генерация ID -> Формирование данных -> Отправка POST-запроса -> Извлечение ответа
    """
    ...
```

**Методы**:
- Нет

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования.
- `messages` (list[dict[str, str]]): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.

**Возвращает**:
- `str`: Содержимое ответа от API.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если HTTP-запрос завершается с ошибкой.

**Примеры**:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Wewordle import Wewordle

async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response = await Wewordle.create_async(model="gpt-3.5-turbo", messages=messages)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Wewordle import Wewordle

async def main():
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    response = await Wewordle.create_async(model="gpt-3.5-turbo", messages=messages, proxy="http://your_proxy:8080")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```