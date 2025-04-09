### **Анализ кода модуля `Vercel.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/deprecated/Vercel.py

Модуль предоставляет класс `Vercel`, который является провайдером для взаимодействия с моделями Vercel AI.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код достаточно структурирован.
    - Присутствуют аннотации типов.
- **Минусы**:
    - Отсутствует docstring для модуля.
    - Некоторые функции не имеют docstring или не полностью документированы.
    - Не используется `logger` для логирования ошибок.
    - Присутствуют закомментированные блоки кода.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Добавить docstring для модуля**: Описать назначение модуля и предоставить примеры использования.
2.  **Добавить docstring для функций и методов**: Описать параметры, возвращаемые значения и возможные исключения.
3.  **Использовать `logger` для логирования ошибок**: Заменить `print` на `logger.error` для более эффективного логирования.
4.  **Удалить закомментированные блоки кода**: Убрать неиспользуемый код для улучшения читаемости.
5.  **Добавить аннотации типов для всех переменных**: Указать типы данных для всех переменных.
6.  **Обработка исключений**: Добавить обработку исключений с использованием `logger.error` для записи информации об ошибках.

**Оптимизированный код:**

```python
"""
Модуль для взаимодействия с моделями Vercel AI через класс Vercel.
====================================================================

Модуль содержит класс :class:`Vercel`, который предоставляет функциональность для создания запросов к Vercel AI API
и получения ответов. Поддерживает stream ответы.

Пример использования
----------------------

>>> from src.endpoints.gpt4free.g4f.Provider.deprecated.Vercel import Vercel
>>> messages = [{'role': 'user', 'content': 'Hello'}]
>>> for message in Vercel.create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
...     print(message, end='')
"""
from __future__ import annotations

import json
import base64
import requests
import random
import uuid

from typing import Messages, TypedDict, CreateResult, Any, Dict
from ..base_provider import AbstractProvider
from ...errors import MissingRequirementsError
from src.logger import logger

try:
    import execjs

    has_requirements: bool = True
except ImportError as ex:
    has_requirements: bool = False
    logger.error('Required package PyExecJS id not installed', ex, exc_info=True)


class Vercel(AbstractProvider):
    """
    Провайдер для взаимодействия с Vercel AI.
    """

    url: str = 'https://sdk.vercel.ai'
    working: bool = False
    supports_message_history: bool = True
    supports_gpt_35_turbo: bool = True
    supports_stream: bool = True

    @staticmethod
    def create_completion(
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str | None = None,
        **kwargs: Any,
    ) -> CreateResult:
        """
        Создает запрос к Vercel AI API и возвращает ответ.

        Args:
            model (str): Идентификатор модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий, следует ли использовать потоковый режим.
            proxy (str | None): Прокси-сервер для использования. По умолчанию None.
            **kwargs (Any): Дополнительные параметры.

        Returns:
            CreateResult: Объект, содержащий ответ от API.

        Raises:
            MissingRequirementsError: Если не установлен пакет "PyExecJS".
            ValueError: Если указанная модель не поддерживается Vercel.
            requests.exceptions.RequestException: При ошибке запроса к API.

        Yields:
            str: Части ответа, если stream=True.
        """
        if not has_requirements:
            raise MissingRequirementsError('Install "PyExecJS" package')

        if not model:
            model = 'gpt-3.5-turbo'
        elif model not in model_info:
            raise ValueError(f'Vercel does not support {model}')

        headers: Dict[str, str] = {
            'authority': 'sdk.vercel.ai',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'custom-encoding': get_anti_bot_token(),
            'origin': 'https://sdk.vercel.ai',
            'pragma': 'no-cache',
            'referer': 'https://sdk.vercel.ai/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.{random.randint(99, 999)}.{random.randint(99, 999)} Safari/537.36',
        }

        json_data: Dict[str, Any] = {
            'model': model_info[model]['id'],
            'messages': messages,
            'playgroundId': str(uuid.uuid4()),
            'chatIndex': 0,
            **model_info[model]['default_params'],
            **kwargs,
        }

        max_retries: int = kwargs.get('max_retries', 20)
        for _ in range(max_retries):
            try:
                response = requests.post(
                    'https://chat.vercel.ai/api/chat',
                    headers=headers,
                    json=json_data,
                    stream=True,
                    proxies={'https': proxy},
                )
                response.raise_for_status()
                for token in response.iter_content(chunk_size=None):
                    yield token.decode()
                break
            except requests.exceptions.RequestException as ex:
                logger.error('Error while sending request', ex, exc_info=True)
                continue


def get_anti_bot_token() -> str:
    """
    Генерирует anti-bot токен для защиты от автоматических запросов.

    Returns:
        str: Anti-bot токен.
    """
    headers: Dict[str, str] = {
        'authority': 'sdk.vercel.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://sdk.vercel.ai/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.{random.randint(99, 999)}.{random.randint(99, 999)} Safari/537.36',
    }

    try:
        response = requests.get('https://sdk.vercel.ai/openai.jpeg', headers=headers).text
        raw_data: Any = json.loads(base64.b64decode(response, validate=True))
        js_script: str = (
            '\'\'\'const globalThis={marker:"mark"};String.prototype.fontcolor=function(){return `<font>${this}</font>`};\n'
            "        return (%s)(%s)\'\'\'"
            % (raw_data['c'], raw_data['a'])
        )
        raw_token: str = json.dumps({'r': execjs.compile(js_script).call(''), 't': raw_data['t']}, separators=(',', ':'))
        return base64.b64encode(raw_token.encode('utf-16le')).decode()
    except requests.exceptions.RequestException as ex:
        logger.error('Error while getting anti bot token', ex, exc_info=True)
        return ''
    except Exception as ex:
        logger.error('Error while processing anti bot token', ex, exc_info=True)
        return ''


class ModelInfo(TypedDict):
    """
    Тип данных для информации о модели.
    """

    id: str
    default_params: Dict[str, Any]


model_info: Dict[str, ModelInfo] = {
    'replicate/llama70b-v2-chat': {
        'id': 'replicate:replicate/llama-2-70b-chat',
        'default_params': {
            'temperature': 0.75,
            'maximumLength': 3000,
            'topP': 1,
            'repetitionPenalty': 1,
        },
    },
    'a16z-infra/llama7b-v2-chat': {
        'id': 'replicate:a16z-infra/llama7b-v2-chat',
        'default_params': {
            'temperature': 0.75,
            'maximumLength': 3000,
            'topP': 1,
            'repetitionPenalty': 1,
        },
    },
    'a16z-infra/llama13b-v2-chat': {
        'id': 'replicate:a16z-infra/llama13b-v2-chat',
        'default_params': {
            'temperature': 0.75,
            'maximumLength': 3000,
            'topP': 1,
            'repetitionPenalty': 1,
        },
    },
    'replicate/llama-2-70b-chat': {
        'id': 'replicate:replicate/llama-2-70b-chat',
        'default_params': {
            'temperature': 0.75,
            'maximumLength': 3000,
            'topP': 1,
            'repetitionPenalty': 1,
        },
    },
    'bigscience/bloom': {
        'id': 'huggingface:bigscience/bloom',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 0.95,
            'topK': 4,
            'repetitionPenalty': 1.03,
        },
    },
    'google/flan-t5-xxl': {
        'id': 'huggingface:google/flan-t5-xxl',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 0.95,
            'topK': 4,
            'repetitionPenalty': 1.03,
        },
    },
    'EleutherAI/gpt-neox-20b': {
        'id': 'huggingface:EleutherAI/gpt-neox-20b',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 0.95,
            'topK': 4,
            'repetitionPenalty': 1.03,
            'stopSequences': [],
        },
    },
    'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5': {
        'id': 'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5',
        'default_params': {
            'maximumLength': 1024,
            'typicalP': 0.2,
            'repetitionPenalty': 1,
        },
    },
    'OpenAssistant/oasst-sft-1-pythia-12b': {
        'id': 'huggingface:OpenAssistant/oasst-sft-1-pythia-12b',
        'default_params': {
            'maximumLength': 1024,
            'typicalP': 0.2,
            'repetitionPenalty': 1,
        },
    },
    'bigcode/santacoder': {
        'id': 'huggingface:bigcode/santacoder',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 0.95,
            'topK': 4,
            'repetitionPenalty': 1.03,
        },
    },
    'command-light-nightly': {
        'id': 'cohere:command-light-nightly',
        'default_params': {
            'temperature': 0.9,
            'maximumLength': 1024,
            'topP': 1,
            'topK': 0,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'command-nightly': {
        'id': 'cohere:command-nightly',
        'default_params': {
            'temperature': 0.9,
            'maximumLength': 1024,
            'topP': 1,
            'topK': 0,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'code-davinci-002': {
        'id': 'openai:code-davinci-002',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 1,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'gpt-3.5-turbo': {
        'id': 'openai:gpt-3.5-turbo',
        'default_params': {
            'temperature': 0.7,
            'maximumLength': 4096,
            'topP': 1,
            'topK': 1,
            'presencePenalty': 1,
            'frequencyPenalty': 1,
            'stopSequences': [],
        },
    },
    'gpt-3.5-turbo-16k': {
        'id': 'openai:gpt-3.5-turbo-16k',
        'default_params': {
            'temperature': 0.7,
            'maximumLength': 16280,
            'topP': 1,
            'topK': 1,
            'presencePenalty': 1,
            'frequencyPenalty': 1,
            'stopSequences': [],
        },
    },
    'gpt-3.5-turbo-16k-0613': {
        'id': 'openai:gpt-3.5-turbo-16k-0613',
        'default_params': {
            'temperature': 0.7,
            'maximumLength': 16280,
            'topP': 1,
            'topK': 1,
            'presencePenalty': 1,
            'frequencyPenalty': 1,
            'stopSequences': [],
        },
    },
    'text-ada-001': {
        'id': 'openai:text-ada-001',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 1,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'text-babbage-001': {
        'id': 'openai:text-babbage-001',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 1,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'text-curie-001': {
        'id': 'openai:text-curie-001',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 1,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'text-davinci-002': {
        'id': 'openai:text-davinci-002',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 1024,
            'topP': 1,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
    'text-davinci-003': {
        'id': 'openai:text-davinci-003',
        'default_params': {
            'temperature': 0.5,
            'maximumLength': 4097,
            'topP': 1,
            'presencePenalty': 0,
            'frequencyPenalty': 0,
            'stopSequences': [],
        },
    },
}