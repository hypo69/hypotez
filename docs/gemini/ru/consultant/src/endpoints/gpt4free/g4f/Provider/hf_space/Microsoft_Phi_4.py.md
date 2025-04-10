### **Анализ кода модуля `Microsoft_Phi_4.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Асинхронная обработка запросов.
  - Использование `StreamSession` для эффективной потоковой передачи данных.
  - Обработка ошибок и логирование.
- **Минусы**:
  - Не все переменные аннотированы типами.
  - Смешанный стиль в использовании кавычек (иногда двойные, иногда одинарные).
  - Некоторые участки кода требуют более подробных комментариев.

**Рекомендации по улучшению**:

1. **Документация модуля**:
   - Добавить заголовок и описание модуля в формате Markdown.

2. **Аннотации типов**:
   - Добавить аннотации типов для всех переменных, где они отсутствуют.
   - Уточнить типы для `media` (использовать `List[Tuple[bytes, str]]` вместо `list`, если это применимо).

3. **Комментарии и docstring**:
   - Добавить docstring для класса `Microsoft_Phi_4` с описанием его назначения.
   - Добавить docstring для метода `run` с описанием параметров и возвращаемых значений.
   - Улучшить комментарии для более понятного описания логики работы с `FormData` и обработки ответов.

4. **Использование кавычек**:
   - Привести все строки к использованию одинарных кавычек.

5. **Обработка ошибок**:
   - Использовать `logger.error` для логирования ошибок с передачей исключения (`ex`) и `exc_info=True`.

6. **Структура кода**:
   - Упростить логику обработки `json_data`, чтобы уменьшить вложенность условий.

7. **Безопасность**:
   - Проверить и обработать возможные уязвимости, связанные с загрузкой файлов (например, проверка расширения файла).

**Оптимизированный код**:

```python
"""
Модуль для работы с моделью Microsoft Phi-4
==============================================

Модуль содержит класс :class:`Microsoft_Phi_4`, который используется для взаимодействия с multimodal моделью Phi-4 от Microsoft через Hugging Face Spaces.
Он поддерживает потоковую передачу данных, обработку мультимедийных файлов и сообщений.

Пример использования:
----------------------

>>> provider = Microsoft_Phi_4()
>>> async for message in provider.create_async_generator(model='phi-4-multimodal', messages=[{'role': 'user', 'content': 'Hello'}]):
...     print(message)
"""

from __future__ import annotations

import json
import uuid
from typing import AsyncGenerator, Optional, List, Tuple, Dict

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
from src.logger import logger  # Импорт logger

class Microsoft_Phi_4(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для multimodal модели Microsoft Phi-4.
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
    model_aliases: Dict[str, str] = {'phi-4': default_vision_model}
    vision_models: List[str] = list(model_aliases.keys())
    models: List[str] = vision_models

    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: Optional[List[Dict[str, str]]] = None) -> AsyncResult:
        """
        Выполняет HTTP-запрос к API.

        Args:
            method (str): HTTP-метод (predict, post, get).
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект для хранения состояния разговора.
            media (Optional[List[Dict[str, str]]], optional): Список медиафайлов для отправки. Defaults to None.

        Returns:
            AsyncResult: Асинхронный результат HTTP-запроса.
        """
        headers: Dict[str, Optional[str]] = {
            'content-type': 'application/json',
            'x-zerogpu-token': conversation.zerogpu_token,
            'x-zerogpu-uuid': conversation.zerogpu_uuid,
            'referer': cls.referer,
        }
        headers = {k: v for k, v in headers.items() if v is not None} # Фильтрация None значений

        if method == 'predict':
            return session.post(f'{cls.api_url}/gradio_api/run/predict', **{
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
        if method == 'post':
            return session.post(f'{cls.api_url}/gradio_api/queue/join?__theme=light', **{
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
                    ],
                },
            })
        return session.get(f'{cls.api_url}/gradio_api/queue/data?session_hash={conversation.session_hash}', **{
            'headers': {
                'accept': 'text/event-stream',
                'content-type': 'application/json',
                'referer': cls.referer,
            }
        })

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
    ) -> AsyncGenerator[str, None]:
        """
        Создает асинхронный генератор для получения ответов от API.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиафайлов для отправки. Defaults to None.
            prompt (str, optional): Текст запроса. Defaults to None.
            proxy (str, optional): Прокси-сервер для использования. Defaults to None.
            cookies (Cookies, optional): Cookies для отправки. Defaults to None.
            api_key (str, optional): API ключ. Defaults to None.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. Defaults to '[object Object]'.
            return_conversation (bool, optional): Возвращать ли объект conversation. Defaults to False.
            conversation (JsonConversation, optional): Объект для хранения состояния разговора. Defaults to None.

        Yields:
            str: Ответ от API.

        Raises:
            ResponseError: Если в ответе содержится ошибка.
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
                yield conversation # type: ignore

            if media is not None:
                data: FormData = FormData()
                mime_types: List[Optional[str]] = [None for _ in range(len(media))]
                for i in range(len(media)):
                    mime_types[i] = is_data_an_audio(media[i][0], media[i][1])
                    media[i] = (to_bytes(media[i][0]), media[i][1])
                    mime_types[i] = is_accepted_format(media[i][0]) if mime_types[i] is None else mime_types[i]
                for image, image_name in media:
                    data.add_field('files', to_bytes(image), filename=image_name) # type: ignore
                async with session.post(f'{cls.api_url}/gradio_api/upload', params={'upload_id': session_hash}, data=data) as response:
                    await raise_for_status(response)
                    image_files: List[str] = await response.json()
                media = [{
                    'path': image_file,
                    'url': f'{cls.api_url}/gradio_api/file={image_file}',
                    'orig_name': media[i][1], # type: ignore
                    'size': len(media[i][0]), # type: ignore
                    'mime_type': mime_types[i], # type: ignore
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
                            msg: str = json_data.get('msg', '')
                            if msg == 'process_completed':
                                output: dict = json_data.get('output', {})
                                error: str = output.get('error')
                                if error:
                                    raise ResponseError(error)
                                data_content: list = output.get('data', [])
                                if data_content:
                                    yield data_content[0][-1]['content']
                                break

                        except json.JSONDecodeError as ex:
                            debug.log('Could not parse JSON:', line.decode(errors='replace'))
                            logger.error('Could not parse JSON', ex, exc_info=True)
                        except ResponseError as ex:
                            logger.error('Response error', ex, exc_info=True)