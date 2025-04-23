# Документация для модуля `Pizzagpt.py`

## Обзор

Модуль `Pizzagpt.py` предоставляет асинхронный генератор для взаимодействия с API Pizzagpt. Он позволяет отправлять запросы к API и получать ответы в виде асинхронного генератора.

## Более детально

Модуль определяет класс `Pizzagpt`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов. Класс предоставляет метод `create_async_generator`, который отправляет запрос к API Pizzagpt и возвращает асинхронный генератор, выдающий содержимое ответа.

## Классы

### `Pizzagpt`

**Описание**: Класс для взаимодействия с API Pizzagpt.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает функциональность асинхронного генератора.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL-адрес Pizzagpt.
- `api_endpoint` (str): Конечная точка API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (List[str]): Список поддерживаемых моделей.

**Принцип работы**:
Класс `Pizzagpt` предназначен для асинхронного взаимодействия с API Pizzagpt. Он использует `aiohttp` для отправки HTTP-запросов и получения ответов. Метод `create_async_generator` форматирует запрос, отправляет его и возвращает асинхронный генератор, который выдает содержимое ответа.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API Pizzagpt.

## Методы класса

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
    Создает асинхронный генератор для получения ответов от API Pizzagpt.

    Args:
        cls (Pizzagpt): Класс Pizzagpt.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL-адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий содержимое ответа.

    Raises:
        ValueError: Если в ответе обнаружено сообщение об обнаружении злоупотреблений.
        Exception: Если возникает ошибка при выполнении HTTP-запроса.

    Как работает функция:
    - Формирует заголовки запроса, включая `origin`, `referer` и `user-agent`.
    - Создает асинхронную сессию с использованием `aiohttp.ClientSession`.
    - Форматирует сообщения с помощью функции `format_prompt`.
    - Создает словарь данных для отправки в теле запроса.
    - Отправляет POST-запрос к API Pizzagpt.
    - Обрабатывает ответ, проверяя наличие ошибок и извлекая содержимое.
    - Если содержимое присутствует, выдает его через генератор и завершает работу.
    """
```

## Параметры класса

- `model` (str): Определяет, какую модель использовать для генерации ответа.
- `messages` (Messages): Список сообщений, отправляемых в API для получения ответа.
- `proxy` (str, optional): Прокси-сервер для использования при отправке запроса. По умолчанию `None`.
- `kwargs`: Дополнительные параметры, которые могут быть переданы в API.

## Примеры

Пример использования `create_async_generator`:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Привет, как дела?"}]
    async for response in Pizzagpt.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())