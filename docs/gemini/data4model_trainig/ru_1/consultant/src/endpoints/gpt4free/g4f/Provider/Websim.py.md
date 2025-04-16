### **Анализ кода модуля `Websim.py`**

#### **Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование асинхронных запросов для неблокирующего выполнения операций.
  - Реализация механизма повторных попыток при получении ошибки `429` (Превышен лимит запросов).
  - Наличие методов для генерации `project_id` в зависимости от типа запроса (`chat` или `image`).
  - Использование `ProviderModelMixin` для упрощения работы с разными моделями.
- **Минусы**:
  - Отсутствует подробная документация по классам и методам.
  - Не хватает обработки исключений и логирования ошибок.
  - Жестко заданы значения `user-agent` и других заголовков.
  - Есть повторяющийся код, который можно вынести в отдельные функции.
  - Не все переменные аннотированы типами.
  - В блоках `except` используется `e` вместо `ex`.

#### **Рекомендации по улучшению:**

1.  **Добавить документацию**:
    - Добавить docstring к классам `Websim`, `_handle_image_request`, `_handle_chat_request` и `generate_project_id` с описанием их назначения, параметров и возвращаемых значений.
    - Описать возможные исключения, которые могут быть выброшены.
2.  **Улучшить обработку исключений и логирование**:
    - Использовать `logger` для записи информации об ошибках и исключениях, возникающих в процессе выполнения запросов.
    - Добавить обработку специфических исключений, связанных с сетевыми запросами.
3.  **Рефакторинг**:
    - Вынести повторяющийся код установки заголовков в отдельную функцию.
    - Использовать константы для URL-адресов API.
    - Переименовать параметр `e` в `ex` в блоках `except`.
4.  **Безопасность**:
    - Рассмотреть возможность использования более надежных способов генерации `project_id`.
5.  **Типизация**:
    - Добавить аннотации типов для всех переменных, где это возможно.

#### **Оптимизированный код:**

```python
from __future__ import annotations

import json
import random
import string
import asyncio
from aiohttp import ClientSession
from typing import AsyncGenerator, Dict, List, Optional

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..requests.raise_for_status import raise_for_status
from ..errors import ResponseStatusError
from ..providers.response import ImageResponse
from .helper import format_prompt, format_image_prompt
from src.logger import logger  # Импорт модуля logger


"""
Модуль для работы с Websim AI
================================

Модуль содержит класс :class:`Websim`, который используется для взаимодействия с Websim AI API.
Поддерживает как текстовые запросы, так и генерацию изображений.

Пример использования
----------------------

>>> Websim.create_async_generator(model='gemini-1.5-pro', messages=[{'role': 'user', 'content': 'Hello'}])
<async_generator object Websim.create_async_generator at 0x...>
"""


class Websim(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для доступа к Websim AI API.
    Поддерживает как текстовые запросы, так и генерацию изображений.
    """
    url = "https://websim.ai"
    login_url = None
    chat_api_endpoint = "https://websim.ai/api/v1/inference/run_chat_completion"
    image_api_endpoint = "https://websim.ai/api/v1/inference/run_image_generation"

    working = True
    needs_auth = False
    use_nodriver = False
    supports_stream = False
    supports_system_message = True
    supports_message_history = True

    default_model = 'gemini-1.5-pro'
    default_image_model = 'flux'
    image_models = [default_image_model]
    models = [default_model, 'gemini-1.5-flash'] + image_models

    @staticmethod
    def generate_project_id(for_image: bool = False) -> str:
        """
        Генерирует project ID в соответствующем формате.

        Args:
            for_image (bool): Если `True`, генерирует ID для запросов изображений. В противном случае - для текстовых запросов.

        Returns:
            str: Сгенерированный project ID.

        Example:
            >>> Websim.generate_project_id(for_image=True)
            'kx0m131_rzz66qb2xoy7'
        """
        chars = string.ascii_lowercase + string.digits

        if for_image:
            first_part = ''.join(random.choices(chars, k=7))
            second_part = ''.join(random.choices(chars, k=12))
            return f"{first_part}_{second_part}"
        else:
            prefix = ''.join(random.choices(chars, k=3))
            suffix = ''.join(random.choices(chars, k=15))
            return f"{prefix}_{suffix}"

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        aspect_ratio: str = "1:1",
        project_id: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для обработки запросов к Websim AI API.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            prompt (str, optional): Промпт для запроса. По умолчанию `None`.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
            project_id (str, optional): Идентификатор проекта. Если `None`, генерируется автоматически.

        Yields:
            AsyncResult: Результат запроса.

        Raises:
            Exception: В случае возникновения ошибки.

        Example:
            >>> async for result in Websim.create_async_generator(model='gemini-1.5-pro', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(result)
        """
        is_image_request = model in cls.image_models

        if project_id is None:
            project_id = cls.generate_project_id(for_image=is_image_request)

        headers = cls._get_headers(is_image_request)  # Используем метод для получения заголовков

        if is_image_request:
            async for result in cls._handle_image_request(
                project_id=project_id,
                messages=messages,
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                headers=headers,
                proxy=proxy,
                **kwargs
            ):
                yield result
        else:
            async for result in cls._handle_chat_request(
                project_id=project_id,
                messages=messages,
                headers=headers,
                proxy=proxy,
                **kwargs
            ):
                yield result

    @classmethod
    def _get_headers(cls, is_image_request: bool) -> Dict[str, str]:
        """
        Возвращает заголовки для запроса в зависимости от типа запроса (изображение или чат).

        Args:
            is_image_request (bool): `True`, если это запрос изображения.

        Returns:
            Dict[str, str]: Словарь с заголовками.
        """
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://websim.ai',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'websim-flags;': ''
        }

        if is_image_request:
            headers['referer'] = 'https://websim.ai/@ISWEARIAMNOTADDICTEDTOPILLOW/ai-image-prompt-generator'
        else:
            headers['referer'] = 'https://websim.ai/@ISWEARIAMNOTADDICTEDTOPILLOW/zelos-ai-assistant'

        return headers

    @classmethod
    async def _handle_image_request(
        cls,
        project_id: str,
        messages: Messages,
        prompt: str,
        aspect_ratio: str,
        headers: dict,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Обрабатывает запрос на генерацию изображения.

        Args:
            project_id (str): Идентификатор проекта.
            messages (Messages): Список сообщений.
            prompt (str): Промпт для генерации изображения.
            aspect_ratio (str): Соотношение сторон изображения.
            headers (dict): Заголовки запроса.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Yields:
            AsyncResult: Результат запроса.

        Raises:
            Exception: В случае возникновения ошибки.
        """
        used_prompt = format_image_prompt(messages, prompt)

        async with ClientSession(headers=headers) as session:
            data = {
                "project_id": project_id,
                "prompt": used_prompt,
                "aspect_ratio": aspect_ratio
            }
            try:
                async with session.post(f"{cls.image_api_endpoint}", json=data, proxy=proxy) as response:
                    await raise_for_status(response)
                    response_text = await response.text()
                    response_json = json.loads(response_text)
                    image_url = response_json.get("url")
                    if image_url:
                        yield ImageResponse(images=[image_url], alt=used_prompt)
            except Exception as ex:
                logger.error('Error while processing image request', ex, exc_info=True)
                raise

    @classmethod
    async def _handle_chat_request(
        cls,
        project_id: str,
        messages: Messages,
        headers: dict,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Обрабатывает запрос к чат-ассистенту.

        Args:
            project_id (str): Идентификатор проекта.
            messages (Messages): Список сообщений для отправки.
            headers (dict): Заголовки запроса.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Yields:
            AsyncResult: Результат запроса.

        Raises:
            ResponseStatusError: Если получен статус ошибки от сервера.
            Exception: В случае других ошибок.
        """
        max_retries = 3
        retry_count = 0
        last_error = None

        while retry_count < max_retries:
            try:
                async with ClientSession(headers=headers) as session:
                    data = {
                        "project_id": project_id,
                        "messages": messages
                    }
                    async with session.post(f"{cls.chat_api_endpoint}", json=data, proxy=proxy) as response:
                        if response.status == 429:
                            response_text = await response.text()
                            last_error = ResponseStatusError(f"Response {response.status}: {response_text}")
                            retry_count += 1
                            if retry_count < max_retries:
                                wait_time = 2 ** retry_count
                                await asyncio.sleep(wait_time)
                                continue
                            else:
                                raise last_error

                        await raise_for_status(response)

                        response_text = await response.text()
                        try:
                            response_json = json.loads(response_text)
                            content = response_json.get("content", "")
                            yield content.strip()
                            break
                        except json.JSONDecodeError:
                            yield response_text
                            break

            except ResponseStatusError as ex:
                if "Rate limit exceeded" in str(ex) and retry_count < max_retries:
                    retry_count += 1
                    wait_time = 2 ** retry_count
                    await asyncio.sleep(wait_time)
                else:
                    if retry_count >= max_retries:
                        raise ex
                    else:
                        raise
            except Exception as ex:
                logger.error('Error while processing chat request', ex, exc_info=True)
                raise