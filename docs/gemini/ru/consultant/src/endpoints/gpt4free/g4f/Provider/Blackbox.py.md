### **Анализ кода модуля `Blackbox.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/Blackbox.py

Модуль содержит класс `Blackbox`, который является асинхронным генератором провайдера для взаимодействия с Blackbox AI. Он поддерживает потоковую передачу, системные сообщения и историю сообщений. Класс предоставляет методы для генерации сессий, получения моделей и проверки премиум-доступа.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Поддержка различных моделей и режимов агентов.
  - Реализация проверки премиум-доступа через HAR файлы.
  - Использование асинхронных запросов для неблокирующего взаимодействия.
- **Минусы**:
  - Повторяющийся код для генерации сессий.
  - Отсутствие обработки ошибок при чтении/записи файлов HAR.
  - Смешивание логики извлечения данных из HAR файлов и обработки API запросов.

**Рекомендации по улучшению:**

1. **Улучшение структуры и переиспользование кода**:
   - Методы `generate_session` и `fetch_validated` дублируются. Необходимо вынести их в отдельные утилиты или использовать один раз и передавать результат.
   - Оптимизировать логику извлечения данных из HAR файлов, выделив её в отдельные функции для повышения читаемости и удобства обслуживания.

2. **Документация**:
   - Добавить docstring для каждой функции, объясняющий её назначение, аргументы и возвращаемые значения.
   - Добавить комментарии для сложных логических блоков, чтобы облегчить понимание кода.

3. **Обработка ошибок**:
   - В блоках `try...except` добавить логирование ошибок с использованием `logger.error` для более детальной отладки.
   - Улучшить обработку ошибок при чтении/записи файлов HAR, чтобы избежать неожиданных сбоев.

4. **Безопасность**:
   - Рассмотреть возможность использования более безопасных методов хранения и обработки HAR файлов.

5. **Аннотации типов**:
   - Убедиться, что все переменные и параметры функций аннотированы типами.

6. **Улучшение логики `_check_premium_access`**:
   - Сделать код более читаемым, разбив его на более мелкие функции.
   - Добавить обработку исключений для каждого шага, чтобы избежать неожиданных сбоев.
   - Пересмотреть логику определения премиум-доступа, чтобы сделать её более надежной.

**Оптимизированный код:**

```python
"""
Модуль для работы с провайдером Blackbox AI.
===========================================

Модуль содержит класс :class:`Blackbox`, который является асинхронным генератором провайдера для взаимодействия с Blackbox AI.
Он поддерживает потоковую передачу, системные сообщения и историю сообщений.
Класс предоставляет методы для генерации сессий, получения моделей и проверки премиум-доступа.
"""
from __future__ import annotations

from aiohttp import ClientSession
import os
import re
import json
import random
import string
import base64
from pathlib import Path
from typing import Optional, List, Dict, AsyncGenerator, Any
from datetime import datetime, timedelta

from ..typing import AsyncResult, Messages, MediaListType
from ..requests.raise_for_status import raise_for_status
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..image import to_data_uri
from ..cookies import get_cookies_dir
from .helper import format_image_prompt
from ..providers.response import JsonConversation, ImageResponse
from ..tools.media import merge_media
from .. import debug
from src.logger import logger

class Conversation(JsonConversation):
    validated_value: str = None
    chat_id: str = None
    message_history: Messages = []

    def __init__(self, model: str):
        self.model = model

class Blackbox(AsyncGeneratorProvider, ProviderModelMixin):
    label = "Blackbox AI"
    url = "https://www.blackbox.ai"
    api_endpoint = "https://www.blackbox.ai/api/chat"
    
    working = True
    supports_stream = True
    supports_system_message = True
    supports_message_history = True
    
    default_model = "blackboxai"
    default_vision_model = default_model
    default_image_model = 'flux'
    
    # Completely free models
    fallback_models = [
        "blackboxai", 
        "blackboxai-pro",
        "gpt-4o-mini", 
        "GPT-4o", 
        "o1", 
        "o3-mini", 
        "Claude-sonnet-3.7", 
        "DeepSeek-V3", 
        "DeepSeek-R1", 
        "DeepSeek-LLM-Chat-(67B)",
        # Image models
        "flux",
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
        'Heroku Agent'
    ]
    
    image_models = [default_image_model]   
    vision_models = [default_vision_model, 'GPT-4o', 'o1', 'o3-mini', 'Gemini-PRO', 'Gemini Agent', 'llama-3.1-8b Agent', 'llama-3.1-70b Agent', 'llama-3.1-405 Agent', 'Gemini-Flash-2.0', 'DeepSeek-V3']

    userSelectedModel = ['GPT-4o', 'o1', 'o3-mini', 'Gemini-PRO', 'Claude-sonnet-3.7', 'DeepSeek-V3', 'DeepSeek-R1', 'Meta-Llama-3.3-70B-Instruct-Turbo', 'Mistral-Small-24B-Instruct-2501', 'DeepSeek-LLM-Chat-(67B)', 'DBRX-Instruct', 'Qwen-QwQ-32B-Preview', 'Nous-Hermes-2-Mixtral-8x7B-DPO', 'Gemini-Flash-2.0']

    # Agent mode configurations
    agentMode = {
        'GPT-4o': {'mode': True, 'id': "GPT-4o", 'name': "GPT-4o"},
        'Gemini-PRO': {'mode': True, 'id': "Gemini-PRO", 'name': "Gemini-PRO"},
        'Claude-sonnet-3.7': {'mode': True, 'id': "Claude-sonnet-3.7", 'name': "Claude-sonnet-3.7"},
        'DeepSeek-V3': {'mode': True, 'id': "deepseek-chat", 'name': "DeepSeek-V3"},
        'DeepSeek-R1': {'mode': True, 'id': "deepseek-reasoner", 'name': "DeepSeek-R1"},
        'Meta-Llama-3.3-70B-Instruct-Turbo': {'mode': True, 'id': "meta-llama/Llama-3.3-70B-Instruct-Turbo", 'name': "Meta-Llama-3.3-70B-Instruct-Turbo"},
        'Gemini-Flash-2.0': {'mode': True, 'id': "Gemini/Gemini-Flash-2.0", 'name': "Gemini-Flash-2.0"},
        'Mistral-Small-24B-Instruct-2501': {'mode': True, 'id': "mistralai/Mistral-Small-24B-Instruct-2501", 'name': "Mistral-Small-24B-Instruct-2501"},
        'DeepSeek-LLM-Chat-(67B)': {'mode': True, 'id': "deepseek-ai/deepseek-llm-67b-chat", 'name': "DeepSeek-LLM-Chat-(67B)"},
        'DBRX-Instruct': {'mode': True, 'id': "databricks/dbrx-instruct", 'name': "DBRX-Instruct"},
        'Qwen-QwQ-32B-Preview': {'mode': True, 'id': "Qwen/QwQ-32B-Preview", 'name': "Qwen-QwQ-32B-Preview"},
        'Nous-Hermes-2-Mixtral-8x7B-DPO': {'mode': True, 'id': "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", 'name': "Nous-Hermes-2-Mixtral-8x7B-DPO"},
    }

    # Trending agent modes
    trendingAgentMode = {
        'blackboxai-pro': {'mode': True, 'id': "BLACKBOXAI-PRO"},
        "Gemini Agent": {'mode': True, 'id': 'gemini'},
        "llama-3.1-405 Agent": {'mode': True, 'id': "llama-3.1-405"},
        'llama-3.1-70b Agent': {'mode': True, 'id': "llama-3.1-70b"},
        'llama-3.1-8b Agent': {'mode': True, 'id': "llama-3.1-8b"},
        'Python Agent': {'mode': True, 'id': "python"},
        'HTML Agent': {'mode': True, 'id': "html"},
        'Builder Agent': {'mode': True, 'id': "builder"},
        'Java Agent': {'mode': True, 'id': "java"},
        'JavaScript Agent': {'mode': True, 'id': "javascript"},
        'React Agent': {'mode': True, 'id': "react"},
        'Android Agent': {'mode': True, 'id': "android"},
        'Flutter Agent': {'mode': True, 'id': "flutter"},
        'Next.js Agent': {'mode': True, 'id': "next.js"},
        'AngularJS Agent': {'mode': True, 'id': "angularjs"},
        'Swift Agent': {'mode': True, 'id': "swift"},
        'MongoDB Agent': {'mode': True, 'id': "mongodb"},
        'PyTorch Agent': {'mode': True, 'id': "pytorch"},
        'Xcode Agent': {'mode': True, 'id': "xcode"},
        'Azure Agent': {'mode': True, 'id': "azure"},
        'Bitbucket Agent': {'mode': True, 'id': "bitbucket"},
        'DigitalOcean Agent': {'mode': True, 'id': "digitalocean"},
        'Docker Agent': {'mode': True, 'id': "docker"},
        'Electron Agent': {'mode': True, 'id': "electron"},
        'Erlang Agent': {'mode': True, 'id': "erlang"},
        'FastAPI Agent': {'mode': True, 'id': "fastapi"},
        'Firebase Agent': {'mode': True, 'id': "firebase"},
        'Flask Agent': {'mode': True, 'id': "flask"},
        'Git Agent': {'mode': True, 'id': "git"},
        'Gitlab Agent': {'mode': True, 'id': "gitlab"},
        'Go Agent': {'mode': True, 'id': "go"},
        'Godot Agent': {'mode': True, 'id': "godot"},
        'Google Cloud Agent': {'mode': True, 'id': "googlecloud"},
        'Heroku Agent': {'mode': True, 'id': "heroku"},
    }
    
    # Complete list of all models (for authorized users)
    _all_models = list(dict.fromkeys([
        default_model,
        *userSelectedModel,
        *image_models,
        *list(agentMode.keys()),
        *list(trendingAgentMode.keys())
    ]))
    
    @classmethod
    def generate_session(cls, id_length: int = 21, days_ahead: int = 365) -> dict[str, Any]:
        """
        Генерирует динамическую сессию с правильным ID и форматом срока действия.
        
        Args:
            id_length (int): Длина числового ID (по умолчанию: 21).
            days_ahead (int): Количество дней до истечения срока действия (по умолчанию: 365).
        
        Returns:
            dict[str, Any]: Словарь сессии с информацией о пользователе и сроком действия.
        
        Example:
            >>> Blackbox.generate_session(id_length=21, days_ahead=365)
            {'user': {'name': 'BLACKBOX AI', 'email': 'gisele@blackbox.ai', 'image': 'https://lh3.googleusercontent.com/a/ACg8oc...', 'id': '...'}, 'expires': '2024-12-31T23:59:59.999Z'}
        """
        # Генерируем числовой ID
        numeric_id = ''.join(random.choice('0123456789') for _ in range(id_length))
        
        # Генерируем дату истечения срока действия
        future_date = datetime.now() + timedelta(days=days_ahead)
        expiry = future_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        # Декодируем закодированный email
        encoded_email = "Z2lzZWxlQGJsYWNrYm94LmFp"  # Base64 encoded email
        email = base64.b64decode(encoded_email).decode('utf-8')
        
        # Генерируем случайный ID изображения для нового формата URL
        chars = string.ascii_letters + string.digits + "-"
        random_img_id = ''.join(random.choice(chars) for _ in range(48))
        image_url = f"https://lh3.googleusercontent.com/a/ACg8oc{random_img_id}=s96-c"
        
        return {
            "user": {
                "name": "BLACKBOX AI", 
                "email": email, 
                "image": image_url, 
                "id": numeric_id
            }, 
            "expires": expiry
        }

    @classmethod
    async def fetch_validated(cls, url: str = "https://www.blackbox.ai", force_refresh: bool = False) -> Optional[str]:
        """
        Получает валидированное значение из кэша или извлекает его с веб-страницы.

        Args:
            url (str, optional): URL для извлечения валидированного значения. По умолчанию "https://www.blackbox.ai".
            force_refresh (bool, optional): Принудительно обновить кэш. По умолчанию False.

        Returns:
            Optional[str]: Валидированное значение или None в случае ошибки.
        
        Raises:
            Exception: Если возникает ошибка при чтении кэша или извлечении данных.
        
        Example:
            >>> await Blackbox.fetch_validated()
            'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
        """
        cache_file = Path(get_cookies_dir()) / 'blackbox.json'
        
        if not force_refresh and cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    if data.get('validated_value'):
                        return data['validated_value']
            except Exception as ex:
                logger.error(f"Blackbox: Error reading cache: {ex}", exc_info=True)
        
        js_file_pattern = r'static/chunks/\\d{4}-[a-fA-F0-9]+\\.js'
        uuid_pattern = r'["\\\']([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})["\\\']'

        def is_valid_context(text: str) -> bool:
            """
            Проверяет, является ли контекст действительным.

            Args:
                text (str): Контекст для проверки.

            Returns:
                bool: True, если контекст действителен, иначе False.
            """
            return any(char + '=' in text for char in 'abcdefghijklmnopqrstuvwxyz')

        async with ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None

                    page_content = await response.text()
                    js_files = re.findall(js_file_pattern, page_content)

                for js_file in js_files:
                    js_url = f"{url}/_next/{js_file}"
                    async with session.get(js_url) as js_response:
                        if js_response.status == 200:
                            js_content = await js_response.text()
                            for match in re.finditer(uuid_pattern, js_content):
                                start = max(0, match.start() - 10)
                                end = min(len(js_content), match.end() + 10)
                                context = js_content[start:end]

                                if is_valid_context(context):
                                    validated_value = match.group(1)
                                    
                                    cache_file.parent.mkdir(exist_ok=True)
                                    try:
                                        with open(cache_file, 'w') as f:
                                            json.dump({'validated_value': validated_value}, f)
                                    except Exception as ex:
                                        logger.error(f"Blackbox: Error writing cache: {ex}", exc_info=True)
                                        
                                    return validated_value

            except Exception as ex:
                logger.error(f"Blackbox: Error retrieving validated_value: {ex}", exc_info=True)

        return None

    @classmethod
    def generate_id(cls, length: int = 7) -> str:
        """
        Генерирует случайный идентификатор заданной длины.

        Args:
            length (int, optional): Длина идентификатора. По умолчанию 7.

        Returns:
            str: Случайный идентификатор.
        
        Example:
            >>> Blackbox.generate_id(length=7)
            'abc1234'
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    @classmethod
    def get_models(cls) -> list[str]:
        """
        Возвращает список доступных моделей в зависимости от статуса авторизации.
        Авторизованные пользователи получают полный список моделей.
        Неавторизованные пользователи получают только fallback_models.

        Returns:
            list[str]: Список доступных моделей.
        
        Example:
            >>> Blackbox.get_models()
            ['blackboxai', 'gpt-4o-mini', ...]
        """
        # Проверяем наличие действительных данных сессии в HAR файлах
        has_premium_access = cls._check_premium_access()
        
        if has_premium_access:
            # Для авторизованных пользователей - все модели
            debug.log(f"Blackbox: Returning full model list with {len(cls._all_models)} models")
            return cls._all_models
        else:
            # Для демо-аккаунтов - только бесплатные модели
            debug.log(f"Blackbox: Returning free model list with {len(cls.fallback_models)} models")
            return cls.fallback_models
    
    @classmethod
    def _check_premium_access(cls) -> bool:
        """
        Проверяет наличие авторизованной сессии в HAR файлах.
        Возвращает True, если найдена действительная сессия, отличающаяся от демо-сессии.

        Returns:
            bool: True, если премиум-доступ подтвержден, иначе False.
        """
        try:
            har_dir = get_cookies_dir()
            if not os.access(har_dir, os.R_OK):
                return False
                
            for root, _, files in os.walk(har_dir):
                for file in files:
                    if file.endswith(".har"):
                        try:
                            with open(os.path.join(root, file), 'rb') as f:
                                har_data = json.load(f)
                                
                            for entry in har_data['log']['entries']:
                                # Проверяем только запросы к blackbox API
                                if 'blackbox.ai/api' in entry['request']['url']:
                                    if 'response' in entry and 'content' in entry['response']:
                                        content = entry['response']['content']
                                        if ('text' in content and 
                                            isinstance(content['text'], str) and 
                                            '"user"' in content['text'] and 
                                            '"email"' in content['text']):
                                            
                                            try:
                                                # Обрабатываем текст запроса
                                                text = content['text'].strip()
                                                if text.startswith('{') and text.endswith('}'):
                                                    text = text.replace('\\\\"', '"')
                                                    session_data = json.loads(text)
                                                    
                                                    # Проверяем, является ли это действительной сессией
                                                    if (isinstance(session_data, dict) and 
                                                        'user' in session_data and 
                                                        'email' in session_data['user']):
                                                        
                                                        # Проверяем, не является ли это демо-сессией
                                                        demo_session = cls.generate_session()
                                                        if (session_data['user'].get('email') != 
                                                            demo_session['user'].get('email')):
                                                            # Это не демо-сессия, значит, у пользователя есть премиум-доступ
                                                            return True
                                            except json.JSONDecodeError as ex:
                                                # Печатаем ошибку только для записей, которые действительно выглядят как данные сессии
                                                if ('"user"' in content['text'] and 
                                                    '"email"' in content['text']):
                                                    logger.error(f"Blackbox: Error parsing likely session data: {ex}", exc_info=True)
                                        
                                    if session_found:
                                        break
                                        
                        except Exception as ex:
                            logger.error(f"Blackbox: Error reading HAR file: {ex}", exc_info=True)
                            
                            if session_found:
                                break
                                
                    if session_found:
                        break

            return False
        except Exception as ex:
            logger.error(f"Blackbox: Error checking premium access: {ex}", exc_info=True)
            return False
    
    # Initialize models with fallback_models
    models = fallback_models
    
    model_aliases = {
        "gpt-4o": "GPT-4o",
        "claude-3.7-sonnet": "Claude-sonnet-3.7",
        "deepseek-v3": "DeepSeek-V3",
        "deepseek-r1": "DeepSeek-R1",
        "deepseek-chat": "DeepSeek-LLM-Chat-(67B)",
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
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с Blackbox AI.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            prompt (str, optional): Промт для отправки. По умолчанию None.
            proxy (str, optional): Прокси для использования. По умолчанию None.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию None.
            top_p (float, optional): Значение top_p. По умолчанию None.
            temperature (float, optional): Значение temperature. По умолчанию None.
            max_tokens (int, optional): Максимальное количество токенов. По умолчанию None.
            conversation (Conversation, optional): Объект Conversation. По умолчанию None.
            return_conversation (bool, optional): Возвращать ли объект Conversation. По умолчанию False.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncGenerator[str | ImageResponse | Conversation, None]: Асинхронный генератор.

        Raises:
            Exception: Если возникает ошибка при создании генератора.
        """
        model = cls.get_model(model)
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.blackbox.ai',
            'referer': 'https://www.blackbox.ai/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        
        async with ClientSession(headers=headers) as session:
            if conversation is None or not hasattr(conversation, "chat_id"):
                conversation = Conversation(model)
                conversation.validated_value = await cls.fetch_validated()
                conversation.chat_id = cls.generate_id()
                conversation.message_history = []

            current_messages = []
            for i, msg in enumerate(messages):
                msg_id = conversation.chat_id if i == 0 and msg["role"] == "user" else cls.generate_id()
                current_msg = {
                    "id": msg_id,
                    "content": msg["content"],
                    "role": msg["role"]
                }
                current_messages.append(current_msg)

            if media is not None:
                current_messages[-1]['data'] = {
                    "imagesData": [
                        {
                            "filePath": f"/{image_name}",
                            "contents": to_data_uri(image)
                        }
                        for image, image_name in merge_media(media, messages)
                    ],
                    "fileText": "",
                    "title": ""
                }

            # Try to get session data from HAR files
            session_data = cls.generate_session()  # Default fallback
            session_found = False

            # Look for HAR session data
            har_dir = get_cookies_dir()
            if os.access(har_dir, os.R_OK):
                for root, _, files in os.walk(har_dir):
                    for file in files:
                        if file.endswith(".har"):
                            try:
                                with open(os.path.join(root, file), 'rb') as f:
                                    har_data = json.load(f)
                                    
                                for entry in har_data['log']['entries']:
                                    # Only look at blackbox API responses
                                    if 'blackbox.ai/api' in entry['request']['url']:
                                        # Look for a response that has the right structure
                                        if 'response' in entry and 'content' in entry['response']:
                                            content = entry['response']['content']
                                            # Look for both regular and Google auth session formats
                                            if ('text' in content and 
                                                isinstance(content['text'], str) and 
                                                '"user"' in content['text'] and 
                                                '"email"' in content['text'] and
                                                '"expires"' in content['text']):
                                                
                                                try:
                                                    # Remove any HTML or other non-JSON content
                                                    text = content['text'].strip()
                                                    if text.startswith('{') and text.endswith('}'):
                                                        # Replace escaped quotes
                                                        text = text.replace('\\\\"', '"')
                                                        har_session = json.loads(text)
                                                        
                                                        # Check if this is a valid session object (supports both regular and Google auth)
                                                        if (isinstance(har_session, dict) and 
                                                            'user' in har_session and 
                                                            'email' in har_session['user'] and
                                                            'expires' in har_session):
                                                            
                                                            file_path = os.path.join(root, file)
                                                            debug.log(f"Blackbox: Found session in HAR file")
                                                            
                                                            session_data = har_session
                                                            session_found = True
                                                            break
                                                except json.JSONDecodeError as ex:
                                                    # Only print error for entries that truly look like session data
                                                    if ('"user"' in content['text'] and 
                                                        '"email"' in content['text']):
                                                        logger.error(f"Blackbox: Error parsing likely session data: {ex}", exc_info=True)
                                        
                                    if session_found:
                                        break
                                        
                            except Exception as ex:
                                logger.error(f"Blackbox: Error reading HAR file: {ex}", exc_info=True)
                            
                            if session_found:
                                break
                                
                    if session_found:
                        break

            data = {
                "messages": current_messages,
                "agentMode": cls.agentMode.get(model, {}) if model in cls.agentMode else {},
                "id": conversation.chat_id,
                "previewToken": None,
                "userId": None,
                "codeModelMode": True,
                "trendingAgentMode": cls.trendingAgentMode.get(model, {}) if model in cls.trendingAgentMode else {},
                "isMicMode": False,
                "userSystemPrompt": None,
                "maxTokens": max_tokens,
                "playgroundTopP": top_p,
                "playgroundTemperature": temperature,
                "isChromeExt": False,
                "githubToken": "",
                "clickedAnswer2": False,
                "clickedAnswer3": False,
                "clickedForceWebSearch": False,
                "visitFromDelta": False,
                "isMemoryEnabled": False,
                "mobileClient": False,
                "userSelectedModel": model if model in cls.userSelectedModel else None,
                "validated": conversation.validated_value,
                "imageGenerationMode": model == cls.default_image_model,
                "webSearchModePrompt": False,
                "deepSearchMode": False,
                "domains": None,
                "vscodeClient": False,
                "codeInterpreterMode": False,
                "customProfile": {
                    "name": "",
                    "occupation": "",
                    "traits": [],
                    "additionalInfo": "",
                    "enableNewChats": False
                },
                "session": session_data if session_data else cls.generate_session(),
                "isPremium": True, 
                "subscriptionCache": None,
                "beastMode": False,
                "webSearchMode": False
            }

            # Add debugging before making the API call
            if isinstance(session_data, dict) and 'user' in session_data:
                # Генеруємо демо-сесію для порівняння
                demo_session = cls.generate_session()
                is_demo = False
                
                if demo_session and isinstance(demo_session, dict) and 'user' in demo_session:
                    if session_data['user'].get('email') == demo_session['user'].get('email'):
                        is_demo = True
                
                if is_demo:
                    debug.log(f"Blackbox: Making API request with built-in Developer Premium Account")
                else:
                    user_email = session_data['user'].get('email', 'unknown')
                    debug.log(f"Blackbox: Making API request with HAR session email: {user_email}")
                
            # Continue with the API request and async generator behavior
            async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                await raise_for_status(response)
                
                # Collect the full response
                full_response = []
                async for chunk in response.content.iter_any():
                    if chunk:
                        chunk_text = chunk.decode()
                        full_response.append(chunk_text)
                        # Only yield chunks for non-image models
                        if model != cls.default_image_model:
                            yield chunk_text
                
                full_response_text = ''.join(full_response)
                
                # For image models, check for image markdown
                if model == cls.default_image_model:
                    image_url_match = re.search(r'!\\[.*?\\]\\((.*?)\\)\', full_response_text)
                    if image_url_match:
                        image_url = image_url_match.group(1)
                        yield ImageResponse(images=[image_url], alt=format_image_prompt(messages, prompt))
                        return
                
                # Handle conversation history once, in one place
                if return_conversation:
                    conversation.message_history.append({"role": "assistant", "content": full_response_text})
                    yield conversation
                # For image models that didn't produce an image, fall back to text response
                elif model == cls.default_image_model:
                    yield full_response_text