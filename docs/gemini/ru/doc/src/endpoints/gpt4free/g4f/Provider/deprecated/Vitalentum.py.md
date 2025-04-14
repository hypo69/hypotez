# Модуль `Vitalentum.py`

## Обзор

Модуль `Vitalentum.py` предоставляет асинхронный генератор для взаимодействия с сервисом Vitalentum, который использует GPT-3.5 Turbo. Он позволяет отправлять сообщения и получать ответы в режиме реального времени.

## Подробней

Этот модуль предназначен для интеграции с API Vitalentum, предоставляя удобный интерфейс для обмена сообщениями с использованием асинхронных генераторов. Vitalentum.io — это сервис, предоставляющий доступ к различным моделям искусственного интеллекта, включая GPT-3.5 Turbo. Данный модуль позволяет отправлять запросы к этому сервису и получать ответы в асинхронном режиме, что особенно полезно для приложений, требующих неблокирующего ввода-вывода.

## Классы

### `Vitalentum`

**Описание**: Класс `Vitalentum` является асинхронным провайдером генератора.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

-   `url` (str): URL сервиса Vitalentum (`https://app.vitalentum.io`).
-   `supports_gpt_35_turbo` (bool): Поддержка модели GPT-3.5 Turbo (True).

**Методы**:

-   `create_async_generator`: Создаёт асинхронный генератор для взаимодействия с Vitalentum.

#### Как работает класс:

Класс `Vitalentum` наследует функциональность асинхронного провайдера генератора от `AsyncGeneratorProvider`. Он определяет URL сервиса Vitalentum и указывает на поддержку модели GPT-3.5 Turbo. Основная функциональность класса заключается в методе `create_async_generator`, который создает асинхронный генератор для отправки сообщений и получения ответов от API Vitalentum.

## Методы класса

### `create_async_generator`

```python
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """Создаёт асинхронный генератор для взаимодействия с Vitalentum.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от Vitalentum.

        Raises:
            Exception: Если возникает ошибка при отправке запроса или обработке ответа.
        """
```

**Назначение**: Создаёт асинхронный генератор для взаимодействия с API Vitalentum.

**Параметры**:

-   `model` (str): Модель, которую следует использовать.
-   `messages` (Messages): Список сообщений для отправки.
-   `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
-   `**kwargs`: Дополнительные аргументы.

**Возвращает**:

-   `AsyncResult`: Асинхронный генератор, возвращающий ответы от Vitalentum.

**Как работает функция**:

1.  Формирует заголовки HTTP-запроса, включая User-Agent, Accept, Origin и Referer.
2.  Преобразует список сообщений в формат JSON, ожидаемый API Vitalentum.
3.  Создает полезную нагрузку (payload) для запроса, включая преобразованные сообщения, температуру и дополнительные аргументы.
4.  Использует `aiohttp.ClientSession` для отправки асинхронного POST-запроса к API Vitalentum.
5.  Обрабатывает ответ, декодируя каждую строку и извлекая содержимое сообщения из JSON.
6.  Генерирует (yield) извлеченное содержимое.
7.  Завершает генерацию, если получает сообщение `data: [DONE]`.

**Примеры**:

```python
# Пример использования (необходимо установить aiohttp и настроить asyncio)
import asyncio
from typing import List, Dict

from aiohttp import ClientSession

# from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vitalentum import Vitalentum

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Привет!"},
        {"role": "bot", "content": "Здравствуйте! Чем могу помочь?"}
    ]
    async for message in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())