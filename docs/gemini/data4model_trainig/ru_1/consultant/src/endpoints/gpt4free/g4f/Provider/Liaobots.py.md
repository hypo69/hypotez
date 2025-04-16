### **Анализ кода модуля `Liaobots.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/Liaobots.py

Модуль содержит класс `Liaobots`, который является асинхронным провайдером для взаимодействия с различными моделями через API liaobots.site.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация для неблокирующего взаимодействия с API.
    - Поддержка истории сообщений и системных сообщений.
    - Использование `aiohttp` для асинхронных HTTP-запросов.
    - Наличие предопределенных моделей и алиасов для удобства использования.
- **Минусы**:
    - Дублирование кода в блоках `try` и `except`.
    - Жестко заданные значения для `authcode` в случае ошибки.
    - Отсутствие обработки исключений для конкретных ошибок `aiohttp`.
    - Игнорирование ошибок SSL (`verify_ssl=False`).
    - Отсутствуют аннотации типов для переменных `_auth_code` и `_cookie_jar`.

**Рекомендации по улучшению**:

1.  **Удаление дублирования кода**:
    - Вынести повторяющийся код из блоков `try` и `except` в отдельную функцию. Это улучшит читаемость и упростит поддержку.
2.  **Обработка исключений**:
    - Добавить обработку конкретных исключений `aiohttp` для более надежной работы.
3.  **Безопасность**:
    - Рассмотреть возможность включения проверки SSL (`verify_ssl=True`) и обработки исключений, связанных с SSL.
4.  **Использовать `logger`**:
    - Логгировать ошибки с помощью `logger` из `src.logger`, чтобы упростить отладку и мониторинг.
5.  **Аннотации типов**:
    - Добавить аннотации типов для переменных `_auth_code` и `_cookie_jar`.
6. **Документация**
    - Добавить docstring к переменным класса. Описать назначение, тип и возможные значения
    - Добавить примеры использовния к функциям. Например
        ```python
        async def initialize_auth_code(cls, session: ClientSession) -> None:
            """
            Инициализирует код аутентификации, выполняя необходимые запросы для входа в систему.
            
            Args:
                session (ClientSession): Асинхровая сессия клиента для выполнения HTTP-запросов.
            
            Returns:
                None
            
            Raises:
                RuntimeError: Если не удается получить код аутентификации.
            
            Example:
                >>> async with aiohttp.ClientSession() as session:
                ...     await Liaobots.initialize_auth_code(session)
                ...     print(Liaobots._auth_code)
                
            """
        ```

**Оптимизированный код**:

```python
"""
Модуль для работы с провайдером Liaobots
==========================================

Модуль содержит класс :class:`Liaobots`, который является асинхронным провайдером
для взаимодействия с различными моделями через API liaobots.site.
"""
from __future__ import annotations

import uuid
import json
from aiohttp import ClientSession, BaseConnector, ClientError

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import get_connector
from ..requests import raise_for_status

from src.logger import logger  # Добавлен импорт logger

models: dict[str, dict[str, str | int]] = {
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
    Асинхронный провайдер для взаимодействия с API liaobots.site.

    Attributes:
        url (str): URL сайта liaobots.site.
        working (bool): Флаг, указывающий на работоспособность провайдера.
        supports_message_history (bool): Флаг, указывающий на поддержку истории сообщений.
        supports_system_message (bool): Флаг, указывающий на поддержку системных сообщений.
        default_model (str): Модель по умолчанию.
        models (list[str]): Список поддерживаемых моделей.
        model_aliases (dict[str, str]): Словарь алиасов моделей.
    """
    url: str = "https://liaobots.site"
    working: bool = True
    supports_message_history: bool = True
    supports_system_message: bool = True

    default_model: str = "gpt-4o-2024-08-06"
    models: list[str] = list(models.keys())
    model_aliases: dict[str, str] = {
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
    """Код аутентификации для доступа к API."""
    _cookie_jar: None = None
    """Контейнер для хранения cookie."""

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
        proxy: str | None = None,
        connector: BaseConnector | None = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с API Liaobots.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. Defaults to None.
            connector (BaseConnector, optional): HTTP-коннектор. Defaults to None.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Части ответа от API.

        Raises:
            RuntimeError: Если не удается получить код аутентификации.
            ClientError: При возникновении ошибок при выполнении HTTP-запросов.
        
        Example:
            >>> model = "gpt-4o-2024-08-06"
            >>> messages = [{"role": "user", "content": "Hello"}]
            >>> async for message in Liaobots.create_async_generator(model, messages):
            ...     print(message)
        """
        model = cls.get_model(model)

        headers: dict[str, str] = {
            "referer": "https://liaobots.work/",
            "origin": "https://liaobots.work",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        async def post_request(session: ClientSession, url: str, data: dict | None = None, json_data: dict | None = None, headers_data: dict | None = None) -> None:
            """
            Выполняет POST-запрос к указанному URL.

            Args:
                session (ClientSession): Асинхровая сессия клиента для выполнения HTTP-запросов.
                url (str): URL для выполнения запроса.
                data (dict, optional): Данные для отправки в теле запроса (form-data). Defaults to None.
                json_data (dict, optional): Данные для отправки в теле запроса (json). Defaults to None.
                headers_data (dict, optional): Дополнительные заголовки для запроса. Defaults to None.

            Yields:
                str: Части ответа от API, если запрос выполнен успешно.

            Raises:
                ClientError: При возникновении ошибок при выполнении HTTP-запросов.
                RuntimeError: Если не удается получить код аутентификации.
            """
            try:
                if headers_data is None:
                    headers_data = {}

                async with session.post(url, json=json_data, data=data, headers=headers_data, verify_ssl=False) as response:
                    await raise_for_status(response)
                    if url == "https://liaobots.work/api/chat":
                        async for line in response.content:
                            if line.startswith(b"data: "):
                                yield json.loads(line[6:]).get("content")
                    else:
                        return await response.json(content_type=None)

            except ClientError as ex:
                logger.error(f'Ошибка при выполнении запроса к {url}', ex, exc_info=True)
                raise
            except json.JSONDecodeError as ex:
                logger.error(f'Ошибка при декодировании JSON ответа от {url}', ex, exc_info=True)
                raise

        async with ClientSession(
            headers=headers,
            cookie_jar=cls._cookie_jar,
            connector=get_connector(connector, proxy, True)
        ) as session:
            data: dict[str, str | dict | list] = {
                "conversationId": str(uuid.uuid4()),
                "model": models[model],
                "messages": messages,
                "key": "",
                "prompt": kwargs.get("system_message", "You are a helpful assistant."),
            }

            if not cls._auth_code:
                response_data = await post_request(
                    session,
                    "https://liaobots.work/recaptcha/api/login",
                    data={"token": "abcdefghijklmnopqrst"}
                )

            try:
                # Попытка выполнить основной запрос
                response_data = await post_request(
                    session,
                    "https://liaobots.work/api/user",
                    json_data={"authcode": cls._auth_code}
                )
                cls._auth_code = response_data["authCode"]
                if not cls._auth_code:
                    raise RuntimeError("Пустой auth code")
                cls._cookie_jar = session.cookie_jar

                async for message in post_request(
                    session,
                    "https://liaobots.work/api/chat",
                    json_data=data,
                    headers_data={"x-auth-code": cls._auth_code}
                ):
                    yield message

            except (ClientError, RuntimeError) as ex:
                # Обработка ошибок и повторная попытка с другим authcode
                logger.error('Произошла ошибка при выполнении основного запроса, попытка повторного запроса с другим authcode', ex, exc_info=True)
                response_data = await post_request(
                    session,
                    "https://liaobots.work/api/user",
                    json_data={"authcode": "jGDRFOqHcZKAo"}
                )
                cls._auth_code = response_data["authCode"]
                if not cls._auth_code:
                    raise RuntimeError("Пустой auth code")
                cls._cookie_jar = session.cookie_jar
                async for message in post_request(
                    session,
                    "https://liaobots.work/api/chat",
                    json_data=data,
                    headers_data={"x-auth-code": cls._auth_code}
                ):
                    yield message

    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Инициализирует код аутентификации, выполняя необходимые запросы для входа в систему.
        
        Args:
            session (ClientSession): Асинхровая сессия клиента для выполнения HTTP-запросов.
        
        Returns:
            None
        
        Raises:
            RuntimeError: Если не удается получить код аутентификации.
        
        Example:
            >>> async with aiohttp.ClientSession() as session:
            ...     await Liaobots.initialize_auth_code(session)
            ...     print(Liaobots._auth_code)
            
        """
        try:
            response_data = await cls.post_request(
                session,
                "https://liaobots.work/api/user",
                json_data={"authcode": "pTIQr4FTnVRfr"}
            )
            cls._auth_code = response_data["authCode"]
            if not cls._auth_code:
                raise RuntimeError("Пустой auth code")
            cls._cookie_jar = session.cookie_jar
        except ClientError as ex:
            logger.error('Ошибка при инициализации auth code', ex, exc_info=True)
            raise

    @classmethod
    async def ensure_auth_code(cls, session: ClientSession) -> None:
        """
        Гарантирует, что код аутентификации инициализирован, и выполняет инициализацию, если это необходимо.
        
        Args:
            session (ClientSession): Асинхровая сессия клиента для выполнения HTTP-запросов.
        
        Returns:
            None
        
        """
        if not cls._auth_code:
            await cls.initialize_auth_code(session)