### **Анализ кода модуля `GeminiPro.py`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Использование асинхронных операций для неблокирующего выполнения.
     - Реализация поддержки стриминга ответов.
     - Наличие обработки ошибок и логирования.
     - Класс `GeminiPro` предоставляет методы для получения моделей и создания асинхронных генераторов.
     - Использование `try-except` блоков для обработки исключений при запросах к API.
   - **Минусы**:
     - Отсутствие подробной документации к большинству функций и параметров.
     - Не все переменные аннотированы типами.
     - Смешанный стиль кавычек (использование как двойных, так и одинарных кавычек).
     - Некоторые участки кода сложны для понимания из-за отсутствия комментариев.
     - Использование `debug.error(e)` вместо `logger.error(e, exc_info=True)` для логирования ошибок.
     - Не все импорты используются.

3. **Рекомендации по улучшению**:
   - Добавить docstring к классу `GeminiPro` с описанием его назначения и основных методов.
   - Добавить docstring к методам `get_models` и `create_async_generator` с подробным описанием параметров и возвращаемых значений.
   - Заменить `debug.error(e)` на `logger.error(e, exc_info=True)` для более информативного логирования ошибок.
   - Использовать только одинарные кавычки для строк.
   - Добавить аннотации типов для всех переменных и параметров функций.
   - Улучшить обработку ошибок, чтобы предоставлять более конкретные сообщения об ошибках.
   - Избавиться от неиспользуемых импортов.

4. **Оптимизированный код**:

```python
"""
Модуль для работы с Gemini Pro API от Google
============================================

Модуль содержит класс :class:`GeminiPro`, который используется для взаимодействия с API Gemini Pro
для генерации контента на основе текстовых запросов и медиа-файлов.

Пример использования:
----------------------

>>> api_key = "YOUR_API_KEY"
>>> model = "gemini-1.5-pro"
>>> messages = [{"role": "user", "content": "Hello, Gemini!"}]
>>> generator = await GeminiPro.create_async_generator(model=model, messages=messages, api_key=api_key)
>>> async for chunk in generator:
...     print(chunk)
"""
from __future__ import annotations

import base64
import json
import requests
from typing import Optional, List, AsyncGenerator, Tuple, Dict, Any, Union
from pathlib import Path
from aiohttp import ClientSession, BaseConnector

from src.logger import logger #  Используем logger из src.logger
from ...typing import AsyncResult, Messages, MediaListType
from ...image import to_bytes, is_data_an_media
from ...errors import MissingAuthError
from ...requests.raise_for_status import raise_for_status
from ...providers.response import Usage, FinishReason
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import get_connector


class GeminiPro(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для доступа к Google Gemini API.

    Поддерживает текстовые и мультимодальные запросы.
    """

    label: str = 'Google Gemini API'
    url: str = 'https://ai.google.dev'
    login_url: str = 'https://aistudio.google.com/u/0/apikey'
    api_base: str = 'https://generativelanguage.googleapis.com/v1beta'

    working: bool = True
    supports_message_history: bool = True
    supports_system_message: bool = True
    needs_auth: bool = True

    default_model: str = 'gemini-1.5-pro'
    default_vision_model: str = default_model
    fallback_models: List[str] = [default_model, 'gemini-2.0-flash-exp', 'gemini-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b']
    model_aliases: Dict[str, str] = {
        'gemini-1.5-flash': 'gemini-1.5-flash',
        'gemini-1.5-flash': 'gemini-1.5-flash-8b',
        'gemini-1.5-pro': 'gemini-pro',
        'gemini-2.0-flash': 'gemini-2.0-flash-exp',
    }

    @classmethod
    def get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]:
        """
        Получает список доступных моделей Gemini API.

        Args:
            api_key (str, optional): API ключ. Defaults to None.
            api_base (str, optional): Базовый URL API. Defaults to api_base.

        Returns:
            list[str]: Список доступных моделей.

        Raises:
            MissingAuthError: Если API ключ недействителен.
        """
        if not cls.models:
            try:
                url: str = f'{cls.api_base if not api_base else api_base}/models'
                response = requests.get(url, params={'key': api_key})
                raise_for_status(response)
                data: dict = response.json()
                cls.models: List[str] = [
                    model.get('name').split('/').pop()
                    for model in data.get('models')
                    if 'generateContent' in model.get('supportedGenerationMethods')
                ]
                cls.models.sort()
            except Exception as ex:
                logger.error(ex, exc_info=True) #  Используем logger.error для логирования ошибок
                if api_key is not None:
                    raise MissingAuthError('Invalid API key')
                return cls.fallback_models
        return cls.models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = False,
        proxy: str = None,
        api_key: str = None,
        api_base: str = api_base,
        use_auth_header: bool = False,
        media: MediaListType = None,
        tools: Optional[list] = None,
        connector: BaseConnector = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с Gemini API.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool, optional): Использовать ли стриминг. Defaults to False.
            proxy (str, optional): Proxy URL. Defaults to None.
            api_key (str, optional): API ключ. Defaults to None.
            api_base (str, optional): Базовый URL API. Defaults to api_base.
            use_auth_header (bool, optional): Использовать ли заголовок авторизации. Defaults to False.
            media (MediaListType, optional): Список медиа-файлов для отправки. Defaults to None.
            tools (Optional[list], optional): Список инструментов для использования. Defaults to None.
            connector (BaseConnector, optional): Connector для сессии aiohttp. Defaults to None.
            **kwargs: Дополнительные параметры для конфигурации генерации.

        Returns:
            AsyncResult: Асинхронный генератор для получения ответов от API.

        Raises:
            MissingAuthError: Если отсутствует API ключ.
            RuntimeError: Если произошла ошибка при запросе к API.
        """
        if not api_key:
            raise MissingAuthError('Add a "api_key"')

        model: str = cls.get_model(model, api_key=api_key, api_base=api_base)

        headers: Optional[Dict[str, str]] = None
        params: Optional[Dict[str, str]] = None
        if use_auth_header:
            headers = {'Authorization': f'Bearer {api_key}'}
        else:
            params = {'key': api_key}

        method: str = 'streamGenerateContent' if stream else 'generateContent'
        url: str = f'{api_base.rstrip("/")}/models/{model}:{method}'
        async with ClientSession(headers=headers, connector=get_connector(connector, proxy)) as session:
            contents: List[Dict[str, Any]] = [
                {
                    'role': 'model' if message['role'] == 'assistant' else 'user',
                    'parts': [{'text': message['content']}]
                }
                for message in messages
                if message['role'] != 'system'
            ]
            if media is not None:
                for media_data, filename in media:
                    image: bytes = to_bytes(media_data)
                    contents[-1]['parts'].append({
                        'inline_data': {
                            'mime_type': is_data_an_media(image, filename),
                            'data': base64.b64encode(media_data).decode()
                        }
                    })
            data: Dict[str, Any] = {
                'contents': contents,
                'generationConfig': {
                    'stopSequences': kwargs.get('stop'),
                    'temperature': kwargs.get('temperature'),
                    'maxOutputTokens': kwargs.get('max_tokens'),
                    'topP': kwargs.get('top_p'),
                    'topK': kwargs.get('top_k'),
                },
                 'tools': [{
                    'function_declarations': [{
                        'name': tool['function']['name'],
                        'description': tool['function']['description'],
                        'parameters': {
                            'type': 'object',
                            'properties': {key: {
                                'type': value['type'],
                                'description': value['title']
                            } for key, value in tool['function']['parameters']['properties'].items()}
                        },
                    } for tool in tools]
                }] if tools else None
            }
            system_prompt: str = '\n'.join(
                message['content']
                for message in messages
                if message['role'] == 'system'
            )
            if system_prompt:
                data['system_instruction'] = {'parts': {'text': system_prompt}}
            async with session.post(url, params=params, json=data) as response:
                if not response.ok:
                    data: dict = await response.json()
                    data = data[0] if isinstance(data, list) else data
                    raise RuntimeError(f'Response {response.status}: {data["error"]["message"]}')
                if stream:
                    lines: List[bytes] = []
                    async for chunk in response.content:
                        if chunk == b'[{\\n':
                            lines = [b'{\\n']
                        elif chunk == b',\\r\\n' or chunk == b']':
                            try:
                                data: bytes = b''.join(lines)
                                data: dict = json.loads(data)
                                yield data['candidates'][0]['content']['parts'][0]['text']
                                if 'finishReason' in data['candidates'][0]:
                                    yield FinishReason(data['candidates'][0]['finishReason'].lower())
                                usage: dict = data.get('usageMetadata')
                                if usage:
                                    yield Usage(
                                        prompt_tokens=usage.get('promptTokenCount'),
                                        completion_tokens=usage.get('candidatesTokenCount'),
                                        total_tokens=usage.get('totalTokenCount')
                                    )
                            except Exception as ex:
                                data: str = data.decode(errors='ignore') if isinstance(data, bytes) else data
                                logger.error(f'Read chunk failed: {data}', ex, exc_info=True) #  Используем logger.error для логирования ошибок
                                raise RuntimeError(f'Read chunk failed: {data}')
                            lines = []
                        else:
                            lines.append(chunk)
                else:
                    data: dict = await response.json()
                    candidate: dict = data['candidates'][0]
                    if candidate['finishReason'] == 'STOP':
                        yield candidate['content']['parts'][0]['text']
                    else:
                        yield candidate['finishReason'] + ' ' + candidate['safetyRatings']