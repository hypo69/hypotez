# Модуль `Pizzagpt`

## Обзор

Модуль `Pizzagpt` предоставляет асинхронный генератор для взаимодействия с API `pizzagpt.it`. Он позволяет отправлять запросы к модели `gpt-4o-mini` через API `chatx-completion` и получать ответы в виде асинхронного генератора текста.

## Подробнее

Этот модуль интегрирован в проект `hypotez` для обеспечения возможности взаимодействия с определенной языковой моделью через API `pizzagpt.it`. Он использует `aiohttp` для асинхронных HTTP-запросов и предоставляет удобный интерфейс для отправки запросов и получения ответов в виде генератора. Модуль также обрабатывает возможные ошибки и возвращает результаты в формате, совместимом с другими компонентами проекта.

## Классы

### `Pizzagpt`

**Описание**: Класс `Pizzagpt` является асинхронным провайдером и миксином моделей. Он предоставляет функциональность для взаимодействия с API `pizzagpt.it`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL для `pizzagpt.it`.
- `api_endpoint` (str): Endpoint API для отправки запросов.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

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
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий текст ответа.

    Raises:
        ValueError: Если обнаружено сообщение о злоупотреблении (`Misuse detected`).

    Как работает функция:
    - Формирует заголовки запроса, включая `x-secret: "Marinara"`.
    - Использует `aiohttp.ClientSession` для отправки асинхронного POST-запроса к API.
    - Форматирует prompt из списка сообщений, используя `format_prompt`.
    - Отправляет запрос с использованием указанного прокси (если он предоставлен).
    - Обрабатывает ответ, извлекая содержимое из JSON.
    - Если в содержимом ответа обнаружено сообщение "Misuse detected", выбрасывает исключение `ValueError`.
    - Возвращает контент в виде асинхронного генератора.

    Внутренние функции:
        - Отсутствуют.

    Примеры:
        >>> async for message in Pizzagpt.create_async_generator(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello"}]):
        ...     print(message)
        Привет!
    """
    ...
```

## Параметры класса

- `url` (str): URL-адрес `https://www.pizzagpt.it`.
- `api_endpoint` (str): Путь `/api/chatx-completion` для доступа к API.
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `False`.
- `default_model` (str): Название модели по умолчанию (`gpt-4o-mini`).
- `models` (List[str]): Список доступных моделей, в данном случае только `gpt-4o-mini`.

## Примеры
```python
from aiohttp import ClientSession
import asyncio

from g4f.Provider.Pizzagpt import Pizzagpt
from g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Как дела?"}]
    async for message in Pizzagpt.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())