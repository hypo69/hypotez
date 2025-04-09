### **Анализ кода модуля `Microsoft_Phi_4.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/Microsoft_Phi_4.py

Модуль `Microsoft_Phi_4.py` предоставляет класс `Microsoft_Phi_4`, который реализует взаимодействие с мультимодальной моделью Microsoft Phi-4 через Hugging Face Spaces.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Асинхронная обработка запросов.
  - Использование `StreamSession` для потоковой передачи данных.
  - Поддержка мультимодальных запросов (текст и изображения).
  - Реализована обработка ошибок.
- **Минусы**:
  - Не все переменные аннотированы типами.
  - Некоторые участки кода выглядят сложными для понимания из-за большого количества вложенных конструкций.
  - Метод `run` содержит много условных ветвлений, что снижает читаемость.

**Рекомендации по улучшению:**

1.  **Добавить docstring для модуля**:

    ```python
    """
    Модуль для взаимодействия с мультимодальной моделью Microsoft Phi-4 через Hugging Face Spaces.
    =============================================================================================

    Модуль содержит класс :class:`Microsoft_Phi_4`, который позволяет отправлять запросы к модели
    и получать ответы как в текстовом, так и в мультимодальном формате (с использованием изображений).

    Пример использования:
    ----------------------
    >>> provider = Microsoft_Phi_4()
    >>> result = await provider.create_async_generator(model='phi-4-multimodal', messages=[{'role': 'user', 'content': 'Hello'}])
    >>> async for chunk in result:
    ...     print(chunk)
    """
    ```

2.  **Добавить аннотации типов**:
    - Добавить аннотации типов для локальных переменных в методах.

3.  **Улучшить читаемость метода `run`**:
    - Разбить метод `run` на несколько подметодов для упрощения логики.

4.  **Добавить логирование**:
    - Добавить логирование для отладки и мониторинга работы провайдера.

5.  **Обработка ошибок**:
    - Улучшить обработку ошибок, добавив более конкретные исключения и логирование ошибок.

**Оптимизированный код:**

```python
from __future__ import annotations

import json
import uuid
from typing import AsyncGenerator, Optional, List

from ...typing import AsyncResult, Messages, Cookies, MediaListType
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt, format_image_prompt
from ...providers.response import JsonConversation
from ...requests.aiohttp import StreamSession, StreamResponse, FormData
from ...requests.raise_for_status import raise_for_status
from ...image import to_bytes, is_accepted_format, is_data_an_audio
from ...errors import ResponseError
from ... import debug
from .DeepseekAI_JanusPro7b import get_zerogpu_token
from .raise_for_status import raise_for_status
from src.logger import logger  # Добавлен импорт logger


class Microsoft_Phi_4(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс для взаимодействия с мультимодальной моделью Microsoft Phi-4 через Hugging Face Spaces.
    """

    label: str = 'Microsoft Phi-4'
    space: str = 'microsoft/phi-4-multimodal'
    url: str = f'https://huggingface.co/spaces/{space}'
    api_url: str = 'https://microsoft-phi-4-multimodal.hf.space'
    referer: str = f'{api_url}?__theme=light'

    working: bool = True
    supports_stream: bool = True
    supports_system_message: bool = True
    supports_message_history: bool = True

    default_model: str = 'phi-4-multimodal'
    default_vision_model: str = default_model
    model_aliases: dict[str, str] = {'phi-4': default_vision_model}
    vision_models: List[str] = list(model_aliases.keys())
    models: List[str] = vision_models

    @classmethod
    def _prepare_headers(cls, conversation: JsonConversation) -> dict[str, str | None]:
        """
        Подготавливает заголовки для запросов.

        Args:
            conversation (JsonConversation): Объект JsonConversation с данными сессии.

        Returns:
            dict[str, str | None]: Словарь с заголовками.
        """
        headers: dict[str, str | None] = {
            'content-type': 'application/json',
            'x-zerogpu-token': conversation.zerogpu_token,
            'x-zerogpu-uuid': conversation.zerogpu_uuid,
            'referer': cls.referer,
        }
        return {k: v for k, v in headers.items() if v is not None}

    @classmethod
    async def _run_predict(cls, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None) -> StreamResponse:
        """
        Выполняет POST запрос к эндпоинту `/gradio_api/run/predict`.

        Args:
            session (StreamSession): Объект StreamSession для выполнения запроса.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект JsonConversation с данными сессии.
            media (list, optional): Список медиафайлов. Defaults to None.

        Returns:
            StreamResponse: Объект StreamResponse с ответом от сервера.
        """
        headers: dict[str, str | None] = cls._prepare_headers(conversation)
        response: StreamResponse = await session.post(f'{cls.api_url}/gradio_api/run/predict', **{
            'headers': headers,
            'json': {
                'data': [
                    [],
                    {
                        'text': prompt,
                        'files': media,
                    },
                    None
                ],
                'event_data': None,
                'fn_index': 10,
                'trigger_id': 8,
                'session_hash': conversation.session_hash
            },
        })
        return response

    @classmethod
    async def _run_post(cls, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None) -> StreamResponse:
        """
        Выполняет POST запрос к эндпоинту `/gradio_api/queue/join`.

        Args:
            session (StreamSession): Объект StreamSession для выполнения запроса.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект JsonConversation с данными сессии.
            media (list, optional): Список медиафайлов. Defaults to None.

        Returns:
            StreamResponse: Объект StreamResponse с ответом от сервера.
        """
        headers: dict[str, str | None] = cls._prepare_headers(conversation)
        response: StreamResponse = await session.post(f'{cls.api_url}/gradio_api/queue/join?__theme=light', **{
            'headers': headers,
            'json': {
                'data': [[
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ] + [[
                    {
                        'role': 'user',
                        'content': {'file': image}
                    } for image in media
                ]],
                'event_data': None,
                'fn_index': 11,
                'trigger_id': 8,
                'session_hash': conversation.session_hash
            },
        })
        return response

    @classmethod
    async def _run_get(cls, session: StreamSession, conversation: JsonConversation) -> StreamResponse:
        """
        Выполняет GET запрос к эндпоинту `/gradio_api/queue/data`.

        Args:
            session (StreamSession): Объект StreamSession для выполнения запроса.
            conversation (JsonConversation): Объект JsonConversation с данными сессии.

        Returns:
            StreamResponse: Объект StreamResponse с ответом от сервера.
        """
        headers: dict[str, str | None] = {
            'accept': 'text/event-stream',
            'content-type': 'application/json',
            'referer': cls.referer,
        }
        response: StreamResponse = await session.get(f'{cls.api_url}/gradio_api/queue/data?session_hash={conversation.session_hash}', **{
            'headers': headers
        })
        return response

    @classmethod
    async def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None) -> StreamResponse:
        """
        Выполняет HTTP запрос к API в зависимости от указанного метода.

        Args:
            method (str): Метод запроса ('predict', 'post', 'get').
            session (StreamSession): Объект StreamSession для выполнения запроса.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект JsonConversation с данными сессии.
            media (list, optional): Список медиафайлов. Defaults to None.

        Returns:
            StreamResponse: Объект StreamResponse с ответом от сервера.
        """
        if method == 'predict':
            return await cls._run_predict(session, prompt, conversation, media)
        if method == 'post':
            return await cls._run_post(session, prompt, conversation, media)
        if method == 'get':
            return await cls._run_get(session, conversation)
        raise ValueError(f'Invalid method: {method}')

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        media: MediaListType = None,
        prompt: str = None,
        proxy: str = None,
        cookies: Cookies = None,
        api_key: str = None,
        zerogpu_uuid: str = '[object Object]',
        return_conversation: bool = False,
        conversation: JsonConversation = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью Microsoft Phi-4.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиафайлов. Defaults to None.
            prompt (str, optional): Текст запроса. Defaults to None.
            proxy (str, optional): Адрес прокси-сервера. Defaults to None.
            cookies (Cookies, optional): Cookie для отправки с запросом. Defaults to None.
            api_key (str, optional): API ключ. Defaults to None.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. Defaults to '[object Object]'.
            return_conversation (bool, optional): Флаг возврата объекта conversation. Defaults to False.
            conversation (JsonConversation, optional): Объект JsonConversation с данными сессии. Defaults to None.

        Yields:
            AsyncGenerator[str, None]: Части ответа от модели.
        """
        prompt = format_prompt(messages) if prompt is None and conversation is None else prompt
        prompt = format_image_prompt(messages, prompt)

        session_hash: str = uuid.uuid4().hex if conversation is None else getattr(conversation, 'session_hash', uuid.uuid4().hex)
        async with StreamSession(proxy=proxy, impersonate='chrome') as session:
            if api_key is None:
                zerogpu_uuid, api_key = await get_zerogpu_token(cls.space, session, conversation, cookies)
            if conversation is None or not hasattr(conversation, 'session_hash'):
                conversation = JsonConversation(session_hash=session_hash, zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid)
            else:
                conversation.zerogpu_token = api_key
            if return_conversation:
                yield conversation

            if media is not None:
                data: FormData = FormData()
                mime_types: list[Optional[str]] = [None for i in range(len(media))]
                for i in range(len(media)):
                    mime_types[i] = is_data_an_audio(media[i][0], media[i][1])
                    media[i] = (to_bytes(media[i][0]), media[i][1])
                    mime_types[i] = is_accepted_format(media[i][0]) if mime_types[i] is None else mime_types[i]
                for image, image_name in media:
                    data.add_field('files', to_bytes(image), filename=image_name)
                async with session.post(f'{cls.api_url}/gradio_api/upload', params={'upload_id': session_hash}, data=data) as response:
                    await raise_for_status(response)
                    image_files: list[str] = await response.json()
                media: list[dict[str, str | int | dict[str, str]]] = [{
                    'path': image_file,
                    'url': f'{cls.api_url}/gradio_api/file={image_file}',
                    'orig_name': media[i][1],
                    'size': len(media[i][0]),
                    'mime_type': mime_types[i],
                    'meta': {
                        '_type': 'gradio.FileData'
                    }
                } for i, image_file in enumerate(image_files)]

            async with cls.run('predict', session, prompt, conversation, media) as response:
                await raise_for_status(response)

            async with cls.run('post', session, prompt, conversation, media) as response:
                await raise_for_status(response)

            async with cls.run('get', session, prompt, conversation) as response:
                response: StreamResponse = response
                async for line in response.iter_lines():
                    if line.startswith(b'data: '):
                        try:
                            json_data: dict = json.loads(line[6:])
                            if json_data.get('msg') == 'process_completed':
                                if 'output' in json_data and 'error' in json_data['output']:
                                    raise ResponseError(json_data['output']['error'])
                                if 'output' in json_data and 'data' in json_data['output']:
                                    yield json_data['output']['data'][0][-1]['content']
                                break

                        except json.JSONDecodeError as ex:
                            debug.log('Could not parse JSON:', line.decode(errors='replace'))
                            logger.error('Could not parse JSON', ex, exc_info=True)  # Добавлено логирование ошибки