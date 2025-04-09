### **Анализ кода модуля `DeepseekAI_JanusPro7b.py`**

**Файл:** `hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/DeepseekAI_JanusPro7b.py`

Модуль предоставляет класс `DeepseekAI_JanusPro7b`, который является асинхронным генератором для взаимодействия с моделью DeepseekAI Janus-Pro-7B через Hugging Face Spaces.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация для неблокирующего взаимодействия.
    - Поддержка стриминга ответов.
    - Обработка текстовых и графических запросов.
    - Использование `JsonConversation` для управления состоянием беседы.
- **Минусы**:
    - Недостаточное количество комментариев и документации.
    - Смешение ответственности в методе `create_async_generator` (обработка токенов, загрузка медиа, запуск запросов).
    - Использование `getattr` вместо более безопасных способов проверки наличия атрибутов.
    - Дублирование кода при обработке ошибок (`if json_data['output']['error'] and "AttributeError" in json_data['output']['error']`).

**Рекомендации по улучшению:**

1.  **Добавить документацию модуля**:

    ```python
    """
    Модуль для взаимодействия с моделью DeepseekAI Janus-Pro-7B через Hugging Face Spaces.
    ==============================================================================

    Этот модуль предоставляет класс `DeepseekAI_JanusPro7b`, который позволяет отправлять запросы
    к модели DeepseekAI Janus-Pro-7B, размещенной на Hugging Face Spaces, и получать ответы в асинхронном режиме.

    Поддерживает текстовые и графические запросы, стриминг ответов и управление состоянием беседы.

    Пример использования:
    ----------------------
    >>> provider = DeepseekAI_JanusPro7b()
    >>> async for message in provider.create_async_generator(model="janus-pro-7b", messages=[{"role": "user", "content": "Hello"}]):
    ...     print(message)
    """
    ```

2.  **Добавить docstring к классу `DeepseekAI_JanusPro7b`**:

    ```python
    class DeepseekAI_JanusPro7b(AsyncGeneratorProvider, ProviderModelMixin):
        """
        Провайдер для взаимодействия с моделью DeepseekAI Janus-Pro-7B через Hugging Face Spaces.

        Поддерживает текстовые и графические запросы, стриминг ответов и управление состоянием беседы.
        """
    ```

3.  **Добавить docstring к методу `run`**:

    ```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
        """
        Выполняет HTTP-запрос к API DeepseekAI Janus-Pro-7B.

        Args:
            method (str): HTTP-метод ("post" или "image").
            session (StreamSession): Асинхронная сессия для выполнения запроса.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект, содержащий информацию о текущем диалоге.
            image (dict, optional): Информация об изображении. По умолчанию None.
            seed (int): Зерно для генерации случайных чисел.

        Returns:
            aiohttp.ClientResponse: Объект ответа от сервера.
        """
    ```

4.  **Добавить docstring к методу `create_async_generator`**:

    ```python
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
        zerogpu_uuid: str = "[object Object]",
        return_conversation: bool = False,
        conversation: JsonConversation = None,
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью DeepseekAI Janus-Pro-7B.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию None.
            prompt (str, optional): Текст запроса. По умолчанию None.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
            cookies (Cookies, optional): Cookie для отправки. По умолчанию None.
            api_key (str, optional): API-ключ. По умолчанию None.
            zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
            return_conversation (bool, optional): Флаг возврата объекта conversation. По умолчанию False.
            conversation (JsonConversation, optional): Объект conversation. По умолчанию None.
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию None.

        Yields:
            AsyncResult: Асинхронный результат ответа от сервера.
        """
    ```

5.  **Добавить docstring к функции `get_zerogpu_token`**:

    ```python
    async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None):
        """
        Получает zerogpu токен для доступа к Hugging Face Spaces.

        Args:
            space (str): Название пространства.
            session (StreamSession): Асинхронная сессия для выполнения запроса.
            conversation (JsonConversation): Объект conversation.
            cookies (Cookies, optional): Cookie для отправки. По умолчанию None.

        Returns:
            tuple[str, str]: UUID и токен zerogpu.
        """
    ```

6.  **Улучшить обработку ошибок**:
    - Использовать `logger.error` для логирования ошибок.
    - Добавить более конкретные исключения.

7.  **Разделить метод `create_async_generator` на несколько**:
    - Отделить логику получения токена и загрузки медиа в отдельные методы.

8.  **Использовать `if conversation and conversation.session_hash is not None:` вместо `getattr(conversation, "session_hash", uuid.uuid4().hex)`**

9.  **Добавить аннотации типов для всех переменных, где это возможно.**

**Оптимизированный код:**

```python
from __future__ import annotations

import json
import uuid
import re
import random
from datetime import datetime, timezone, timedelta
import urllib.parse

from ...typing import AsyncResult, Messages, Cookies, MediaListType
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt, format_image_prompt
from ...providers.response import JsonConversation, ImageResponse, Reasoning
from ...requests.aiohttp import StreamSession, StreamResponse, FormData
from ...requests.raise_for_status import raise_for_status
from ...image import to_bytes, is_accepted_format
from ...cookies import get_cookies
from ...errors import ResponseError
from ... import debug
from .raise_for_status import raise_for_status
from src.logger import logger  # Import logger

"""
Модуль для взаимодействия с моделью DeepseekAI Janus-Pro-7B через Hugging Face Spaces.
==============================================================================

Этот модуль предоставляет класс `DeepseekAI_JanusPro7b`, который позволяет отправлять запросы
к модели DeepseekAI Janus-Pro-7B, размещенной на Hugging Face Spaces, и получать ответы в асинхронном режиме.

Поддерживает текстовые и графические запросы, стриминг ответов и управление состоянием беседы.

Пример использования:
----------------------
>>> provider = DeepseekAI_JanusPro7b()
>>> async for message in provider.create_async_generator(model="janus-pro-7b", messages=[{"role": "user", "content": "Hello"}]):
...     print(message)
"""


class DeepseekAI_JanusPro7b(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с моделью DeepseekAI Janus-Pro-7B через Hugging Face Spaces.

    Поддерживает текстовые и графические запросы, стриминг ответов и управление состоянием беседы.
    """

    label: str = "DeepseekAI Janus-Pro-7B"
    space: str = "deepseek-ai/Janus-Pro-7B"
    url: str = f"https://huggingface.co/spaces/{space}"
    api_url: str = "https://deepseek-ai-janus-pro-7b.hf.space"
    referer: str = f"{api_url}?__theme=light"

    working: bool = True
    supports_stream: bool = True
    supports_system_message: bool = True
    supports_message_history: bool = True

    default_model: str = "janus-pro-7b"
    default_image_model: str = "janus-pro-7b-image"
    default_vision_model: str = default_model
    image_models: list[str] = [default_image_model]
    vision_models: list[str] = [default_vision_model]
    models: list[str] = vision_models + image_models

    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
        """
        Выполняет HTTP-запрос к API DeepseekAI Janus-Pro-7B.

        Args:
            method (str): HTTP-метод ("post" или "image").
            session (StreamSession): Асинхронная сессия для выполнения запроса.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект, содержащий информацию о текущем диалоге.
            image (dict, optional): Информация об изображении. По умолчанию None.
            seed (int): Зерно для генерации случайных чисел.

        Returns:
            aiohttp.ClientResponse: Объект ответа от сервера.
        """
        headers: dict[str, str] = {
            "content-type": "application/json",
            "x-zerogpu-token": conversation.zerogpu_token,
            "x-zerogpu-uuid": conversation.zerogpu_uuid,
            "referer": cls.referer,
        }
        if method == "post":
            return session.post(f"{cls.api_url}/gradio_api/queue/join?__theme=light", **{
                "headers": {k: v for k, v in headers.items() if v is not None},
                "json": {"data": [image, prompt, seed, 0.95, 0.1], "event_data": None, "fn_index": 2, "trigger_id": 10, "session_hash": conversation.session_hash},
            })
        elif method == "image":
            return session.post(f"{cls.api_url}/gradio_api/queue/join?__theme=light", **{
                "headers": {k: v for k, v in headers.items() if v is not None},
                "json": {"data": [prompt, seed, 5, 1], "event_data": None, "fn_index": 3, "trigger_id": 20, "session_hash": conversation.session_hash},
            })
        return session.get(f"{cls.api_url}/gradio_api/queue/data?session_hash={conversation.session_hash}", **{
            "headers": {
                "accept": "text/event-stream",
                "content-type": "application/json",
                "referer": cls.referer,
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
        zerogpu_uuid: str = "[object Object]",
        return_conversation: bool = False,
        conversation: JsonConversation = None,
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью DeepseekAI Janus-Pro-7B.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию None.
            prompt (str, optional): Текст запроса. По умолчанию None.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
            cookies (Cookies, optional): Cookie для отправки. По умолчанию None.
            api_key (str, optional): API-ключ. По умолчанию None.
            zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
            return_conversation (bool, optional): Флаг возврата объекта conversation. По умолчанию False.
            conversation (JsonConversation, optional): Объект conversation. По умолчанию None.
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию None.

        Yields:
            AsyncResult: Асинхронный результат ответа от сервера.
        """
        method: str = "post"
        if model == cls.default_image_model or prompt is not None:
            method = "image"
        prompt: str = format_prompt(messages) if prompt is None and conversation is None else prompt
        prompt: str = format_image_prompt(messages, prompt)
        if seed is None:
            seed: int = random.randint(1000, 999999)

        session_hash: str = uuid.uuid4().hex if conversation is None else conversation.session_hash if conversation.session_hash is not None else uuid.uuid4().hex
        async with StreamSession(proxy=proxy, impersonate="chrome") as session:
            if api_key is None:
                zerogpu_uuid, api_key = await get_zerogpu_token(cls.space, session, conversation, cookies)
            if conversation is None or not hasattr(conversation, "session_hash"):
                conversation: JsonConversation = JsonConversation(session_hash=session_hash, zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid)
            else:
                conversation.zerogpu_token: str = api_key
            if return_conversation:
                yield conversation

            if media is not None:
                data: FormData = FormData()
                for i in range(len(media)):
                    media[i]: tuple[bytes, str] = (to_bytes(media[i][0]), media[i][1])
                for image, image_name in media:
                    data.add_field(f"files", image, filename=image_name)
                try:
                    async with session.post(f"{cls.api_url}/gradio_api/upload", params={"upload_id": session_hash}, data=data) as response:
                        await raise_for_status(response)
                        image_files: list[str] = await response.json()
                except Exception as ex:
                    logger.error("Error while uploading media", ex, exc_info=True)
                    raise
                media_list: list[dict] = [{
                    "path": image_file,
                    "url": f"{cls.api_url}/gradio_api/file={image_file}",
                    "orig_name": media[i][1],
                    "size": len(media[i][0]),
                    "mime_type": is_accepted_format(media[i][0]),
                    "meta": {
                        "_type": "gradio.FileData"
                    }
                } for i, image_file in enumerate(image_files)]

            try:
                async with cls.run(method, session, prompt, conversation, None if media is None else media_list.pop(), seed) as response:
                    await raise_for_status(response)

                async with cls.run("get", session, prompt, conversation, None, seed) as response:
                    response: StreamResponse = response
                    counter: int = 3
                    async for line in response.iter_lines():
                        decoded_line: str = line.decode(errors="replace")
                        if decoded_line.startswith('data: '):
                            try:
                                json_data: dict = json.loads(decoded_line[6:])
                                if json_data.get('msg') == 'log':
                                    yield Reasoning(status=json_data["log"])

                                if json_data.get('msg') == 'progress':
                                    if 'progress_data' in json_data:
                                        if json_data['progress_data']:
                                            progress: dict = json_data['progress_data'][0]
                                            yield Reasoning(status=f"{progress['desc']} {progress['index']}/{progress['length']}")
                                        else:
                                            yield Reasoning(status=f"Generating")

                                elif json_data.get('msg') == 'heartbeat':
                                    yield Reasoning(status=f"Generating{''.join(['.' for i in range(counter)])}")
                                    counter += 1

                                elif json_data.get('msg') == 'process_completed':
                                    if 'output' in json_data and 'error' in json_data['output']:
                                        error_message: str = json_data['output']['error'].split(" <a ")[0]
                                        if "AttributeError" in error_message:
                                            error_message = "Missing images input"
                                        raise ResponseError(error_message)
                                    if 'output' in json_data and 'data' in json_data['output']:
                                        yield Reasoning(status="Finished")
                                        if "image" in json_data['output']['data'][0][0]:
                                            yield ImageResponse([image["image"]["url"] for image in json_data['output']['data'][0]], prompt)
                                        else:
                                            yield json_data['output']['data'][0]
                                        break

                            except json.JSONDecodeError as ex:
                                debug.log("Could not parse JSON:", decoded_line)
                                logger.error("Could not parse JSON", ex, exc_info=True)
            except Exception as ex:
                logger.error("Error while processing request", ex, exc_info=True)
                raise


async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None) -> tuple[str, str]:
    """
    Получает zerogpu токен для доступа к Hugging Face Spaces.

    Args:
        space (str): Название пространства.
        session (StreamSession): Асинхронная сессия для выполнения запроса.
        conversation (JsonConversation): Объект conversation.
        cookies (Cookies, optional): Cookie для отправки. По умолчанию None.

    Returns:
        tuple[str, str]: UUID и токен zerogpu.
    """
    zerogpu_uuid: str | None = None if conversation is None else getattr(conversation, "zerogpu_uuid", None)
    zerogpu_token: str = "[object Object]"

    cookies: Cookies = get_cookies("huggingface.co", raise_requirements_error=False) if cookies is None else cookies
    if zerogpu_uuid is None:
        try:
            async with session.get(f"https://huggingface.co/spaces/{space}", cookies=cookies) as response:
                text: str = await response.text()
                match: re.Match | None = re.search(r"&quot;token&quot;:&quot;([^&]+?)&quot;", text)
                if match:
                    zerogpu_token: str = match.group(1)
                match = re.search(r"&quot;sessionUuid&quot;:&quot;([^&]+?)&quot;", text)
                if match:
                    zerogpu_uuid: str = match.group(1)
        except Exception as ex:
            logger.error("Error while fetching zerogpu token", ex, exc_info=True)
            raise

    if cookies:
        # Get current UTC time + 10 minutes
        dt: str = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(timespec='milliseconds')
        encoded_dt: str = urllib.parse.quote(dt)
        try:
            async with session.get(f"https://huggingface.co/api/spaces/{space}/jwt?expiration={encoded_dt}&include_pro_status=true", cookies=cookies) as response:
                response_data: dict = await response.json()
                if "token" in response_data:
                    zerogpu_token: str = response_data["token"]
        except Exception as ex:
            logger.error("Error while fetching JWT token", ex, exc_info=True)
            raise

    return zerogpu_uuid, zerogpu_token