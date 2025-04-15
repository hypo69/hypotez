### **Анализ кода модуля `Pi.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/Pi.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация.
    - Использование `StreamSession` для эффективной обработки потоковых данных.
    - Четкое разделение на методы `start_conversation`, `ask`, `get_chat_history`.
- **Минусы**:
    - Отсутствует документация классов и методов.
    - Не все переменные аннотированы типами.
    - Не используется модуль логирования `logger`.

**Рекомендации по улучшению:**

1.  **Добавить документацию:**
    - Добавить docstring для класса `Pi` и всех его методов, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Описать назначение каждой функции и класса.
2.  **Аннотация типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
3.  **Использовать логирование**:
    - Добавить логирование с использованием модуля `logger` для отслеживания ошибок и важной информации.
4.  **Улучшить обработку ошибок**:
    - Добавить более детальную обработку ошибок с использованием `try-except` блоков и логированием ошибок.
5.  **Удалить дублирование кода**:
    -  `use_nodriver` повторяется дважды. Убрать дублирование
6.  **Использовать одинарные кавычки**:
    -  В `start_conversation` и `ask` методах использовать одинарные кавычки

**Оптимизированный код:**

```python
from __future__ import annotations

import json
from typing import AsyncGenerator, Optional, Dict

from ..typing import AsyncResult, Messages, Cookies
from .base_provider import AsyncGeneratorProvider, format_prompt
from ..requests import StreamSession, get_args_from_nodriver, raise_for_status, merge_cookies
from src.logger import logger  # Import the logger


"""
Модуль для взаимодействия с моделью Pi от g4f
=================================================

Этот модуль содержит класс `Pi`, который является асинхронным провайдером для взаимодействия с моделью Pi.
Он поддерживает потоковую передачу данных и использует `StreamSession` для эффективной обработки.

Пример использования:
----------------------

>>> pi_provider = Pi()
>>> messages = [{"role": "user", "content": "Hello, Pi!"}]
>>> async for message in pi_provider.create_async_generator(model="pi", messages=messages, stream=True):
...     print(message)
"""


class Pi(AsyncGeneratorProvider):
    """
    Провайдер для асинхронного взаимодействия с моделью Pi.
    """

    url: str = "https://pi.ai/talk"
    working: bool = True
    use_nodriver: bool = True
    supports_stream: bool = True
    default_model: str = "pi"
    models: list[str] = [default_model]
    _headers: Optional[Dict[str, str]] = None
    _cookies: Cookies = {}

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: Optional[str] = None,
        timeout: int = 180,
        conversation_id: Optional[str] = None,
        **kwargs,
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью Pi.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий на потоковую передачу данных.
            proxy (Optional[str]): Прокси-сервер для использования.
            timeout (int): Время ожидания ответа.
            conversation_id (Optional[str]): Идентификатор разговора.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

        Raises:
            Exception: В случае ошибки при получении аргументов или отправке запроса.

        """
        try:
            if cls._headers is None:
                args = await get_args_from_nodriver(cls.url, proxy=proxy, timeout=timeout)
                cls._cookies = args.get("cookies", {})
                cls._headers = args.get("headers")
            async with StreamSession(headers=cls._headers, cookies=cls._cookies, proxy=proxy) as session:
                if not conversation_id:
                    conversation_id = await cls.start_conversation(session)
                if messages and isinstance(messages, list) and messages[-1] and isinstance(messages[-1], dict):
                    prompt = format_prompt(messages)
                else:
                    prompt = messages[-1]["content"] if messages and isinstance(messages, list) and messages[-1] and isinstance(messages[-1], dict) and "content" in messages[-1] else ""
                answer = cls.ask(session, prompt, conversation_id)
                async for line in answer:
                    if "text" in line:
                        yield line["text"]
        except Exception as ex:
            logger.error("Error in create_async_generator", ex, exc_info=True)
            raise

    @classmethod
    async def start_conversation(cls, session: StreamSession) -> str:
        """
        Начинает новый разговор с моделью Pi.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.

        Returns:
            str: Идентификатор нового разговора.

        Raises:
            Exception: В случае ошибки при отправке запроса.
        """
        try:
            async with session.post('https://pi.ai/api/chat/start', data='{}', headers={
                'accept': 'application/json',
                'x-api-version': '3'
            }) as response:
                await raise_for_status(response)
                return (await response.json())['conversations'][0]['sid']
        except Exception as ex:
            logger.error("Error in start_conversation", ex, exc_info=True)
            raise

    async def get_chat_history(session: StreamSession, conversation_id: str):
        """
        Получает историю разговора с моделью Pi.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            conversation_id (str): Идентификатор разговора.

        Returns:
            dict: История разговора в формате JSON.

        Raises:
            Exception: В случае ошибки при отправке запроса.
        """
        try:
            params = {
                'conversation': conversation_id,
            }
            async with session.get('https://pi.ai/api/chat/history', params=params) as response:
                await raise_for_status(response)
                return await response.json()
        except Exception as ex:
            logger.error("Error in get_chat_history", ex, exc_info=True)
            raise

    @classmethod
    async def ask(cls, session: StreamSession, prompt: str, conversation_id: str) -> AsyncGenerator[dict, None]:
        """
        Отправляет запрос к модели Pi и возвращает ответ.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текст запроса.
            conversation_id (str): Идентификатор разговора.

        Yields:
            dict: Части ответа модели в формате JSON.

        Raises:
            Exception: В случае ошибки при отправке запроса.
        """
        try:
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
        except Exception as ex:
            logger.error("Error in ask", ex, exc_info=True)
            raise