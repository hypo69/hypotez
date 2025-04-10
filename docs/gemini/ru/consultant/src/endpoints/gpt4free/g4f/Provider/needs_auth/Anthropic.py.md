### **Анализ кода модуля `Anthropic.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и разбит на методы, что облегчает чтение и понимание.
    - Присутствуют аннотации типов, что улучшает читаемость и упрощает отладку.
    - Обработка ошибок выполняется с использованием `try-except` блоков и логируется через `logger.error`.
    - Использование `async` и `await` для асинхронных операций.
- **Минусы**:
    - Не все методы и классы имеют подробные docstring, описывающие их назначение и параметры.
    - Отсутствуют примеры использования в docstring.
    - Есть смешение стилей в использовании кавычек (иногда используются двойные кавычки вместо одинарных).
    - Некоторые участки кода требуют более детальных комментариев для пояснения логики.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить подробные docstring ко всем классам и методам, включая описание параметров, возвращаемых значений и возможных исключений.
    - Включить примеры использования в docstring, чтобы упростить понимание и использование кода.

2.  **Унифицировать кавычки**:
    - Заменить все двойные кавычки на одинарные для соответствия стандартам кодирования.

3.  **Улучшить комментарии**:
    - Добавить больше комментариев для пояснения сложных участков кода и логических операций.
    - Сделать комментарии более информативными, избегая общих фраз вроде "получаем" или "делаем".

4.  **Логирование**:
    - Убедиться, что все исключения логируются с использованием `logger.error` и передачей `exc_info=True` для получения полной трассировки.

5.  **Обработка ошибок**:
    - Проверить все места, где вызывается `raise_for_status`, и убедиться, что ошибки обрабатываются корректно.

6. **Использовать `j_loads` или `j_loads_ns`**:
    - заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

7. **Аннотации**
    - Для всех переменных должны быть определены аннотации типа.
    - Для всех функций все входные и выходные параметры аннотириваны

**Оптимизированный код:**

```python
from __future__ import annotations

import requests
import json
import base64
from typing import Optional, List, Dict, AsyncGenerator, Tuple, Any
from pathlib import Path

from src.logger import logger # Import logger
from ..helper import filter_none
from ...typing import AsyncResult, Messages, MediaListType
from ...requests import StreamSession, raise_for_status
from ...providers.response import FinishReason, ToolCalls, Usage
from ...errors import MissingAuthError
from ...image import to_bytes, is_accepted_format
from .OpenaiAPI import OpenaiAPI


class Anthropic(OpenaiAPI):
    """
    Модуль для взаимодействия с Anthropic API.
    ===========================================
    Этот класс предоставляет методы для отправки запросов к API Anthropic,
    включая поддержку стриминга, мультимодальных сообщений и инструментов.
    """

    label: str = 'Anthropic API'
    url: str = 'https://console.anthropic.com'
    login_url: str = 'https://console.anthropic.com/settings/keys'
    working: bool = True
    api_base: str = 'https://api.anthropic.com/v1'
    needs_auth: bool = True
    supports_stream: bool = True
    supports_system_message: bool = True
    supports_message_history: bool = True
    default_model: str = 'claude-3-5-sonnet-latest'
    models: List[str] = [
        default_model,
        'claude-3-5-sonnet-20241022',
        'claude-3-5-haiku-latest',
        'claude-3-5-haiku-20241022',
        'claude-3-opus-latest',
        'claude-3-opus-20240229',
        'claude-3-sonnet-20240229',
        'claude-3-haiku-20240307'
    ]
    models_aliases: Dict[str, str] = {
        'claude-3.5-sonnet': default_model,
        'claude-3-opus': 'claude-3-opus-latest',
        'claude-3-sonnet': 'claude-3-sonnet-20240229',
        'claude-3-haiku': 'claude-3-haiku-20240307',
    }

    @classmethod
    def get_models(cls, api_key: str = None, **kwargs) -> List[str]:
        """
        Получает список доступных моделей из Anthropic API.

        Args:
            api_key (str, optional): API ключ для аутентификации. Defaults to None.

        Returns:
            List[str]: Список идентификаторов моделей.
        """
        if not cls.models:
            url: str = f'https://api.anthropic.com/v1/models'
            headers: Dict[str, str] = {
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
            try:
                response = requests.get(url, headers=headers)
                raise_for_status(response)
                models_data = response.json()
                cls.models = [model['id'] for model in models_data['data']]
            except requests.exceptions.RequestException as ex:
                logger.error('Ошибка при получении списка моделей', ex, exc_info=True)
                return []  # В случае ошибки возвращаем пустой список
        return cls.models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        media: MediaListType = None,
        api_key: str = None,
        temperature: float = None,
        max_tokens: int = 4096,
        top_k: int = None,
        top_p: float = None,
        stop: list[str] = None,
        stream: bool = False,
        headers: dict = None,
        impersonate: str = None,
        tools: Optional[list] = None,
        extra_data: dict = {},
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронно создает генератор для взаимодействия с Anthropic API.

        Args:
            model (str): Идентификатор модели.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. Defaults to None.
            timeout (int, optional): Максимальное время ожидания запроса. Defaults to 120.
            media (MediaListType, optional): Список медиа-файлов для отправки. Defaults to None.
            api_key (str, optional): API ключ для аутентификации. Defaults to None.
            temperature (float, optional): Температура для генерации текста. Defaults to None.
            max_tokens (int, optional): Максимальное количество токенов в ответе. Defaults to 4096.
            top_k (int, optional): Параметр top_k для генерации текста. Defaults to None.
            top_p (float, optional): Параметр top_p для генерации текста. Defaults to None.
            stop (list[str], optional): Список стоп-слов для остановки генерации. Defaults to None.
            stream (bool, optional): Флаг для включения стриминга. Defaults to False.
            headers (dict, optional): Дополнительные заголовки для запроса. Defaults to None.
            impersonate (str, optional): User agent для имитации. Defaults to None.
            tools (Optional[list], optional): Список инструментов для использования. Defaults to None.
            extra_data (dict, optional): Дополнительные данные для запроса. Defaults to {}.

        Yields:
            AsyncGenerator[str | FinishReason | Usage | ToolCalls, None]: Генератор, возвращающий части ответа от API.

        Raises:
            MissingAuthError: Если не предоставлен API ключ.
        """
        if api_key is None:
            raise MissingAuthError('Add a "api_key"')

        if media is not None:
            insert_images: List[Dict[str, Any]] = []
            for image, _ in media:
                data: bytes = to_bytes(image)
                insert_images.append({
                    'type': 'image',
                    'source': {
                        'type': 'base64',
                        'media_type': is_accepted_format(data),
                        'data': base64.b64encode(data).decode(),
                    }
                })
            messages[-1]['content'] = [
                *insert_images,
                {
                    'type': 'text',
                    'text': messages[-1]['content']
                }
            ]
        system: Optional[str] = '\n'.join([message['content'] for message in messages if message.get('role') == 'system'])
        if system:
            messages = [message for message in messages if message.get('role') != 'system']
        else:
            system = None

        async with StreamSession(
            proxy=proxy,
            headers=cls.get_headers(stream, api_key, headers),
            timeout=timeout,
            impersonate=impersonate,
        ) as session:
            data: Dict[str, Any] = filter_none(
                messages=messages,
                model=cls.get_model(model, api_key=api_key),
                temperature=temperature,
                max_tokens=max_tokens,
                top_k=top_k,
                top_p=top_p,
                stop_sequences=stop,
                system=system,
                stream=stream,
                tools=tools,
                **extra_data
            )
            try:
                async with session.post(f'{cls.api_base}/messages', json=data) as response:
                    await raise_for_status(response)
                    if not stream:
                        data = await response.json()
                        cls.raise_error(data)
                        if 'type' in data and data['type'] == 'message':
                            tool_calls: List[Dict[str, Any]] = []
                            for content in data['content']:
                                if content['type'] == 'text':
                                    yield content['text']
                                elif content['type'] == 'tool_use':
                                    tool_calls.append({
                                        'id': content['id'],
                                        'type': 'function',
                                        'function': { 'name': content['name'], 'arguments': content['input'] }
                                    })
                            if data['stop_reason'] == 'end_turn':
                                yield FinishReason('stop')
                            elif data['stop_reason'] == 'max_tokens':
                                yield FinishReason('length')
                            yield Usage(**data['usage'])
                            if tool_calls:
                                yield ToolCalls(tool_calls)  # Возвращаем tool_calls после обработки
                    else:
                        content_block: Optional[Dict[str, Any]] = None
                        partial_json: List[str] = []
                        tool_calls: List[Dict[str, Any]] = []
                        async for line in response.iter_lines():
                            if line.startswith(b'data: '):
                                chunk: bytes = line[6:]
                                if chunk == b'[DONE]':
                                    break
                                data = json.loads(chunk.decode('utf-8'))  # Декодируем chunk в строку
                                cls.raise_error(data)
                                if 'type' in data:
                                    if data['type'] == 'content_block_start':
                                        content_block = data['content_block']
                                    if content_block is None:
                                        pass  # Message start
                                    elif data['type'] == 'content_block_delta':
                                        if content_block['type'] == 'text':
                                            yield data['delta']['text']
                                        elif content_block['type'] == 'tool_use':
                                            partial_json.append(data['delta']['partial_json'])
                                    elif data['type'] == 'message_delta':
                                        if data['delta']['stop_reason'] == 'end_turn':
                                            yield FinishReason('stop')
                                        elif data['delta']['stop_reason'] == 'max_tokens':
                                            yield FinishReason('length')
                                        yield Usage(**data['usage'])
                                    elif data['type'] == 'content_block_stop':
                                        if content_block['type'] == 'tool_use':
                                            tool_calls.append({
                                                'id': content_block['id'],
                                                'type': 'function',
                                                'function': { 'name': content_block['name'], 'arguments': ''.join(partial_json) }
                                            })
                                            partial_json = []
                        if tool_calls:
                            yield ToolCalls(tool_calls)
            except Exception as ex:
                logger.error('Ошибка при создании асинхронного генератора', ex, exc_info=True)
                raise  # Перебрасываем исключение после логирования

    @classmethod
    def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
        """
        Формирует заголовки для запроса к Anthropic API.

        Args:
            stream (bool): Флаг для включения стриминга.
            api_key (str, optional): API ключ для аутентификации. Defaults to None.
            headers (dict, optional): Дополнительные заголовки для запроса. Defaults to None.

        Returns:
            dict: Словарь с заголовками для запроса.
        """
        default_headers: Dict[str, str] = {
            'Accept': 'text/event-stream' if stream else 'application/json',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01',
        }
        if api_key is not None:
            default_headers['x-api-key'] = api_key
        if headers is not None:
            default_headers.update(headers)
        return default_headers