### **Анализ кода модуля `ChatGptEs.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код предоставляет асинхронный генератор для взаимодействия с сервисом ChatGptEs.
  - Используется `curl_cffi` для обхода Cloudflare, что является хорошим решением.
  - Присутствует обработка ошибок и логирование.
  - Код поддерживает прокси.
- **Минусы**:
  - Отсутствуют аннотации типов для аргументов и возвращаемых значений функций.
  - Не используются возможности модуля `src.logger` для логирования.
  - Присутствуют участки кода, которые могут быть упрощены или улучшены с точки зрения читаемости.
  - Обработка ошибок выполняется без использования `logger.error`.
  - В коде используются двойные кавычки вместо одинарных.

#### **Рекомендации по улучшению**:
1. **Добавить аннотации типов**:
   - Для всех аргументов функций и возвращаемых значений необходимо добавить аннотации типов.
2. **Использовать `logger`**:
   - Заменить `print` на `logger.info` и `logger.error` для логирования.
3. **Улучшить читаемость**:
   - Разбить длинные строки на несколько, чтобы улучшить читаемость.
   - Использовать более понятные имена переменных.
4. **Использовать одинарные кавычки**:
   - Заменить двойные кавычки на одинарные, где это необходимо.
5. **Добавить Docstring**:
   - Описать подробно что делает класс
   - Описать подробно что делает каждая функция

#### **Оптимизированный код**:
```python
from __future__ import annotations

import os
import re
import json
from typing import AsyncGenerator, Optional, List, Dict, Any

from src.logger import logger # Импорт модуля logger
try:
    from curl_cffi.requests import Session
    has_curl_cffi = True
except ImportError:
    has_curl_cffi = False

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import format_prompt
from ..errors import MissingRequirementsError


class ChatGptEs(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Модуль для асинхронного взаимодействия с ChatGptEs.
    ====================================================

    Этот класс предоставляет асинхронный генератор для взаимодействия с API ChatGptEs.
    Поддерживает обход защиты Cloudflare с использованием curl_cffi.

    Пример использования
    ----------------------
    >>> ChatGptEs.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}])
    """
    url: str = 'https://chatgpt.es'
    api_endpoint: str = 'https://chatgpt.es/wp-admin/admin-ajax.php'

    working: bool = True
    supports_stream: bool = True
    supports_system_message: bool = False
    supports_message_history: bool = False

    default_model: str = 'gpt-4o'
    models: List[str] = ['gpt-4', default_model, 'gpt-4o-mini']

    SYSTEM_PROMPT: str = 'Your default language is English. Always respond in English unless the user\'s message is in a different language. If the user\'s message is not in English, respond in the language of the user\'s message. Maintain this language behavior throughout the conversation unless explicitly instructed otherwise. User input:'

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """
        Создает асинхронный генератор для взаимодействия с ChatGptEs.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию None.
            **kwargs (Any): Дополнительные аргументы.

        Yields:
            AsyncGenerator[str, None]: Асинхронный генератор с ответами от ChatGptEs.

        Raises:
            MissingRequirementsError: Если не установлен curl_cffi.
            ValueError: Если получен неожиданный формат ответа или произошла ошибка при запросе.

        """
        if not has_curl_cffi:
            raise MissingRequirementsError('Install or update "curl_cffi" package | pip install -U curl_cffi')

        model = cls.get_model(model)
        prompt = f'{cls.SYSTEM_PROMPT} {format_prompt(messages)}'

        # Use curl_cffi with automatic Cloudflare bypass
        session = Session()
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'referer': cls.url,
            'origin': cls.url,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
        })

        if proxy:
            session.proxies = {'https': proxy, 'http': proxy}

        # First request to get nonce and post_id
        try:
            initial_response = session.get(cls.url, impersonate='chrome110')
            initial_text = initial_response.text
        except Exception as ex:
            logger.error('Error while getting initial response', ex, exc_info=True)
            raise ValueError('Failed to get initial response') from ex

        # More comprehensive nonce extraction
        nonce_patterns: List[str] = [
            r'<input\s+type=[\'"]hidden[\'"]\s+name=[\'"]_wpnonce[\'"]\s+value=[\'"]([^\'"]+)[\'"]',
            r'"_wpnonce":"([^"]+)"',
            r'var\s+wpaicg_nonce\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'wpaicg_nonce\s*:\s*[\'"]([^\'"]+)[\'"]'
        ]

        nonce_: Optional[str] = None
        for pattern in nonce_patterns:
            match = re.search(pattern, initial_text)
            if match:
                nonce_ = match.group(1)
                break

        if not nonce_:
            # Try to find any nonce-like pattern as a last resort
            general_nonce = re.search(r'nonce[\'"]?\s*[=:]\s*[\'"]([a-zA-Z0-9]+)[\'"]', initial_text)
            if general_nonce:
                nonce_ = general_nonce.group(1)
            else:
                # Fallback, but this likely won't work
                nonce_ = '8cf9917be2'

        # Look for post_id in HTML
        post_id_patterns: List[str] = [
            r'<input\s+type=[\'"]hidden[\'"]\s+name=[\'"]post_id[\'"]\s+value=[\'"]([^\'"]+)[\'"]',
            r'"post_id":"([^"]+)"',
            r'var\s+post_id\s*=\s*[\'"]?(\d+)[\'"]?'
        ]

        post_id: Optional[str] = None
        for pattern in post_id_patterns:
            match = re.search(pattern, initial_text)
            if match:
                post_id = match.group(1)
                break

        if not post_id:
            post_id = '106'  # Default from curl example

        client_id = os.urandom(5).hex()

        # Prepare data
        data: Dict[str, str] = {
            '_wpnonce': nonce_ if nonce_ else '',
            'post_id': post_id if post_id else '',
            'url': cls.url,
            'action': 'wpaicg_chat_shortcode_message',
            'message': prompt,
            'bot_id': '0',
            'chatbot_identity': 'shortcode',
            'wpaicg_chat_client_id': client_id,
            'wpaicg_chat_history': json.dumps([f'Human: {prompt}'])
        }

        # Execute POST request
        try:
            response = session.post(
                cls.api_endpoint,
                data=data,
                impersonate='chrome110'
            )

            if response.status_code != 200:
                raise ValueError(f'Error: {response.status_code} - {response.text}')

            result: Dict[str, Any] = response.json()
            if 'data' in result:
                if isinstance(result['data'], str) and 'Du musst das Kästchen anklicken!' in result['data']:
                    raise ValueError(result['data'])
                yield result['data']
            else:
                raise ValueError(f'Unexpected response format: {result}')

        except Exception as ex:
            logger.error('Error while executing POST request', ex, exc_info=True)
            raise