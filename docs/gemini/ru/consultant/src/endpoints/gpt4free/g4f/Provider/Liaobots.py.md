### **Анализ кода модуля `Liaobots.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/Liaobots.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронности для неблокирующих операций.
    - Реализация поддержки истории сообщений и системных сообщений.
    - Наличие модели `ProviderModelMixin` для управления моделями.
- **Минусы**:
    - Повторяющийся код в блоках `try` и `except`.
    - Жестко заданные значения `authcode` в нескольких местах.
    - Отсутствие обработки исключений при `json.loads`.
    - Не все переменные аннотированы типами.

#### **Рекомендации по улучшению**:

1. **Удаление повторяющегося кода**:
   - Вынести повторяющийся код из блоков `try` и `except` в отдельную функцию. Это улучшит читаемость и упростит поддержку кода.

2. **Обработка исключений**:
   - Добавить обработку исключений при `json.loads`, чтобы избежать неожиданных сбоев.

3. **Использование `logger`**:
   - Логгировать ошибки и важные события, чтобы упростить отладку и мониторинг.

4. **Избавиться от дублирования кода**:
   - Повторяющийся код в `try...except` блоке следует вынести в отдельную функцию для повторного использования.

5. **Аннотации типов**:
   - Добавить аннотации типов для всех переменных и параметров функций.

6. **Использовать `j_loads`**:
   - Для парсинга json необходимо использовать `j_loads` из `src.utils`.

7. **Пересмотреть логику получения `authcode`**:
   - Сейчас в коде в нескольких местах хардкодится `authcode`. Необходимо пересмотреть логику его получения и инициализации, чтобы избежать дублирования и сделать код более гибким.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с провайдером Liaobots.
========================================

Модуль содержит класс :class:`Liaobots`, который используется для взаимодействия с Liaobots API.
Поддерживает асинхронные запросы и предоставляет функциональность для работы с различными моделями.

Пример использования
----------------------

>>> provider = Liaobots()
>>> models = provider.models
"""
from __future__ import annotations

import uuid
import json
from typing import AsyncGenerator, Dict, List, Optional
from aiohttp import ClientSession, BaseConnector

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import get_connector
from ..requests import raise_for_status
from src.logger import logger  # Импорт logger
from src.utils.proxy_manager import ProxyManager


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

    Поддерживает историю сообщений и системные сообщения.
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
    _cookie_jar: Optional[ClientSession] = None
    
    @classmethod
    def is_supported(cls, model: str) -> bool:
        """
        Проверяет, поддерживается ли данная модель.

        Args:
            model (str): Название модели.

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
        Создает асинхронный генератор для взаимодействия с Liaobots API.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str]): Адрес прокси-сервера.
            connector (Optional[BaseConnector]): Объект коннектора.

        Yields:
            str: Части контента, возвращаемые от API.

        Raises:
            RuntimeError: Если не удалось получить код авторизации.
            Exception: При возникновении других ошибок.
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
            data: Dict[str, str | Dict] = {
                "conversationId": str(uuid.uuid4()),
                "model": models[model],
                "messages": messages,
                "key": "",
                "prompt": kwargs.get("system_message", "You are a helpful assistant."),
            }

            if not cls._auth_code:
                await cls._get_auth_code(session)

            try:
                async for content in cls._send_chat_request(session, data):
                    yield content
            except Exception as ex:
                logger.error("Ошибка при отправке запроса в Liaobots API", ex, exc_info=True)
                try:
                    # Повторная попытка с другим кодом авторизации
                    await cls._get_auth_code(session, authcode="jGDRFOqHcZKAo")
                    async for content in cls._send_chat_request(session, data):
                        yield content
                except Exception as ex:
                    logger.error("Повторная попытка отправки запроса не удалась", ex, exc_info=True)
                    raise

    @classmethod
    async def _get_auth_code(cls, session: ClientSession, authcode: str = "pTIQr4FTnVRfr") -> None:
        """
        Получает код авторизации из API.

        Args:
            session (ClientSession): Сессия aiohttp.
            authcode (str): Код авторизации для запроса. По умолчанию "pTIQr4FTnVRfr".

        Raises:
            RuntimeError: Если не удалось получить код авторизации.
        """
        try:
            async with session.post(
                "https://liaobots.work/api/user",
                json={"authcode": authcode},
                verify_ssl=False,
            ) as response:
                await raise_for_status(response)
                response_json = await response.json(content_type=None)
                cls._auth_code = response_json["authCode"]
                if not cls._auth_code:
                    raise RuntimeError("Empty auth code")
                cls._cookie_jar = session.cookie_jar
        except Exception as ex:
            logger.error("Ошибка при получении кода авторизации", ex, exc_info=True)
            raise

    @classmethod
    async def _send_chat_request(cls, session: ClientSession, data: Dict[str, str | Dict]) -> AsyncGenerator[str, None]:
        """
        Отправляет запрос чата в API и возвращает асинхронный генератор контента.

        Args:
            session (ClientSession): Сессия aiohttp.
            data (Dict[str, str | Dict]): Данные для отправки в запросе.

        Yields:
            str: Части контента, возвращаемые от API.

        Raises:
            Exception: При возникновении ошибок при отправке запроса.
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
                        try:
                            content = json.loads(line[6:]).get("content")
                            yield content
                        except json.JSONDecodeError as ex:
                            logger.error("Ошибка при декодировании JSON", ex, exc_info=True)
                            continue  # Пропускаем текущую строку и переходим к следующей
        except Exception as ex:
            logger.error("Ошибка при отправке запроса чата", ex, exc_info=True)
            raise

    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Инициализирует код авторизации, выполняя необходимые запросы для входа в систему.

        Args:
            session (ClientSession): Сессия aiohttp.
        """
        await cls._get_auth_code(session)

    @classmethod
    async def ensure_auth_code(cls, session: ClientSession) -> None:
        """
        Убеждается, что код авторизации инициализирован, и выполняет инициализацию, если это необходимо.

        Args:
            session (ClientSession): Сессия aiohttp.
        """
        if not cls._auth_code:
            await cls.initialize_auth_code(session)