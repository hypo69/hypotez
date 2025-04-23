### Как использовать блок кода NoowAi
=========================================================================================

Описание
-------------------------
Этот код реализует асинхронного провайдера `NoowAi` для взаимодействия с API `noowai.com`. Он отправляет сообщения и получает ответы в режиме реального времени, используя асинхронные генераторы для обработки потоковых данных.

Шаги выполнения
-------------------------
1. **Инициализация заголовков**:
   - Код задает заголовки HTTP-запроса, включая `User-Agent`, `Accept`, `Content-Type` и другие параметры, необходимые для взаимодействия с сервером `noowai.com`.

2. **Создание сессии**:
   - Используется `ClientSession` из библиотеки `aiohttp` для создания асинхронной сессии, в которой будут выполняться HTTP-запросы.

3. **Формирование данных**:
   - Создается словарь `data`, содержащий параметры запроса, такие как `botId`, `customId`, `chatId`, `messages` и `newMessage`. `chatId` генерируется случайным образом с помощью функции `get_random_string`.

4. **Отправка запроса**:
   - Асинхронно отправляется POST-запрос на URL `f"{cls.url}/wp-json/mwai-ui/v1/chats/submit"` с использованием `session.post`. Параметр `stream=True` указывает, что ожидается потоковый ответ.

5. **Обработка потока данных**:
   - Код асинхронно итерируется по строкам в ответе сервера (`response.content`).
   - Каждая строка проверяется на наличие префикса `b"data: "`.
   - Если строка начинается с этого префикса, она декодируется из JSON.
   - Проверяется наличие ключа `"type"` в декодированной строке.
   - В зависимости от значения `"type"` выполняются следующие действия:
     - Если `"type" == "live"`, извлекаются данные из `line["data"]` и передаются в генератор с помощью `yield`.
     - Если `"type" == "end"`, цикл завершается.
     - Если `"type" == "error"`, вызывается исключение `RuntimeError` с сообщением об ошибке.

Пример использования
-------------------------

```python
from __future__ import annotations

import json
from aiohttp import ClientSession

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider
from .helper import get_random_string

class NoowAi(AsyncGeneratorProvider):
    url = "https://noowai.com"
    supports_message_history = True
    supports_gpt_35_turbo = True
    working = False

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/",
            "Content-Type": "application/json",
            "Origin": cls.url,
            "Alt-Used": "noowai.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        async with ClientSession(headers=headers) as session:
            data = {
                "botId": "default",
                "customId": "d49bc3670c3d858458576d75c8ea0f5d",
                "session": "N/A",
                "chatId": get_random_string(),
                "contextId": 25,
                "messages": messages,
                "newMessage": messages[-1]["content"],
                "stream": True
            }
            async with session.post(f"{cls.url}/wp-json/mwai-ui/v1/chats/submit", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for line in response.content:
                    if line.startswith(b"data: "):
                        try:
                            line = json.loads(line[6:])
                            assert "type" in line
                        except:
                            raise RuntimeError(f"Broken line: {line.decode()}")
                        if line["type"] == "live":
                            yield line["data"]
                        elif line["type"] == "end":
                            break
                        elif line["type"] == "error":
                            raise RuntimeError(line["data"])