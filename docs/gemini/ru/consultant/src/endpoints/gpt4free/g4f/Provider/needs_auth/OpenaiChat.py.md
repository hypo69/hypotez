### **Анализ кода модуля `OpenaiChat.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на логические блоки, что облегчает его понимание.
  - Присутствуют docstring для большинства функций и классов.
  - Используются асинхронные операции для неблокирующего выполнения задач.
- **Минусы**:
  - Встречаются смешанные стили кавычек (и одинарные, и двойные).
  - Некоторые docstring написаны на английском языке.
  - Не все переменные аннотированы типами.
  - Есть закомментированный код, который следует удалить или пересмотреть.
  - Отсутствует единообразный подход к обработке исключений (иногда просто `except Exception as e`, иногда с логированием).
  - Не везде используется `logger` из `src.logger` для логирования.

#### **Рекомендации по улучшению**:
- **Форматирование**:
  - Привести все строки к одинарным кавычкам.
  - Убедиться, что все переменные и параметры функций аннотированы типами.
- **Документация**:
  - Перевести все docstring на русский язык и привести к единому стилю.
  - Уточнить и дополнить docstring, где это необходимо.
- **Обработка исключений**:
  - Использовать `logger` из `src.logger` для логирования ошибок.
  - Использовать `ex` вместо `e` в блоках обработки исключений.
- **Удаление неиспользуемого кода**:
  - Удалить закомментированный код или восстановить его, если он все еще нужен.
- **Использование `j_loads` или `j_loads_ns`**:
  - Проверить, можно ли заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns` в каких-либо местах.
- **webdriver**:
  - В коде используется `nodriver`, который, вероятно, является заменой `webdriver`. Убедиться, что он правильно настроен и используется.

#### **Оптимизированный код**:
```python
from __future__ import annotations

import os
import re
import asyncio
import uuid
import json
import base64
import time
import random
from typing import AsyncIterator, Iterator, Optional, Generator, Dict, List
from copy import copy

try:
    import nodriver
    has_nodriver = True
except ImportError:
    has_nodriver = False

from ..base_provider import AsyncAuthedProvider, ProviderModelMixin
from ...typing import AsyncResult, Messages, Cookies, MediaListType
from ...requests.raise_for_status import raise_for_status
from ...requests import StreamSession
from ...requests import get_nodriver
from ...image import ImageRequest, to_image, to_bytes, is_accepted_format
from ...errors import MissingAuthError, NoValidHarFileError
from ...providers.response import JsonConversation, FinishReason, SynthesizeData, AuthResult, ImageResponse
from ...providers.response import Sources, TitleGeneration, RequestLogin, Reasoning
from ...tools.media import merge_media
from ..helper import format_cookies, get_last_user_message
from ..openai.models import default_model, default_image_model, models, image_models, text_models
from ..openai.har_file import get_request_config
from ..openai.har_file import RequestConfig, arkReq, arkose_url, start_url, conversation_url, backend_url, backend_anon_url
from ..openai.proofofwork import generate_proof_token
from ..openai.new import get_requirements_token, get_config
from ... import debug
from src.logger import logger  # Добавлен импорт logger

DEFAULT_HEADERS: Dict[str, str] = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.8',
    'referer': 'https://chatgpt.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

INIT_HEADERS: Dict[str, str] = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"14.4.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

UPLOAD_HEADERS: Dict[str, str] = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.8',
    'referer': 'https://chatgpt.com/',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'x-ms-blob-type': 'BlockBlob',
    'x-ms-version': '2020-04-08',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

class OpenaiChat(AsyncAuthedProvider, ProviderModelMixin):
    """
    Класс для создания и управления беседами с чат-сервисом OpenAI.
    """

    label: str = 'OpenAI ChatGPT'
    url: str = 'https://chatgpt.com'
    working: bool = True
    use_nodriver: bool = True
    supports_gpt_4: bool = True
    supports_message_history: bool = True
    supports_system_message: bool = True
    default_model: str = default_model
    default_image_model: str = default_image_model
    image_models: List[str] = image_models
    vision_models: List[str] = text_models
    models: List[str] = models
    synthesize_content_type: str = 'audio/aac'
    request_config: RequestConfig = RequestConfig()

    _api_key: Optional[str] = None
    _headers: Optional[dict] = None
    _cookies: Cookies = None
    _expires: Optional[int] = None

    @classmethod
    async def on_auth_async(cls, proxy: Optional[str] = None, **kwargs) -> AsyncIterator:
        """
        Асинхронно выполняет аутентификацию и возвращает результаты.

        Args:
            proxy (Optional[str], optional): Прокси для использования. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncIterator: Асинхронный итератор с результатами аутентификации.
        """
        async for chunk in cls.login(proxy=proxy):
            yield chunk
        yield AuthResult(
            api_key=cls._api_key,
            cookies=cls._cookies or cls.request_config.cookies or {},
            headers=cls._headers or cls.request_config.headers or cls.get_default_headers(),
            expires=cls._expires,
            proof_token=cls.request_config.proof_token,
            turnstile_token=cls.request_config.turnstile_token
        )

    @classmethod
    async def upload_images(
        cls,
        session: StreamSession,
        auth_result: AuthResult,
        media: MediaListType,
    ) -> list[ImageRequest]:
        """
        Загружает изображение на сервис и получает URL для скачивания.

        Args:
            session (StreamSession): Объект StreamSession для использования в запросах.
            auth_result (AuthResult): Результаты аутентификации.
            media (MediaListType): Изображения для загрузки (PIL Image или bytes).

        Returns:
            list[ImageRequest]: Список объектов ImageRequest с URL для скачивания и другими данными.
        """
        async def upload_image(image: bytes, image_name: Optional[str] = None) -> ImageRequest:
            """
            Загружает одно изображение.

            Args:
                image (bytes): Изображение в виде байтов.
                image_name (Optional[str], optional): Имя изображения. По умолчанию None.

            Returns:
                ImageRequest: Объект ImageRequest с данными загруженного изображения.
            """
            debug.log(f'Uploading image: {image_name}')
            # Преобразует изображение в PIL Image и получает расширение
            data_bytes = to_bytes(image)
            image_obj = to_image(data_bytes)
            extension = image_obj.format.lower()
            data: dict[str, str | int] = {
                'file_name': '' if image_name is None else image_name,
                'file_size': len(data_bytes),
                'use_case': 'multimodal'
            }
            # Отправляет данные изображения и получает данные изображения
            headers = auth_result.headers if hasattr(auth_result, 'headers') else None
            try:
                async with session.post(f'{cls.url}/backend-api/files', json=data, headers=headers) as response:
                    cls._update_request_args(auth_result, session)
                    await raise_for_status(response, 'Create file failed')
                    response_json = await response.json()
                    image_data: dict[str, str | int] = {
                        **data,
                        **response_json,
                        'mime_type': is_accepted_format(data_bytes),
                        'extension': extension,
                        'height': image_obj.height,
                        'width': image_obj.width
                    }
            except Exception as ex:
                logger.error('Error while creating file', ex, exc_info=True)
                raise
            # Отправляет байты изображения по upload URL и проверяет статус
            await asyncio.sleep(1)
            try:
                async with session.put(
                    image_data['upload_url'],
                    data=data_bytes,
                    headers={
                        **UPLOAD_HEADERS,
                        'Content-Type': image_data['mime_type'],
                        'x-ms-blob-type': 'BlockBlob',
                        'x-ms-version': '2020-04-08',
                        'Origin': 'https://chatgpt.com',
                    }
                ) as response:
                    await raise_for_status(response)
            except Exception as ex:
                logger.error('Error while uploading image', ex, exc_info=True)
                raise
            # Отправляет file ID и получает download URL
            try:
                async with session.post(
                    f'{cls.url}/backend-api/files/{image_data["file_id"]}/uploaded',
                    json={},
                    headers=auth_result.headers
                ) as response:
                    cls._update_request_args(auth_result, session)
                    await raise_for_status(response, 'Get download url failed')
                    image_data['download_url'] = (await response.json())['download_url']
            except Exception as ex:
                logger.error('Error while getting download URL', ex, exc_info=True)
                raise
            return ImageRequest(image_data)
        return [await upload_image(image, image_name) for image, image_name in media]

    @classmethod
    def create_messages(cls, messages: Messages, image_requests: Optional[list[ImageRequest]] = None, system_hints: Optional[list[str]] = None) -> list[dict]:
        """
        Создает список сообщений для пользовательского ввода.

        Args:
            messages (Messages): Список предыдущих сообщений.
            image_requests (Optional[list[ImageRequest]], optional): Список запросов изображений. По умолчанию None.
            system_hints (Optional[list[str]], optional): Список системных подсказок. По умолчанию None.

        Returns:
            list[dict]: Список сообщений с пользовательским вводом и изображением (если есть).
        """
        messages = [{
            'id': str(uuid.uuid4()),
            'author': {'role': message['role']},
            'content': {'content_type': 'text', 'parts': [message['content']]},
            'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}, **({'system_hints': system_hints} if system_hints else {})},
            'create_time': time.time(),
        } for message in messages]
        # Проверяет, есть ли ответ с изображением
        if image_requests:
            # Изменяет content в последнем сообщении пользователя
            messages[-1]['content'] = {
                'content_type': 'multimodal_text',
                'parts': [*[{
                    'asset_pointer': f'file-service://{image_request.get("file_id")}',
                    'height': image_request.get('height'),
                    'size_bytes': image_request.get('file_size'),
                    'width': image_request.get('width'),
                }
                for image_request in image_requests],
                messages[-1]['content']['parts'][0]]
            }
            # Добавляет объект metadata с attachments
            messages[-1]['metadata'] = {
                'attachments': [{
                    'height': image_request.get('height'),
                    'id': image_request.get('file_id'),
                    'mimeType': image_request.get('mime_type'),
                    'name': image_request.get('file_name'),
                    'size': image_request.get('file_size'),
                    'width': image_request.get('width'),
                }
                for image_request in image_requests]
            }
        return messages

    @classmethod
    async def get_generated_image(cls, session: StreamSession, auth_result: AuthResult, element: dict, prompt: Optional[str] = None) -> Optional[ImageResponse]:
        """
        Получает сгенерированное изображение.

        Args:
            session (StreamSession): Объект StreamSession для использования в запросах.
            auth_result (AuthResult): Результаты аутентификации.
            element (dict): Элемент с данными изображения.
            prompt (Optional[str], optional): Подсказка для генерации изображения. По умолчанию None.

        Returns:
            Optional[ImageResponse]: Объект ImageResponse с данными изображения или None в случае ошибки.
        """
        try:
            prompt = element['metadata']['dalle']['prompt']
            file_id = element['asset_pointer'].split('file-service://', 1)[1]
        except TypeError:
            return
        except Exception as ex:
            raise RuntimeError(f'No Image: {ex.__class__.__name__}: {ex}') from ex
        try:
            async with session.get(f'{cls.url}/backend-api/files/{file_id}/download', headers=auth_result.headers) as response:
                cls._update_request_args(auth_result, session)
                await raise_for_status(response)
                download_url = (await response.json())['download_url']
                return ImageResponse(download_url, prompt)
        except Exception as ex:
            raise RuntimeError(f'Error in downloading image: {ex}') from ex

    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        proxy: Optional[str] = None,
        timeout: int = 180,
        auto_continue: bool = False,
        action: Optional[str] = 'next',
        conversation: Optional[Conversation] = None,
        media: MediaListType = None,
        return_conversation: bool = False,
        web_search: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для беседы.

        Args:
            model (str): Имя модели.
            messages (Messages): Список предыдущих сообщений.
            auth_result (AuthResult): Результаты аутентификации.
            proxy (Optional[str], optional): Прокси для использования. По умолчанию None.
            timeout (int, optional): Время ожидания запроса. По умолчанию 180.
            auto_continue (bool, optional): Флаг для автоматического продолжения беседы. По умолчанию False.
            action (Optional[str], optional): Тип действия ('next', 'continue', 'variant'). По умолчанию 'next'.
            conversation (Optional[Conversation], optional): Объект Conversation. По умолчанию None.
            media (MediaListType, optional): Изображения для включения в беседу. По умолчанию None.
            return_conversation (bool, optional): Флаг для включения полей ответа в вывод. По умолчанию False.
            web_search (bool, optional): Флаг для включения веб-поиска. По умолчанию False.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Асинхронные результаты от генератора.

        Raises:
            RuntimeError: Если произошла ошибка во время обработки.
        """
        async with StreamSession(
            proxy=proxy,
            impersonate='chrome',
            timeout=timeout
        ) as session:
            image_requests: Optional[list[ImageRequest]] = None
            if not cls.needs_auth:
                if cls._headers is None:
                    cls._create_request_args(cls._cookies)
                    try:
                        async with session.get(cls.url, headers=INIT_HEADERS) as response:
                            cls._update_request_args(auth_result, session)
                            await raise_for_status(response)
                    except Exception as ex:
                        logger.error('Error while getting URL', ex, exc_info=True)
                        raise
            else:
                if cls._headers is None and getattr(auth_result, 'cookies', None):
                    cls._create_request_args(auth_result.cookies, auth_result.headers)
                if not cls._set_api_key(getattr(auth_result, 'api_key', None)):
                    raise MissingAuthError('Access token is not valid')
                try:
                    async with session.get(cls.url, headers=cls._headers) as response:
                        cls._update_request_args(auth_result, session)
                        await raise_for_status(response)
                except Exception as ex:
                    logger.error('Error while getting URL', ex, exc_info=True)
                    raise
                try:
                    image_requests = await cls.upload_images(session, auth_result, merge_media(media, messages))
                except Exception as ex:
                    logger.error('OpenaiChat: Upload image failed', ex, exc_info=True)
            model = cls.get_model(model)
            if conversation is None:
                conversation = Conversation(None, str(uuid.uuid4()), getattr(auth_result, 'cookies', {}).get('oai-did'))
            else:
                conversation = copy(conversation)
            if getattr(auth_result, 'cookies', {}).get('oai-did') != getattr(conversation, 'user_id', None):
                conversation = Conversation(None, str(uuid.uuid4()))
            if cls._api_key is None:
                auto_continue = False
            conversation.finish_reason = None
            sources = Sources([])
            while conversation.finish_reason is None:
                try:
                    async with session.post(
                        f'{cls.url}/backend-anon/sentinel/chat-requirements'
                        if cls._api_key is None else
                        f'{cls.url}/backend-api/sentinel/chat-requirements',
                        json={'p': None if not getattr(auth_result, 'proof_token', None) else get_requirements_token(getattr(auth_result, 'proof_token', None))},
                        headers=cls._headers
                    ) as response:
                        if response.status in (401, 403):
                            raise MissingAuthError(f'Response status: {response.status}')
                        else:
                            cls._update_request_args(auth_result, session)
                        await raise_for_status(response)
                        chat_requirements: dict = await response.json()
                        need_turnstile: bool = chat_requirements.get('turnstile', {}).get('required', False)
                        need_arkose: bool = chat_requirements.get('arkose', {}).get('required', False)
                        chat_token: str = chat_requirements.get('token')
                except Exception as ex:
                    logger.error('Error while getting chat requirements', ex, exc_info=True)
                    raise

                if 'proofofwork' in chat_requirements:
                    user_agent = getattr(auth_result, 'headers', {}).get('user-agent')
                    proof_token = getattr(auth_result, 'proof_token', None)
                    if proof_token is None:
                        auth_result.proof_token = get_config(user_agent)
                    proofofwork = generate_proof_token(
                        **chat_requirements['proofofwork'],
                        user_agent=user_agent,
                        proof_token=proof_token
                    )
                [debug.log(text) for text in (
                    #f"Arkose: {\'False\' if not need_arkose else auth_result.arkose_token[:12]+\'...\'}",
                    #f"Proofofwork: {\'False\' if proofofwork is None else proofofwork[:12]+\'...\'}",
                    #f"AccessToken: {\'False\' if cls._api_key is None else cls._api_key[:12]+\'...\'}",
                )]
                if action is None or action == 'variant' or action == 'continue' and conversation.message_id is None:
                    action = 'next'
                data: dict = {
                    'action': action,
                    'parent_message_id': conversation.message_id,
                    'model': model,
                    'timezone_offset_min': -60,
                    'timezone': 'Europe/Berlin',
                    'conversation_mode': {'kind': 'primary_assistant'},
                    'enable_message_followups': True,
                    'system_hints': ['search'] if web_search else None,
                    'supports_buffering': True,
                    'supported_encodings': ['v1'],
                    'client_contextual_info': {'is_dark_mode': False, 'time_since_loaded': random.randint(20, 500), 'page_height': 578, 'page_width': 1850, 'pixel_ratio': 1, 'screen_height': 1080, 'screen_width': 1920},
                    'paragen_cot_summary_display_override': 'allow'
                }
                if conversation.conversation_id is not None:
                    data['conversation_id'] = conversation.conversation_id
                    debug.log(f'OpenaiChat: Use conversation: {conversation.conversation_id}')
                if action != 'continue':
                    data['parent_message_id'] = getattr(conversation, 'parent_message_id', conversation.message_id)
                    conversation.parent_message_id = None
                    messages = messages if conversation.conversation_id is None else [{'role': 'user', 'content': get_last_user_message(messages)}]
                    data['messages'] = cls.create_messages(messages, image_requests, ['search'] if web_search else None)
                headers = {
                    **cls._headers,
                    'accept': 'text/event-stream',
                    'content-type': 'application/json',
                    'openai-sentinel-chat-requirements-token': chat_token,
                }
                if proofofwork is not None:
                    headers['openai-sentinel-proof-token'] = proofofwork
                if need_turnstile and getattr(auth_result, 'turnstile_token', None) is not None:
                    headers['openai-sentinel-turnstile-token'] = auth_result.turnstile_token
                try:
                    async with session.post(
                        f'{cls.url}/backend-anon/conversation'
                        if cls._api_key is None else
                        f'{cls.url}/backend-api/conversation',
                        json=data,
                        headers=headers
                    ) as response:
                        cls._update_request_args(auth_result, session)
                        if response.status in (401, 403, 429):
                            raise MissingAuthError('Access token is not valid')
                        await raise_for_status(response)
                        buffer: str = ''
                        async for line in response.iter_lines():
                            async for chunk in cls.iter_messages_line(session, auth_result, line, conversation, sources):
                                if isinstance(chunk, str):
                                    chunk = chunk.replace('\\ue203', '').replace('\\ue204', '').replace('\\ue206', '')
                                    buffer += chunk
                                    if buffer.find('\ue200') != -1:
                                        if buffer.find('\ue201') != -1:
                                            buffer = buffer.replace('\ue200', '').replace('\ue202', '\n').replace('\ue201', '')
                                            buffer = buffer.replace('navlist\n', '#### ')
                                            def replacer(match: re.Match) -> str:
                                                """
                                                Заменяет ссылки в тексте.

                                                Args:
                                                    match (re.Match): Объект Match с данными о совпадении.

                                                Returns:
                                                    str: Строка с замененной ссылкой.
                                                """
                                                link: Optional[str] = None
                                                if len(sources.list) > int(match.group(1)):
                                                    link = sources.list[int(match.group(1))]['url']
                                                    return f'[[{int(match.group(1))+1}]]({link})'
                                                return f' [{int(match.group(1))+1}]'
                                            buffer = re.sub(r'(?:cite\nturn0search|cite\nturn0news|turn0news)(\d+)', replacer, buffer)
                                        else:
                                            continue
                                    yield buffer
                                    buffer = ''
                                else:
                                    yield chunk
                            if conversation.finish_reason is not None:
                                break
                except Exception as ex:
                    logger.error('Error while getting conversation', ex, exc_info=True)
                    raise
                if sources.list:
                    yield sources
                if return_conversation:
                    yield conversation
                if auth_result.api_key is not None:
                    yield SynthesizeData(cls.__name__, {
                        'conversation_id': conversation.conversation_id,
                        'message_id': conversation.message_id,
                        'voice': 'maple',
                    })
                if auto_continue and conversation.finish_reason == 'max_tokens':
                    conversation.finish_reason = None
                    action = 'continue'
                    await asyncio.sleep(5)
                else:
                    break
            yield FinishReason(conversation.finish_reason)

    @classmethod
    async def iter_messages_line(cls, session: StreamSession, auth_result: AuthResult, line: bytes, fields: Conversation, sources: Sources) -> AsyncIterator:
        """
        Итерирует сообщения в строке.

        Args:
            session (StreamSession): Объект StreamSession для использования в запросах.
            auth_result (AuthResult): Результаты аутентификации.
            line (bytes): Строка с сообщением.
            fields (Conversation): Объект Conversation.
            sources (Sources): Объект Sources.

        Yields:
            AsyncIterator: Асинхронный итератор с сообщениями.
        """
        if not line.startswith(b'data: '):
            return
        elif line.startswith(b'data: [DONE]'):
            return
        try:
            line = json.loads(line[6:])
        except Exception as ex:
            logger.error('Error while loading JSON', ex, exc_info=True)
            return
        if not isinstance(line, dict):
            return
        if 'type' in line:
            if line['type'] == 'title_generation':
                yield TitleGeneration(line['title'])
        if 'v' in line:
            v = line.get('v')
            if isinstance(v, str) and fields.is_recipient:
                if 'p' not in line or line.get('p') == '/message/content/parts/0':
                    yield Reasoning(token=v) if fields.is_thinking else v
            elif isinstance(v, list):
                for m in v:
                    if m.get('p') == '/message/content/parts/0' and fields.is_recipient:
                        yield m.get('v')
                    elif m.get('p') == '/message/metadata/search_result_groups':
                        for entry in [p.get('entries') for p in m.get('v')]:
                            for link in entry:
                                sources.add_source(link)
                    elif re.match(r'^/message/metadata/content_references/\d+$', m.get('p')):# type: ignore
                        sources.add_source(m.get('v'))
                    elif m.get('p') == '/message/metadata/finished_text':
                        fields.is_thinking = False
                        yield Reasoning(status=m.get('v'))
                    elif m.get('p') == '/message/metadata':
                        fields.finish_reason = m.get('v', {}).get('finish_details', {}).get('type')
                        break
            elif isinstance(v, dict):
                if fields.conversation_id is None:
                    fields.conversation_id = v.get('conversation_id')
                    debug.log(f'OpenaiChat: New conversation: {fields.conversation_id}')
                m = v.get('message', {})
                fields.is_recipient = m.get('recipient', 'all') == 'all'
                if fields.is_recipient:
                    c = m.get('content', {})
                    if c.get('content_type') == 'text' and m.get('author', {}).get('role') == 'tool' and 'initial_text' in m.get('metadata', {}):
                        fields.is_thinking = True
                        yield Reasoning(status=m.get('metadata', {}).get('initial_text'))
                    if c.get('content_type') == 'multimodal_text':
                        generated_images: list[asyncio.Task[Optional[ImageResponse]]] = []
                        for element in c.get('parts'):
                            if isinstance(element, dict) and element.get('content_type') == 'image_asset_pointer':
                                image: asyncio.Task[Optional[ImageResponse]] = asyncio.ensure_future(cls.get_generated_image(session, auth_result, element))
                                generated_images.append(image)
                        for image_response in await asyncio.gather(*generated_images):
                            if image_response is not None:
                                yield image_response
                    if m.get('author', {}).get('role') == 'assistant':
                        if fields.parent_message_id is None:
                            fields.parent_message_id = v.get('message', {}).get('id')
                        fields.message_id = v.get('message', {}).get('id')
            return
        if 'error' in line and line.get('error'):
            raise RuntimeError(line.get('error'))

    @classmethod
    async def synthesize(cls, params: dict) -> AsyncIterator[bytes]:
        """
        Синтезирует данные.

        Args:
            params (dict): Параметры для синтеза.

        Yields:
            AsyncIterator[bytes]: Асинхронный итератор с байтами.
        """
        async for _ in cls.login():
            pass
        async with StreamSession(
            impersonate='chrome',
            timeout=0
        ) as session:
            try:
                async with session.get(
                    f'{cls.url}/backend-api/synthesize',
                    params=params,
                    headers=cls._headers
                ) as response:
                    await raise_for_status(response)
                    async for chunk in response.iter_content():
                        yield chunk
            except Exception as ex:
                logger.error('Error while synthesizing', ex, exc_info=True)
                raise

    @classmethod
    async def login(