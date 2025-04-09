# Модуль `AI365VIP`

## Обзор

Модуль `AI365VIP` предоставляет асинхронный генератор для взаимодействия с API AI365VIP, который позволяет использовать различные модели, такие как `gpt-3.5-turbo` и `gpt-4o`. Этот модуль предназначен для получения ответов от AI моделей через асинхронный стриминг.

## Подробней

Модуль определяет класс `AI365VIP`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP запросов. Модуль предоставляет возможность выбора модели, передачи сообщений и обработки ответов от AI моделей в режиме реального времени.

## Классы

### `AI365VIP`

**Описание**: Класс для взаимодействия с API AI365VIP. Позволяет отправлять запросы к AI моделям и получать ответы в асинхронном режиме.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора и управления моделями.

**Атрибуты**:
- `url` (str): Базовый URL для API AI365VIP (`"https://chat.ai365vip.com"`).
- `api_endpoint` (str): URL endpoint для отправки запросов (`"/api/chat"`).
- `working` (bool): Индикатор работоспособности провайдера (по умолчанию `False`).
- `default_model` (str): Модель, используемая по умолчанию (`'gpt-3.5-turbo'`).
- `models` (List[str]): Список поддерживаемых моделей (`['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4o']`).
- `model_aliases` (Dict[str, str]): Псевдонимы моделей (например, `{"gpt-3.5-turbo": "gpt-3.5-turbo-16k"}`).

**Методы**:
- `create_async_generator`: Асинхронный генератор для получения ответов от AI моделей.

## Функции

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
    Создает асинхронный генератор для получения ответов от AI моделей через API AI365VIP.

    Args:
        cls (AI365VIP): Ссылка на класс `AI365VIP`.
        model (str): Идентификатор модели, которую необходимо использовать.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Адрес прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, который выдает части ответа от AI модели.

    Raises:
        aiohttp.ClientResponseError: Если HTTP запрос завершается с ошибкой.

    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API AI365VIP и получения ответов от AI моделей.

**Параметры**:
- `cls` (AI365VIP): Ссылка на класс `AI365VIP`.
- `model` (str): Идентификатор модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Адрес прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает части ответа от AI модели.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если HTTP запрос завершается с ошибкой.

**Как работает функция**:

1. **Подготовка заголовков**: Функция начинает с подготовки HTTP заголовков, необходимых для запроса к API AI365VIP. В заголовках указывается тип контента, User-Agent, Referer и другие необходимые параметры.
2. **Создание асинхронной сессии**: Используется `aiohttp.ClientSession` для создания асинхронной сессии, которая позволяет отправлять HTTP запросы асинхронно.
3. **Формирование данных запроса**: Создается словарь `data`, который содержит информацию о модели, сообщениях и других параметрах, необходимых для запроса.
4. **Отправка POST запроса**: С использованием асинхронной сессии отправляется POST запрос к API endpoint (`cls.url + cls.api_endpoint`) с данными в формате JSON.
5. **Обработка ответа**: Функция итерируется по частям ответа, полученным от сервера, и декодирует их в формат UTF-8, после чего возвращает их через генератор.

```
A: Подготовка HTTP заголовков
│
B: Создание асинхронной сессии (ClientSession)
│
C: Формирование данных запроса (JSON)
│
D: Отправка POST запроса к API endpoint
│
E: Итерация по частям ответа и декодирование
│
F: Выдача частей ответа через генератор
```

**Примеры**:

Пример использования `create_async_generator`:

```python
import asyncio
from typing import AsyncGenerator, List, Dict, Any

from aiohttp import ClientSession

from ...typing import Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt


class AI365VIP(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://chat.ai365vip.com"
    api_endpoint = "/api/chat"
    working = False
    default_model = 'gpt-3.5-turbo'
    models = [
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-16k',
        'gpt-4o',
    ]
    model_aliases = {
        "gpt-3.5-turbo": "gpt-3.5-turbo-16k",
    }

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": cls.url,
            "referer": f"{cls.url}/en",
            "sec-ch-ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"127.0.6533.119"',
            "sec-ch-ua-full-version-list": '"Chromium";v="127.0.6533.119", "Not)A;Brand";v="99.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Linux"',
            "sec-ch-ua-platform-version": '"4.19.276"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
        async with ClientSession(headers=headers) as session:
            data = {
                "model": {
                    "id": model,
                    "name": "GPT-3.5",
                    "maxLength": 3000,
                    "tokenLimit": 2048
                },
                "messages": [{"role": "user", "content": format_prompt(messages)}],
                "key": "",
                "prompt": "You are a helpful assistant.",
                "temperature": 1
            }
            async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content:
                    if chunk:
                        yield chunk.decode()


async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    model = "gpt-3.5-turbo"

    async for message in AI365VIP.create_async_generator(model=model, messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())