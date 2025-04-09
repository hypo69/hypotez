### **Анализ кода модуля `GeminiPro.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация для неблокирующего выполнения.
    - Использование `ProviderModelMixin` для работы с моделями.
    - Обработка как streaming, так и не-streaming запросов.
    - Поддержка system_message.
- **Минусы**:
    - Отсутствие документации и аннотаций типов.
    - Смешанный стиль кавычек.
    - Не используется `logger` для логирования ошибок.
    - Не используются `j_loads` или `j_loads_ns`.
    - Использование `Union` вместо `|`.
    - Обработка ошибок происходит без использования `logger.error`.

#### **Рекомендации по улучшению**:
1.  **Добавить документацию**:
    - Добавить docstring к классам и методам, описывающие их назначение, параметры и возвращаемые значения.
2.  **Использовать аннотации типов**:
    - Добавить аннотации типов для переменных и параметров функций.
3.  **Улучшить обработку ошибок**:
    - Использовать `logger.error` для логирования ошибок с передачей `ex` и `exc_info=True`.
4.  **Унифицировать стиль кавычек**:
    - Использовать только одинарные кавычки.
5.  **Заменить `Union` на `|`**:
    - Использовать `|` вместо `Union`.
6.  **Использовать `j_loads` или `j_loads_ns`**:
    - Для чтения JSON или конфигурационных файлов.
7.  **Удалить неиспользуемые импорты**:
    - Проверить и удалить неиспользуемые импорты.
8. **Использовать driver.execute_locator**:
    - Если в коде используется webdriver, знай как его использовать
    наследуй Driver, Chrome, Firexox, Playwright
    Далее определи так
    # Создание инстанса драйвера (пример с Chrome)
    driver = Drivewr(Chrome)
    В модулях Driver И Chrome, Firexox, Playwright уже содержатся все настройки selenium.
    Основная комада, которая используется в коде: `driver.execute_locator(l:dict)`
    Она возвращает аначение вебэелемента по локатору.

#### **Оптимизированный код**:

```python
"""
Модуль для взаимодействия с Google Gemini API.
================================================

Предоставляет асинхронный класс `GeminiPro` для генерации контента с использованием моделей Gemini.
Поддерживает streaming, system_message и работу с media.
"""

from __future__ import annotations

import base64
import json
import requests
from typing import Optional
from aiohttp import ClientSession, BaseConnector

from ...typing import AsyncResult, Messages, MediaListType
from ...image import to_bytes, is_data_an_media
from ...errors import MissingAuthError
from ...requests.raise_for_status import raise_for_status
from ...providers.response import Usage, FinishReason
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import get_connector
from ... import debug
from src.logger import logger  # Добавлен импорт logger


class GeminiPro(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Асинхронный провайдер для Google Gemini API.

    Поддерживает streaming, system_message и работу с media.
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
    fallback_models: list[str] = [default_model, 'gemini-2.0-flash-exp', 'gemini-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b']
    model_aliases: dict[str, str] = {
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
            list[str]: Список моделей.

        Raises:
            MissingAuthError: Если API ключ недействителен.
        """
        if not cls.models:
            try:
                url: str = f'{cls.api_base if not api_base else api_base}/models'
                response = requests.get(url, params={'key': api_key})
                raise_for_status(response)
                data: dict = response.json()
                cls.models = [
                    model.get('name').split('/').pop()
                    for model in data.get('models')
                    if 'generateContent' in model.get('supportedGenerationMethods')
                ]
                cls.models.sort()
            except Exception as ex:
                logger.error('Error while getting models', ex, exc_info=True) # Логирование ошибки
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
        Создает асинхронный генератор для запросов к Gemini API.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений.
            stream (bool, optional): Использовать streaming. Defaults to False.
            proxy (str, optional): Proxy URL. Defaults to None.
            api_key (str, optional): API ключ. Defaults to None.
            api_base (str, optional): Базовый URL API. Defaults to api_base.
            use_auth_header (bool, optional): Использовать заголовок авторизации. Defaults to False.
            media (MediaListType, optional): Список медиафайлов. Defaults to None.
            tools (Optional[list], optional): Список инструментов. Defaults to None.
            connector (BaseConnector, optional): Connector для aiohttp. Defaults to None.

        Returns:
            AsyncResult: Асинхронный генератор.

        Raises:
            MissingAuthError: Если отсутствует API ключ.
            RuntimeError: При ошибке ответа от API.
        """
        if not api_key:
            raise MissingAuthError('Add a "api_key"')

        model = cls.get_model(model, api_key=api_key, api_base=api_base)

        headers: Optional[dict] = None
        params: Optional[dict] = None
        if use_auth_header:
            headers = {'Authorization': f'Bearer {api_key}'}
        else:
            params = {'key': api_key}

        method: str = 'streamGenerateContent' if stream else 'generateContent'
        url: str = f'{api_base.rstrip("/")}/models/{model}:{method}'
        async with ClientSession(headers=headers, connector=get_connector(connector, proxy)) as session:
            contents: list[dict] = [
                {
                    'role': 'model' if message['role'] == 'assistant' else 'user',
                    'parts': [{'text': message['content']}]
                }
                for message in messages
                if message['role'] != 'system'
            ]
            if media is not None:
                for media_data, filename in media:
                    image = to_bytes(media_data)
                    contents[-1]['parts'].append({
                        'inline_data': {
                            'mime_type': is_data_an_media(image, filename),
                            'data': base64.b64encode(media_data).decode()
                        }
                    })
            data: dict = {
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
                    try:
                        data = await response.json()
                        data = data[0] if isinstance(data, list) else data
                        raise RuntimeError(f'Response {response.status}: {data["error"]["message"]}')
                    except Exception as ex:
                        logger.error('Error in response', ex, exc_info=True)
                        raise  # Re-raise the exception after logging
                if stream:
                    lines: list[bytes] = []
                    async for chunk in response.content:
                        if chunk == b'[{\n':
                            lines = [b'{\n']
                        elif chunk == b',\r\n' or chunk == b']':
                            try:
                                data = b''.join(lines)
                                data = json.loads(data)
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
                                data = data.decode(errors='ignore') if isinstance(data, bytes) else data
                                logger.error(f'Read chunk failed: {data}', ex, exc_info=True) # Логирование ошибки
                                raise RuntimeError(f'Read chunk failed: {data}') from ex
                            lines = []
                        else:
                            lines.append(chunk)
                else:
                    data = await response.json()
                    candidate: dict = data['candidates'][0]
                    if candidate['finishReason'] == 'STOP':
                        yield candidate['content']['parts'][0]['text']
                    else:
                        yield candidate['finishReason'] + ' ' + candidate['safetyRatings']