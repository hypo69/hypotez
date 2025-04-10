### **Анализ кода модуля `HuggingChat.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/hf/HuggingChat.py

Модуль `HuggingChat.py` предоставляет реализацию асинхронного провайдера для взаимодействия с Hugging Face Chat. Он включает в себя функциональность для аутентификации, создания бесед, обмена сообщениями и обработки ответов, включая текст, изображения и результаты веб-поиска.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Асинхронная реализация для неблокирующего взаимодействия.
  - Поддержка потоковой передачи ответов.
  - Обработка различных типов контента, включая текст и изображения.
  - Интеграция с `curl_cffi` для повышения производительности.
- **Минусы**:
  - Не всегда последовательное использование аннотаций типов.
  - Обработка ошибок могла бы быть более детализированной.
  - Отсутствуют docstring для некоторых методов и классов.

**Рекомендации по улучшению**:

1. **Добавить docstring**: Добавить подробные docstring для всех классов и методов, включая описание параметров, возвращаемых значений и возможных исключений.
2. **Аннотации типов**: Убедиться, что все переменные и параметры функций аннотированы типами.
3. **Логирование**: Добавить логирование для отладки и мониторинга, особенно в блоках обработки исключений.
4. **Обработка ошибок**: Улучшить обработку ошибок, чтобы предоставлять более конкретные сообщения об ошибках и рекомендации.
5. **Удалить неиспользуемые импорты**: Удалить неиспользуемые импорты, чтобы уменьшить зависимость и улучшить читаемость кода.
6. **Форматирование**: Привести код в соответствие со стандартами PEP8.
7. **Использовать `j_loads` или `j_loads_ns`**: Для чтения JSON конфигурационных файлов.

**Оптимизированный код**:

```python
from __future__ import annotations

import json
import re
import os
import requests
import base64
import uuid
from typing import AsyncIterator, Optional, List

try:
    from curl_cffi.requests import Session
    from curl_cffi import CurlMime

    has_curl_cffi = True
except ImportError:
    has_curl_cffi = False

from ..base_provider import ProviderModelMixin, AsyncAuthedProvider, AuthResult
from ..helper import format_prompt, format_image_prompt, get_last_user_message
from ...typing import AsyncResult, Messages, Cookies, MediaListType
from ...errors import MissingRequirementsError, MissingAuthError, ResponseError
from ...image import to_bytes
from ...requests import get_args_from_nodriver, DEFAULT_HEADERS
from ...requests.raise_for_status import raise_for_status
from ...providers.response import (
    JsonConversation,
    ImageResponse,
    Sources,
    TitleGeneration,
    Reasoning,
    RequestLogin,
    FinishReason,
)
from ...cookies import get_cookies
from ...tools.media import merge_media
from .models import (
    default_model,
    default_vision_model,
    fallback_models,
    image_models,
    model_aliases,
)
from ... import debug
from src.logger import logger


class Conversation(JsonConversation):
    """
    Класс для управления состоянием беседы с HuggingChat.

    Args:
        models (dict): Словарь, содержащий информацию о моделях, используемых в беседе.
    """

    def __init__(self, models: dict):
        """
        Инициализирует объект Conversation.

        Args:
            models (dict): Словарь, содержащий информацию о моделях, используемых в беседе.
        """
        self.models: dict = models


class HuggingChat(AsyncAuthedProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с Hugging Face Chat.
    """

    domain: str = "huggingface.co"
    origin: str = f"https://{domain}"
    url: str = f"{origin}/chat"

    working: bool = True
    use_nodriver: bool = True
    supports_stream: bool = True
    needs_auth: bool = True
    default_model: str = default_model
    default_vision_model: str = default_vision_model
    model_aliases: dict = model_aliases
    image_models: list[str] = image_models
    text_models: list[str] = fallback_models
    models: list[str] = []
    vision_models: list[str] = []

    @classmethod
    def get_models(cls) -> list[str]:
        """
        Получает список доступных моделей из Hugging Face Chat.

        Returns:
            list[str]: Список идентификаторов моделей.

        Raises:
            Exception: Если не удается получить список моделей.
        """
        if not cls.models:
            try:
                text = requests.get(cls.url).text
                text = re.search(r"models:(\\[.+?\\]),oldModels:", text).group(1)
                text = re.sub(r",parameters:{[^}]+?}", "", text)
                text = text.replace("void 0", "null")

                def add_quotation_mark(match):
                    return f'{match.group(1)}"{match.group(2)}":'

                text = re.sub(r"([{,])([A-Za-z0-9_]+?):", add_quotation_mark, text)
                models = json.loads(text)
                cls.text_models = [model["id"] for model in models]
                cls.models = cls.text_models + cls.image_models
                cls.vision_models = [
                    model["id"] for model in models if model["multimodal"]
                ]
            except Exception as ex:
                logger.error(
                    f"{cls.__name__}: Error reading models: {type(ex).__name__}: {ex}",
                    exc_info=True,
                )  # Используем logger.error для логирования ошибок
                cls.models = [*fallback_models]
        return cls.models

    @classmethod
    async def on_auth_async(
        cls, cookies: Cookies = None, proxy: str = None, **kwargs
    ) -> AsyncIterator:
        """
        Асинхронно аутентифицирует пользователя.

        Args:
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию None.
            proxy (str, optional): Proxy для использования при аутентификации. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Yields:
            AuthResult: Результат аутентификации.
            RequestLogin: Запрос на ввод данных для входа.

        Raises:
            MissingAuthError: Если не удалось аутентифицироваться.
        """
        if cookies is None:
            cookies = get_cookies(cls.domain, single_browser=True)
        if "hf-chat" in cookies:
            yield AuthResult(
                cookies=cookies, impersonate="chrome", headers=DEFAULT_HEADERS
            )
            return
        if cls.needs_auth:
            login_url = os.environ.get("G4F_LOGIN_URL") or ""
            yield RequestLogin(cls.__name__, login_url)
            yield AuthResult(
                **(
                    await get_args_from_nodriver(
                        cls.url, proxy=proxy, wait_for='form[action$="/logout"]'
                    )
                )
            )
        else:
            yield AuthResult(
                cookies={"hf-chat": str(uuid.uuid4())}  # Generate a session ID
            )

    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        prompt: str = None,
        media: MediaListType = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        web_search: bool = False,
        **kwargs,
    ) -> AsyncResult:
        """
        Создает аутентифицированный запрос к Hugging Face Chat.

        Args:
            model (str): Идентификатор модели для использования.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результат аутентификации.
            prompt (str, optional): Дополнительный текст-подсказка. По умолчанию None.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию None.
            return_conversation (bool, optional): Флаг, указывающий, следует ли возвращать объект Conversation. По умолчанию False.
            conversation (Conversation, optional): Объект Conversation для продолжения беседы. По умолчанию None.
            web_search (bool, optional): Флаг, указывающий, следует ли выполнять веб-поиск. По умолчанию False.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Части ответа от Hugging Face Chat.
            ImageResponse: Ответ с изображением.
            Sources: Источники веб-поиска.
            TitleGeneration: Сгенерированный заголовок.
            Reasoning: Рассуждения модели.
            FinishReason: Причина завершения.

        Raises:
            MissingRequirementsError: Если не установлен пакет `curl_cffi`.
            MissingAuthError: Если не удалось аутентифицироваться.
            ResponseError: Если получен неожиданный статус ответа.
            RuntimeError: Если не удалось обработать ответ от сервера.
        """
        if not has_curl_cffi:
            raise MissingRequirementsError(
                'Install "curl_cffi" package | pip install -U curl_cffi'
            )
        if not model and media is not None:
            model = cls.default_vision_model
        model = cls.get_model(model)

        session = Session(**auth_result.get_dict())

        if conversation is None or not hasattr(conversation, "models"):
            conversation = Conversation({})

        if model not in conversation.models:
            conversationId = cls.create_conversation(session, model)
            debug.log(f"Conversation created: {json.dumps(conversationId[8:] + '...')}")
            messageId = cls.fetch_message_id(session, conversationId)
            conversation.models[model] = {
                "conversationId": conversationId,
                "messageId": messageId,
            }
            if return_conversation:
                yield conversation
            inputs = format_prompt(messages)
        else:
            conversationId = conversation.models[model]["conversationId"]
            conversation.models[model]["messageId"] = cls.fetch_message_id(
                session, conversationId
            )
            inputs = get_last_user_message(messages)

        settings = {
            "inputs": inputs,
            "id": conversation.models[model]["messageId"],
            "is_retry": False,
            "is_continue": False,
            "web_search": web_search,
            "tools": ["000000000000000000000001"] if model in cls.image_models else [],
        }

        headers = {
            "accept": "*/*",
            "origin": cls.origin,
            "referer": f"{cls.url}/conversation/{conversationId}",
        }
        data = CurlMime()
        data.addpart("data", data=json.dumps(settings, separators=(",", ":")))
        for image, filename in merge_media(media, messages):
            data.addpart(
                "files",
                filename=f"base64;{filename}",
                data=base64.b64encode(to_bytes(image)),
            )

        response = session.post(
            f"{cls.url}/conversation/{conversationId}",
            headers=headers,
            multipart=data,
            stream=True,
        )
        raise_for_status(response)

        sources = None
        try:
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    line = json.loads(line)
                except json.JSONDecodeError as ex:
                    logger.error(f"Failed to decode JSON: {line}, error: {ex}", exc_info=True)
                    continue
                if "type" not in line:
                    raise RuntimeError(f"Response: {line}")
                elif line["type"] == "stream":
                    yield line["token"].replace("\\u0000", "")
                elif line["type"] == "finalAnswer":
                    if sources is not None:
                        yield sources
                    yield FinishReason("stop")
                    break
                elif line["type"] == "file":
                    url = f"{cls.url}/conversation/{conversationId}/output/{line['sha']}"
                    yield ImageResponse(
                        url,
                        format_image_prompt(messages, prompt),
                        options={"cookies": auth_result.cookies},
                    )
                elif line["type"] == "webSearch" and "sources" in line:
                    sources = Sources(line["sources"])
                elif line["type"] == "title":
                    yield TitleGeneration(line["title"])
                elif line["type"] == "reasoning":
                    yield Reasoning(line.get("token"), status=line.get("status"))
        except Exception as ex:
            logger.error(f"Error processing response: {ex}", exc_info=True)
            raise

    @classmethod
    def create_conversation(cls, session: Session, model: str) -> str:
        """
        Создает новую беседу с Hugging Face Chat.

        Args:
            session (Session): Сессия для выполнения запросов.
            model (str): Идентификатор модели для использования.

        Returns:
            str: Идентификатор созданной беседы.

        Raises:
            MissingAuthError: Если не удалось аутентифицироваться.
            ResponseError: Если получен неожиданный статус ответа.
        """
        if model in cls.image_models:
            model = cls.default_model
        json_data = {"model": model}
        response = session.post(f"{cls.url}/conversation", json=json_data)
        if response.status_code == 401:
            raise MissingAuthError(response.text)
        if response.status_code == 400:
            raise ResponseError(f"{response.text}: Model: {model}")
        raise_for_status(response)
        return response.json().get("conversationId")

    @classmethod
    def fetch_message_id(cls, session: Session, conversation_id: str) -> str:
        """
        Извлекает идентификатор последнего сообщения в беседе.

        Args:
            session (Session): Сессия для выполнения запросов.
            conversation_id (str): Идентификатор беседы.

        Returns:
            str: Идентификатор последнего сообщения.

        Raises:
            RuntimeError: Если не удалось извлечь идентификатор сообщения.
        """
        # Get the data response and parse it properly
        response = session.get(
            f"{cls.url}/conversation/{conversation_id}/__data.json?x-sveltekit-invalidated=11"
        )
        raise_for_status(response)

        # Split the response content by newlines and parse each line as JSON
        try:
            json_data = None
            for line in response.text.split("\\n"):
                if line.strip():
                    try:
                        parsed = json.loads(line)
                        if isinstance(parsed, dict) and "nodes" in parsed:
                            json_data = parsed
                            break
                    except json.JSONDecodeError:
                        continue

            if not json_data:
                raise RuntimeError("Failed to parse response data")

            if json_data["nodes"][-1]["type"] == "error":
                if json_data["nodes"][-1]["status"] == 403:
                    raise MissingAuthError(
                        json_data["nodes"][-1]["error"]["message"]
                    )
                raise ResponseError(json.dumps(json_data["nodes"][-1]))

            data = json_data["nodes"][1]["data"]
            keys = data[data[0]["messages"]]
            message_keys = data[keys[-1]]
            return data[message_keys["id"]]

        except (KeyError, IndexError, TypeError) as ex:
            raise RuntimeError(f"Failed to extract message ID: {str(ex)}")