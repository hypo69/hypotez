## \file hypotez/src/endpoints/gpt4free/g4f/Provider/deprecated/Ails.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с провайдером Ails.
=====================================
Модуль предоставляет асинхронный генератор для взаимодействия с API Ails,
поддерживает историю сообщений и модель gpt-3.5-turbo.

 .. module:: src.endpoints.gpt4free.g4f.Provider.deprecated.Ails
"""

from __future__ import annotations

import hashlib
import time
import uuid
import json
from datetime import datetime
from aiohttp import ClientSession

from ...typing import SHA256, AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider


class Ails(AsyncGeneratorProvider):
    """
    Провайдер Ails для генерации текста.
    """
    url = "https://ai.ls"
    working = False
    supports_message_history = True
    supports_gpt_35_turbo = True

    @staticmethod
    async def create_async_generator(
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от API Ails.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг потоковой передачи данных.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий результаты от API.

        Raises:
            Exception: Если ответ содержит запрещенные слова ("ai.ls" или "ai.ci").

        Example:
            >>> model = "gpt-3.5-turbo"
            >>> messages = [{"role": "user", "content": "Hello"}]
            >>> stream = True
            >>> async for token in Ails.create_async_generator(model, messages, stream):
            ...     print(token, end="")
        """
        headers = {
            "authority": "api.caipacity.com",
            "accept": "*/*",
            "accept-language": "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "authorization": "Bearer free",
            "client-id": str(uuid.uuid4()),
            "client-v": "0.1.278",
            "content-type": "application/json",
            "origin": "https://ai.ls",
            "referer": "https://ai.ls/",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "from-url": "https://ai.ls/?chat=1"
        }
        async with ClientSession(
                headers=headers
            ) as session:
            timestamp = _format_timestamp(int(time.time() * 1000))
            json_data = {
                "model": "gpt-3.5-turbo",
                "temperature": kwargs.get("temperature", 0.6),
                "stream": True,
                "messages": messages,
                "d": datetime.now().strftime("%Y-%m-%d"),
                "t": timestamp,
                "s": _hash({"t": timestamp, "m": messages[-1]["content"]}),
            }
            async with session.post(
                        "https://api.caipacity.com/v1/chat/completions",
                        proxy=proxy,
                        json=json_data
                    ) as response:
                response.raise_for_status()
                start = "data: "
                async for line in response.content:
                    line = line.decode('utf-8')
                    if line.startswith(start) and line != "data: [DONE]":
                        line = line[len(start):-1]
                        line = json.loads(line)
                        token = line["choices"][0]["delta"].get("content")
                        
                        if token:
                            if "ai.ls" in token or "ai.ci" in token:
                                raise Exception(f"Response Error: {token}")
                            yield token


def _hash(json_data: dict[str, str]) -> SHA256:
    """
    Вычисляет SHA256 хеш на основе переданных данных.

    Args:
        json_data (dict[str, str]): Словарь с данными для хеширования, содержащий ключи "t" (timestamp) и "m" (message).

    Returns:
        SHA256: SHA256 хеш, вычисленный на основе конкатенации timestamp, message и секретной строки.
    """
    base_string: str = f'{json_data["t"]}:{json_data["m"]}:WI,2rU#_r:r~aF4aJ36[.Z(/8Rv93Rf:{len(json_data["m"])}'
    return SHA256(hashlib.sha256(base_string.encode()).hexdigest())


def _format_timestamp(timestamp: int) -> str:
    """
    Форматирует timestamp.

    Args:
        timestamp (int): Timestamp для форматирования.

    Returns:
        str: Отформатированная строка timestamp.
    """
    e = timestamp
    n = e % 10
    r = n + 1 if n % 2 == 0 else n
    return str(e - n + r)
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует асинхронного провайдера `Ails` для работы с API `ai.ls`. Он создает запросы к API для получения ответов на сообщения, используя модель `gpt-3.5-turbo`. Код включает в себя создание заголовков запроса, формирование данных JSON, отправку запроса и обработку потоковых ответов. Также реализованы функции для хеширования данных и форматирования временных меток.

Шаги выполнения
-------------------------
1. **Инициализация**: Класс `Ails` наследуется от `AsyncGeneratorProvider` и определяет URL, поддержку истории сообщений и модели `gpt-3.5-turbo`.
2. **Создание асинхронного генератора**: Функция `create_async_generator` создает асинхронный генератор для взаимодействия с API.
3. **Формирование заголовков**: Функция создает заголовки запроса, включая `authorization`, `client-id`, и `user-agent`.
4. **Создание сессии**: Создается асинхронная сессия `ClientSession` с заданными заголовками.
5. **Формирование данных JSON**: Создается JSON-данные для отправки в запросе, включая модель, температуру, сообщения, дату и хеш.
6. **Отправка запроса**: Отправляется POST-запрос к API с использованием асинхронной сессии и прокси-сервера, если он указан.
7. **Обработка ответа**: Код обрабатывает потоковый ответ от API, извлекая полезные данные из каждой строки и проверяя наличие запрещенных слов.
8. **Хеширование данных**: Функция `_hash` вычисляет SHA256 хеш на основе переданных данных.
9. **Форматирование временной метки**: Функция `_format_timestamp` форматирует временную метку.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Ails import Ails

async def main():
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Напиши небольшое стихотворение о космосе."}]
    stream = True

    try:
        async for token in Ails.create_async_generator(model, messages, stream):
            print(token, end="")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())