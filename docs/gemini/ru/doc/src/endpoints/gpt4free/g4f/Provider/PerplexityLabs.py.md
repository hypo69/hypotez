# Модуль PerplexityLabs 
## Обзор
Модуль `PerplexityLabs` предоставляет реализацию класса `PerplexityLabs`, который является асинхронным генератором ответов на вопросы, использующим API Perplexity Labs. 
Он позволяет взаимодействовать с различными моделями Perplexity Labs, такими как `r1-1776`, `sonar`, `sonar-reasoning`, `sonar-pro` и `sonar-reasoning-pro`, и получать ответы на вопросы в виде потока текста.
## Подробнее
Класс `PerplexityLabs` использует WebSockets для связи с API Perplexity Labs, отправляя запросы с вопросами и получая ответы в формате JSON.
## Классы
### `class PerplexityLabs`
**Описание**: Класс `PerplexityLabs` является асинхронным генератором ответов на вопросы, использующим API Perplexity Labs. 
**Наследует**:
    - `AsyncGeneratorProvider`: Предоставляет базовые функции для работы с асинхронными генераторами.
    - `ProviderModelMixin`: Предоставляет функции для работы с различными моделями.
**Атрибуты**:
    - `url`: URL-адрес API Perplexity Labs.
    - `working`: Флаг, указывающий, доступен ли API.
    - `default_model`: Название модели по умолчанию (`r1-1776`).
    - `models`: Список доступных моделей Perplexity Labs.
**Методы**:
    - `create_async_generator()`: Асинхронная функция, которая создает генератор ответов на вопросы.

#### `async def create_async_generator(cls, model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult:`
**Функция**: Создает асинхронный генератор ответов на вопросы, используя API Perplexity Labs.
**Параметры**:
    - `model`: Название используемой модели Perplexity Labs.
    - `messages`: Список сообщений (история диалога).
    - `proxy`: Прокси-сервер.
**Возвращает**:
    - `AsyncResult`: Асинхронный результат, содержащий генератор ответов.
**Как работает функция**:
    - Функция устанавливает соединение с API Perplexity Labs с помощью WebSockets.
    - Она отправляет запросы с вопросами и получает ответы в формате JSON.
    - Функция преобразует полученный JSON-ответ в строку текста и возвращает его через генератор.
    - Генератор выдает ответы частями по мере их получения.
    - Функция поддерживает источники данных для ответов (citations) и указывает причину окончания ответа (FinishReason).
**Примеры**:
```python
# Пример использования PerplexityLabs
from hypotez.src.endpoints.gpt4free.g4f.Provider import PerplexityLabs

# Инициализация PerplexityLabs
provider = PerplexityLabs()

# Создание асинхронного генератора ответов
async_generator = await provider.create_async_generator(
    model="r1-1776",
    messages=[
        {"role": "user", "content": "Привет, как дела?"}
    ]
)

# Получение ответа
async for response in async_generator:
    print(response)

```
```python
from __future__ import annotations

import random
import json

from ..typing import AsyncResult, Messages
from ..requests import StreamSession, raise_for_status
from ..errors import ResponseError
from ..providers.response import FinishReason, Sources
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin

API_URL = "https://www.perplexity.ai/socket.io/"
WS_URL = "wss://www.perplexity.ai/socket.io/"

class PerplexityLabs(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://labs.perplexity.ai"
    working = True

    default_model = "r1-1776"
    models = [
        default_model,
        "sonar-pro",
        "sonar",
        "sonar-reasoning",
        "sonar-reasoning-pro",
    ]

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        headers = {
            "Origin": cls.url,
            "Referer": f"{cls.url}/",
        }
        async with StreamSession(headers=headers, proxy=proxy, impersonate="chrome") as session:
            t = format(random.getrandbits(32), "08x")
            async with session.get(
                f"{API_URL}?EIO=4&transport=polling&t={t}"
            ) as response:
                await raise_for_status(response)
                text = await response.text()
            assert text.startswith("0")
            sid = json.loads(text[1:])["sid"]
            post_data = '40{"jwt":"anonymous-ask-user"}\''
            async with session.post(
                f"{API_URL}?EIO=4&transport=polling&t={t}&sid={sid}",
                data=post_data
            ) as response:
                await raise_for_status(response)
                assert await response.text() == "OK"
            async with session.get(
                f"{API_URL}?EIO=4&transport=polling&t={t}&sid={sid}",
                data=post_data
            ) as response:
                await raise_for_status(response)
                assert (await response.text()).startswith("40")
            async with session.ws_connect(f"{WS_URL}?EIO=4&transport=websocket&sid={sid}", autoping=False) as ws:
                await ws.send_str("2probe")
                assert(await ws.receive_str() == "3probe")
                await ws.send_str("5")
                assert(await ws.receive_str() == "6")
                message_data = {
                    "version": "2.18",
                    "source": "default",
                    "model": model,
                    "messages": [message for message in messages if isinstance(message["content"], str)],
                }
                await ws.send_str("42" + json.dumps(["perplexity_labs", message_data]))
                last_message = 0
                while True:
                    message = await ws.receive_str()
                    if message == "2":
                        if last_message == 0:
                            raise RuntimeError("Unknown error")
                        await ws.send_str("3")
                        continue
                    try:
                        if last_message == 0 and model == cls.default_model:
                            yield "<think>"
                        data = json.loads(message[2:])[1]
                        yield data["output"][last_message:]
                        last_message = len(data["output"])
                        if data["final"]:
                            if data["citations"]:
                                yield Sources(data["citations"])
                            yield FinishReason("stop")
                            break
                    except Exception as e:
                        raise ResponseError(f"Message: {message}") from e