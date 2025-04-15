### **Анализ кода модуля `PollinationsAI.py`**

=========================================================================================

Модуль предоставляет класс `PollinationsAI`, который является асинхронным провайдером для взаимодействия с API Pollinations AI, поддерживающим как генерацию текста, так и изображений.

#### **Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Поддержка асинхронных операций.
  - Реализация методов для работы с текстовыми и графическими моделями.
  - Использование `DEFAULT_HEADERS` для HTTP-запросов.
  - Обработка ошибок при запросе моделей.
- **Минусы**:
  - Смешанный стиль кодирования (использование и `requests`, и `aiohttp`).
  - Не везде используется `logger` для логирования ошибок.
  - Отсутствуют docstring для некоторых методов и классов.
  - Дублирование кода при обработке ошибок.

#### **Рекомендации по улучшению**:

1.  **Документирование**:
    - Добавить docstring для класса `PollinationsAI` с описанием его назначения и основных методов.
    - Добавить docstring для внутренних методов, таких как `_generate_image` и `_generate_text`.
    - Улучшить существующие docstring, сделав их более подробными и информативными.

2.  **Логирование**:
    - Заменить `debug.error` на `logger.error` из модуля `src.logger.logger` для единообразного логирования ошибок.
    - Добавить логирование важных событий, таких как успешное получение списка моделей.

3.  **Обработка ошибок**:
    - Использовать `ex` вместо `e` в блоках `except`.
    - Добавить обработку исключений для всех сетевых запросов, чтобы обеспечить устойчивость к сбоям.

4.  **Унификация HTTP-клиента**:
    - Использовать только `aiohttp` вместо комбинации `requests` и `aiohttp`, чтобы избежать смешивания синхронного и асинхронного кода.
    - Создать единый `ClientSession` для всех запросов и использовать его повторно.

5.  **Форматирование**:
    - Использовать одинарные кавычки для всех строк.

6. **Аннотации**:
   - Во всем коде проставить аннотации типов

#### **Оптимизированный код**:

```python
from __future__ import annotations

import json
import random
import asyncio
from urllib.parse import quote_plus
from typing import Optional, List, Dict, Tuple, AsyncGenerator, Any
from aiohttp import ClientSession

from .helper import filter_none, format_image_prompt
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..typing import AsyncResult, Messages, MediaListType
from ..image import is_data_an_audio
from ..errors import ModelNotFoundError
from ..requests.raise_for_status import raise_for_status
from ..requests.aiohttp import get_connector
from ..image.copy_images import save_response_media
from ..image import use_aspect_ratio
from ..providers.response import FinishReason, Usage, ToolCalls, ImageResponse
from ..tools.media import render_messages
from ..logger import logger  # Import logger
from aiohttp import ClientResponse


DEFAULT_HEADERS: Dict[str, str] = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'referer': 'https://pollinations.ai/',
    'origin': 'https://pollinations.ai',
}


class PollinationsAI(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с API Pollinations AI, поддерживающий генерацию текста и изображений.

    Args:
        label (str): Название провайдера.
        url (str): URL провайдера.

    Returns:
        None
    """
    label: str = 'Pollinations AI'
    url: str = 'https://pollinations.ai'

    working: bool = True
    supports_system_message: bool = True
    supports_message_history: bool = True

    # API endpoints
    text_api_endpoint: str = 'https://text.pollinations.ai'
    openai_endpoint: str = 'https://text.pollinations.ai/openai'
    image_api_endpoint: str = 'https://image.pollinations.ai/'

    # Models configuration
    default_model: str = 'openai'
    default_image_model: str = 'flux'
    default_vision_model: str = default_model
    text_models: List[str] = [default_model]
    image_models: List[str] = [default_image_model]
    extra_image_models: List[str] = ['flux-pro', 'flux-dev', 'flux-schnell', 'midjourney', 'dall-e-3', 'turbo']
    vision_models: List[str] = [default_vision_model, 'gpt-4o-mini', 'o3-mini', 'openai', 'openai-large']
    extra_text_models: List[str] = vision_models
    _models_loaded: bool = False
    model_aliases: Dict[str, str] = {
        ### Text Models ###
        'gpt-4o-mini': 'openai',
        'gpt-4': 'openai-large',
        'gpt-4o': 'openai-large',
        'o3-mini': 'openai-reasoning',
        'qwen-2.5-coder-32b': 'qwen-coder',
        'llama-3.3-70b': 'llama',
        'mistral-nemo': 'mistral',
        'gpt-4o-mini': 'searchgpt',
        'llama-3.1-8b': 'llamalight',
        'llama-3.3-70b': 'llama-scaleway',
        'phi-4': 'phi',
        'gemini-2.0': 'gemini',
        'gemini-2.0-flash': 'gemini',
        'gemini-2.0-flash-thinking': 'gemini-thinking',
        'deepseek-r1': 'deepseek-r1-llama',
        'gpt-4o-audio': 'openai-audio',
        
        ### Image Models ###
        'sdxl-turbo': 'turbo',
    }

    @classmethod
    def get_models(cls, **kwargs) -> List[str]:
        """
        Получает список доступных моделей из API Pollinations AI.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            List[str]: Список доступных моделей.
        """
        if not cls._models_loaded:
            try:
                # Update of image models
                image_response = requests.get('https://image.pollinations.ai/models') #  Использовать aiohttp
                if image_response.ok:
                    new_image_models = image_response.json()
                else:
                    new_image_models = []

                # Combine models without duplicates
                all_image_models = (
                    cls.image_models +  # Already contains the default
                    cls.extra_image_models + 
                    new_image_models
                )
                cls.image_models = list(dict.fromkeys(all_image_models))

                # Update of text models
                text_response = requests.get('https://text.pollinations.ai/models') #  Использовать aiohttp
                text_response.raise_for_status()
                models = text_response.json()
                original_text_models = [
                    model.get('name') 
                    for model in models
                    if model.get('type') == 'chat'
                ]
                cls.audio_models = {
                    model.get('name'): model.get('voices')
                    for model in models
                    if model.get('audio')
                }
                
                # Combining text models
                combined_text = (
                    cls.text_models +  # Already contains the default
                    cls.extra_text_models + 
                    original_text_models +\
                    cls.vision_models
                )
                cls.text_models = list(dict.fromkeys(combined_text))
                
                cls._models_loaded = True
                logger.info('Successfully fetched models from API') #  Логируем успешное получение списка моделей

            except Exception as ex: #  Используем ex вместо e
                logger.error(f'Failed to fetch models: {ex}', exc_info=True) #  Используем logger.error для логирования ошибок
                # Save default models in case of an error
                if not cls.text_models:
                    cls.text_models = [cls.default_model]
                if not cls.image_models:
                    cls.image_models = [cls.default_image_model]

        return cls.text_models + cls.image_models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        cache: bool = False,
        # Image generation parameters
        prompt: str = None,
        aspect_ratio: str = '1:1',
        width: int = None,
        height: int = None,
        seed: Optional[int] = None,
        nologo: bool = True,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False,
        n: int = 1,
        # Text generation parameters
        media: MediaListType = None,
        temperature: float = None,
        presence_penalty: float = None,
        top_p: float = None,
        frequency_penalty: float = None,
        response_format: Optional[dict] = None,
        extra_parameters: list[str] = ['tools', 'parallel_tool_calls', 'tool_choice', 'reasoning_effort', 'logit_bias', 'voice', 'modalities', 'audio'],
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для выполнения запросов к API Pollinations AI.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений.
            stream (bool, optional): Использовать потоковую передачу. По умолчанию True.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
            cache (bool, optional): Использовать кэширование. По умолчанию False.
            prompt (str, optional): Текст запроса для генерации изображения. По умолчанию None.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию '1:1'.
            width (int, optional): Ширина изображения. По умолчанию None.
            height (int, optional): Высота изображения. По умолчанию None.
            seed (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию None.
            nologo (bool, optional): Убрать логотип. По умолчанию True.
            private (bool, optional): Сделать приватным. По умолчанию False.
            enhance (bool, optional): Улучшить изображение. По умолчанию False.
            safe (bool, optional): Безопасный режим. По умолчанию False.
            n (int, optional): Количество изображений. По умолчанию 1.
            media (MediaListType, optional): Список медиа-файлов. По умолчанию None.
            temperature (float, optional): Температура. По умолчанию None.
            presence_penalty (float, optional): Штраф за присутствие. По умолчанию None.
            top_p (float, optional): Top-p. По умолчанию None.
            frequency_penalty (float, optional): Штраф за частоту. По умолчанию None.
            response_format (Optional[dict], optional): Формат ответа. По умолчанию None.
            extra_parameters (list[str], optional): Дополнительные параметры. По умолчанию ['tools', 'parallel_tool_calls', 'tool_choice', 'reasoning_effort', 'logit_bias', 'voice', 'modalities', 'audio'].
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Результат выполнения запроса.
        """
        # Load model list
        cls.get_models()
        if not model:
            has_audio = 'audio' in kwargs
            if not has_audio and media is not None:
                for media_data, filename in media:
                    if is_data_an_audio(media_data, filename):
                        has_audio = True
                        break
            model = next(iter(cls.audio_models)) if has_audio else model
        try:
            model = cls.get_model(model)
        except ModelNotFoundError as ex: #  Используем ex вместо e
            if model not in cls.image_models:
                raise ex

        if model in cls.image_models:
            async for chunk in cls._generate_image(
                model=model,
                prompt=format_image_prompt(messages, prompt),
                proxy=proxy,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height,
                seed=seed,
                cache=cache,
                nologo=nologo,
                private=private,
                enhance=enhance,
                safe=safe,
                n=n
            ):
                yield chunk
        else:
            async for result in cls._generate_text(
                model=model,
                messages=messages,
                media=media,
                proxy=proxy,
                temperature=temperature,
                presence_penalty=presence_penalty,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                response_format=response_format,
                seed=seed,
                cache=cache,
                stream=stream,
                extra_parameters=extra_parameters,
                **kwargs
            ):
                yield result

    @classmethod
    async def _generate_image(
        cls,
        model: str,
        prompt: str,
        proxy: str,
        aspect_ratio: str,
        width: int,
        height: int,
        seed: Optional[int],
        cache: bool,
        nologo: bool,
        private: bool,
        enhance: bool,
        safe: bool,
        n: int
    ) -> AsyncResult:
        """
        Генерирует изображение с использованием API Pollinations AI.

        Args:
            model (str): Название модели.
            prompt (str): Текст запроса.
            proxy (str): Адрес прокси-сервера.
            aspect_ratio (str): Соотношение сторон изображения.
            width (int): Ширина изображения.
            height (int): Высота изображения.
            seed (Optional[int]): Зерно для генерации случайных чисел.
            cache (bool): Использовать кэширование.
            nologo (bool): Убрать логотип.
            private (bool): Сделать приватным.
            enhance (bool): Улучшить изображение.
            safe (bool): Безопасный режим.
            n (int): Количество изображений.

        Yields:
            AsyncResult: Результат генерации изображения.
        """
        params = use_aspect_ratio({
            'width': width,
            'height': height,
            'model': model,
            'nologo': str(nologo).lower(),
            'private': str(private).lower(),
            'enhance': str(enhance).lower(),
            'safe': str(safe).lower()
        }, aspect_ratio)
        query = '&'.join(f'{k}={quote_plus(str(v))}' for k, v in params.items() if v is not None)
        prompt = quote_plus(prompt)[:2048-256-len(query)]
        url = f'{cls.image_api_endpoint}prompt/{prompt}?{query}'
        def get_image_url(i: int = 0, seed: Optional[int] = None) -> str:
            """
            Формирует URL для запроса изображения.

            Args:
                i (int, optional): Индекс изображения. По умолчанию 0.
                seed (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию None.

            Returns:
                str: URL для запроса изображения.
            """
            if i == 0:
                if not cache and seed is None:
                    seed = random.randint(0, 2**32)
            else:
                seed = random.randint(0, 2**32)
            return f'{url}&seed={seed}' if seed else url
        async with ClientSession(headers=DEFAULT_HEADERS, connector=get_connector(proxy=proxy)) as session:
            async def get_image(i: int = 0, seed: Optional[int] = None) -> str:
                """
                Получает URL изображения.

                Args:
                    i (int, optional): Индекс изображения. По умолчанию 0.
                    seed (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию None.

                Returns:
                    str: URL изображения.
                """
                async with session.get(get_image_url(i, seed), allow_redirects=False) as response:
                    try:
                        await raise_for_status(response)
                    except Exception as ex: #  Используем ex вместо e
                        logger.error(f'Error fetching image: {ex}', exc_info=True) #  Используем logger.error для логирования ошибок
                        return str(response.url)
                    return str(response.url)
            yield ImageResponse(await asyncio.gather(*[
                get_image(i, seed) for i in range(int(n))
            ]), prompt)

    @classmethod
    async def _generate_text(
        cls,
        model: str,
        messages: Messages,
        media: MediaListType,
        proxy: str,
        temperature: float,
        presence_penalty: float,
        top_p: float,
        frequency_penalty: float,
        response_format: Optional[dict],
        seed: Optional[int],
        cache: bool,
        stream: bool,
        extra_parameters: list[str],
        **kwargs
    ) -> AsyncResult:
        """
        Генерирует текст с использованием API Pollinations AI.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений.
            media (MediaListType): Список медиа-файлов.
            proxy (str): Адрес прокси-сервера.
            temperature (float): Температура.
            presence_penalty (float): Штраф за присутствие.
            top_p (float): Top-p.
            frequency_penalty (float): Штраф за частоту.
            response_format (Optional[dict]): Формат ответа.
            seed (Optional[int]): Зерно для генерации случайных чисел.
            cache (bool): Использовать кэширование.
            stream (bool): Использовать потоковую передачу.
            extra_parameters (list[str]): Дополнительные параметры.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Результат генерации текста.
        """
        if not cache and seed is None:
            seed = random.randint(9999, 99999999)
        json_mode = False
        if response_format and response_format.get('type') == 'json_object':
            json_mode = True

        async with ClientSession(headers=DEFAULT_HEADERS, connector=get_connector(proxy=proxy)) as session:
            if model in cls.audio_models:
                url = cls.text_api_endpoint
                stream = False
            else:
                url = cls.openai_endpoint
            extra_parameters = {param: kwargs[param] for param in extra_parameters if param in kwargs}
            data = filter_none(**{
                'messages': list(render_messages(messages, media)),
                'model': model,
                'temperature': temperature,
                'presence_penalty': presence_penalty,
                'top_p': top_p,
                'frequency_penalty': frequency_penalty,
                'jsonMode': json_mode,
                'stream': stream,
                'seed': seed,
                'cache': cache,
                **extra_parameters
            })
            async with session.post(url, json=data) as response:
                await raise_for_status(response)
                async for chunk in save_response_media(response, format_image_prompt(messages), [model]):
                    yield chunk
                    return
                if response.headers['content-type'].startswith('text/plain'):
                    yield await response.text()
                    return
                elif response.headers['content-type'].startswith('text/event-stream'):
                    async for line in response.content:
                        if line.startswith(b'data: '):
                            if line[6:].startswith(b'[DONE]'):
                                break
                            result = json.loads(line[6:])
                            choices = result.get('choices', [{}])
                            choice = choices.pop() if choices else {}
                            content = choice.get('delta', {}).get('content')
                            if content:
                                yield content
                            if 'usage' in result:
                                yield Usage(**result['usage'])
                            finish_reason = choice.get('finish_reason')
                            if finish_reason:
                                yield FinishReason(finish_reason)
                    return
                result = await response.json()
                choice = result['choices'][0]
                message = choice.get('message', {})
                content = message.get('content', '')

                if 'tool_calls' in message:
                    yield ToolCalls(message['tool_calls'])

                if content:
                    yield content

                if 'usage' in result:
                    yield Usage(**result['usage'])

                finish_reason = choice.get('finish_reason')
                if finish_reason:
                    yield FinishReason(finish_reason)