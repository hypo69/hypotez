### **Анализ кода модуля `raise_for_status.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/requests/raise_for_status.py

Модуль содержит функции для проверки статуса ответа и выброса исключений в зависимости от статуса и содержимого ответа. В основном, он обрабатывает ответы от серверов Cloudflare и OpenAI, а также общие ошибки, такие как Rate Limit и Bad Gateway.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и читаем.
  - Обработка различных типов ошибок и статусов ответов.
  - Использование асинхронной обработки.
- **Минусы**:
  - Использование `Union` вместо `|` для аннотаций типов.
  - Не хватает документации для функций и классов.
  - Отсутствует логирование ошибок.
  - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Заменить `Union` на `|`**:
    - В аннотациях типов использовать `|` вместо `Union`.
2.  **Добавить документацию**:
    - Добавить docstring к каждой функции, описывающий ее назначение, аргументы, возвращаемые значения и возможные исключения.
    - Подробно документировать логику работы функций, особенно условия и обработку ошибок.
3.  **Добавить логирование**:
    - Использовать модуль `logger` для логирования ошибок и предупреждений. Это поможет в отладке и мониторинге.
4.  **Аннотировать типы**:
    - Добавить аннотации типов для всех переменных, где это возможно.
5.  **Использовать `ex` вместо `e` в блоках обработки исключений**:
    - В блоках `except` использовать `ex` для обозначения исключения.
6.  **Улучшить обработку ошибок**:
    - Сделать обработку ошибок более информативной, добавив контекст и детали.

**Оптимизированный код:**

```python
from __future__ import annotations

from typing import Union
from aiohttp import ClientResponse
from requests import Response as RequestsResponse
from src.logger import logger  # Import logger
from ..errors import ResponseStatusError, RateLimitError, MissingAuthError


class CloudflareError(ResponseStatusError):
    """
    Исключение, выбрасываемое при обнаружении Cloudflare.
    """

    ...


def is_cloudflare(text: str) -> bool:
    """
    Проверяет, содержит ли текст признаки Cloudflare.

    Args:
        text (str): Текст для проверки.

    Returns:
        bool: True, если обнаружены признаки Cloudflare, иначе False.
    """
    if "Generated by cloudfront" in text or '<p id="cf-spinner-please-wait">' in text:
        return True
    elif "<title>Attention Required! | Cloudflare</title>" in text or 'id="cf-cloudflare-status"' in text:
        return True
    return '<div id="cf-please-wait">' in text or "<title>Just a moment...</title>" in text


def is_openai(text: str) -> bool:
    """
    Проверяет, содержит ли текст признаки OpenAI.

    Args:
        text (str): Текст для проверки.

    Returns:
        bool: True, если обнаружены признаки OpenAI, иначе False.
    """
    return "<p>Unable to load site</p>" in text or 'id="challenge-error-text"' in text


async def raise_for_status_async(response: ClientResponse | StreamResponse, message: str | None = None):
    """
    Асинхронно проверяет статус ответа и выбрасывает исключение при ошибке.

    Args:
        response (ClientResponse | StreamResponse): Объект ответа.
        message (str | None, optional): Сообщение об ошибке. Defaults to None.

    Raises:
        MissingAuthError: Если статус ответа 401.
        CloudflareError: Если статус ответа 403 и обнаружен Cloudflare.
        ResponseStatusError: Если статус ответа 403 и обнаружен OpenAI, или если произошла другая ошибка.
        RateLimitError: Если статус ответа 504.
    """
    if response.ok:
        return
    is_html: bool = False
    if message is None:
        content_type: str = response.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            try:
                message = await response.json()
                message = message.get("error", message)
                if isinstance(message, dict):
                    message = message.get("message", message)
            except Exception as ex:
                logger.error('Error while parsing JSON', ex, exc_info=True)
                message = "Failed to parse JSON"
        else:
            try:
                message = (await response.text()).strip()
                is_html = content_type.startswith("text/html") or message.startswith("<!DOCTYPE")
            except Exception as ex:
                logger.error('Error while reading text', ex, exc_info=True)
                message = "Failed to read text"
    if message is None or is_html:
        if response.status == 520:
            message = "Unknown error (Cloudflare)"
        elif response.status in (429, 402):
            message = "Rate limit"
    if response.status == 401:
        raise MissingAuthError(f"Response {response.status}: {message}")
    if response.status == 403 and is_cloudflare(message):
        raise CloudflareError(f"Response {response.status}: Cloudflare detected")
    elif response.status == 403 and is_openai(message):
        raise ResponseStatusError(f"Response {response.status}: OpenAI Bot detected")
    elif response.status == 502:
        raise ResponseStatusError(f"Response {response.status}: Bad Gateway")
    elif response.status == 504:
        raise RateLimitError(f"Response {response.status}: Gateway Timeout ")
    else:
        raise ResponseStatusError(f"Response {response.status}: {'HTML content' if is_html else message}")


def raise_for_status(response: Response | StreamResponse | ClientResponse | RequestsResponse, message: str | None = None):
    """
    Проверяет статус ответа и выбрасывает исключение при ошибке.

    Args:
        response (Response | StreamResponse | ClientResponse | RequestsResponse): Объект ответа.
        message (str | None, optional): Сообщение об ошибке. Defaults to None.

    Raises:
        MissingAuthError: Если статус ответа 401.
        CloudflareError: Если статус ответа 403 и обнаружен Cloudflare.
        ResponseStatusError: Если статус ответа 403 и обнаружен OpenAI, или если произошла другая ошибка.
        RateLimitError: Если статус ответа 504.
    """
    if hasattr(response, "status"):
        return raise_for_status_async(response, message)
    if response.ok:
        return
    is_html: bool = False
    if message is None:
        try:
            is_html = response.headers.get("content-type", "").startswith("text/html") or response.text.startswith("<!DOCTYPE")
            message = response.text
        except Exception as ex:
            logger.error('Error while processing headers or text', ex, exc_info=True)
            message = "Failed to process headers or text"
    if message is None or is_html:
        if response.status_code == 520:
            message = "Unknown error (Cloudflare)"
        elif response.status_code in (429, 402):
            raise RateLimitError(f"Response {response.status_code}: Rate Limit")
    if response.status_code == 401:
        raise MissingAuthError(f"Response {response.status_code}: {message}")
    if response.status_code == 403 and is_cloudflare(response.text):
        raise CloudflareError(f"Response {response.status_code}: Cloudflare detected")
    elif response.status_code == 403 and is_openai(response.text):
        raise ResponseStatusError(f"Response {response.status_code}: OpenAI Bot detected")
    elif response.status_code == 502:
        raise ResponseStatusError(f"Response {response.status_code}: Bad Gateway")
    elif response.status_code == 504:
        raise RateLimitError(f"Response {response.status_code}: Gateway Timeout ")
    else:
        raise ResponseStatusError(f"Response {response.status_code}: {'HTML content' if is_html else message}")