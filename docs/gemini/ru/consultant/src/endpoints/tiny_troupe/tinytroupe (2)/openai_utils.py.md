### **Анализ кода модуля `openai_utils.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/openai_utils.py

Модуль содержит классы для взаимодействия с OpenAI API, включая поддержку кэширования запросов, обработки различных типов данных и управления конфигурацией.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура классов для работы с OpenAI API.
  - Реализована поддержка кэширования API-вызовов.
  - Обработка различных типов данных (bool, int, float, list) с приведением типов.
  - Поддержка Azure OpenAI API.
- **Минусы**:
  - Смешанный стиль аннотаций типов (иногда `Union`, иногда `|`).
  - Некоторые docstring отсутствуют или неполные.
  - Использование `configparser` и `os.getenv` напрямую, что может быть улучшено с использованием более централизованного подхода к конфигурации.
  - Не все функции и методы имеют подробные docstring, описывающие их назначение, аргументы и возвращаемые значения.

**Рекомендации по улучшению**:

1. **Общие улучшения**:
   - Заменить `Union` на `|` для аннотаций типов.
   - Добавить/улучшить docstring для всех функций и классов, включая описание аргументов, возвращаемых значений и возможных исключений.
   - Использовать `logger.error(..., exc_info=True)` для логирования исключений, чтобы получить трассировку стека.
   - Улучшить обработку конфигурации, возможно, через единый класс конфигурации.
   - Добавить больше комментариев для пояснения сложных участков кода.

2. **Класс `LLMRequest`**:
   - Улучшить docstring для `__init__` и `call`, чтобы явно указать, какие исключения могут быть вызваны и при каких условиях.
   - Добавить примеры использования в docstring.
   - Явное указание типов для атрибутов класса.

3. **Классы `OpenAIClient` и `AzureClient`**:
   - Добавить docstring для методов `_setup_from_config`, `_raw_model_call`, `_raw_model_response_extractor`, `_count_tokens`, `_save_cache`, `_load_cache`, `get_embedding`, `_raw_embedding_model_call`, `_raw_embedding_model_response_extractor`.
   - Добавить обработку исключений при загрузке/сохранении кэша.
   - Использовать `j_loads` или `j_loads_ns` для загрузки конфигурационных файлов.
   - В методе `send_message` добавить логирование входных параметров `current_messages` и `model_params` для облегчения отладки.
   - В методе `_count_tokens` обрабатывать `KeyError` и `NotImplementedError` с использованием `logger.error` и `exc_info=True`.

4. **Функции `register_client`, `_get_client_for_api_type`, `client`, `force_api_type`, `force_api_cache`**:
   - Добавить docstring для каждой функции.
   - Улучшить обработку исключений в `_get_client_for_api_type`.

5. **Исключения `InvalidRequestError` и `NonTerminalError`**:
   - Добавить docstring для каждого класса исключений.

**Оптимизированный код**:

```python
"""
Модуль для работы с OpenAI API и Azure OpenAI API
==================================================

Модуль содержит классы для взаимодействия с OpenAI API, включая поддержку кэширования запросов,
обработки различных типов данных и управления конфигурацией.

Пример использования
----------------------

>>> from tinytroupe.openai_utils import OpenAIClient
>>> client = OpenAIClient()
>>> messages = [{"role": "user", "content": "Hello, world!"}]
>>> response = client.send_message(messages)
>>> print(response)
{'role': 'assistant', 'content': 'Hello!'}
"""

import os
import openai
from openai import OpenAI, AzureOpenAI
import time
import json
import pickle
import logging
import configparser
from pydantic import BaseModel
from typing import Union, Optional, List
import textwrap  # to dedent strings

import tiktoken
from tinytroupe import utils
from tinytroupe.control import transactional

logger = logging.getLogger('tinytroupe')

# Читаем конфигурационный файл
config = utils.read_config_file()

###########################################################################
# Default parameter values
###########################################################################
default = {}
default['model'] = config['OpenAI'].get('MODEL', 'gpt-4o')
default['max_tokens'] = int(config['OpenAI'].get('MAX_TOKENS', '1024'))
default['temperature'] = float(config['OpenAI'].get('TEMPERATURE', '1.0'))
default['top_p'] = int(config['OpenAI'].get('TOP_P', '0'))
default['frequency_penalty'] = float(config['OpenAI'].get('FREQ_PENALTY', '0.0'))
default['presence_penalty'] = float(config['OpenAI'].get('PRESENCE_PENALTY', '0.0'))
default['timeout'] = float(config['OpenAI'].get('TIMEOUT', '30.0'))
default['max_attempts'] = float(config['OpenAI'].get('MAX_ATTEMPTS', '0.0'))
default['waiting_time'] = float(config['OpenAI'].get('WAITING_TIME', '1'))
default['exponential_backoff_factor'] = float(config['OpenAI'].get('EXPONENTIAL_BACKOFF_FACTOR', '5'))

default['embedding_model'] = config['OpenAI'].get('EMBEDDING_MODEL', 'text-embedding-3-small')

default['cache_api_calls'] = config['OpenAI'].getboolean('CACHE_API_CALLS', False)
default['cache_file_name'] = config['OpenAI'].get('CACHE_FILE_NAME', 'openai_api_cache.pickle')

###########################################################################
# Model calling helpers
###########################################################################

class LLMRequest:
    """
    Класс, представляющий запрос к LLM модели.
    Содержит входные сообщения, конфигурацию модели и вывод модели.
    """
    def __init__(self, system_template_name: str | None = None, system_prompt: str | None = None,
                 user_template_name: str | None = None, user_prompt: str | None = None,
                 output_type: type | None = None,
                 **model_params):
        """
        Инициализирует экземпляр LLMCall с указанными системными и пользовательскими шаблонами или подсказками.
        Если указан шаблон, соответствующая подсказка должна быть None, и наоборот.

        Args:
            system_template_name (str | None, optional): Имя системного шаблона. Defaults to None.
            system_prompt (str | None, optional): Системная подсказка. Defaults to None.
            user_template_name (str | None, optional): Имя пользовательского шаблона. Defaults to None.
            user_prompt (str | None, optional): Пользовательская подсказка. Defaults to None.
            output_type (type | None, optional): Тип вывода. Defaults to None.
            **model_params: Дополнительные параметры модели.

        Raises:
            ValueError: Если указаны и шаблон, и подсказка, или если ни один из них не указан.
        
        Example:
            >>> request = LLMRequest(system_prompt='You are a helpful assistant.', user_prompt='What is the capital of France?')
        """
        if (system_template_name is not None and system_prompt is not None) or \
           (user_template_name is not None and user_prompt is not None) or\
           (system_template_name is None and system_prompt is None) or \
           (user_template_name is None and user_prompt is None):
            raise ValueError('Either the template or the prompt must be specified, but not both.')
        
        self.system_template_name = system_template_name
        self.user_template_name = user_template_name
        
        self.system_prompt = textwrap.dedent(system_prompt) # remove identation
        self.user_prompt = textwrap.dedent(user_prompt) # remove identation

        self.output_type = output_type

        self.model_params = model_params
        self.model_output = None

        self.messages = []

        #  will be set after the call
        self.response_raw = None
        self.response_json = None
        self.response_value = None
        self.response_justification = None
        self.response_confidence = None
    
    def __call__(self, *args, **kwds):
        return self.call(*args, **kwds)

    def call(self, **rendering_configs) -> str | int | float | bool | list | None:
        """
        Вызывает LLM модель с указанными конфигурациями рендеринга.

        Args:
            rendering_configs: Конфигурации рендеринга (переменные шаблона), используемые при составлении начальных сообщений.
        
        Returns:
            str | int | float | bool | list | None: Содержимое ответа модели.
        
        Raises:
            ValueError: Если `output_type` не поддерживается.

        Example:
            >>> request = LLMRequest(system_prompt='You are a helpful assistant.', user_prompt='What is the capital of {country}?', output_type=str)
            >>> request.call(country='France')
            'Paris'
        """
        if self.system_template_name is not None and self.user_template_name is not None:
            self.messages = utils.compose_initial_LLM_messages_with_templates(self.system_template_name, self.user_template_name, rendering_configs)
        else:
            self.messages = [{"role": "system", "content": self.system_prompt},
                             {"role": "user", "content": self.user_prompt}]
        
        
        #
        # Setup typing for the output
        #
        if self.output_type is not None:
            # specify the structured output
            self.model_params["response_format"] = LLMScalarWithJustificationResponse
            self.messages.append({"role": "user",
                                  "content": "In your response, you **MUST** provide a value, along with a justification and your confidence level that the value and justification are correct (0.0 means no confidence, 1.0 means complete confidence)."+\
                                             "Furtheremore, your response **MUST** be a JSON object with the following structure: {\\"value\\": value, \\"justification\\": justification, \\"confidence\\": confidence}."})

            # specify the value type
            if self.output_type == bool:
                self.messages.append(self._request_bool_llm_message())
            elif self.output_type == int:
                self.messages.append(self._request_integer_llm_message())
            elif self.output_type == float:
                self.messages.append(self._request_float_llm_message())
            elif self.output_type == list and all(isinstance(option, str) for option in self.output_type):
                self.messages.append(self._request_enumerable_llm_message(self.output_type))
            elif self.output_type == str:
                pass
            else:
                raise ValueError(f"Unsupported output type: {self.output_type}")
        
        #
        # call the LLM model
        #
        self.model_output = client().send_message(self.messages, **self.model_params)

        if 'content' in self.model_output:
            self.response_raw = self.response_value = self.model_output['content']
            

            # further, if an output type is specified, we need to coerce the result to that type
            if self.output_type is not None:
                self.response_json = utils.extract_json(self.response_raw)

                self.response_value = self.response_json["value"]
                self.response_justification = self.response_json["justification"]
                self.response_confidence = self.response_json["confidence"]

                if self.output_type == bool:
                    self.response_value = self._coerce_to_bool(self.response_value)
                elif self.output_type == int:
                    self.response_value = self._coerce_to_integer(self.response_value)
                elif self.output_type == float:
                    self.response_value = self._coerce_to_float(self.response_value)
                elif self.output_type == list and all(isinstance(option, str) for option in self.output_type):
                    self.response_value = self._coerce_to_enumerable(self.response_value, self.output_type)
                elif self.output_type == str:
                    pass
                else:
                    raise ValueError(f"Unsupported output type: {self.output_type}")
            
            return self.response_value
        
        else:
            logger.error(f"Model output does not contain 'content' key: {self.model_output}")
            return None

    def _coerce_to_bool(self, llm_output: str | bool) -> bool:
        """
        Приводит вывод LLM к логическому значению.

        Этот метод ищет строку "True", "False", "Yes", "No", "Positive", "Negative" в выводе LLM, так что
          - регистр нейтрализован;
          - учитывается первое вхождение строки, остальное игнорируется. Например, "Yes, that is true" будет считаться "Yes";
          - если такая строка не найдена, метод выдает ошибку. Поэтому важно, чтобы подсказки фактически запрашивали логическое значение.

        Args:
            llm_output (str, bool): Вывод LLM для приведения.
        
        Returns:
            bool: Логическое значение вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого логического значения.

        Example:
            >>> request = LLMRequest()
            >>> request._coerce_to_bool('Yes')
            True
            >>> request._coerce_to_bool('False')
            False
        """

        # if the LLM output is already a boolean, we return it
        if isinstance(llm_output, bool):
            return llm_output

        # let's extract the first occurrence of the string "True", "False", "Yes", "No", "Positive", "Negative" in the LLM output.
        # using a regular expression
        import re
        match = re.search(r'\b(?:True|False|Yes|No|Positive|Negative)\b', llm_output, re.IGNORECASE)
        if match:
            first_match = match.group(0).lower()
            if first_match in ['true', 'yes', 'positive']:
                return True
            elif first_match in ['false', 'no', 'negative']:
                return False
            
        raise ValueError('The LLM output does not contain a recognizable boolean value.')

    def _request_bool_llm_message(self) -> dict:
        """
        Возвращает сообщение для запроса логического значения от LLM.

        Returns:
            dict: Словарь, представляющий сообщение для запроса логического значения.
        
        Example:
            >>> request = LLMRequest()
            >>> request._request_bool_llm_message()
            {'role': 'user', 'content': "The `value` field you generate **must** be either 'True' or 'False'. This is critical for later processing. If you don't know the correct answer, just output 'False'."}
        """
        return {'role': 'user',
                'content': "The `value` field you generate **must** be either 'True' or 'False'. This is critical for later processing. If you don't know the correct answer, just output 'False'."}


    def _coerce_to_integer(self, llm_output: str) -> int:
        """
        Приводит вывод LLM к целочисленному значению.

        Этот метод ищет первое вхождение целого числа в выводе LLM, так что
          - учитывается первое вхождение целого числа, остальное игнорируется. Например, "There are 3 cats" будет считаться 3;
          - если целое число не найдено, метод выдает ошибку. Поэтому важно, чтобы подсказки фактически запрашивали целочисленное значение.

        Args:
            llm_output (str, int): Вывод LLM для приведения.
        
        Returns:
            int: Целочисленное значение вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого целочисленного значения.

        Example:
            >>> request = LLMRequest()
            >>> request._coerce_to_integer('There are 3 cats')
            3
        """

        # if the LLM output is already an integer, we return it
        if isinstance(llm_output, int):
            return llm_output

        # let's extract the first occurrence of an integer in the LLM output.
        # using a regular expression
        import re
        match = re.search(r'\b\d+\b', llm_output)
        if match:
            return int(match.group(0))
            
        raise ValueError('The LLM output does not contain a recognizable integer value.')

    def _request_integer_llm_message(self) -> dict:
        """
        Возвращает сообщение для запроса целого числа от LLM.

        Returns:
            dict: Словарь, представляющий сообщение для запроса целого числа.
        
        Example:
            >>> request = LLMRequest()
            >>> request._request_integer_llm_message()
            {'role': 'user', 'content': "The `value` field you generate **must** be an integer number (e.g., '1'). This is critical for later processing.."}
        """
        return {'role': 'user',
                'content': "The `value` field you generate **must** be an integer number (e.g., '1'). This is critical for later processing.."}
    
    def _coerce_to_float(self, llm_output: str) -> float:
        """
        Приводит вывод LLM к значению с плавающей точкой.

        Этот метод ищет первое вхождение числа с плавающей точкой в выводе LLM, так что
          - учитывается первое вхождение числа с плавающей точкой, остальное игнорируется. Например, "The price is $3.50" будет считаться 3.50;
          - если число с плавающей точкой не найдено, метод выдает ошибку. Поэтому важно, чтобы подсказки фактически запрашивали значение с плавающей точкой.

        Args:
            llm_output (str, float): Вывод LLM для приведения.
        
        Returns:
            float: Значение с плавающей точкой вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого значения с плавающей точкой.

        Example:
            >>> request = LLMRequest()
            >>> request._coerce_to_float('The price is $3.50')
            3.5
        """

        # if the LLM output is already a float, we return it
        if isinstance(llm_output, float):
            return llm_output
        

        # let's extract the first occurrence of a float in the LLM output.
        # using a regular expression
        import re
        match = re.search(r'\b\d+\.\d+\b', llm_output)
        if match:
            return float(match.group(0))
            
        raise ValueError('The LLM output does not contain a recognizable float value.')

    def _request_float_llm_message(self) -> dict:
        """
        Возвращает сообщение для запроса числа с плавающей точкой от LLM.

        Returns:
            dict: Словарь, представляющий сообщение для запроса числа с плавающей точкой.

        Example:
            >>> request = LLMRequest()
            >>> request._request_float_llm_message()
            {'role': 'user', 'content': "The `value` field you generate **must** be a float number (e.g., '980.16'). This is critical for later processing."}
        """
        return {'role': 'user',
                'content': "The `value` field you generate **must** be a float number (e.g., '980.16'). This is critical for later processing."}
    
    def _coerce_to_enumerable(self, llm_output: str, options: list) -> str:
        """
        Приводит вывод LLM к одному из указанных вариантов.

        Этот метод ищет первое вхождение одного из указанных вариантов в выводе LLM, так что
          - учитывается первое вхождение варианта, остальное игнорируется. Например, "I prefer cats" будет считаться "cats";
          - если вариант не найден, метод выдает ошибку. Поэтому важно, чтобы подсказки фактически запрашивали один из указанных вариантов.

        Args:
            llm_output (str): Вывод LLM для приведения.
            options (list): Список вариантов для рассмотрения.
        
        Returns:
            str: Значение варианта вывода LLM.

        Raises:
            ValueError: Если вывод LLM не содержит распознаваемого значения варианта.
        
        Example:
            >>> request = LLMRequest()
            >>> request._coerce_to_enumerable('I prefer cats', ['cats', 'dogs'])
            'cats'
        """

        # let's extract the first occurrence of one of the specified options in the LLM output.
        # using a regular expression
        import re
        match = re.search(r'\b(?:' + '|'.join(options) + r')\b', llm_output, re.IGNORECASE)
        if match:
            return match.group(0)
            
        raise ValueError('The LLM output does not contain a recognizable option value.')

    def _request_enumerable_llm_message(self, options: list) -> dict:
        """
        Возвращает сообщение для запроса одного из указанных вариантов от LLM.

        Args:
            options (list): Список вариантов для выбора.
        
        Returns:
            dict: Словарь, представляющий сообщение для запроса одного из указанных вариантов.

        Example:
            >>> request = LLMRequest()
            >>> request._request_enumerable_llm_message(['cats', 'dogs'])
            {'role': 'user', 'content': "The `value` field you generate **must** be exactly one of the following strings: 'cats', 'dogs'. This is critical for later processing."}
        """
        options_list_as_string = ', '.join([f"'{o}'" for o in options])
        return {'role': 'user',
                'content': f"The `value` field you generate **must** be exactly one of the following strings: {options_list_as_string}. This is critical for later processing."}
    
    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта LLMRequest.

        Returns:
            str: Строковое представление объекта LLMRequest.
        """
        return f'LLMRequest(messages={self.messages}, model_params={self.model_params}, model_output={self.model_output})'

#
# Data structures to enforce output format during LLM API call.
#
class LLMScalarWithJustificationResponse(BaseModel):
    """
    LLMTypedResponse представляет типизированный ответ от LLM (Language Learning Model).
    Атрибуты:
        value (str, int, float, list): Значение ответа.
        justification (str): Обоснование или объяснение ответа.
    """
    value: str | int | float | bool
    justification: str
    confidence: float


###########################################################################
# Client class
###########################################################################

class OpenAIClient:
    """
    Утилитный класс для взаимодействия с OpenAI API.
    """

    def __init__(self, cache_api_calls: bool = default['cache_api_calls'], cache_file_name: str = default['cache_file_name']) -> None:
        """
        Инициализирует OpenAIClient.

        Args:
            cache_api_calls (bool): Должны ли API-вызовы кэшироваться и использоваться повторно?
            cache_file_name (str): Имя файла для кэширования API-вызовов.
        """
        logger.debug('Initializing OpenAIClient')

        # should we cache api calls and reuse them?
        self.set_api_cache(cache_api_calls, cache_file_name)
    
    def set_api_cache(self, cache_api_calls: bool, cache_file_name: str = default['cache_file_name']) -> None:
        """
        Включает или отключает кэширование API-вызовов.

        Args:
            cache_api_calls (bool): Включать или отключать кэширование API-вызовов.
            cache_file_name (str): Имя файла для использования для кэширования API-вызовов.
        
        Example:
            >>> client = OpenAIClient()
            >>> client.set_api_cache(True, 'my_cache.pickle')
        """
        self.cache_api_calls = cache_api_calls
        self.cache_file_name = cache_file_name
        if self.cache_api_calls:
            # load the cache, if any
            self.api_cache = self._load_cache()
    
    
    def _setup_from_config(self) -> None:
        """
        Настраивает конфигурации OpenAI API для этого клиента.
        
        Example:
            >>> client = OpenAIClient()
            >>> client._setup_from_config()
        """
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def send_message(self,
                    current_messages: list,
                     model: str = default['model'],
                     temperature: float = default['temperature'],
                     max_tokens: int = default['max_tokens'],
                     top_p: float = default['top_p'],
                     frequency_penalty: float = default['frequency_penalty'],
                     presence_penalty: float = default['presence_penalty'],
                     stop: list = [],
                     timeout: float = default['timeout'],
                     max_attempts: float = default['max_attempts'],
                     waiting_time: float = default['waiting_time'],
                     exponential_backoff_factor: float = default['exponential_backoff_factor'],
                     n: int = 1,
                     response_format: dict | None = None,
                     echo: bool = False) -> dict | None:
        """
        Отправляет сообщение в OpenAI API и возвращает ответ.

        Args:
            current_messages (list): Список словарей, представляющих историю разговора.
            model (str): ID модели, используемой для генерации ответа.
            temperature (float): Контролирует "креативность" ответа. Более высокие значения приводят к более разнообразным ответам.
            max_tokens (int): Максимальное количество токенов (слов или знаков пунктуации) для генерации в ответе.
            top_p (float): Контролирует "качество" ответа. Более высокие значения приводят к более связным ответам.
            frequency_penalty (float): Контролирует "повторение" ответа. Более высокие значения приводят к меньшему повторению.
            presence_penalty (float): Контролирует "разнообразие" ответа. Более высокие значения приводят к более разнообразным ответам.
            stop (str): Строка, которая, если встречается в сгенерированном ответе, приведет к остановке генерации.
            max_attempts (int): Максимальное количество попыток, прежде чем отказаться от генерации ответа.
            timeout (int): Максимальное количество секунд ожидания ответа от API.
            waiting_time (int): Количество секунд ожидания между запросами.
            exponential_backoff_factor (int): Фактор, на который следует увеличивать время ожидания между запросами.
            n (int): Количество завершений для генерации.
            response_format (dict, optional): Формат ответа, если есть.
            echo (bool): Вернуть ли эхо-запрос в ответе.

        Returns:
            dict | None: Словарь, представляющий сгенерированный ответ.

        Raises:
            openai.InvalidRequestError: Если запрос недействителен.
            openai.RateLimitError: Если достигнут предел скорости.
            Exception: При возникновении другой ошибки.

        Example:
            >>> client = OpenAIClient()
            >>> messages = [{"role": "user", "content": "Hello, world!"}]
            >>> response = client.send_message(messages)
            >>> print(response)
            {'role': 'assistant', 'content': 'Hello!'}
        """

        def aux_exponential_backoff():
            nonlocal waiting_time

            # in case waiting time was initially set to 0
            if waiting_time <= 0:
                waiting_time = 2

            logger.info(f'Request failed. Waiting {waiting_time} seconds between requests...')
            time.sleep(waiting_time)

            # exponential backoff
            waiting_time = waiting_time * exponential_backoff_factor

        # setup the OpenAI configurations for this client.
        self._setup_from_config()
        
        # We need to adapt the parameters to the API type, so we create a dictionary with them first
        chat_api_params = {
            'model': model,
            'messages': current_messages,
            'temperature': temperature,
            'max_tokens':max_tokens,
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'stop': stop,
            'timeout': timeout,
            'stream': False,
            'n': n,
        }

        if response_format is not None:
            chat_api_params['response_format'] = response_format

        i = 0
        while i < max_attempts:
            try:
                i += 1

                try:
                    logger.debug(f'Sending messages to OpenAI API. Token count={self._count_tokens(current_messages, model)}.')
                except NotImplementedError:
                    logger.debug(f'Token count not implemented for model {model}.')
                    
                start_time = time.monotonic()
                logger.debug(f'Calling model with client class {self.__class__.__name__}.')

                ###############################################################
                # call the model, either from the cache or from the API
                ###############################################################
                cache_key = str((model, chat_api_params)) # need string to be hashable
                if self.cache_api_calls and (cache_key in self.api_cache):
                    response = self.api_cache[cache_key]
                else:
                    if waiting_time > 0:
                        logger.info(f'Waiting {waiting_time} seconds before next API request (to avoid throttling)...')
                        time.sleep(waiting_time)
                    
                    response = self._raw_model_call(model, chat_api_params)
                    if self.cache_api_calls:
                        self.api_cache[cache_key] = response
                        self._save_cache()
                
                
                logger.debug(f'Got response from API: {response}')
                end_time = time.monotonic()
                logger.debug(
                    f'Got response in {end_time - start_time:.2f} seconds after {i} attempts.')

                return utils.sanitize_dict(self._raw_model_response_extractor(response))

            except openai.InvalidRequestError as ex:
                logger.error(f'[{i}] Invalid request error, won\'t retry: {ex}', exc_info=True)

                # there's no point in retrying if the request is invalid
                # so we return None right away
                return None
            
            except openai.BadRequestError as ex:
                logger.error(f'[{i}] Invalid request error, won\'t retry: {ex}', exc_info=True)
                
                # there's no point in retrying if the request is invalid
                # so we return None right away
                return None
            
            except openai.RateLimitError:
                logger.warning(
                    f'[{i}] Rate limit error, waiting a bit and trying again.')
                aux_exponential_backoff()
            
            except NonTerminalError as ex:
                logger.error(f'[{i}] Non-terminal error: {ex}', exc_info=True)
                aux_exponential_backoff()
                
            except Exception as ex:
                logger.error(f'[{i}] Error: {ex}', exc_info=True)

        logger.error(f'Failed to get response after {max_attempts} attempts.')
        return None
    
    def _raw_model_call(self, model: str, chat_api_params: dict) -> dict:
        """
        Вызывает OpenAI API с заданными параметрами.
        Подклассы должны переопределить этот метод для реализации собственных API-вызовов.

        Args:
            model (str): ID модели, используемой для генерации ответа.
            chat_api_params (dict): Параметры для вызова API чата.
        
        Returns:
            dict: Ответ от API.
        
        Example:
            >>> client = OpenAIClient()
            >>> chat_api_params = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Hello, world!'}]}
            >>> response = client._raw_model_call(chat_api_params)
        """
        if 'response_format' in chat_api_params:
            # to enforce the response format via pydantic, we need to use a different method

            del chat_api_params['stream']

            return self.client.beta.chat.completions.parse(
                    **chat_api_params
                )
        
        else:
            return self.client.chat.