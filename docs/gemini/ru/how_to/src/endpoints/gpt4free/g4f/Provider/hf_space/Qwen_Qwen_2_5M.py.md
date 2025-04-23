## \file hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/Qwen_Qwen_2_5M.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с Qwen Qwen-2.5M через HF Space.
===========================================================
Этот модуль обеспечивает асинхронное взаимодействие с моделью Qwen Qwen-2.5M,
размещенной на HF Space. Он поддерживает потоковую передачу ответов, отправку системных сообщений
и предоставляет средства для управления историей разговоров.

 .. module:: src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5M
"""

from __future__ import annotations

import aiohttp
import json
import uuid

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt
from ...providers.response import JsonConversation, Reasoning
from ..helper import get_last_user_message
from ... import debug


class Qwen_Qwen_2_5M(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс для взаимодействия с моделью Qwen Qwen-2.5M через HF Space.

    Args:
        AsyncGeneratorProvider: Базовый класс для асинхронных провайдеров, генерирующих данные.
        ProviderModelMixin: Миксин для поддержки моделей провайдеров.
    """

    label: str = "Qwen Qwen-2.5M"
    """Текстовое имя провайдера."""
    url: str = "https://qwen-qwen2-5-1m-demo.hf.space"
    """URL HF Space, где размещена модель."""
    api_endpoint: str = f"{url}/run/predict?__theme=light"
    """URL API для отправки запросов."""

    working: bool = True
    """Указывает, работает ли провайдер в данный момент."""
    supports_stream: bool = True
    """Указывает, поддерживает ли провайдер потоковую передачу ответов."""
    supports_system_message: bool = True
    """Указывает, поддерживает ли провайдер отправку системных сообщений."""
    supports_message_history: bool = False
    """Указывает, поддерживает ли провайдер историю сообщений."""

    default_model: str = "qwen-2.5-1m-demo"
    """Модель по умолчанию."""
    model_aliases: dict[str, str] = {"qwen-2.5-1m": default_model}
    """Алиасы моделей."""
    models: list[str] = list(model_aliases.keys())
    """Список поддерживаемых моделей."""

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        return_conversation: bool = False,
        conversation: JsonConversation = None,
        **kwargs,
    ) -> AsyncResult:
        """
        Асинхронно генерирует ответы от модели Qwen Qwen-2.5M.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки в модель.
            proxy (str, optional): Прокси для использования при отправке запросов. По умолчанию `None`.
            return_conversation (bool, optional): Если `True`, возвращает объект `JsonConversation`. По умолчанию `False`.
            conversation (JsonConversation, optional): Объект `JsonConversation` для поддержания состояния разговора. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

        Raises:
            aiohttp.ClientError: Если возникает ошибка при отправке запроса.
            json.JSONDecodeError: Если не удается декодировать JSON из ответа.

        Example:
            >>> async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m-demo", messages=[{"role": "user", "content": "Hello"}]):
            ...     print(response)
        """

        def generate_session_hash() -> str:
            """
            Генерирует уникальный хеш сессии.

            Returns:
                str: Уникальный хеш сессии.
            """
            return str(uuid.uuid4()).replace('-', '')[:12]

        # Генерация уникального хеша сессии, если он не предоставлен
        session_hash: str = generate_session_hash() if conversation is None else getattr(conversation, "session_hash")

        # Если требуется возврат объекта разговора, функция генерирует объект JsonConversation с хешем сессии
        if return_conversation:
            yield JsonConversation(session_hash=session_hash)

        # Форматирование запроса, если это новый разговор, иначе извлекается последнее сообщение пользователя
        prompt: str = format_prompt(messages) if conversation is None else get_last_user_message(messages)

        headers: dict[str, str] = {
            'accept': '*/*',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'origin': cls.url,
            'referer': f'{cls.url}/?__theme=light',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }

        payload_predict: dict[str, list[list[dict | str] | list | None] | int | None | str] = {
            "data": [{"files": [], "text": prompt}, [], []],
            "event_data": None,
            "fn_index": 1,
            "trigger_id": 5,
            "session_hash": session_hash
        }

        async with aiohttp.ClientSession() as session:
            # Отправка запроса predict
            async with session.post(cls.api_endpoint, headers=headers, json=payload_predict) as response:
                data: list[str] = (await response.json())['data']

            join_url: str = f"{cls.url}/queue/join?__theme=light"
            join_data: dict[str, list[list[dict | str] | list | None] | int | None | str] = {"data": [[[{"id": None, "elem_id": None, "elem_classes": None, "name": None, "text": prompt, "flushing": None, "avatar": "", "files": []}, None]], None, 0], "event_data": None, "fn_index": 2, "trigger_id": 5, "session_hash": session_hash}

            async with session.post(join_url, headers=headers, json=join_data) as response:
                event_id: str = (await response.json())['event_id']

            # Подготовка запроса потока данных
            url_data: str = f'{cls.url}/queue/data?session_hash={session_hash}'

            headers_data: dict[str, str] = {
                'accept': 'text/event-stream',
                'referer': f'{cls.url}/?__theme=light',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
            }
            # Отправка запроса потока данных
            async with session.get(url_data, headers=headers_data) as response:
                yield_response: str = ""
                yield_response_len: int = 0
                async for line in response.content:
                    decoded_line: str = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        try:
                            json_data: dict = json.loads(decoded_line[6:])

                            # Поиск этапов генерации
                            if json_data.get('msg') == 'process_generating':
                                if 'output' in json_data and 'data' in json_data['output'] and json_data['output']['data'][0]:
                                    output_data: list = json_data['output']['data'][0][0]
                                    if len(output_data) > 2:
                                        text: str = output_data[2].split("\\n<summary>")[0]
                                        if text == "Qwen is thinking...":
                                            yield Reasoning(None, text)
                                        elif text.startswith(yield_response):
                                            yield text[yield_response_len:]
                                        else:
                                            yield text
                                        yield_response_len = len(text)
                                        yield_response = text

                            # Проверка завершения
                            if json_data.get('msg') == 'process_completed':
                                # Финальная проверка для получения полного ответа
                                if 'output' in json_data and 'data' in json_data['output']:
                                    output_data: str = json_data['output']['data'][0][0][1][0]["text"].split("\\n<summary>")[0]
                                    yield output_data[yield_response_len:]
                                    yield_response_len = len(text)
                                break

                        except json.JSONDecodeError:
                            debug.log("Could not parse JSON:", decoded_line)


"""
Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет класс `Qwen_Qwen_2_5M`, который позволяет взаимодействовать с моделью Qwen Qwen-2.5M через HF Space. Он поддерживает потоковую передачу ответов, отправку системных сообщений и предоставляет средства для управления историей разговоров.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `Qwen_Qwen_2_5M`.
2. **Вызов `create_async_generator`**: Вызовите асинхронный генератор `create_async_generator` для получения ответов от модели.
3. **Обработка ответов**: Используйте асинхронный цикл `async for` для обработки потоковых ответов от модели.
4. **Обработка ошибок**: Обрабатывайте исключения `aiohttp.ClientError` и `json.JSONDecodeError` для обеспечения надежности.

Пример использования
-------------------------

```python
    import asyncio
    from src.endpoints.gpt4free.g4f.Provider.hf_space import Qwen_Qwen_2_5M

    async def main():
        messages = [{"role": "user", "content": "Hello"}]
        async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m-demo", messages=messages):
            print(response)

    if __name__ == "__main__":
        asyncio.run(main())
```
"""