### **Анализ кода модуля `ChatGpt.py`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и разбит на логические блоки.
  - Присутствует обработка ошибок при запросах к серверам.
  - Используются асинхронные операции (stream = True) для улучшения производительности.
- **Минусы**:
  - Отсутствует полная документация для всех функций и классов.
  - Некоторые переменные не имеют аннотации типов.
  - Не используются логирование для отслеживания ошибок и хода выполнения программы.
  - Не все комментарии переведены на русский язык.
  - Некоторые магические строки не вынесены в константы.

## Рекомендации по улучшению:

1.  **Добавить документацию**:
    - Добавить docstring для всех функций, методов и классов, чтобы объяснить их назначение, параметры и возвращаемые значения.
    - Перевести все docstring на русский язык и использовать формат UTF-8.
    - Для внутренних функций также добавить docstring.
2.  **Добавить аннотации типов**:
    - Указать типы для всех переменных, аргументов функций и возвращаемых значений.
    - Использовать `Optional` для переменных, которые могут быть `None`.
3.  **Использовать логирование**:
    - Заменить `print` на `logger.info`, `logger.warning`, `logger.error` для отслеживания хода выполнения программы и записи ошибок.
    - Логировать важные события, такие как успешное получение данных, ошибки при запросах и т.д.
4.  **Улучшить обработку ошибок**:
    - Логировать ошибки с использованием `logger.error` и передавать исключение как аргумент.
    - Добавить обработку исключений для всех потенциально опасных операций, таких как запросы к сети и декодирование JSON.
5.  **Рефакторинг кода**:
    - Вынести повторяющиеся значения (например, URL, заголовки) в константы.
    - Упростить логику, где это возможно, чтобы улучшить читаемость кода.
    - Переписать комментарии на более конкретные и понятные.
6.  **Безопасность**:
    - Рассмотреть возможность использования более безопасных способов хранения и передачи секретных данных, таких как токены и ключи API.
7.  **Совместимость**:
    - Проверить совместимость с разными версиями Python и библиотек.
8.  **Удалить неиспользуемые импорты**:
    - Удалить импорты, которые не используются в коде.

## Оптимизированный код:

```python
from __future__ import annotations

from typing import Messages, CreateResult, Optional
from pathlib import Path
import time
import uuid
import random
import json
from requests import Session

from src.logger import logger  # Импортируем модуль логгирования
from .openai.new import (
    get_config,
    get_answer_token,
    process_turnstile,
    get_requirements_token
)

# Константы для URL
CHATGPT_URL = 'https://chatgpt.com/'
BACKEND_ANON_SENTINEL_CHAT_REQUIREMENTS_URL = 'https://chatgpt.com/backend-anon/sentinel/chat-requirements'
BACKEND_ANON_CONVERSATION_URL = 'https://chatgpt.com/backend-anon/conversation'

# Константы для заголовков
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'


def format_conversation(messages: list) -> list:
    """
    Форматирует список сообщений для отправки в API ChatGPT.

    Args:
        messages (list): Список сообщений, где каждое сообщение - словарь с ключами 'role' и 'content'.

    Returns:
        list: Список отформатированных сообщений в виде словарей, готовых для отправки в API.
    """
    conversation = []

    for message in messages:
        conversation.append({
            'id': str(uuid.uuid4()),
            'author': {
                'role': message['role'],
            },
            'content': {
                'content_type': 'text',
                'parts': [
                    message['content'],
                ],
            },
            'metadata': {
                'serialization_metadata': {
                    'custom_symbol_offsets': [],
                },
            },
            'create_time': round(time.time(), 3),
        })

    return conversation


def init_session(user_agent: str) -> Session:
    """
    Инициализирует сессию requests с необходимыми заголовками и куками.

    Args:
        user_agent (str): User-agent для установки в заголовках сессии.

    Returns:
        Session: Инициализированная сессия requests.
    """
    session = Session()

    cookies = {
        '_dd_s': '',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-arch': '"arm"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"14.4.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
    }

    session.get(CHATGPT_URL, cookies=cookies, headers=headers)

    return session


class ChatGpt(AbstractProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с ChatGPT.
    """
    label = 'ChatGpt'
    url = CHATGPT_URL
    working = False
    supports_message_history = True
    supports_system_message = True
    supports_stream = True
    default_model = 'auto'
    models = [
        default_model,
        'gpt-3.5-turbo',
        'gpt-4o',
        'gpt-4o-mini',
        'gpt-4',
        'gpt-4-turbo',
        'chatgpt-4o-latest',
    ]

    model_aliases = {
        'gpt-4o': 'chatgpt-4o-latest',
    }

    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Возвращает модель, если она поддерживается, иначе возвращает модель по умолчанию.

        Args:
            model (str): Название модели.

        Returns:
            str: Поддерживаемая модель или модель по умолчанию.
        """
        if model in cls.models:
            return model
        elif model in cls.model_aliases:
            return cls.model_aliases[model]
        else:
            return cls.default_model

    @classmethod
    def create_completion(
            cls,
            model: str,
            messages: Messages,
            stream: bool,
            **kwargs
    ) -> CreateResult:
        """
        Создает запрос к ChatGPT и возвращает результат.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий, нужно ли использовать потоковую передачу.
            **kwargs: Дополнительные аргументы.

        Returns:
            CreateResult: Результат запроса.
        """
        model = cls.get_model(model)
        if model not in cls.models:
            raise ValueError(f'Model \'{model}\' is not available. Available models: {\', \'.join(cls.models)}')

        user_agent = DEFAULT_USER_AGENT
        session: Session = init_session(user_agent)

        config = get_config(user_agent)
        pow_req = get_requirements_token(config)
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.8',
            'content-type': 'application/json',
            'oai-device-id': f'{uuid.uuid4()}',
            'oai-language': 'en-US',
            'origin': CHATGPT_URL,
            'priority': 'u=1, i',
            'referer': CHATGPT_URL,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': f'{user_agent}'
        }

        try:
            response = session.post(
                BACKEND_ANON_SENTINEL_CHAT_REQUIREMENTS_URL,
                headers=headers,
                json={'p': pow_req}
            )
            response.raise_for_status()
        except Exception as ex:
            logger.error('Error while getting chat requirements', ex, exc_info=True)
            return

        try:
            response_data = response.json()
            if "detail" in response_data and "Unusual activity" in response_data["detail"]:
                logger.warning("Unusual activity detected")
                return

            turnstile = response_data.get('turnstile', {})
            turnstile_required = turnstile.get('required')
            pow_conf = response_data.get('proofofwork', {})

            if turnstile_required:
                turnstile_dx = turnstile.get('dx')
                turnstile_token = process_turnstile(turnstile_dx, pow_req)

            headers = {
                **headers,
                'openai-sentinel-turnstile-token': turnstile_token,
                'openai-sentinel-chat-requirements-token': response_data.get('token'),
                'openai-sentinel-proof-token': get_answer_token(
                    pow_conf.get('seed'), pow_conf.get('difficulty'), config
                )
            }

            json_data = {
                'action': 'next',
                'messages': format_conversation(messages),
                'parent_message_id': str(uuid.uuid4()),
                'model': model,
                'timezone_offset_min': -120,
                'suggestions': [
                    'Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.',
                    'Could you help me plan a relaxing day that focuses on activities for rejuvenation? To start, can you ask me what my favorite forms of relaxation are?',
                    'I have a photoshoot tomorrow. Can you recommend me some colors and outfit options that will look good on camera?',
                    'Make up a 5-sentence story about "Sharky", a tooth-brushing shark superhero. Make each sentence a bullet point.',
                ],
                'history_and_training_disabled': False,
                'conversation_mode': {
                    'kind': 'primary_assistant',
                },
                'force_paragen': False,
                'force_paragen_model_slug': '',
                'force_nulligen': False,
                'force_rate_limit': False,
                'reset_rate_limits': False,
                'websocket_request_id': str(uuid.uuid4()),
                'system_hints': [],
                'force_use_sse': True,
                'conversation_origin': None,
                'client_contextual_info': {
                    'is_dark_mode': True,
                    'time_since_loaded': random.randint(22, 33),
                    'page_height': random.randint(600, 900),
                    'page_width': random.randint(500, 800),
                    'pixel_ratio': 2,
                    'screen_height': random.randint(800, 1200),
                    'screen_width': random.randint(1200, 2000),
                },
            }

            time.sleep(2)

            response = session.post(
                BACKEND_ANON_CONVERSATION_URL,
                headers=headers,
                json=json_data,
                stream=True
            )
            response.raise_for_status()

            replace = ''
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode()

                    if decoded_line.startswith('data:'):
                        json_string = decoded_line[6:].strip()

                        if json_string == '[DONE]':
                            break

                        if json_string:
                            try:
                                data = json.loads(json_string)
                            except json.JSONDecodeError as ex:
                                logger.error('Error decoding JSON', ex, exc_info=True)
                                continue

                            if data.get('message') and data['message'].get('author'):
                                role = data['message']['author'].get('role')
                                if role == 'assistant':
                                    tokens = data['message']['content'].get('parts', [])
                                    if tokens:
                                        yield tokens[0].replace(replace, '')
                                        replace = tokens[0]
        except Exception as ex:
            logger.error('Error during conversation', ex, exc_info=True)
            yield 'Произошла ошибка во время разговора. Пожалуйста, попробуйте еще раз.'