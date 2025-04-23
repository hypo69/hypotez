## \file hypotez/src/endpoints/gpt4free/g4f/Provider/Pi.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль, реализующий асинхронного провайдера Pi для взаимодействия с сервисом pi.ai.
=========================================================================================

Этот модуль содержит класс `Pi`, который предоставляет асинхронные методы для
генерации ответов от модели Pi.ai. Он поддерживает потоковую передачу ответов,
использует `StreamSession` для асинхронных HTTP-запросов и управляет cookies
и заголовками для поддержания сессии.

Зависимости:
    - requests
    - aiohttp

 .. module:: src.endpoints.gpt4free.g4f.Provider.Pi
"""

from __future__ import annotations

import json

from ..typing import AsyncResult, Messages, Cookies
from .base_provider import AsyncGeneratorProvider, format_prompt
from ..requests import StreamSession, get_args_from_nodriver, raise_for_status, merge_cookies


class Pi(AsyncGeneratorProvider):
    """
    Провайдер Pi для асинхронного взаимодействия с сервисом pi.ai.

    Этот класс предоставляет методы для начала разговора, отправки запросов и получения ответов
    от модели Pi.ai с использованием асинхронного генератора.
    """
    url = "https://pi.ai/talk"
    working = True
    use_nodriver = True
    supports_stream = True
    use_nodriver = True
    default_model = "pi"
    models = [default_model]
    _headers: dict = None
    _cookies: Cookies = {}

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        timeout: int = 180,
        conversation_id: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от модели Pi.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий на потоковую передачу данных.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `180`.
            conversation_id (str, optional): Идентификатор разговора. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий части ответа.

        Raises:
            Exception: Если не удается получить аргументы из nodriver.

        Example:
            >>> async for message in Pi.create_async_generator(model="pi", messages=[{"role": "user", "content": "Hello"}], stream=True):
            ...     print(message)
        """
        if cls._headers is None:
            args = await get_args_from_nodriver(cls.url, proxy=proxy, timeout=timeout)
            cls._cookies = args.get("cookies", {})
            cls._headers = args.get("headers")
        async with StreamSession(headers=cls._headers, cookies=cls._cookies, proxy=proxy) as session:
            if not conversation_id:
                conversation_id = await cls.start_conversation(session)
                prompt = format_prompt(messages)
            else:
                prompt = messages[-1]["content"]
            answer = cls.ask(session, prompt, conversation_id)
            async for line in answer:
                if "text" in line:
                    yield line["text"]

    @classmethod
    async def start_conversation(cls, session: StreamSession) -> str:
        """
        Начинает новый разговор с сервисом Pi.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.

        Returns:
            str: Идентификатор нового разговора.

        Raises:
            Exception: Если запрос завершается с ошибкой.

        Example:
            >>> session = StreamSession()
            >>> conversation_id = await Pi.start_conversation(session)
            >>> print(conversation_id)
            'xxxx-xxxx-xxxx-xxxx'
        """
        async with session.post('https://pi.ai/api/chat/start', data="{}", headers={
            'accept': 'application/json',
            'x-api-version': '3'
        }) as response:
            await raise_for_status(response)
            return (await response.json())['conversations'][0]['sid']

    async def get_chat_history(session: StreamSession, conversation_id: str):
        """
        Получает историю чата по идентификатору разговора.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            conversation_id (str): Идентификатор разговора.

        Returns:
            dict: История чата в формате JSON.

        Raises:
            Exception: Если запрос завершается с ошибкой.

        Example:
            >>> session = StreamSession()
            >>> history = await Pi.get_chat_history(session, "xxxx-xxxx-xxxx-xxxx")
            >>> print(history)
            {'messages': [...]}
        """
        params = {
            'conversation': conversation_id,
        }
        async with session.get('https://pi.ai/api/chat/history', params=params) as response:
            await raise_for_status(response)
            return await response.json()

    @classmethod
    async def ask(cls, session: StreamSession, prompt: str, conversation_id: str):
        """
        Отправляет запрос в чат и возвращает ответ.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текст запроса.
            conversation_id (str): Идентификатор разговора.

        Yields:
            str: Части ответа из потока данных.

        Raises:
            Exception: Если запрос завершается с ошибкой.

        Example:
            >>> session = StreamSession()
            >>> async for message in Pi.ask(session, "Hello", "xxxx-xxxx-xxxx-xxxx"):
            ...     print(message)
            'Hello, how can I help you?'
        """
        json_data = {
            'text': prompt,
            'conversation': conversation_id,
            'mode': 'BASE',
        }
        async with session.post('https://pi.ai/api/chat', json=json_data) as response:
            await raise_for_status(response)
            cls._cookies = merge_cookies(cls._cookies, response)
            async for line in response.iter_lines():
                if line.startswith(b'data: {"text":'):
                    yield json.loads(line.split(b'data: ')[1])
                elif line.startswith(b'data: {"title":'):
                    yield json.loads(line.split(b'data: ')[1])

#########################################################################################
# Как использовать этот блок кода
# =========================================================================================
#
# Описание
# -------------------------
# Этот код реализует асинхронного провайдера `Pi` для взаимодействия с сервисом pi.ai.
# Он включает методы для создания асинхронного генератора, начала разговора, получения истории чата
# и отправки запросов в чат.
#
# Шаги выполнения
# -------------------------
# 1. **Инициализация**: Создается экземпляр класса `Pi`.
# 2. **Получение аргументов**: При необходимости вызывается `get_args_from_nodriver` для
#    получения cookies и headers.
# 3. **Начало разговора**: Вызывается `start_conversation` для получения идентификатора разговора.
# 4. **Форматирование запроса**: Запрос форматируется с использованием `format_prompt`.
# 5. **Отправка запроса**: Запрос отправляется с использованием `StreamSession` и метода `ask`.
# 6. **Получение ответа**: Ответ получается в виде асинхронного генератора, который возвращает
#    части ответа.
#
# Пример использования
# -------------------------
#
# ```python
# import asyncio
#
# from g4f.Provider import Pi
#
# async def main():
#     messages = [{"role": "user", "content": "Hello"}]
#     async for message in Pi.create_async_generator(model="pi", messages=messages, stream=True):
#         print(message, end="")
#
# if __name__ == "__main__":
#     asyncio.run(main())
# ```