### **Анализ кода модуля `Anthropic.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код структурирован в виде класса `Anthropic`, наследующего `OpenaiAPI`, что способствует повторному использованию кода и расширяемости.
  - Присутствует обработка ошибок и логирование исключений.
  - Использованы асинхронные операции для неблокирующего выполнения запросов.
  - Добавлена поддержка стриминга ответов от API.
  - Есть методы для получения списка моделей и формирования заголовков запросов.
- **Минусы**:
  - Некоторые участки кода требуют более подробных комментариев и документации.
  - Не все переменные и параметры аннотированы типами.
  - Присутствуют устаревшие конструкции, которые можно заменить более современными.
  - Отсутствует логирование важных событий и ошибок.
  - Не все функции имеют docstring.

#### **Рекомендации по улучшению**:
1. **Добавить документацию к классу `Anthropic`**:
   - Описать назначение класса, основные атрибуты и методы.

2. **Улучшить документацию функций**:
   - Добавить docstring к функциям `get_models`, `create_async_generator`, `get_headers`, описывающие входные параметры, возвращаемые значения и возможные исключения.
   - В docstring добавить примеры использования функций.

3. **Добавить аннотации типов**:
   - Указать типы для всех переменных и параметров функций, где они отсутствуют.

4. **Улучшить обработку ошибок**:
   - Добавить логирование ошибок с использованием `logger.error` из модуля `src.logger`.
   - Указывать `exc_info=True` при логировании исключений для получения полной трассировки.

5. **Оптимизировать код**:
   - Использовать более современные конструкции Python, такие как walrus operator (:=) где это уместно.
   - Упростить логику работы с `partial_json` в стриминговом режиме.

6. **Добавить комментарии**:
   - Добавить комментарии к сложным участкам кода, объясняющие их назначение.

7. **Проверить и обновить зависимости**:
   - Убедиться, что все используемые библиотеки актуальны.

#### **Оптимизированный код**:
```python
from __future__ import annotations

import requests
import json
import base64
from typing import Optional, List

from ..helper import filter_none
from ...typing import AsyncResult, Messages, MediaListType
from ...requests import StreamSession, raise_for_status
from ...providers.response import FinishReason, ToolCalls, Usage
from ...errors import MissingAuthError
from ...image import to_bytes, is_accepted_format
from .OpenaiAPI import OpenaiAPI
from src.logger import logger  # Import logger

"""
Модуль для взаимодействия с Anthropic API
===========================================

Этот модуль содержит класс `Anthropic`, который наследует `OpenaiAPI` и предоставляет функциональность для
взаимодействия с API Anthropic, включая поддержку стриминга, управления моделями и обработки изображений.
"""


class Anthropic(OpenaiAPI):
    """
    Класс для взаимодействия с Anthropic API.

    Этот класс предоставляет методы для выполнения запросов к API Anthropic,
    включая поддержку стриминга, управления моделями и обработки изображений.
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
    models_aliases: dict[str, str] = {
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
            api_key (str, optional): Ключ API для аутентификации. Defaults to None.

        Returns:
            List[str]: Список идентификаторов моделей.
        """
        if not cls.models:
            url: str = f'https://api.anthropic.com/v1/models'
            headers: dict[str, str] = {
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
            try:
                response = requests.get(url, headers=headers)
                raise_for_status(response)
                models = response.json()
                cls.models = [model['id'] for model in models['data']]
            except requests.exceptions.RequestException as ex:
                logger.error('Error while fetching models', ex, exc_info=True)
                return []
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
        Создает асинхронный генератор для взаимодействия с Anthropic API.

        Args:
            model (str): Идентификатор модели для использования.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера. Defaults to None.
            timeout (int, optional): Время ожидания запроса в секундах. Defaults to 120.
            media (MediaListType, optional): Список медиафайлов для отправки. Defaults to None.
            api_key (str, optional): Ключ API для аутентификации. Defaults to None.
            temperature (float, optional): Температура для управления случайностью ответов. Defaults to None.
            max_tokens (int, optional): Максимальное количество токенов в ответе. Defaults to 4096.
            top_k (int, optional): Параметр Top-K для фильтрации токенов. Defaults to None.
            top_p (float, optional): Параметр Top-P для фильтрации токенов. Defaults to None.
            stop (list[str], optional): Список стоп-последовательностей. Defaults to None.
            stream (bool, optional): Включить стриминг ответов. Defaults to False.
            headers (dict, optional): Дополнительные заголовки для отправки. Defaults to None.
            impersonate (str, optional): Параметр для имитации пользователя. Defaults to None.
            tools (Optional[list], optional): Список инструментов для использования. Defaults to None.
            extra_data (dict, optional): Дополнительные данные для отправки. Defaults to {}.

        Yields:
            AsyncResult: Результаты взаимодействия с API.

        Raises:
            MissingAuthError: Если не предоставлен ключ API.
        """
        if api_key is None:
            raise MissingAuthError('Add a "api_key"')

        if media is not None:
            insert_images: list[dict] = []
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

        system: str = '\n'.join([message['content'] for message in messages if message.get('role') == 'system'])
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
            data: dict = filter_none(
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
                            for content in data['content']:
                                if content['type'] == 'text':
                                    yield content['text']
                                elif content['type'] == 'tool_use':
                                    tool_calls: list[dict] = []
                                    tool_calls.append({
                                        'id': content['id'],
                                        'type': 'function',
                                        'function': {'name': content['name'], 'arguments': content['input']}
                                    })
                            if data['stop_reason'] == 'end_turn':
                                yield FinishReason('stop')
                            elif data['stop_reason'] == 'max_tokens':
                                yield FinishReason('length')
                            yield Usage(**data['usage'])
                    else:
                        content_block: Optional[dict] = None
                        partial_json: list[str] = []
                        tool_calls: list[dict] = []
                        async for line in response.iter_lines():
                            if line.startswith(b'data: '):
                                chunk: bytes = line[6:]
                                if chunk == b'[DONE]':
                                    break
                                data = json.loads(chunk)
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
                                                'function': {'name': content_block['name'], 'arguments': ''.join(partial_json)}
                                            })
                                            partial_json = []
                        if tool_calls:
                            yield ToolCalls(tool_calls)
            except Exception as ex:
                logger.error('Error while creating async generator', ex, exc_info=True)
                raise

    @classmethod
    def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
        """
        Получает заголовки для запроса к Anthropic API.

        Args:
            stream (bool): Включить стриминг ответов.
            api_key (str, optional): Ключ API для аутентификации. Defaults to None.
            headers (dict, optional): Дополнительные заголовки. Defaults to None.

        Returns:
            dict: Словарь заголовков для запроса.
        """
        default_headers: dict = {
            'Accept': 'text/event-stream' if stream else 'application/json',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01',
        }
        if api_key is not None:
            default_headers['x-api-key'] = api_key
        if headers is not None:
            default_headers.update(headers)
        return default_headers