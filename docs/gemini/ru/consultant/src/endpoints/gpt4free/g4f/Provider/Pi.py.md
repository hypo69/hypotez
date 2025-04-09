### **Анализ кода модуля `Pi.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/Pi.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование асинхронных операций для неблокирующего выполнения.
  - Класс `Pi` хорошо структурирован и следует принципам ООП.
  - Обработка ошибок с использованием `raise_for_status`.
  - Поддержка потоковой передачи данных.
  - Повторное использование сессий для повышения производительности.
- **Минусы**:
  - Отсутствует полная документация для всех методов и атрибутов класса.
  - Некоторые магические значения, такие как `'https://pi.ai/api/chat/start'`, лучше вынести в константы.
  - Не все переменные аннотированы типами.
  - Смешанный стиль кавычек (используются как одинарные, так и двойные кавычки).

#### **Рекомендации по улучшению**:

1. **Документация**:
   - Добавить docstring для класса `Pi` и его методов, включая описание параметров, возвращаемых значений и возможных исключений.
   - Описать назначение каждого атрибута класса, например, `url`, `working`, `_headers`, `_cookies`.

2. **Типизация**:
   - Указать типы для всех переменных, где это возможно.

3. **Константы**:
   - Вынести URL-адреса в константы для удобства изменения и поддержки.

4. **Логирование**:
   - Добавить логирование для отладки и мониторинга работы класса.

5. **Обработка ошибок**:
   - Улучшить обработку ошибок, добавив более конкретные исключения и логирование ошибок.

6. **Форматирование**:
   - Привести все строки к одному стилю кавычек (одинарные).

#### **Оптимизированный код**:

```python
from __future__ import annotations

import json
from typing import AsyncGenerator, Optional, Dict, Any

from ..typing import AsyncResult, Messages, Cookies
from .base_provider import AsyncGeneratorProvider, format_prompt
from ..requests import StreamSession, get_args_from_nodriver, raise_for_status, merge_cookies
from src.logger import logger  # Import logger module

"""
Модуль для взаимодействия с Pi.ai
=====================================

Модуль содержит класс :class:`Pi`, который используется для взаимодействия с Pi.ai API.
Он поддерживает асинхронное создание генераторов, начало разговоров, получение истории чата и отправку запросов.

Пример использования
----------------------

>>> pi = Pi()
>>> messages = [{"role": "user", "content": "Hello, Pi!"}]
>>> async for message in pi.create_async_generator(model="pi", messages=messages, stream=True):
...     print(message)
"""


class Pi(AsyncGeneratorProvider):
    """
    Провайдер для взаимодействия с Pi.ai.
    Поддерживает потоковую передачу сообщений.
    """
    url = "https://pi.ai/talk"
    working = True
    use_nodriver = True
    supports_stream = True
    default_model = "pi"
    models = [default_model]
    _headers: Optional[Dict[str, str]] = None  # HTTP headers
    _cookies: Cookies = {}
    API_CHAT_START_URL = 'https://pi.ai/api/chat/start'
    API_CHAT_HISTORY_URL = 'https://pi.ai/api/chat/history'
    API_CHAT_URL = 'https://pi.ai/api/chat'

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: Optional[str] = None,
        timeout: int = 180,
        conversation_id: Optional[str] = None,
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронно создает генератор для получения ответов от Pi.ai.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг потоковой передачи.
            proxy (Optional[str]): HTTP-прокси для использования.
            timeout (int): Время ожидания запроса.
            conversation_id (Optional[str]): Идентификатор разговора.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Части ответа от Pi.ai.

        Raises:
            Exception: В случае ошибки при получении аргументов от nodriver.
        """
        if cls._headers is None:
            try:
                args = await get_args_from_nodriver(cls.url, proxy=proxy, timeout=timeout)
                cls._cookies = args.get('cookies', {})
                cls._headers = args.get('headers')
            except Exception as ex:
                logger.error('Error while getting arguments from nodriver', ex, exc_info=True)
                raise
        async with StreamSession(headers=cls._headers, cookies=cls._cookies, proxy=proxy) as session:
            if not conversation_id:
                conversation_id = await cls.start_conversation(session)
            prompt = format_prompt(messages) if conversation_id else messages[-1]['content'] # fix: format_prompt вызывался, когда conversation_id был None
            answer = cls.ask(session, prompt, conversation_id)
            async for line in answer:
                if 'text' in line:
                    yield line['text']

    @classmethod
    async def start_conversation(cls, session: StreamSession) -> str:
        """
        Начинает новый разговор с Pi.ai.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.

        Returns:
            str: Идентификатор нового разговора.

        Raises:
            Exception: В случае ошибки при создании нового разговора.
        """
        try:
            async with session.post(cls.API_CHAT_START_URL, data='{}', headers={
                'accept': 'application/json',
                'x-api-version': '3'
            }) as response:
                await raise_for_status(response)
                return (await response.json())['conversations'][0]['sid']
        except Exception as ex:
            logger.error('Error starting conversation', ex, exc_info=True)
            raise

    async def get_chat_history(session: StreamSession, conversation_id: str) -> Any: # add Any
        """
        Получает историю чата с Pi.ai.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            conversation_id (str): Идентификатор разговора.

        Returns:
            Any: История чата в формате JSON.

        Raises:
            Exception: В случае ошибки при получении истории чата.
        """
        params = {
            'conversation': conversation_id,
        }
        try:
            async with session.get(self.API_CHAT_HISTORY_URL, params=params) as response:
                await raise_for_status(response)
                return await response.json()
        except Exception as ex:
            logger.error(f'Error getting chat history for conversation {conversation_id}', ex, exc_info=True)
            raise

    @classmethod
    async def ask(cls, session: StreamSession, prompt: str, conversation_id: str) -> AsyncGenerator[Dict[str, str], None]: # add type
        """
        Отправляет запрос в Pi.ai и возвращает ответ.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текст запроса.
            conversation_id (str): Идентификатор разговора.

        Yields:
            Dict[str, str]: Части ответа от Pi.ai.

        Raises:
            Exception: В случае ошибки при отправке запроса.
        """
        json_data = {
            'text': prompt,
            'conversation': conversation_id,
            'mode': 'BASE',
        }
        try:
            async with session.post(cls.API_CHAT_URL, json=json_data) as response:
                await raise_for_status(response)
                cls._cookies = merge_cookies(cls._cookies, response)
                async for line in response.iter_lines():
                    if line.startswith(b'data: {"text":'):
                        yield json.loads(line.split(b'data: ')[1])
                    elif line.startswith(b'data: {"title":'):
                        yield json.loads(line.split(b'data: ')[1])
        except Exception as ex:
            logger.error(f'Error during ask with prompt: {prompt} and conversation_id: {conversation_id}', ex, exc_info=True)
            raise