### **Анализ кода модуля `Anthropic.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и понятен.
    - Присутствуют аннотации типов.
    - Используется `StreamSession` для асинхронной потоковой передачи данных.
- **Минусы**:
    - Отсутствует подробная документация для всех функций и классов.
    - Некоторые участки кода требуют дополнительных комментариев для лучшего понимания логики.
    - Не все переменные аннотированы типами.
    - Используется `requests` вместо `httpx`, который рекомендуется для асинхронных приложений.
    - Не используется `logger` для логирования ошибок и информации.

**Рекомендации по улучшению:**

1.  **Добавить документацию**:
    - Добавить docstring к классам и методам, описывающие их назначение, параметры и возвращаемые значения.
2.  **Использовать `logger`**:
    - Заменить `print` на `logger.info` или `logger.debug` для информационных сообщений.
    - Использовать `logger.error` для логирования ошибок и исключений, передавая `ex` и `exc_info=True`.
3.  **Улучшить обработку исключений**:
    - Добавить более конкретные блоки `except` для обработки различных типов исключений.
    - Логировать исключения с использованием `logger.error`.
4.  **Улучшить типизацию**:
    - Добавить аннотации типов для всех переменных, где это необходимо.
5.  **Использовать httpx**:
    - Заменить модуль `requests` на `httpx`, так как он предоставляет нативный асинхронный клиент.
6.  **Добавить больше комментариев**:
    - Добавить комментарии к сложным участкам кода, объясняющие логику и назначение.

**Оптимизированный код:**

```python
from __future__ import annotations

import json
import base64
from typing import Optional, List, Dict, AsyncGenerator, Tuple

import httpx

from ..helper import filter_none
from ...typing import AsyncResult, Messages, MediaListType
from ...requests import StreamSession, raise_for_status
from ...providers.response import FinishReason, ToolCalls, Usage
from ...errors import MissingAuthError
from ...image import to_bytes, is_accepted_format
from .OpenaiAPI import OpenaiAPI
from src.logger import logger  # Import logger

class Anthropic(OpenaiAPI):
    """
    Класс для взаимодействия с Anthropic API.

    Этот класс предоставляет методы для генерации текста с использованием различных моделей Anthropic,
    поддерживает потоковую передачу данных, системные сообщения и историю сообщений.
    """
    label: str = "Anthropic API"
    url: str = "https://console.anthropic.com"
    login_url: str = "https://console.anthropic.com/settings/keys"
    working: bool = True
    api_base: str = "https://api.anthropic.com/v1"
    needs_auth: bool = True
    supports_stream: bool = True
    supports_system_message: bool = True
    supports_message_history: bool = True
    default_model: str = "claude-3-5-sonnet-latest"
    models: List[str] = [
        default_model,
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-latest",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-latest",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
    models_aliases: Dict[str, str] = {
        "claude-3.5-sonnet": default_model,
        "claude-3-opus": "claude-3-opus-latest",
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        "claude-3-haiku": "claude-3-haiku-20240307",
    }

    @classmethod
    def get_models(cls, api_key: str = None, **kwargs) -> List[str]:
        """
        Получает список доступных моделей из Anthropic API.

        Args:
            api_key (str, optional): API ключ для аутентификации. По умолчанию None.

        Returns:
            List[str]: Список идентификаторов моделей.

        Raises:
            httpx.HTTPStatusError: Если HTTP запрос завершается с ошибкой.
        """
        if not cls.models:
            url: str = f"https://api.anthropic.com/v1/models"
            try:
                response = httpx.get(url, headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                })
                response.raise_for_status()  # Raise HTTPStatusError for bad responses (4xx or 5xx)
                models: dict = response.json()
                cls.models = [model["id"] for model in models["data"]]
            except httpx.HTTPStatusError as ex:
                logger.error("Error fetching models from Anthropic API", ex, exc_info=True)
                raise
            except Exception as ex:
                logger.error("Unexpected error while fetching models", ex, exc_info=True)
                raise
        return cls.models

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        media: MediaListType = None,
        api_key: str = None,
        temperature: float = None,
        max_tokens: int = 4096,
        top_k: int = None,
        top_p: float = None,
        stop: List[str] = None,
        stream: bool = False,
        headers: Dict = None,
        impersonate: str = None,
        tools: Optional[List] = None,
        extra_data: Dict = {},
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронно создает генератор для получения ответов от Anthropic API.

        Args:
            model (str): Идентификатор модели.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Proxy URL. По умолчанию None.
            timeout (int, optional): Timeout для запроса. По умолчанию 120.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию None.
            api_key (str, optional): API ключ для аутентификации. По умолчанию None.
            temperature (float, optional): Температура для генерации текста. По умолчанию None.
            max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
            top_k (int, optional): Top-k параметр. По умолчанию None.
            top_p (float, optional): Top-p параметр. По умолчанию None.
            stop (List[str], optional): Список стоп-последовательностей. По умолчанию None.
            stream (bool, optional): Включить потоковую передачу данных. По умолчанию False.
            headers (Dict, optional): Дополнительные заголовки для запроса. По умолчанию None.
            impersonate (str, optional): User agent для имитации. По умолчанию None.
            tools (Optional[List], optional): Список инструментов. По умолчанию None.
            extra_data (Dict, optional): Дополнительные данные для запроса. По умолчанию {}.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий результаты от API.

        Raises:
            MissingAuthError: Если отсутствует API ключ.
            httpx.HTTPStatusError: Если HTTP запрос завершается с ошибкой.
            Exception: При возникновении непредвиденной ошибки.
        """
        if api_key is None:
            raise MissingAuthError('Add a "api_key"')

        if media is not None:
            insert_images: List[Dict] = []
            for image, _ in media:
                data: bytes = to_bytes(image)
                insert_images.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": is_accepted_format(data),
                        "data": base64.b64encode(data).decode(),
                    }
                })
            messages[-1]["content"] = [
                *insert_images,
                {
                    "type": "text",
                    "text": messages[-1]["content"]
                }
            ]
        system: str = "\\n".join([message["content"] for message in messages if message.get("role") == "system"])
        if system:
            messages = [message for message in messages if message.get("role") != "system"]
        else:
            system = None

        async with StreamSession(
            proxy=proxy,
            headers=cls.get_headers(stream, api_key, headers),
            timeout=timeout,
            impersonate=impersonate,
        ) as session:
            data: Dict = filter_none(
                messages=messages,
                model=cls.get_model(model, api_key=api_key),
                temperature=temperature,
                max_tokens=max_tokens,
                top_k=top_k,
                top_p=top_p,
                stop_sequences=stop,
                system=system,
                stream=stream,
                tools=tools,
                **extra_data
            )
            try:
                async with session.post(f"{cls.api_base}/messages", json=data) as response:
                    await raise_for_status(response)
                    if not stream:
                        data: dict = await response.json()
                        cls.raise_error(data)
                        if "type" in data and data["type"] == "message":
                            for content in data["content"]:
                                if content["type"] == "text":
                                    yield content["text"]
                                elif content["type"] == "tool_use":
                                    tool_calls: List[Dict] = []
                                    tool_calls.append({
                                        "id": content["id"],
                                        "type": "function",
                                        "function": { "name": content["name"], "arguments": content["input"] }
                                    })
                            if data["stop_reason"] == "end_turn":
                                yield FinishReason("stop")
                            elif data["stop_reason"] == "max_tokens":
                                yield FinishReason("length")
                            yield Usage(**data["usage"])
                    else:
                        content_block: Optional[Dict] = None
                        partial_json: List[str] = []
                        tool_calls: List[Dict] = []
                        async for line in response.iter_lines():
                            if line.startswith(b"data: "):
                                chunk: bytes = line[6:]
                                if chunk == b"[DONE]":
                                    break
                                data: dict = json.loads(chunk.decode('utf-8'))  # Ensure chunk is decoded to string
                                cls.raise_error(data)
                                if "type" in data:
                                    if data["type"] == "content_block_start":
                                        content_block = data["content_block"]
                                    if content_block is None:
                                        pass  # Message start
                                    elif data["type"] == "content_block_delta":
                                        if content_block["type"] == "text":
                                            yield data["delta"]["text"]
                                        elif content_block["type"] == "tool_use":
                                            partial_json.append(data["delta"]["partial_json"])
                                    elif data["type"] == "message_delta":
                                        if data["delta"]["stop_reason"] == "end_turn":
                                            yield FinishReason("stop")
                                        elif data["delta"]["stop_reason"] == "max_tokens":
                                            yield FinishReason("length")
                                        yield Usage(**data["usage"])
                                    elif data["type"] == "content_block_stop":
                                        if content_block["type"] == "tool_use":
                                            tool_calls.append({
                                                "id": content_block["id"],
                                                "type": "function",
                                                "function": { "name": content_block["name"], "arguments": "".join(partial_json) }  # Join partial_json
                                            })
                                            partial_json = []
                        if tool_calls:
                            yield ToolCalls(tool_calls)
            except httpx.HTTPStatusError as ex:
                logger.error("HTTP error during API request", ex, exc_info=True)
                raise
            except MissingAuthError as ex:
                logger.error("Authentication error", ex, exc_info=True)
                raise
            except Exception as ex:
                logger.error("Unexpected error during API request", ex, exc_info=True)
                raise

    @classmethod
    def get_headers(cls, stream: bool, api_key: str = None, headers: Dict = None) -> Dict:
        """
        Получает заголовки для HTTP запроса.

        Args:
            stream (bool): Включить потоковую передачу данных.
            api_key (str, optional): API ключ для аутентификации. По умолчанию None.
            headers (Dict, optional): Дополнительные заголовки. По умолчанию None.

        Returns:
            Dict: Словарь с заголовками.
        """
        base_headers: Dict = {
            "Accept": "text/event-stream" if stream else "application/json",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        if api_key is not None:
            base_headers["x-api-key"] = api_key
        if headers is not None:
            base_headers.update(headers)
        return base_headers