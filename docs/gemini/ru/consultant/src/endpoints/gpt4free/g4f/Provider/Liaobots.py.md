### **Анализ кода модуля `Liaobots.py`**

#### **1. Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование асинхронных операций для неблокирующего выполнения.
    - Поддержка истории сообщений и системных сообщений.
    - Наличие модели fallback.
- **Минусы**:
    - Повторяющийся код в блоках `try` и `except`.
    - Отсутствие обработки исключений при инициализации `_auth_code`.
    - Жестко заданные значения `authcode` в теле метода.
    - Не все переменные аннотированы типами.
    - Не хватает docstring для класса.
    - Дублирование кода, нелогичная обработка ошибок.

#### **2. Рекомендации по улучшению:**

- Добавление docstring для класса `Liaobots` с описанием его назначения, основных атрибутов и методов.
- Удаление дублирующегося кода из блоков `try` и `except` путем вынесения общего кода в отдельную функцию.
- Обработка исключений при инициализации `_auth_code` для обеспечения стабильной работы.
- Использовать `logger` из модуля `src.logger` для логирования ошибок и отладочной информации.
- Избавиться от хардкода `authcode`.
- Добавить аннотации типов для всех переменных и параметров функций.

#### **3. Оптимизированный код:**

```python
"""
Модуль для работы с Liaobots API
===================================

Модуль содержит класс :class:`Liaobots`, который используется для взаимодействия с Liaobots API для
генерации текста на основе предоставленных сообщений.

Пример использования
----------------------

>>> provider = Liaobots()
>>> #messages = [...]
>>> #async for message in provider.create_async_generator(model, messages):
>>> #    print(message)
"""
from __future__ import annotations

import uuid
import json
from typing import AsyncGenerator, Dict, List, Optional
from aiohttp import ClientSession, BaseConnector, ClientResponse

from src.logger import logger  # Импортируем logger
from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import get_connector
from ..requests import raise_for_status

models: Dict[str, Dict[str, str | int]] = {
    "claude-3-5-sonnet-20241022": {
        "id": "claude-3-5-sonnet-20241022",
        "name": "Claude-3.5-Sonnet-V2",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "claude-3-5-sonnet-20241022-t": {
        "id": "claude-3-5-sonnet-20241022-t",
        "name": "Claude-3.5-Sonnet-V2-T",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "claude-3-7-sonnet-20250219": {
        "id": "claude-3-7-sonnet-20250219",
        "name": "Claude-3.7-Sonnet",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "claude-3-7-sonnet-20250219-t": {
        "id": "claude-3-7-sonnet-20250219-t",
        "name": "Claude-3.7-Sonnet-T",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "claude-3-7-sonnet-20250219-thinking": {
        "id": "claude-3-7-sonnet-20250219-thinking",
        "name": "Claude-3.7-Sonnet-Thinking",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "claude-3-opus-20240229": {
        "id": "claude-3-opus-20240229",
        "name": "Claude-3-Opus",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "claude-3-sonnet-20240229": {
        "id": "claude-3-sonnet-20240229",
        "name": "Claude-3-Sonnet",
        "model": "Claude",
        "provider": "Anthropic",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "deepseek-r1": {
        "id": "deepseek-r1",
        "name": "DeepSeek-R1",
        "model": "DeepSeek-R1",
        "provider": "DeepSeek",
        "maxLength": 400000,
        "tokenLimit": 100000,
        "context": "128K",
    },
    "deepseek-r1-distill-llama-70b": {
        "id": "deepseek-r1-distill-llama-70b",
        "name": "DeepSeek-R1-70B",
        "model": "DeepSeek-R1-70B",
        "provider": "DeepSeek",
        "maxLength": 400000,
        "tokenLimit": 100000,
        "context": "128K",
    },
    "deepseek-v3": {
        "id": "deepseek-v3",
        "name": "DeepSeek-V3",
        "model": "DeepSeek-V3",
        "provider": "DeepSeek",
        "maxLength": 400000,
        "tokenLimit": 100000,
        "context": "128K",
    },
    "gemini-2.0-flash": {
        "id": "gemini-2.0-flash",
        "name": "Gemini-2.0-Flash",
        "model": "Gemini",
        "provider": "Google",
        "maxLength": 4000000,
        "tokenLimit": 1000000,
        "context": "1024K",
    },
    "gemini-2.0-flash-thinking-exp": {
        "id": "gemini-2.0-flash-thinking-exp",
        "name": "Gemini-2.0-Flash-Thinking-Exp",
        "model": "Gemini",
        "provider": "Google",
        "maxLength": 4000000,
        "tokenLimit": 1000000,
        "context": "1024K",
    },
    "gemini-2.0-pro-exp": {
        "id": "gemini-2.0-pro-exp",
        "name": "Gemini-2.0-Pro-Exp",
        "model": "Gemini",
        "provider": "Google",
        "maxLength": 4000000,
        "tokenLimit": 1000000,
        "context": "1024K",
    },
    "gpt-4o-2024-08-06": {
        "id": "gpt-4o-2024-08-06",
        "name": "GPT-4o",
        "model": "ChatGPT",
        "provider": "OpenAI",
        "maxLength": 260000,
        "tokenLimit": 126000,
        "context": "128K",
    },
    "gpt-4o-mini-2024-07-18": {
        "id": "gpt-4o-mini-2024-07-18",
        "name": "GPT-4o-Mini",
        "model": "ChatGPT",
        "provider": "OpenAI",
        "maxLength": 260000,
        "tokenLimit": 126000,
        "context": "128K",
    },
    "gpt-4o-mini-free": {
        "id": "gpt-4o-mini-free",
        "name": "GPT-4o-Mini-Free",
        "model": "ChatGPT",
        "provider": "OpenAI",
        "maxLength": 31200,
        "tokenLimit": 7800,
        "context": "8K",
    },
    "grok-3": {
        "id": "grok-3",
        "name": "Grok-3",
        "model": "Grok",
        "provider": "x.ai",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "grok-3-r1": {
        "id": "grok-3-r1",
        "name": "Grok-3-Thinking",
        "model": "Grok",
        "provider": "x.ai",
        "maxLength": 800000,
        "tokenLimit": 200000,
        "context": "200K",
    },
    "o3-mini": {
        "id": "o3-mini",
        "name": "o3-mini",
        "model": "o3",
        "provider": "OpenAI",
        "maxLength": 400000,
        "tokenLimit": 100000,
        "context": "128K",
    },
}


class Liaobots(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер Liaobots для асинхронной генерации текста.

    Поддерживает историю сообщений, системные сообщения и выбор различных моделей.
    """

    url: str = "https://liaobots.site"
    working: bool = True
    supports_message_history: bool = True
    supports_system_message: bool = True

    default_model: str = "gpt-4o-2024-08-06"
    models: List[str] = list(models.keys())
    model_aliases: Dict[str, str] = {
        # Anthropic
        "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
        "claude-3.5-sonnet": "claude-3-5-sonnet-20241022-t",
        "claude-3.7-sonnet": "claude-3-7-sonnet-20250219",
        "claude-3.7-sonnet": "claude-3-7-sonnet-20250219-t",
        "claude-3.7-sonnet-thinking": "claude-3-7-sonnet-20250219-thinking",
        "claude-3-opus": "claude-3-opus-20240229",
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        # DeepSeek
        "deepseek-r1": "deepseek-r1-distill-llama-70b",
        # Google
        "gemini-2.0-flash-thinking": "gemini-2.0-flash-thinking-exp",
        "gemini-2.0-pro": "gemini-2.0-pro-exp",
        # OpenAI
        "gpt-4": default_model,
        "gpt-4o": default_model,
        "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
        "gpt-4o-mini": "gpt-4o-mini-free",
    }

    _auth_code: str = ""
    _cookie_jar: Optional[dict] = None

    @classmethod
    def is_supported(cls, model: str) -> bool:
        """
        Проверяет, поддерживается ли данная модель.

        Args:
            model (str): Идентификатор модели.

        Returns:
            bool: True, если модель поддерживается, иначе False.
        """
        return model in models or model in cls.model_aliases

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        connector: Optional[BaseConnector] = None,
        **kwargs,
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от Liaobots API.

        Args:
            model (str): Идентификатор модели.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str]): Прокси-сервер для использования.
            connector (Optional[BaseConnector]): HTTP-коннектор для использования.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Части контента, полученные от API.
        """
        model = cls.get_model(model)

        headers: Dict[str, str] = {
            "referer": "https://liaobots.work/",
            "origin": "https://liaobots.work",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        async with ClientSession(
            headers=headers,
            cookie_jar=cls._cookie_jar,
            connector=get_connector(connector, proxy, True),
        ) as session:
            data: Dict[str, str | list | Dict] = {
                "conversationId": str(uuid.uuid4()),
                "model": models[model],
                "messages": messages,
                "key": "",
                "prompt": kwargs.get("system_message", "You are a helpful assistant."),
            }
            await cls.ensure_auth_code(session)  # Ensure auth code is initialized
            try:
                async for content in cls._stream_content(session, data):
                    yield content
            except Exception as ex:
                logger.error("Error while streaming content", ex, exc_info=True)
                raise

    @classmethod
    async def _stream_content(cls, session: ClientSession, data: Dict[str, str | list | Dict]) -> AsyncGenerator[str, None]:
        """
        Асинхронно получает и обрабатывает контент от API.

        Args:
            session (ClientSession): Aiohttp ClientSession.
            data (Dict[str, str | list | Dict]): Данные для отправки в API.

        Yields:
            str: Части контента, полученные от API.
        """
        try:
            async with session.post(
                "https://liaobots.work/api/chat",
                json=data,
                headers={"x-auth-code": cls._auth_code},
                verify_ssl=False,
            ) as response:
                await raise_for_status(response)
                async for line in response.content:
                    if line.startswith(b"data: "):
                        yield json.loads(line[6:]).get("content")
        except Exception as ex:
            logger.error("Error during content streaming", ex, exc_info=True)
            raise

    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Инициализирует auth code, выполняя необходимые запросы для логина.

        Args:
            session (ClientSession): Aiohttp ClientSession.
        """
        try:
            async with session.post(
                "https://liaobots.work/recaptcha/api/login",
                data={"token": "abcdefghijklmnopqrst"},
                verify_ssl=False
            ) as response:
                await raise_for_status(response)

            async with session.post(
                "https://liaobots.work/api/user",
                json={"authcode": "pTIQr4FTnVRfr"},  # TODO: Remove hardcoded authcode
                verify_ssl=False
            ) as response:
                await raise_for_status(response)
                response_data = await response.json(content_type=None)
                cls._auth_code = response_data["authCode"]
                if not cls._auth_code:
                    raise RuntimeError("Empty auth code")
                cls._cookie_jar = session.cookie_jar
        except Exception as ex:
            logger.error("Error during auth code initialization", ex, exc_info=True)
            raise

    @classmethod
    async def ensure_auth_code(cls, session: ClientSession) -> None:
        """
        Проверяет, инициализирован ли auth code, и выполняет инициализацию, если это необходимо.

        Args:
            session (ClientSession): Aiohttp ClientSession.
        """
        if not cls._auth_code:
            await cls.initialize_auth_code(session)