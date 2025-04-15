# Модуль для работы с провайдером ChatAnywhere (Устаревший)

## Обзор

Модуль `ChatAnywhere.py` предназначен для асинхронного взаимодействия с сервисом ChatAnywhere.cn. Он предоставляет функциональность для генерации текста на основе предоставленных сообщений, используя асинхронные генераторы. Модуль поддерживает модель `gpt-3.5-turbo` и хранит историю сообщений.
Модуль помечен как устаревший и может быть удален в будущих версиях.

## Подробнее

Модуль определяет класс `ChatAnywhere`, который наследуется от `AsyncGeneratorProvider`. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов к API ChatAnywhere.
В данном коде не используется модуль `logger` для логгирования, что может быть улучшено для отслеживания ошибок и предупреждений.
Также в коде не обрабатываются возможные исключения, что может привести к неожиданному завершению программы.

## Классы

### `ChatAnywhere`

**Описание**: Класс `ChatAnywhere` предоставляет реализацию для взаимодействия с сервисом ChatAnywhere.cn. Он позволяет отправлять запросы на генерацию текста и получать ответы в виде асинхронного генератора.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес сервиса ChatAnywhere.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `working` (bool): Указывает, работает ли провайдер в данный момент.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от сервиса ChatAnywhere.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    temperature: float = 0.5,
    **kwargs
) -> AsyncResult:
    """ Создает асинхронный генератор для получения ответов от сервиса ChatAnywhere.

    Args:
        cls (ChatAnywhere): Ссылка на класс.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию 120.
        temperature (float, optional): Температура генерации текста. По умолчанию 0.5.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки текста.

    Raises:
        aiohttp.ClientResponseError: Если HTTP-ответ содержит ошибку.

    Как работает функция:
    1. Формирует заголовки запроса, включая User-Agent, Accept и Content-Type.
    2. Создает асинхронную сессию с использованием `aiohttp.ClientSession`.
    3. Формирует данные запроса, включая список сообщений, идентификатор, заголовок, промпт, температуру и модель.
    4. Отправляет POST-запрос к API ChatAnywhere (`/v1/chat/gpt/`).
    5. Итерируется по чанкам в ответе и декодирует их.
    6. Возвращает чанки текста через асинхронный генератор.
    """
    ...
```

## Параметры метода `create_async_generator`

- `cls`: Ссылка на класс `ChatAnywhere`.
- `model` (str): Используемая модель.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания ответа в секундах. По умолчанию 120.
- `temperature` (float, optional): Температура генерации текста. По умолчанию 0.5.
- `**kwargs`: Дополнительные аргументы.

## Примеры

Пример использования метода `create_async_generator`:

```python
import asyncio
from typing import AsyncGenerator, List, Dict, Any, Optional

from aiohttp import ClientSession, ClientTimeout


class ChatAnywhere(AsyncGeneratorProvider):
    url = "https://chatanywhere.cn"
    supports_gpt_35_turbo = True
    supports_message_history = True
    working = False

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: List[Dict[str, str]],
        proxy: str = None,
        timeout: int = 120,
        temperature: float = 0.5,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Referer": f"{cls.url}/",
            "Origin": cls.url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Authorization": "",
            "Connection": "keep-alive",
            "TE": "trailers"
        }
        async with ClientSession(headers=headers, timeout=ClientTimeout(timeout)) as session:
            data = {
                "list": messages,
                "id": "s1_qYuOLXjI3rEpc7WHfQ",
                "title": messages[-1]["content"],
                "prompt": "",
                "temperature": temperature,
                "models": "61490748",
                "continuous": True
            }
            async with session.post(f"{cls.url}/v1/chat/gpt/", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content.iter_any():
                    if chunk:
                        yield chunk.decode()

async def main():
    messages = [{"role": "user", "content": "Hello, ChatAnywhere!"}]
    generator = ChatAnywhere.create_async_generator(model="gpt-3.5-turbo", messages=messages)
    async for chunk in await generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())