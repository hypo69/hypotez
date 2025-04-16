### **Анализ кода модуля `Microsoft_Phi_4.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/Microsoft_Phi_4.py

Модуль для работы с моделью Microsoft Phi-4 Multimodal через Hugging Face Space.
===========================================================================

Модуль содержит класс `Microsoft_Phi_4`, который позволяет взаимодействовать с моделью Microsoft Phi-4 Multimodal,
размещенной на Hugging Face Space, для генерации текста и обработки изображений.

Пример использования
----------------------

```python
# Пример использования требует дополнительных компонентов и настройки.
# В данном контексте представлен только для демонстрации структуры.
# >>> provider = Microsoft_Phi_4()
# >>> messages = [{"role": "user", "content": "Hello, Phi-4!"}]
# >>> async for response in provider.create_async_generator(model="phi-4-multimodal", messages=messages):
# ...     print(response)
```

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная обработка запросов.
    - Поддержка потоковой передачи данных.
    - Использование `FormData` для отправки изображений.
    - Обработка ошибок и логирование.
- **Минусы**:
    - Использование устаревшего `Union`.
    - Отсутствие подробных комментариев и документации для некоторых методов и параметров.
    - Смешанный стиль кода (использование `getattr` вместо прямого доступа к атрибутам).
    - Отсутствие обработки исключений при загрузке изображений.
    - Дублирование `raise_for_status`

#### **Рекомендации по улучшению**:

1.  **Заменить `Union` на `|`**:
    -   В аннотациях типов использовать `|` вместо `Union`.
2.  **Добавить комментарии и документацию**:
    -   Добавить подробные docstring для всех методов и классов.
    -   Описать назначение каждого параметра и возвращаемого значения.
    -   Включить примеры использования, где это возможно.
3.  **Улучшить обработку исключений**:
    -   Добавить обработку исключений при загрузке изображений.
    -   Использовать `logger.error` для логирования ошибок с `exc_info=True`.
4.  **Улучшить читаемость кода**:
    -   Использовать более понятные имена переменных.
    -   Избегать использования `getattr` там, где можно использовать прямой доступ к атрибутам.
5.  **Избегать дублирования кода**:
    -   Вынести повторяющиеся блоки кода в отдельные функции.
6.  **Использовать `j_loads`**:
    -   Для чтения JSON использовать `j_loads`.
7. **Проверять все переменные на None**:
    - В коде есть места, где значения берутся из `conversation` через `getattr`, но не проверяются на `None`.
8. **Документировать все внутренние функции**
9. **Заменить `e` на `ex` в обработке исключений**

#### **Оптимизированный код**:

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
from ...errors import ResponseError
from ... import debug
from src.logger import logger
from .DeepseekAI_JanusPro7b import get_zerogpu_token


class Microsoft_Phi_4(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Модуль для работы с моделью Microsoft Phi-4 Multimodal через Hugging Face Space.
    ===========================================================================

    Класс `Microsoft_Phi_4` позволяет взаимодействовать с моделью Microsoft Phi-4 Multimodal,
    размещенной на Hugging Face Space, для генерации текста и обработки изображений.

    Args:
        label (str): Метка провайдера.
        space (str): Название пространства на Hugging Face.
        url (str): URL пространства.
        api_url (str): URL API для взаимодействия.
        referer (str): Referer для HTTP-запросов.
        working (bool): Флаг, указывающий, работает ли провайдер.
        supports_stream (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
        supports_system_message (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
        supports_message_history (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
        default_model (str): Модель по умолчанию.
        default_vision_model (str): Модель для обработки изображений по умолчанию.
        model_aliases (dict): Алиасы моделей.
        vision_models (list): Список моделей для обработки изображений.
        models (list): Список поддерживаемых моделей.

    Example:
        >>> provider = Microsoft_Phi_4()
        >>> messages = [{"role": "user", "content": "Hello, Phi-4!"}]
        >>> async for response in provider.create_async_generator(model="phi-4-multimodal", messages=messages):
        ...     print(response)
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
    model_aliases: dict = {'phi-4': default_vision_model}
    vision_models: List[str] = list(model_aliases.keys())
    models: List[str] = vision_models

    @classmethod
    async def _run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: Optional[list] = None) -> StreamResponse:
        """
        Выполняет HTTP-запрос к API.

        Args:
            method (str): HTTP-метод ('predict', 'post', 'get').
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект, содержащий информацию о текущем диалоге.
            media (Optional[list], optional): Список медиафайлов для отправки. Defaults to None.

        Returns:
            StreamResponse: Ответ от API.

        Raises:
            Exception: В случае ошибки при выполнении запроса.
        """
        headers: dict = {
            'content-type': 'application/json',
            'x-zerogpu-token': conversation.zerogpu_token,
            'x-zerogpu-uuid': conversation.zerogpu_uuid,
            'referer': cls.referer,
        }
        headers = {k: v for k, v in headers.items() if v is not None} #  Удаляет None значения из headers
        api_url: str = f'{cls.api_url}/gradio_api/run/predict' #  Определяет URL для запроса в зависимости от method
        json_data: dict = { #  Формирует данные для отправки в запросе
                    "data":[\
                        [],\
                        {\
                            "text": prompt,\
                            "files": media,\
                        },\
                        None\
                    ],\
                    "event_data": None,\
                    "fn_index": 10,\
                    "trigger_id": 8,\
                    "session_hash": conversation.session_hash\
                }
        queue_join_url: str = f'{cls.api_url}/gradio_api/queue/join?__theme=light'
        queue_data_url: str = f"{cls.api_url}/gradio_api/queue/data?session_hash={conversation.session_hash}"
        try:
            if method == 'predict':
                response: StreamResponse = await session.post(api_url, headers=headers, json=json_data)
                return response

            if method == 'post':
                post_data: dict = {\
                        "data": [[\
                                {\
                                "role": "user",\
                                "content": prompt,\
                                }\
                            ]] + [[\
                                {\
                                    "role": "user",\
                                    "content": {"file": image}\
                                } for image in media\
                            ]],\
                        "event_data": None,\
                        "fn_index": 11,\
                        "trigger_id": 8,\
                        "session_hash": conversation.session_hash\
                    }
                response: StreamResponse = await session.post(queue_join_url, headers=headers, json=post_data)
                return response

            if method == 'get':
                headers = {\
                    "accept": "text/event-stream",\
                    "content-type": "application/json",\
                    "referer": cls.referer,\
                }
                response: StreamResponse = await session.get(queue_data_url, headers=headers)
                return response
            raise ValueError(f'Invalid method: {method}')
        except Exception as ex:
            logger.error('Error while processing request', ex, exc_info=True)
            raise

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        media: Optional[MediaListType] = None,
        prompt: Optional[str] = None,
        proxy: Optional[str] = None,
        cookies: Optional[Cookies] = None,
        api_key: Optional[str] = None,
        zerogpu_uuid: str = '[object Object]',
        return_conversation: bool = False,
        conversation: Optional[JsonConversation] = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            media (Optional[MediaListType], optional): Список медиафайлов. Defaults to None.
            prompt (Optional[str], optional): Текст запроса. Defaults to None.
            proxy (Optional[str], optional): Прокси-сервер. Defaults to None.
            cookies (Optional[Cookies], optional): Куки для отправки. Defaults to None.
            api_key (Optional[str], optional): API ключ. Defaults to None.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. Defaults to '[object Object]'.
            return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект диалога. Defaults to False.
            conversation (Optional[JsonConversation], optional): Объект диалога. Defaults to None.

        Yields:
            str: Ответ от модели.

        Raises:
            ResponseError: Если в ответе от API содержится ошибка.
            Exception: В случае других ошибок.
        """
        prompt: str = format_prompt(messages) if prompt is None and conversation is None else prompt #  Форматирует prompt, если он не передан
        prompt: str = format_image_prompt(messages, prompt) #  Форматирует prompt для изображений

        session_hash: str = uuid.uuid4().hex if conversation is None else getattr(conversation, "session_hash", uuid.uuid4().hex) #  Генерирует session_hash, если он не передан
        async with StreamSession(proxy=proxy, impersonate='chrome') as session: #  Создает асинхронную сессию
            if api_key is None: #  Получает токен ZeroGPU, если api_key не передан
                zerogpu_uuid, api_key = await get_zerogpu_token(cls.space, session, conversation, cookies)
            if conversation is None or not hasattr(conversation, "session_hash"): #  Создает объект диалога, если он не передан
                conversation = JsonConversation(session_hash=session_hash, zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid)
            else:
                conversation.zerogpu_token = api_key
            if return_conversation: #  Возвращает объект диалога, если return_conversation = True
                yield conversation

            media_files: list = []
            mime_types: list = []
            if media is not None: #  Загружает медиафайлы на сервер
                data: FormData = FormData()
                mime_types = [None for _ in range(len(media))] #  Создает список mime_types
                for i in range(len(media)):
                    mime_types[i] = is_data_an_audio(media[i][0], media[i][1]) #  Определяет mime_type для аудио
                    media[i] = (to_bytes(media[i][0]), media[i][1]) #  Преобразует медиафайлы в байты
                    mime_types[i] = is_accepted_format(media[i][0]) if mime_types[i] is None else mime_types[i] #  Определяет mime_type для изображений
                for image, image_name in media:
                    data.add_field(f'files', to_bytes(image), filename=image_name) #  Добавляет медиафайлы в FormData
                try:
                    upload_url: str = f'{cls.api_url}/gradio_api/upload' #  Определяет URL для загрузки медиафайлов
                    params: dict = {'upload_id': session_hash} #  Определяет параметры запроса
                    async with session.post(upload_url, params=params, data=data) as response: #  Загружает медиафайлы
                        response.raise_for_status()
                        image_files: list = await response.json() #  Получает список загруженных файлов
                except Exception as ex:
                    logger.error('Error while uploading images', ex, exc_info=True) #  Логирует ошибку
                    raise
                media_files = [{\
                    "path": image_file,\
                    "url": f"{cls.api_url}/gradio_api/file={image_file}",\
                    "orig_name": media[i][1],\
                    "size": len(media[i][0]),\
                    "mime_type": mime_types[i],\
                    "meta": {\
                        "_type": "gradio.FileData"\
                    }\
                } for i, image_file in enumerate(image_files)] #  Формирует список медиафайлов
            
            try:
                async with cls._run('predict', session, prompt, conversation, media_files) as response:
                    response.raise_for_status()

                async with cls._run('post', session, prompt, conversation, media_files) as response:
                    response.raise_for_status()

                async with cls._run('get', session, prompt, conversation) as response:
                    response: StreamResponse = response
                    async for line in response.iter_lines():
                        if line.startswith(b'data: '):
                            try:
                                json_data: dict = json.loads(line[6:]) #  Загружает JSON из строки
                                if json_data.get('msg') == 'process_completed':
                                    output_data: dict = json_data.get('output')
                                    if output_data and 'error' in output_data:
                                        raise ResponseError(output_data['error'])
                                    if output_data and 'data' in output_data:
                                        yield output_data['data'][0][-1]["content"]
                                    break

                            except json.JSONDecodeError as ex:
                                debug.log('Could not parse JSON:', line.decode(errors='replace'))
                                logger.error('Could not parse JSON:', ex, exc_info=True)

            except Exception as ex:
                logger.error('Error while processing stream', ex, exc_info=True) #  Логирует ошибку
                raise