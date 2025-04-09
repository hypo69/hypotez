### **Анализ кода модуля `Vercel.py`**

---

#### **1. Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код разбит на логические блоки, что облегчает его понимание.
  - Используются стандартные библиотеки, такие как `json`, `base64`, `execjs`, `queue` и `threading`.
  - Присутствует обработка исключений.
- **Минусы**:
  - Отсутствует документация в формате docstring для функций и классов.
  - Не используются аннотации типов для переменных и возвращаемых значений функций.
  - Смешанный стиль кавычек (используются как одинарные, так и двойные кавычки).
  - Отсутствует логирование ошибок и информации о работе программы.
  - Не везде добавлены пробелы вокруг операторов присваивания.
  - Функция `_create_completion` содержит закомментированный код и заглушку `yield 'Vercel is currently not working.'`.
  - Не используется модуль `logger` из `src.logger`.
  - Не используется `j_loads` для чтения `json` файлов
  - Не используется `Driver` для работы с `webdriver`

#### **2. Рекомендации по улучшению:**

- Добавить docstring для всех функций и классов, включая описание аргументов, возвращаемых значений и возможных исключений.
- Использовать аннотации типов для всех переменных и возвращаемых значений функций.
- Привести все строки к единому стилю кавычек (одинарные).
- Добавить логирование для отслеживания ошибок и хода выполнения программы с использованием модуля `logger` из `src.logger`.
- Устранить смешанный стиль использования пробелов вокруг операторов присваивания.
- Разобраться с закомментированным кодом в функции `_create_completion` и либо удалить его, либо доработать и включить в работу.
- Использовать `j_loads` для чтения `json` файлов
- Избавиться от хардкода URL-ов, вынести в переменные окружения.
- Обеспечить обработку ошибок с использованием `logger.error` и передачей исключения `ex`.
- Добавить обработки исключений, которые могут возникнуть в разных частях кода.
- Удалить неиспользуемые импорты.
- Добавить пояснения в комментариях к сложным участкам кода.
- Улучшить обработку ошибок в блоке `request_thread`, чтобы логировать ошибки и не замалчивать их.
- Использовать `with` для управления сессиями `requests`, чтобы обеспечить корректное закрытие соединений.

#### **3. Оптимизированный код:**

```python
"""
Модуль для работы с Vercel Provider
======================================

Модуль содержит класс :class:`Client`, который используется для взаимодействия с API Vercel.
"""

import os
import json
import base64
import execjs
import queue
import threading
from typing import Dict, Generator, List, Optional

from curl_cffi import requests

from src.logger import logger

url: str = 'https://play.vercel.ai'
supports_stream: bool = True
needs_auth: bool = False

models: Dict[str, str] = {
    'claude-instant-v1': 'anthropic:claude-instant-v1',
    'claude-v1': 'anthropic:claude-v1',
    'alpaca-7b': 'replicate:replicate/alpaca-7b',
    'stablelm-tuned-alpha-7b': 'replicate:stability-ai/stablelm-tuned-alpha-7b',
    'bloom': 'huggingface:bigscience/bloom',
    'bloomz': 'huggingface:bigscience/bloomz',
    'flan-t5-xxl': 'huggingface:google/flan-t5-xxl',
    'flan-ul2': 'huggingface:google/flan-ul2',
    'gpt-neox-20b': 'huggingface:EleutherAI/gpt-neox-20b',
    'oasst-sft-4-pythia-12b-epoch-3.5': 'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5',
    'santacoder': 'huggingface:bigcode/santacoder',
    'command-medium-nightly': 'cohere:command-medium-nightly',
    'command-xlarge-nightly': 'cohere:command-xlarge-nightly',
    'code-cushman-001': 'openai:code-cushman-001',
    'code-davinci-002': 'openai:code-davinci-002',
    'gpt-3.5-turbo': 'openai:gpt-3.5-turbo',
    'text-ada-001': 'openai:text-ada-001',
    'text-babbage-001': 'openai:text-babbage-001',
    'text-curie-001': 'openai:text-curie-001',
    'text-davinci-002': 'openai:text-davinci-002',
    'text-davinci-003': 'openai:text-davinci-003'
}
model: List[str] = list(models.keys())

vercel_models: Dict[str, Dict] = {
    'anthropic:claude-instant-v1': {'id': 'anthropic:claude-instant-v1', 'provider': 'anthropic', 'providerHumanName': 'Anthropic', 'makerHumanName': 'Anthropic', 'minBillingTier': 'hobby', 'parameters': {'temperature': {'value': 1, 'range': [0, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'topK': {'value': 1, 'range': [1, 500]}, 'presencePenalty': {'value': 1, 'range': [0, 1]}, 'frequencyPenalty': {'value': 1, 'range': [0, 1]}, 'stopSequences': {'value': ['\n\nHuman:'], 'range': []}}, 'name': 'claude-instant-v1'},
    'anthropic:claude-v1': {'id': 'anthropic:claude-v1', 'provider': 'anthropic', 'providerHumanName': 'Anthropic', 'makerHumanName': 'Anthropic', 'minBillingTier': 'hobby', 'parameters': {'temperature': {'value': 1, 'range': [0, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'topK': {'value': 1, 'range': [1, 500]}, 'presencePenalty': {'value': 1, 'range': [0, 1]}, 'frequencyPenalty': {'value': 1, 'range': [0, 1]}, 'stopSequences': {'value': ['\n\nHuman:'], 'range': []}}, 'name': 'claude-v1'},
    'replicate:replicate/alpaca-7b': {'id': 'replicate:replicate/alpaca-7b', 'provider': 'replicate', 'providerHumanName': 'Replicate', 'makerHumanName': 'Stanford', 'parameters': {'temperature': {'value': 0.75, 'range': [0.01, 5]}, 'maximumLength': {'value': 200, 'range': [50, 512]}, 'topP': {'value': 0.95, 'range': [0.01, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'repetitionPenalty': {'value': 1.1765, 'range': [0.01, 5]}, 'stopSequences': {'value': [], 'range': []}}, 'version': '2014ee1247354f2e81c0b3650d71ca715bc1e610189855f134c30ecb841fae21', 'name': 'alpaca-7b'},
    'replicate:stability-ai/stablelm-tuned-alpha-7b': {'id': 'replicate:stability-ai/stablelm-tuned-alpha-7b', 'provider': 'replicate', 'makerHumanName': 'StabilityAI', 'providerHumanName': 'Replicate', 'parameters': {'temperature': {'value': 0.75, 'range': [0.01, 5]}, 'maximumLength': {'value': 200, 'range': [50, 512]}, 'topP': {'value': 0.95, 'range': [0.01, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'repetitionPenalty': {'value': 1.1765, 'range': [0.01, 5]}, 'stopSequences': {'value': [], 'range': []}}, 'version': '4a9a32b4fd86c2d047f1d271fa93972683ec6ef1cf82f402bd021f267330b50b', 'name': 'stablelm-tuned-alpha-7b'},
    'huggingface:bigscience/bloom': {'id': 'huggingface:bigscience/bloom', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'BigScience', 'instructions': "Do NOT talk to Bloom as an entity, it's not a chatbot but a webpage/blog/article completion model. For the best results: mimic a few words of a webpage similar to the content you want to generate. Start a sentence as if YOU were writing a blog, webpage, math post, coding article and Bloom will generate a coherent follow-up.", 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'bloom'},
    'huggingface:bigscience/bloomz': {'id': 'huggingface:bigscience/bloomz', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'BigScience', 'instructions': 'We recommend using the model to perform tasks expressed in natural language. For example, given the prompt "Translate to English: Je t\'aime.", the model will most likely answer "I love you."', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'bloomz'},
    'huggingface:google/flan-t5-xxl': {'id': 'huggingface:google/flan-t5-xxl', 'provider': 'huggingface', 'makerHumanName': 'Google', 'providerHumanName': 'HuggingFace', 'name': 'flan-t5-xxl', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}},
    'huggingface:google/flan-ul2': {'id': 'huggingface:google/flan-ul2', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'Google', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'flan-ul2'},
    'huggingface:EleutherAI/gpt-neox-20b': {'id': 'huggingface:EleutherAI/gpt-neox-20b', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'EleutherAI', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'gpt-neox-20b'},
    'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5': {'id': 'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'OpenAssistant', 'parameters': {'maximumLength': {'value': 200, 'range': [50, 1024]}, 'typicalP': {'value': 0.2, 'range': [0.1, 0.99]}, 'repetitionPenalty': {'value': 1, 'range': [0.1, 2]}}, 'name': 'oasst-sft-4-pythia-12b-epoch-3.5'},
    'huggingface:bigcode/santacoder': {
        'id': 'huggingface:bigcode/santacoder', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'BigCode', 'instructions': 'The model was trained on GitHub code. As such it is not an instruction model and commands like "Write a function that computes the square root." do not work well. You should phrase commands like they occur in source code such as comments (e.g. # the following function computes the sqrt) or write a function signature and docstring and let the model complete the function body.', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'santacoder'},
    'cohere:command-medium-nightly': {'id': 'cohere:command-medium-nightly', 'provider': 'cohere', 'providerHumanName': 'Cohere', 'makerHumanName': 'Cohere', 'name': 'command-medium-nightly', 'parameters': {'temperature': {'value': 0.9, 'range': [0, 2]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0, 1]}, 'topK': {'value': 0, 'range': [0, 500]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'cohere:command-xlarge-nightly': {'id': 'cohere:command-xlarge-nightly', 'provider': 'cohere', 'providerHumanName': 'Cohere', 'makerHumanName': 'Cohere', 'name': 'command-xlarge-nightly', 'parameters': {'temperature': {'value': 0.9, 'range': [0, 2]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0, 1]}, 'topK': {'value': 0, 'range': [0, 500]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:gpt-4': {'id': 'openai:gpt-4', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'gpt-4', 'minBillingTier': 'pro', 'parameters': {'temperature': {'value': 0.7, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:code-cushman-001': {'id': 'openai:code-cushman-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'code-cushman-001'},
    'openai:code-davinci-002': {'id': 'openai:code-davinci-002', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'code-davinci-002'},
    'openai:gpt-3.5-turbo': {'id': 'openai:gpt-3.5-turbo', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'parameters': {'temperature': {'value': 0.7, 'range': [0, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'topK': {'value': 1, 'range': [1, 500]}, 'presencePenalty': {'value': 1, 'range': [0, 1]}, 'frequencyPenalty': {'value': 1, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'gpt-3.5-turbo'},
    'openai:text-ada-001': {'id': 'openai:text-ada-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-ada-001', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-babbage-001': {'id': 'openai:text-babbage-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-babbage-001', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-curie-001': {'id': 'openai:text-curie-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-curie-001', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-davinci-002': {'id': 'openai:text-davinci-002', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-davinci-002', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-davinci-003': {'id': 'openai:text-davinci-003', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-davinci-003', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}}}


# based on https://github.com/ading2210/vercel-llm-api // modified
class Client:
    """
    Клиент для взаимодействия с API Vercel.
    """

    def __init__(self) -> None:
        """
        Инициализирует клиент для взаимодействия с API Vercel.
        """
        self.session: requests.Session = requests.Session()
        self.headers: Dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Te': 'trailers',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.headers.update(self.headers)

    def get_token(self) -> str:
        """
        Получает токен для авторизации.

        Returns:
            str: Токен авторизации.
        """
        try:
            b64: str = self.session.get('https://sdk.vercel.ai/openai.jpeg').text
            data: Dict = json.loads(base64.b64decode(b64))

            code: str = 'const globalThis = {data: `sentinel`}; function token() {return (%s)(%s)}' % (
                data['c'], data['a'])

            token_string: str = json.dumps(separators=(',', ':'),
                                            obj={'r': execjs.compile(code).call('token'), 't': data['t']})

            return base64.b64encode(token_string.encode()).decode()
        except Exception as ex:
            logger.error('Ошибка при получении токена', ex, exc_info=True)
            return ''

    def get_default_params(self, model_id: str) -> Dict:
        """
        Получает параметры по умолчанию для указанной модели.

        Args:
            model_id (str): Идентификатор модели.

        Returns:
            Dict: Словарь параметров по умолчанию.
        """
        return {key: param['value'] for key, param in vercel_models[model_id]['parameters'].items()}

    def generate(self, model_id: str, prompt: str, params: Dict = {}) -> Generator[Dict, None, None]:
        """
        Генерирует текст на основе указанной модели и промпта.

        Args:
            model_id (str): Идентификатор модели.
            prompt (str): Промпт для генерации текста.
            params (Dict, optional): Дополнительные параметры. По умолчанию пустой словарь.

        Yields:
            Generator[Dict, None, None]: Генератор токенов сгенерированного текста.
        """
        if ':' not in model_id:
            model_id: str = models[model_id]

        defaults: Dict = self.get_default_params(model_id)

        payload: Dict = defaults | params | {
            'prompt': prompt,
            'model': model_id,
        }

        headers: Dict = self.headers | {
            'Accept-Encoding': 'gzip, deflate, br',
            'Custom-Encoding': self.get_token(),
            'Host': 'sdk.vercel.ai',
            'Origin': 'https://sdk.vercel.ai',
            'Referrer': 'https://sdk.vercel.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        chunks_queue: queue.Queue = queue.Queue()
        error: Optional[Exception] = None
        response: Optional[requests.Response] = None

        def callback(data: bytes) -> None:
            """
            Callback-функция для обработки чанков данных.

            Args:
                data (bytes): Чанк данных.
            """
            chunks_queue.put(data.decode())

        def request_thread() -> None:
            """
            Функция для выполнения запроса в отдельном потоке.
            """
            nonlocal response, error
            for _ in range(3):
                try:
                    with self.session.post('https://sdk.vercel.ai/api/generate',
                                             json=payload, headers=headers, content_callback=callback) as res:
                        res.raise_for_status()
                        response = res

                except Exception as ex:
                    logger.error(f'Ошибка при запросе к API Vercel (попытка {_ + 1})', ex, exc_info=True)
                    if _ == 2:
                        error = ex
                    else:
                        continue

        thread: threading.Thread = threading.Thread(target=request_thread, daemon=True)
        thread.start()

        text: str = ''
        index: int = 0
        while True:
            try:
                chunk: str = chunks_queue.get(block=True, timeout=0.1)

            except queue.Empty:
                if error:
                    raise error

                elif response:
                    break

                else:
                    continue

            text += chunk
            lines: List[str] = text.split('\n')

            if len(lines) - 1 > index:
                new: List[str] = lines[index:-1]
                for word in new:
                    try:
                        yield json.loads(word)
                    except json.JSONDecodeError as ex:
                        logger.error(f'Не удалось декодировать JSON: {word}', ex, exc_info=True)
                index = len(lines) - 1


def _create_completion(model: str, messages: list, stream: bool, **kwargs) -> Generator[str, None, None]:
    """
    Создает завершение текста на основе указанной модели и сообщений.

    Args:
        model (str): Идентификатор модели.
        messages (list): Список сообщений для создания завершения.
        stream (bool): Флаг потоковой передачи.
        **kwargs: Дополнительные аргументы.

    Yields:
        Generator[str, None, None]: Генератор токенов завершенного текста.
    """
    yield 'Vercel is currently not working.'
    return

    conversation: str = 'This is a conversation between a human and a language model, respond to the last message accordingly, referring to the past history of messages if needed.\n'

    for message in messages:
        conversation += '%s: %s\n' % (message['role'], message['content'])

    conversation += 'assistant: '

    completion: Generator = Client().generate(model, conversation)

    for token in completion:
        yield token


params: str = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
              f'({", ".join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])})'