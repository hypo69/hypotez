# Модуль Wewordle
## Обзор

Модуль `Wewordle` предназначен для асинхронного взаимодействия с сервисом `wewordle.org` для получения ответов от модели GPT-3.5 Turbo. Этот модуль является устаревшим (`deprecated`) и находится в пакете `g4f.Provider.deprecated`. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов.

## Подробней

Модуль предоставляет класс `Wewordle`, который наследуется от `AsyncProvider`. Он позволяет отправлять сообщения к API `wewordle.org` и получать ответы, используя прокси-сервер при необходимости.

## Классы

### `Wewordle`

**Описание**: Класс для взаимодействия с сервисом `wewordle.org`.

**Наследует**: `AsyncProvider`

**Атрибуты**:
- `url` (str): URL сервиса `wewordle.org`.
- `working` (bool): Указывает, работает ли провайдер (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo (по умолчанию `True`).

**Методы**:
- `create_async`: Асинхронный метод для создания запроса к API и получения ответа.

## Методы класса

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
    """Асинхронно отправляет сообщения к API wewordle.org и возвращает ответ.

    Args:
        cls: Класс, к которому принадлежит метод.
        model (str): Модель для использования (в данном случае всегда GPT-3.5 Turbo).
        messages (list[dict[str, str]]): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        str: Ответ от API в виде строки.

    Raises:
        aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

    Внутренние функции:
        Отсутствуют
    """
    ...
```

**Параметры**:
- `cls`: Класс, к которому принадлежит метод.
- `model` (str): Модель для использования (в данном случае всегда GPT-3.5 Turbo).
- `messages` (list[dict[str, str]]): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь, содержащий как минимум ключи "role" и "content".
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы (не используются).

**Как работает функция**:
1. Формирует заголовки HTTP-запроса, включая `accept`, `pragma`, `Content-Type` и `Connection`.
2. Генерирует случайные идентификаторы пользователя (`_user_id`) и приложения (`_app_id`).
3. Определяет текущую дату и время в формате UTC (`_request_date`).
4. Формирует структуру данных `data`, включающую информацию о пользователе, сообщениях и подписке.
5. Отправляет POST-запрос к API `wewordle.org` с использованием `aiohttp.ClientSession`.
6. Проверяет статус ответа и извлекает содержимое сообщения из JSON-ответа.
7. Возвращает содержимое сообщения, если оно присутствует.

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

# Пример использования класса Wewordle
async def main():
    messages = [{"role": "user", "content": "Hello, GPT!"}]
    proxy = None  # Замените на URL вашего прокси-сервера, если необходимо

    async with ClientSession() as session:
        response = await Wewordle.create_async(model="gpt-3.5-turbo", messages=messages, proxy=proxy)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Параметры класса

- `url` (str): URL сервиса `wewordle.org`.
- `working` (bool): Указывает, работает ли провайдер (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo (по умолчанию `True`).