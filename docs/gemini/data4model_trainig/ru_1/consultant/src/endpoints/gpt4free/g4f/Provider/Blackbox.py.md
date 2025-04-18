### **Анализ кода модуля `Blackbox.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/Blackbox.py

Модуль содержит класс `Blackbox`, который является асинхронным генератором провайдера для взаимодействия с Blackbox AI. Он поддерживает потоковую передачу, системные сообщения и историю сообщений.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и содержит много полезных функций.
  - Присутствуют обработки исключений.
  - Используются асинхронные операции.
  - Есть поддержка различных моделей и режимов агентов.
- **Минусы**:
  - Некоторые docstring отсутствуют или неполные.
  - В некоторых местах используются смешанные стили кавычек.
  - Не все переменные и параметры аннотированы типами.
  - Дублирование кода в методах `generate_session` и `fetch_validated`.
  - Отсутствует единый стиль форматирования.
  - Не везде используется модуль `logger` для логирования.

**Рекомендации по улучшению:**

1.  **Документирование кода**:
    - Добавить docstring для всех методов и классов, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Перевести существующие docstring на русский язык.
2.  **Унификация стиля**:
    - Привести все строки к использованию одинарных кавычек.
    - Добавить аннотации типов для всех переменных и параметров функций.
    - Использовать `|` вместо `Union[]` для аннотаций типов.
    - Добавить пробелы вокруг операторов присваивания.
3.  **Логирование**:
    - Заменить `debug.log` на `logger.debug` из модуля `src.logger`.
    - Добавить логирование ошибок с использованием `logger.error` и `exc_info=True`.
4.  **Рефакторинг**:
    - Избавиться от дублирования кода в методах `generate_session` и `fetch_validated`, вынеся общую логику в отдельные функции.
    - Проверить и улучшить обработку исключений, чтобы избежать пустых блоков `except`.
5.  **Безопасность**:
    - Убедиться, что все HAR файлы обрабатываются безопасно и не содержат конфиденциальную информацию.
6.  **Обработка `...`**:
    - Убедиться, что все строки с `...` не документируются.
7.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, параметров и возвращаемых значений функций.
8.  **webdriver**:
    - Если в коде планируется использование webdriver, необходимо использовать `driver.execute_locator(l: dict)` для взаимодействия с веб-элементами.

**Оптимизированный код:**

```python
"""
Модуль для взаимодействия с Blackbox AI через API.
====================================================

Модуль содержит класс :class:`Blackbox`, который является асинхронным генератором провайдера для взаимодействия с Blackbox AI.
Он поддерживает потоковую передачу, системные сообщения и историю сообщений.
"""

from __future__ import annotations

import asyncio
import base64
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import random
import re
import string
from typing import AsyncGenerator, Optional, List, Dict, Any, Tuple

from aiohttp import ClientSession

from ..typing import AsyncResult, Messages, MediaListType
from ..requests.raise_for_status import raise_for_status
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..image import to_data_uri
from ..cookies import get_cookies_dir
from .helper import format_image_prompt
from ..providers.response import JsonConversation, ImageResponse
from ..tools.media import merge_media
from src.logger import logger


class Conversation(JsonConversation):
    """
    Класс для представления истории разговора с Blackbox AI.
    """

    validated_value: str = None
    chat_id: str = None
    message_history: Messages = []

    def __init__(self, model: str) -> None:
        """
        Инициализирует объект Conversation.

        Args:
            model (str): Модель, используемая в разговоре.
        """
        self.model = model


class Blackbox(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с Blackbox AI.
    """

    label: str = 'Blackbox AI'
    url: str = 'https://www.blackbox.ai'
    api_endpoint: str = 'https://www.blackbox.ai/api/chat'

    working: bool = True
    supports_stream: bool = True
    supports_system_message: bool = True
    supports_message_history: bool = True

    default_model: str = 'blackboxai'
    default_vision_model: str = default_model
    default_image_model: str = 'flux'

    # Полностью бесплатные модели
    fallback_models: List[str] = [
        'blackboxai',
        'blackboxai-pro',
        'gpt-4o-mini',
        'GPT-4o',
        'o1',
        'o3-mini',
        'Claude-sonnet-3.7',
        'DeepSeek-V3',
        'DeepSeek-R1',
        'DeepSeek-LLM-Chat-(67B)',
        # Image models
        'flux',
        # Trending agent modes
        'Python Agent',
        'HTML Agent',
        'Builder Agent',
        'Java Agent',
        'JavaScript Agent',
        'React Agent',
        'Android Agent',
        'Flutter Agent',
        'Next.js Agent',
        'AngularJS Agent',
        'Swift Agent',
        'MongoDB Agent',
        'PyTorch Agent',
        'Xcode Agent',
        'Azure Agent',
        'Bitbucket Agent',
        'DigitalOcean Agent',
        'Docker Agent',
        'Electron Agent',
        'Erlang Agent',
        'FastAPI Agent',
        'Firebase Agent',
        'Flask Agent',
        'Git Agent',
        'Gitlab Agent',
        'Go Agent',
        'Godot Agent',
        'Google Cloud Agent',
        'Heroku Agent',
    ]

    image_models: List[str] = [default_image_model]
    vision_models: List[str] = [
        default_vision_model,
        'GPT-4o',
        'o1',
        'o3-mini',
        'Gemini-PRO',
        'Gemini Agent',
        'llama-3.1-8b Agent',
        'llama-3.1-70b Agent',
        'llama-3.1-405 Agent',
        'Gemini-Flash-2.0',
        'DeepSeek-V3',
    ]

    userSelectedModel: List[str] = [
        'GPT-4o',
        'o1',
        'o3-mini',
        'Gemini-PRO',
        'Claude-sonnet-3.7',
        'DeepSeek-V3',
        'DeepSeek-R1',
        'Meta-Llama-3.3-70B-Instruct-Turbo',
        'Mistral-Small-24B-Instruct-2501',
        'DeepSeek-LLM-Chat-(67B)',
        'DBRX-Instruct',
        'Qwen-QwQ-32B-Preview',
        'Nous-Hermes-2-Mixtral-8x7B-DPO',
        'Gemini-Flash-2.0',
    ]

    # Agent mode configurations
    agentMode: Dict[str, Dict[str, Any]] = {
        'GPT-4o': {'mode': True, 'id': 'GPT-4o', 'name': 'GPT-4o'},
        'Gemini-PRO': {'mode': True, 'id': 'Gemini-PRO', 'name': 'Gemini-PRO'},
        'Claude-sonnet-3.7': {'mode': True, 'id': 'Claude-sonnet-3.7', 'name': 'Claude-sonnet-3.7'},
        'DeepSeek-V3': {'mode': True, 'id': 'deepseek-chat', 'name': 'DeepSeek-V3'},
        'DeepSeek-R1': {'mode': True, 'id': 'deepseek-reasoner', 'name': 'DeepSeek-R1'},
        'Meta-Llama-3.3-70B-Instruct-Turbo': {
            'mode': True,
            'id': 'meta-llama/Llama-3.3-70B-Instruct-Turbo',
            'name': 'Meta-Llama-3.3-70B-Instruct-Turbo',
        },
        'Gemini-Flash-2.0': {'mode': True, 'id': 'Gemini/Gemini-Flash-2.0', 'name': 'Gemini-Flash-2.0'},
        'Mistral-Small-24B-Instruct-2501': {
            'mode': True,
            'id': 'mistralai/Mistral-Small-24B-Instruct-2501',
            'name': 'Mistral-Small-24B-Instruct-2501',
        },
        'DeepSeek-LLM-Chat-(67B)': {
            'mode': True,
            'id': 'deepseek-ai/deepseek-llm-67b-chat',
            'name': 'DeepSeek-LLM-Chat-(67B)',
        },
        'DBRX-Instruct': {'mode': True, 'id': 'databricks/dbrx-instruct', 'name': 'DBRX-Instruct'},
        'Qwen-QwQ-32B-Preview': {'mode': True, 'id': 'Qwen/QwQ-32B-Preview', 'name': 'Qwen-QwQ-32B-Preview'},
        'Nous-Hermes-2-Mixtral-8x7B-DPO': {
            'mode': True,
            'id': 'NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO',
            'name': 'Nous-Hermes-2-Mixtral-8x7B-DPO',
        },
    }

    # Trending agent modes
    trendingAgentMode: Dict[str, Dict[str, Any]] = {
        'blackboxai-pro': {'mode': True, 'id': 'BLACKBOXAI-PRO'},
        'Gemini Agent': {'mode': True, 'id': 'gemini'},
        'llama-3.1-405 Agent': {'mode': True, 'id': 'llama-3.1-405'},
        'llama-3.1-70b Agent': {'mode': True, 'id': 'llama-3.1-70b'},
        'llama-3.1-8b Agent': {'mode': True, 'id': 'llama-3.1-8b'},
        'Python Agent': {'mode': True, 'id': 'python'},
        'HTML Agent': {'mode': True, 'id': 'html'},
        'Builder Agent': {'mode': True, 'id': 'builder'},
        'Java Agent': {'mode': True, 'id': 'java'},
        'JavaScript Agent': {'mode': True, 'id': 'javascript'},
        'React Agent': {'mode': True, 'id': 'react'},
        'Android Agent': {'mode': True, 'id': 'android'},
        'Flutter Agent': {'mode': True, 'id': 'flutter'},
        'Next.js Agent': {'mode': True, 'id': 'next.js'},
        'AngularJS Agent': {'mode': True, 'id': 'angularjs'},
        'Swift Agent': {'mode': True, 'id': 'swift'},
        'MongoDB Agent': {'mode': True, 'id': 'mongodb'},
        'PyTorch Agent': {'mode': True, 'id': 'pytorch'},
        'Xcode Agent': {'mode': True, 'id': 'xcode'},
        'Azure Agent': {'mode': True, 'id': 'azure'},
        'Bitbucket Agent': {'mode': True, 'id': 'bitbucket'},
        'DigitalOcean Agent': {'mode': True, 'id': 'digitalocean'},
        'Docker Agent': {'mode': True, 'id': 'docker'},
        'Electron Agent': {'mode': True, 'id': 'electron'},
        'Erlang Agent': {'mode': True, 'id': 'erlang'},
        'FastAPI Agent': {'mode': True, 'id': 'fastapi'},
        'Firebase Agent': {'mode': True, 'id': 'firebase'},
        'Flask Agent': {'mode': True, 'id': 'flask'},
        'Git Agent': {'mode': True, 'id': 'git'},
        'Gitlab Agent': {'mode': True, 'id': 'gitlab'},
        'Go Agent': {'mode': True, 'id': 'go'},
        'Godot Agent': {'mode': True, 'id': 'godot'},
        'Google Cloud Agent': {'mode': True, 'id': 'googlecloud'},
        'Heroku Agent': {'mode': True, 'id': 'heroku'},
    }

    # Полный список всех моделей (для авторизованных пользователей)
    _all_models: List[str] = list(
        dict.fromkeys(
            [
                default_model,
                *userSelectedModel,
                *image_models,
                *list(agentMode.keys()),
                *list(trendingAgentMode.keys()),
            ]
        )
    )

    @classmethod
    def generate_session(cls, id_length: int = 21, days_ahead: int = 365) -> dict:
        """
        Генерирует динамическую сессию с правильным ID и форматом срока действия.

        Args:
            id_length (int, optional): Длина числового ID. По умолчанию 21.
            days_ahead (int, optional): Количество дней до истечения срока действия. По умолчанию 365.

        Returns:
            dict: Словарь сессии с информацией о пользователе и сроком действия.
        """
        # Генерируем числовой ID
        numeric_id: str = ''.join(random.choice('0123456789') for _ in range(id_length))

        # Генерируем будущую дату истечения срока действия
        future_date: datetime = datetime.now() + timedelta(days=days_ahead)
        expiry: str = future_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        # Декодируем закодированный email
        encoded_email: str = 'Z2lzZWxlQGJsYWNrYm94LmFp'  # Base64 encoded email
        email: str = base64.b64decode(encoded_email).decode('utf-8')

        # Генерируем случайный ID изображения для нового формата URL
        chars: str = string.ascii_letters + string.digits + '-'
        random_img_id: str = ''.join(random.choice(chars) for _ in range(48))
        image_url: str = f'https://lh3.googleusercontent.com/a/ACg8oc{random_img_id}=s96-c'

        return {
            'user': {'name': 'BLACKBOX AI', 'email': email, 'image': image_url, 'id': numeric_id},
            'expires': expiry,
        }

    @classmethod
    async def fetch_validated(cls, url: str = 'https://www.blackbox.ai', force_refresh: bool = False) -> Optional[str]:
        """
        Извлекает валидированное значение с веб-страницы Blackbox AI.

        Args:
            url (str, optional): URL для извлечения значения. По умолчанию 'https://www.blackbox.ai'.
            force_refresh (bool, optional): Принудительное обновление кэша. По умолчанию False.

        Returns:
            Optional[str]: Валидированное значение, если оно найдено, иначе None.
        """
        cache_file: Path = Path(get_cookies_dir()) / 'blackbox.json'

        if not force_refresh and cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data: Dict[str, str] = json.load(f)
                    if data.get('validated_value'):
                        return data['validated_value']
            except Exception as ex:
                logger.debug(f'Blackbox: Ошибка при чтении кэша: {ex}')
        js_file_pattern: str = r'static/chunks/\\d{4}-[a-fA-F0-9]+\\.js'
        uuid_pattern: str = r'["\\\']([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})["\\\']'

        def is_valid_context(text: str) -> bool:
            """
            Проверяет, является ли контекст действительным.

            Args:
                text (str): Текст для проверки.

            Returns:
                bool: True, если контекст действителен, иначе False.
            """
            return any(char + '=' in text for char in 'abcdefghijklmnopqrstuvwxyz')

        async with ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None

                    page_content: str = await response.text()
                    js_files: List[str] = re.findall(js_file_pattern, page_content)

                for js_file in js_files:
                    js_url: str = f'{url}/_next/{js_file}'
                    async with session.get(js_url) as js_response:
                        if js_response.status == 200:
                            js_content: str = await js_response.text()
                            for match in re.finditer(uuid_pattern, js_content):
                                start: int = max(0, match.start() - 10)
                                end: int = min(len(js_content), match.end() + 10)
                                context: str = js_content[start : end]

                                if is_valid_context(context):
                                    validated_value: str = match.group(1)

                                    cache_file.parent.mkdir(exist_ok=True)
                                    try:
                                        with open(cache_file, 'w') as f:
                                            json.dump({'validated_value': validated_value}, f)
                                    except Exception as ex:
                                        logger.debug(f'Blackbox: Ошибка при записи кэша: {ex}')

                                    return validated_value

            except Exception as ex:
                logger.debug(f'Blackbox: Ошибка при получении validated_value: {ex}')

        return None

    @classmethod
    def generate_id(cls, length: int = 7) -> str:
        """
        Генерирует случайный идентификатор заданной длины.

        Args:
            length (int, optional): Длина идентификатора. По умолчанию 7.

        Returns:
            str: Случайный идентификатор.
        """
        chars: str = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @classmethod
    def get_models(cls) -> list:
        """
        Возвращает список доступных моделей в зависимости от статуса авторизации.
        Авторизованные пользователи получают полный список моделей.
        Неавторизованные пользователи получают только fallback_models.

        Returns:
            list: Список доступных моделей.
        """
        # Проверяем наличие действительных данных сессии в HAR файлах
        has_premium_access: bool = cls._check_premium_access()

        if has_premium_access:
            # Для авторизованных пользователей - все модели
            logger.debug(f'Blackbox: Возвращаем полный список моделей с {len(cls._all_models)} моделями')
            return cls._all_models
        else:
            # Для демо аккаунтов - только бесплатные модели
            logger.debug(f'Blackbox: Возвращаем список бесплатных моделей с {len(cls.fallback_models)} моделями')
            return cls.fallback_models

    @classmethod
    def _check_premium_access(cls) -> bool:
        """
        Проверяет наличие авторизованной сессии в HAR файлах.
        Возвращает True, если найдена действительная сессия, отличная от демо.

        Returns:
            bool: True, если у пользователя есть премиум доступ, иначе False.
        """
        try:
            har_dir: str = get_cookies_dir()
            if not os.access(har_dir, os.R_OK):
                return False

            for root, _, files in os.walk(har_dir):
                for file in files:
                    if file.endswith('.har'):
                        try:
                            with open(os.path.join(root, file), 'rb') as f:
                                har_data: dict = json.load(f)

                            for entry in har_data['log']['entries']:
                                # Проверяем только запросы к blackbox API
                                if 'blackbox.ai/api' in entry['request']['url']:
                                    if 'response' in entry and 'content' in entry['response']:
                                        content: dict = entry['response']['content']
                                        if (
                                            'text' in content
                                            and isinstance(content['text'], str)
                                            and '"user"' in content['text']
                                            and '"email"' in content['text']
                                        ):
                                            try:
                                                # Обрабатываем текст запроса
                                                text: str = content['text'].strip()
                                                if text.startswith('{') and text.endswith('}'):
                                                    text = text.replace('\\\\"', '"')
                                                    session_data: dict = json.loads(text)

                                                    # Проверяем, является ли это действительной сессией
                                                    if (
                                                        isinstance(session_data, dict)
                                                        and 'user' in session_data
                                                        and 'email' in session_data['user']
                                                    ):
                                                        # Проверяем, не является ли это демо сессией
                                                        demo_session: dict = cls.generate_session()
                                                        if (
                                                            session_data['user'].get('email')
                                                            != demo_session['user'].get('email')
                                                        ):
                                                            # Это не демо сессия, поэтому у пользователя есть премиум доступ
                                                            return True
                                            except:  # noqa: E722
                                                pass
                        except:  # noqa: E722
                            pass
            return False
        except Exception as ex:
            logger.debug(f'Blackbox: Ошибка при проверке премиум доступа: {ex}')
            return False

    # Инициализируем модели с fallback_models
    models: List[str] = fallback_models

    model_aliases: Dict[str, str] = {
        'gpt-4o': 'GPT-4o',
        'claude-3.7-sonnet': 'Claude-sonnet-3.7',
        'deepseek-v3': 'DeepSeek-V3',
        'deepseek-r1': 'DeepSeek-R1',
        'deepseek-chat': 'DeepSeek-LLM-Chat-(67B)',
    }

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        media: MediaListType = None,
        top_p: float = None,
        temperature: float = None,
        max_tokens: int = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs,
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с Blackbox AI.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            prompt (str, optional): Дополнительный промпт. По умолчанию None.
            proxy (str, optional): Прокси сервер. По умолчанию None.
            media (MediaListType, optional): Список медиа файлов. По умолчанию None.
            top_p (float, optional): Значение top_p. По умолчанию None.
            temperature (float, optional): Температура. По умолчанию None.
            max_tokens (int, optional): Максимальное количество токенов. По умолчанию None.
            conversation (Conversation, optional): Объект Conversation. По умолчанию None.
            return_conversation (bool, optional): Возвращать ли объект Conversation. По умолчанию False.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncGenerator[str | ImageResponse | Conversation, None]: Асинхронный генератор, возвращающий текст, изображения или объект Conversation.

        """
        model = cls.get_model(model)
        headers: Dict[str, str] = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.blackbox.ai',
            'referer': 'https://www.blackbox.ai/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        async with ClientSession(headers=headers) as session:
            if conversation is None or not hasattr(conversation, 'chat_id'):
                conversation = Conversation(model)
                conversation.validated_value = await cls.fetch_validated()
                conversation.chat_id = cls.generate_id()
                conversation.message_history = []

            current_messages: List[Dict[str, Any]] = []
            for i, msg in enumerate(messages):
                msg_id: str = conversation.chat_id if i == 0 and msg['role'] == 'user' else cls.generate_id()
                current_msg: Dict[str, Any] = {'id': msg_id, 'content': msg['content'], 'role': msg['role']}
                current_messages.append(current_msg)

            if media is not None:
                current_messages[-1]['data'] = {
                    'imagesData': [
                        {
                            'filePath': f'/{image_name}',
                            'contents': to_data_uri(image),
                        }
                        for image, image_name in merge_media(media, messages)
                    ],
                    'fileText': '',
                    'title': '',
                }

            # Пытаемся получить данные сессии из HAR файлов
            session_data: dict = cls.generate_session()  # Default fallback
            session_found: bool = False

            # Ищем данные сессии в HAR
            har_dir: str = get_cookies_dir()
            if os.access(har_dir, os.R_OK):
                for root, _, files in os.walk(har_dir):
                    for file in files:
                        if file.endswith('.har'):
                            try:
                                with open(os.path.join(root, file), 'rb') as f:
                                    har_data: dict = json.load(f)

                                for entry in har_data['log']['entries']:
                                    # Смотрим только ответы blackbox API
                                    if 'blackbox.ai/api' in entry['request']['url']:
                                        # Ищем ответ с правильной структурой
                                        if 'response' in entry and 'content' in entry['response']:
                                            content: dict = entry['response']['content']
                                            # Ищем как обычные сессии, так и сессии Google Auth
                                            if (
                                                'text' in content
                                                and isinstance(content['text'], str)
                                                and '"user"' in content['text']
                                                and '"email"' in content['text']
                                                and '"expires"' in content['text']
                                            ):
                                                try:
                                                    # Убираем HTML или другой не-JSON контент
                                                    text: str = content['text'].strip()
                                                    if text.startswith('{') and text.endswith('}'):
                                                        # Заменяем экранированные кавычки
                                                        text = text.replace('\\\\"', '"')
                                                        har_session: dict = json.loads(text)

                                                        # Проверяем, является ли это действительным объектом сессии (поддерживает как обычную, так и Google Auth)
                                                        if (
                                                            isinstance(har_session, dict)
                                                            and 'user' in har_session
                                                            and 'email' in har_session['user']
                                                            and 'expires' in har_session
                                                        ):
                                                            file_path: str = os.path.join(root, file)
                                                            logger.debug(f'Blackbox: Найдена сессия в HAR файле')

                                                            session_data = har_session
                                                            session_found = True
                                                            break
                                                except json.JSONDecodeError as ex:
                                                    # Выводим ошибку только для записей, которые действительно выглядят как данные сессии
                                                    if '"user"' in content['text'] and '"email"' in content['text']:
                                                        logger.debug(f'Blackbox: Ошибка при разборе вероятных данных сессии: {ex}')

                                    if session_found:
                                        break

                            except Exception as ex:
                                logger.debug(f'Blackbox: Ошибка при чтении HAR файла: {ex}')

                            if session_found:
                                break

                    if session_found:
                        break

            data: Dict[str, Any] = {
                'messages': current_messages,
                'agentMode': cls.agentMode.get(model, {}) if model in cls.agentMode else {},
                'id': conversation.chat_id,
                'previewToken': None,
                'userId': None,
                'codeModelMode': True,
                'trendingAgentMode': cls.trendingAgentMode.get(model, {}) if model in cls.trendingAgentMode else {},
                'isMicMode': False,
                'userSystemPrompt': None,
                'maxTokens': max_tokens,
                'playgroundTopP': top_p,
                'playgroundTemperature': temperature,
                'isChromeExt': False,
                'githubToken': '',
                'clickedAnswer2': False,
                'clickedAnswer3': False,
                'clickedForceWebSearch': False,
                'visitFromDelta': False,
                'isMemoryEnabled': False,
                'mobileClient': False,
                'userSelectedModel': model if model in cls.userSelectedModel else None,
                'validated': conversation.validated_value,
                'imageGenerationMode': model == cls.default_image_model,
                'webSearchModePrompt': False,
                'deepSearchMode': False,
                'domains': None,
                'vscodeClient': False,
                'codeInterpreterMode': False,
                'customProfile': {
                    'name': '',
                    'occupation': '',
                    'traits': [],
                    'additionalInfo': '',
                    'enableNewChats': False,
                },
                'session': session_data if session_data else cls.generate_session(),
                'isPremium': True,
                'subscriptionCache': None,
                'beastMode': False,
                'webSearchMode': False,
            }

            # Добавляем отладочные сообщения перед вызовом API
            if isinstance(session_data, dict) and 'user' in session_data:
                # Генерируем демо-сессию для сравнения
                demo_session: dict = cls.generate_session()
                is_demo: bool = False

                if demo_session and isinstance(demo_session, dict) and 'user' in demo_session:
                    if session_data['user'].get('email') == demo_session['user'].get('email'):
                        is_demo = True

                if is_demo:
                    logger.debug('Blackbox: Making API request with built-in Developer Premium Account')
                else:
                    user_email: str = session_data['user'].get('email', 'unknown')
                    logger.debug(f'Blackbox: Making API request with HAR session email: {user_email}')

            # Продолжаем с запросом API и асинхронным поведением генератора
            async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                await raise_for_status(response)

                # Собираем полный ответ
                full_response: List[str] = []
                async for chunk in response.content.iter_any():
                    if chunk:
                        chunk_text: str = chunk.decode()
                        full_response.append(chunk_text)
                        # Выдаем только чанки для не-графических моделей
                        if model != cls.default_image_model:
                            yield chunk_text

                full_response_text: str = ''.join(full_response)

                # Для графических моделей проверяем наличие графической разметки
                if model == cls.default_image_model:
                    image_url_match: Optional[re.Match[str]] = re.search(r'!\\[.*?\\]\\((.*?)\\)\', full_response_text)
                    if image_url_match:
                        image_url: str = image_url_match.group(1)
                        yield ImageResponse(images=[image_url], alt=format_image_prompt(messages, prompt))
                        return

                # Обрабатываем историю разговоров один раз, в одном месте
                if return_conversation:
                    conversation.message_history.append({'role': 'assistant', 'content': full_response_text})
                    yield conversation
                # Для графических моделей, которые не выдали изображение, возвращаемся к текстовому ответу
                elif model == cls.default_image_model:
                    yield full_response_text