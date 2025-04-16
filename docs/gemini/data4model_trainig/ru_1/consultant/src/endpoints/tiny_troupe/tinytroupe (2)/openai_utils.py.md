### **Анализ кода модуля `openai_utils.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/openai_utils.py

Модуль содержит утилиты для взаимодействия с OpenAI API, включая классы для управления запросами к языковой модели, кэширования API-вызовов и обработки различных типов ответов.

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Наличие классов для работы с OpenAI API и Azure API.
  - Реализация кэширования API-вызовов.
  - Обработка различных типов ответов от языковой модели.
  - Использование `logger` для логирования.
  - Использование textwrap.dedent для удаления отступов.
- **Минусы**:
  - Не все функции и классы имеют подробные docstring.
  - Использование `Union` вместо `|` для объединения типов.
  - В некоторых местах отсутствует аннотация типов.
  - Смешанный стиль кавычек (иногда используются двойные кавычки вместо одинарных).
  - Большое количество параметров по умолчанию, что усложняет чтение и понимание.

**Рекомендации по улучшению**:

1.  **Документация**:
    - Дополнить docstring для всех классов и функций, включая описание параметров, возвращаемых значений и возможных исключений.

2.  **Типизация**:
    - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений, где они отсутствуют.
    - Использовать `|` вместо `Union[]` для указания нескольких возможных типов.

3.  **Форматирование**:
    - Использовать только одинарные кавычки (`'`) для строк.
    - Добавить пробелы вокруг операторов присваивания.

4.  **Обработка ошибок**:
    - Убедиться, что все исключения обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.

5.  **Конфигурация**:
    - Рассмотреть возможность использования более структурированного подхода к управлению конфигурацией, чтобы упростить чтение и поддержку кода.

6.  **Кэширование**:
    - Убедиться, что кэширование API-вызовов работает корректно и эффективно, особенно в многопоточной среде.

7.  **Рефакторинг**:
    - Рассмотреть возможность рефакторинга больших функций на более мелкие и управляемые.

**Оптимизированный код**:

```python
import os
import time
import json
import pickle
import logging
import textwrap
import re
from pathlib import Path
from typing import Union, Optional, List, Dict, Any

import openai
import tiktoken
from openai import OpenAI, AzureOpenAI
from pydantic import BaseModel
from configparser import ConfigParser

from tinytroupe import utils
from tinytroupe.control import transactional
from src.logger import logger  # Используем logger из src.logger

# Чтение конфигурационного файла
config: ConfigParser = utils.read_config_file()

###########################################################################
# Значения параметров по умолчанию
###########################################################################
default: Dict[str, Any] = {}
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
# Вспомогательные классы для вызова моделей
###########################################################################

class LLMRequest:
    """
    Класс, представляющий запрос к языковой модели (LLM).
    Содержит входные сообщения, конфигурацию модели и вывод модели.
    """
    def __init__(
        self,
        system_template_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        user_template_name: Optional[str] = None,
        user_prompt: Optional[str] = None,
        output_type: Optional[type] = None,
        **model_params: Any
    ) -> None:
        """
        Инициализирует экземпляр LLMCall с указанными системными и пользовательскими шаблонами или системными и пользовательскими подсказками.
        Если указан шаблон, соответствующая подсказка должна быть `None`, и наоборот.

        Args:
            system_template_name (Optional[str]): Имя системного шаблона.
            system_prompt (Optional[str]): Системная подсказка.
            user_template_name (Optional[str]): Имя пользовательского шаблона.
            user_prompt (Optional[str]): Пользовательская подсказка.
            output_type (Optional[type]): Тип ожидаемого вывода.
            **model_params (Any): Дополнительные параметры модели.

        Raises:
            ValueError: Если указаны и шаблон, и подсказка, или если не указан ни шаблон, ни подсказка.
        """
        if (system_template_name is not None and system_prompt is not None) or \
           (user_template_name is not None and user_prompt is not None) or \
           (system_template_name is None and system_prompt is None) or \
           (user_template_name is None and user_prompt is None):
            raise ValueError('Должен быть указан либо шаблон, либо подсказка, но не оба.')

        self.system_template_name: Optional[str] = system_template_name
        self.user_template_name: Optional[str] = user_template_name
        self.system_prompt: Optional[str] = textwrap.dedent(system_prompt) if system_prompt else None  # Удаляем отступы
        self.user_prompt: Optional[str] = textwrap.dedent(user_prompt) if user_prompt else None  # Удаляем отступы
        self.output_type: Optional[type] = output_type
        self.model_params: Dict[str, Any] = model_params
        self.model_output: Optional[Dict[str, Any]] = None
        self.messages: List[Dict[str, str]] = []
        self.response_raw: Optional[str] = None
        self.response_json: Optional[Dict[str, Any]] = None
        self.response_value: Optional[Union[str, int, float, bool]] = None
        self.response_justification: Optional[str] = None
        self.response_confidence: Optional[float] = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Вызывает метод `call`.
        """
        return self.call(*args, **kwds)

    def call(self, **rendering_configs: Any) -> Optional[Union[str, int, float, bool]]:
        """
        Вызывает языковую модель с указанными конфигурациями рендеринга.

        Args:
            rendering_configs (Any): Конфигурации рендеринга (переменные шаблона), используемые при составлении начальных сообщений.

        Returns:
            Optional[Union[str, int, float, bool]]: Содержимое ответа модели.
        """
        if self.system_template_name is not None and self.user_template_name is not None:
            self.messages = utils.compose_initial_LLM_messages_with_templates(self.system_template_name, self.user_template_name, rendering_configs)
        else:
            self.messages = [{"role": 'system', "content": self.system_prompt},
                             {"role": 'user', "content": self.user_prompt}]

        #
        # Настройка типов для вывода
        #
        if self.output_type is not None:
            # Укажите структурированный вывод
            self.model_params['response_format'] = {'type': 'json_object'}
            self.messages.append({"role": 'user',
                                  "content": 'В своем ответе вы **ДОЛЖНЫ** предоставить значение, а также обоснование и уровень уверенности в том, что значение и обоснование верны (0.0 означает отсутствие уверенности, 1.0 означает полную уверенность).' +
                                             'Кроме того, ваш ответ **ДОЛЖЕН** быть объектом JSON со следующей структурой: {"value": value, "justification": justification, "confidence": confidence}.'})

            # Укажите тип значения
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
                raise ValueError(f'Неподдерживаемый тип вывода: {self.output_type}')

        #
        # Вызов LLM модели
        #
        self.model_output = client().send_message(self.messages, **self.model_params)

        if 'content' in self.model_output:
            self.response_raw = self.response_value = self.model_output['content']

            # Далее, если указан тип вывода, нам нужно привести результат к этому типу
            if self.output_type is not None:
                self.response_json = utils.extract_json(self.response_raw)

                self.response_value = self.response_json['value']
                self.response_justification = self.response_json['justification']
                self.response_confidence = self.response_json['confidence']

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
                    raise ValueError(f'Неподдерживаемый тип вывода: {self.output_type}')

            return self.response_value

        else:
            logger.error(f'Вывод модели не содержит ключ \'content\': {self.model_output}')
            return None

    def _coerce_to_bool(self, llm_output: Union[str, bool]) -> bool:
        """
        Приводит вывод LLM к логическому значению.

        Этот метод ищет строки "True", "False", "Yes", "No", "Positive", "Negative" в выводе LLM, такие что:
          - регистр нейтрализован;
          - учитывается первое вхождение строки, остальное игнорируется. Например, " Yes, that is true" будет считаться "Yes";
          - если такая строка не найдена, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали логическое значение.

        Args:
            llm_output (Union[str, bool]): Вывод LLM для приведения.

        Returns:
            bool: Логическое значение вывода LLM.
        """
        if isinstance(llm_output, bool):
            return llm_output

        match = re.search(r'\b(?:True|False|Yes|No|Positive|Negative)\b', llm_output, re.IGNORECASE)
        if match:
            first_match = match.group(0).lower()
            if first_match in ['true', 'yes', 'positive']:
                return True
            elif first_match in ['false', 'no', 'negative']:
                return False

        raise ValueError('Вывод LLM не содержит распознаваемого логического значения.')

    def _request_bool_llm_message(self) -> Dict[str, str]:
        """
        Формирует сообщение для запроса логического значения от LLM.

        Returns:
            Dict[str, str]: Словарь с сообщением для LLM.
        """
        return {"role": 'user',
                "content": 'Поле `value`, которое вы генерируете, **должно** быть либо \'True\', либо \'False\'. Это критически важно для дальнейшей обработки. Если вы не знаете правильный ответ, просто выведите \'False\'.'}

    def _coerce_to_integer(self, llm_output: str) -> int:
        """
        Приводит вывод LLM к целочисленному значению.

        Этот метод ищет первое вхождение целого числа в выводе LLM, такое что:
          - учитывается первое вхождение целого числа, остальное игнорируется. Например, "There are 3 cats" будет считаться 3;
          - если целое число не найдено, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали целочисленное значение.

        Args:
            llm_output (str): Вывод LLM для приведения.

        Returns:
            int: Целочисленное значение вывода LLM.
        """
        if isinstance(llm_output, int):
            return llm_output

        match = re.search(r'\b\d+\b', llm_output)
        if match:
            return int(match.group(0))

        raise ValueError('Вывод LLM не содержит распознаваемого целочисленного значения.')

    def _request_integer_llm_message(self) -> Dict[str, str]:
        """
        Формирует сообщение для запроса целочисленного значения от LLM.

        Returns:
            Dict[str, str]: Словарь с сообщением для LLM.
        """
        return {"role": 'user',
                "content": 'Поле `value`, которое вы генерируете, **должно** быть целым числом (например, \'1\'). Это критически важно для дальнейшей обработки.'}

    def _coerce_to_float(self, llm_output: str) -> float:
        """
        Приводит вывод LLM к значению с плавающей точкой.

        Этот метод ищет первое вхождение числа с плавающей точкой в выводе LLM, такое что:
          - учитывается первое вхождение числа с плавающей точкой, остальное игнорируется. Например, "The price is $3.50" будет считаться 3.50;
          - если число с плавающей точкой не найдено, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали значение с плавающей точкой.

        Args:
            llm_output (str): Вывод LLM для приведения.

        Returns:
            float: Значение с плавающей точкой вывода LLM.
        """
        if isinstance(llm_output, float):
            return llm_output

        match = re.search(r'\b\d+\.\d+\b', llm_output)
        if match:
            return float(match.group(0))

        raise ValueError('Вывод LLM не содержит распознаваемого значения с плавающей точкой.')

    def _request_float_llm_message(self) -> Dict[str, str]:
        """
        Формирует сообщение для запроса значения с плавающей точкой от LLM.

        Returns:
            Dict[str, str]: Словарь с сообщением для LLM.
        """
        return {"role": 'user',
                "content": 'Поле `value`, которое вы генерируете, **должно** быть числом с плавающей точкой (например, \'980.16\'). Это критически важно для дальнейшей обработки.'}

    def _coerce_to_enumerable(self, llm_output: str, options: List[str]) -> str:
        """
        Приводит вывод LLM к одному из указанных вариантов.

        Этот метод ищет первое вхождение одного из указанных вариантов в выводе LLM, такое что:
          - учитывается первое вхождение варианта, остальное игнорируется. Например, "I prefer cats" будет считаться "cats";
          - если вариант не найден, метод вызывает ошибку. Поэтому важно, чтобы подсказки действительно запрашивали один из указанных вариантов.

        Args:
            llm_output (str): Вывод LLM для приведения.
            options (List[str]): Список вариантов для рассмотрения.

        Returns:
            str: Значение варианта вывода LLM.
        """
        match = re.search(r'\b(?:' + '|'.join(options) + r')\b', llm_output, re.IGNORECASE)
        if match:
            return match.group(0)

        raise ValueError('Вывод LLM не содержит распознаваемого значения варианта.')

    def _request_enumerable_llm_message(self, options: List[str]) -> Dict[str, str]:
        """
        Формирует сообщение для запроса перечислимого значения от LLM.

        Args:
            options (List[str]): Список допустимых вариантов.

        Returns:
            Dict[str, str]: Словарь с сообщением для LLM.
        """
        options_list_as_string = ', '.join([f"'{o}'" for o in options])
        return {"role": 'user',
                "content": f'Поле `value`, которое вы генерируете, **должно** быть ровно одной из следующих строк: {options_list_as_string}. Это критически важно для дальнейшей обработки.'}

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта LLMRequest.

        Returns:
            str: Строковое представление объекта.
        """
        return f'LLMRequest(messages={self.messages}, model_params={self.model_params}, model_output={self.model_output})'


#
# Структуры данных для принудительного применения формата вывода во время вызова LLM API.
#
class LLMScalarWithJustificationResponse(BaseModel):
    """
    LLMTypedResponse представляет типизированный ответ от LLM (Language Learning Model).
    Атрибуты:
        value (str, int, float, list): Значение ответа.
        justification (str): Обоснование или объяснение ответа.
    """
    value: Union[str, int, float, bool]
    justification: str
    confidence: float


###########################################################################
# Класс клиента
###########################################################################

class OpenAIClient:
    """
    Утилитный класс для взаимодействия с OpenAI API.
    """

    def __init__(self, cache_api_calls: bool = default['cache_api_calls'], cache_file_name: str = default['cache_file_name']) -> None:
        """
        Инициализирует OpenAIClient.

        Args:
            cache_api_calls (bool): Должны ли мы кэшировать вызовы API и использовать их повторно?
            cache_file_name (str): Имя файла для использования для кэширования вызовов API.
        """
        logger.debug('Инициализация OpenAIClient')

        # Должны ли мы кэшировать вызовы API и использовать их повторно?
        self.set_api_cache(cache_api_calls, cache_file_name)

    def set_api_cache(self, cache_api_calls: bool, cache_file_name: str = default['cache_file_name']) -> None:
        """
        Включает или отключает кэширование вызовов API.

        Args:
            cache_api_calls (bool): Следует ли кэшировать вызовы API.
            cache_file_name (str): Имя файла для использования для кэширования вызовов API.
        """
        self.cache_api_calls: bool = cache_api_calls
        self.cache_file_name: str = cache_file_name
        if self.cache_api_calls:
            # Загрузите кэш, если он есть
            self.api_cache: Dict[str, Any] = self._load_cache()

    def _setup_from_config(self) -> None:
        """
        Настраивает конфигурации OpenAI API для этого клиента.
        """
        self.client: OpenAI = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def send_message(
        self,
        current_messages: List[Dict[str, str]],
        model: str = default['model'],
        temperature: float = default['temperature'],
        max_tokens: int = default['max_tokens'],
        top_p: float = default['top_p'],
        frequency_penalty: float = default['frequency_penalty'],
        presence_penalty: float = default['presence_penalty'],
        stop: Optional[List[str]] = None,
        timeout: float = default['timeout'],
        max_attempts: float = default['max_attempts'],
        waiting_time: float = default['waiting_time'],
        exponential_backoff_factor: float = default['exponential_backoff_factor'],
        n: int = 1,
        response_format: Optional[Dict[str, str]] = None,
        echo: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Отправляет сообщение в OpenAI API и возвращает ответ.

        Args:
            current_messages (List[Dict[str, str]]): Список словарей, представляющих историю разговора.
            model (str): ID модели, используемой для создания ответа.
            temperature (float): Управляет "креативностью" ответа. Более высокие значения приводят к более разнообразным ответам.
            max_tokens (int): Максимальное количество токенов (слов или знаков препинания), которые нужно создать в ответе.
            top_p (float): Управляет "качеством" ответа. Более высокие значения приводят к более связным ответам.
            frequency_penalty (float): Управляет "повторением" ответа. Более высокие значения приводят к меньшему повторению.
            presence_penalty (float): Управляет "разнообразием" ответа. Более высокие значения приводят к более разнообразным ответам.
            stop (Optional[List[str]]): Строка, которая, если она встречается в сгенерированном ответе, приведет к остановке генерации.
            timeout (float): Максимальное количество секунд ожидания ответа от API.
            max_attempts (float): Максимальное количество попыток, которые нужно предпринять, прежде чем отказаться от создания ответа.
            waiting_time (float): Количество секунд ожидания между запросами.
            exponential_backoff_factor (float): Коэффициент, на который следует увеличивать время ожидания между запросами.
            n (int): Количество завершений, которые нужно создать.
            response_format (Optional[Dict[str, str]]): Формат ответа, если есть.
            echo (bool): Должен ли запрос быть отражен в ответе?

        Returns:
            Optional[Dict[str, Any]]: Словарь, представляющий сгенерированный ответ.
        """

        def aux_exponential_backoff() -> None:
            """
            Вспомогательная функция для экспоненциального отката.
            """
            nonlocal waiting_time

            # В случае, если время ожидания было первоначально установлено на 0
            if waiting_time <= 0:
                waiting_time = 2

            logger.info(f'Запрос не удался. Ожидание {waiting_time} секунд между запросами...')
            time.sleep(waiting_time)

            # Экспоненциальный откат
            waiting_time = waiting_time * exponential_backoff_factor

        # Настройка конфигураций OpenAI для этого клиента.
        self._setup_from_config()

        # Нам нужно адаптировать параметры к типу API, поэтому сначала мы создаем словарь с ними
        chat_api_params: Dict[str, Any] = {
            'model': model,
            'messages': current_messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
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
                    logger.debug(f'Отправка сообщений в OpenAI API. Количество токенов={self._count_tokens(current_messages, model)}.')
                except NotImplementedError:
                    logger.debug(f'Подсчет токенов не реализован для модели {model}.')

                start_time = time.monotonic()
                logger.debug(f'Вызов модели с классом клиента {self.__class__.__name__}.')

                ###############################################################
                # Вызов модели, либо из кэша, либо из API
                ###############################################################
                cache_key: str = str((model, chat_api_params))  # Нужна строка, чтобы быть хэшируемой
                if self.cache_api_calls and (cache_key in self.api_cache):
                    response = self.api_cache[cache_key]
                else:
                    if waiting_time > 0:
                        logger.info(f'Ожидание {waiting_time} секунд перед следующим запросом API (чтобы избежать регулирования)...')
                        time.sleep(waiting_time)

                    response = self._raw_model_call(model, chat_api_params)
                    if self.cache_api_calls:
                        self.api_cache[cache_key] = response
                        self._save_cache()

                logger.debug(f'Получен ответ от API: {response}')
                end_time = time.monotonic()
                logger.debug(f'Получен ответ за {end_time - start_time:.2f} секунд после {i} попыток.')

                return utils.sanitize_dict(self._raw_model_response_extractor(response))

            except openai.InvalidRequestError as ex:
                logger.error(f'[{i}] Недопустимая ошибка запроса, не буду повторять: {ex}', exc_info=True)

                # Нет смысла повторять попытку, если запрос недействителен
                # Поэтому мы сразу возвращаем None
                return None

            except openai.BadRequestError as ex:
                logger.error(f'[{i}] Недопустимая ошибка запроса, не буду повторять: {ex}', exc_info=True)

                # Нет смысла повторять попытку, если запрос недействителен
                # Поэтому мы сразу возвращаем None
                return None

            except openai.RateLimitError:
                logger.warning(f'[{i}] Ошибка ограничения скорости, немного жду и пробую снова.')
                aux_exponential_backoff()

            except NonTerminalError as ex:
                logger.error(f'[{i}] Нетерминальная ошибка: {ex}', exc_info=True)
                aux_exponential_backoff()

            except Exception as ex:
                logger.error(f'[{i}] Ошибка: {ex}', exc_info=True)

        logger.error(f'Не удалось получить ответ после {max_attempts} попыток.')
        return None

    def _raw_model_call(self, model: str, chat_api_params: Dict[str, Any]) -> Any:
        """
        Вызывает OpenAI API с заданными параметрами. Подклассы должны
        переопределить этот метод, чтобы реализовать свои собственные вызовы API.
        """

        if 'response_format' in chat_api_params:
            # Чтобы принудительно применить формат ответа через pydantic, нам нужно использовать другой метод

            del chat_api_params['stream']

            return self.client.beta.chat.completions.parse(
                **chat_api_params
            )

        else:
            return self.client.chat.completions.create(
                **chat_api_params
            )

    def _raw_model_response_extractor(self, response: Any) -> Dict[str, Any]:
        """
        Извлекает ответ из ответа API. Подклассы должны
        переопределить этот метод, чтобы реализовать извлечение собственного ответа.
        """
        return response.choices[0].message.to_dict()

    def _count_tokens(self, messages: List[Dict[str, str]], model: str) -> Optional[int]:
        """
        Подсчитайте количество токенов OpenAI в списке сообщений с помощью tiktoken.

        Адаптировано из https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

        Args:
            messages (List[Dict[str, str]]): Список словарей, представляющих историю разговора.
            model (str): Имя модели, используемой для кодирования строки.
        """
        try:
            try:
                encoding = tiktoken.encoding_for_model(model)
            except KeyError:
                logger.debug('Подсчет токенов: модель не найдена. Использование кодировки cl100k_base.')
                encoding = tiktoken.get_encoding('cl100k_base')
            if model in {
                'gpt-3.5-turbo-0613',
                'gpt-3.5-turbo-16k-0613',
                'gpt-4-0314',
                'gpt-4-32k-0314',
                'gpt-4-0613',
                'gpt-4-32k-0613',
            }:
                tokens_per_message = 3
                tokens_per_name = 1
            elif model == 'gpt-3.5-turbo-0301':
                tokens_per_message = 4  # Каждое сообщение следует <|start|>{role/name}\n{content}<|end|>\n

                tokens_per_name = -1  # Если есть имя, роль опускается
            elif 'gpt-3.5-turbo' in model:
                logger.debug('Подсчет токенов: gpt-3.5-turbo может обновляться с течением времени. Возврат количества токенов с учетом gpt-3.5-turbo-0613.')
                return self._count_tokens(messages, model='gpt-3.5-turbo-0613')
            elif ('gpt-4' in model) or ('ppo' in model):
                logger.debug('Подсчет токенов: gpt-4 может обновляться с течением времени. Возврат количества токенов с учетом gpt-4-0613.')
                return self._count_tokens(messages, model='gpt-4-0613')
            else:
                raise NotImplementedError(
                    f'num_tokens_from_messages() не реализован для модели {model}. См. https://github.com/openai/openai-python/blob/main/chatml.md для получения информации о том, как сообщения преобразуются в токены.')
            num_tokens = 0
            for message in messages:
                num_tokens += tokens_per_message
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == 'name':
                        num_tokens += tokens_per_name
            num_tokens += 3  # Каждый ответ начинается с <|start|>assistant<|message|>
            return num_tokens

        except Exception as ex:
            logger.error(f'Ошибка подсчета токенов: {ex}', exc_info=True)
            return None

    def _save_cache(self) -> None:
        """
        Сохраняет кэш API на диск. Мы используем pickle, чтобы сделать это, потому что некоторые объекты
        не сериализуются в JSON.
        """
        # Используйте pickle для сохранения кэша
        pickle.dump(self.api_cache, open(self.cache_file_name, 'wb'))

    def _load_cache(self) -> Dict[str, Any]:
        """
        Загружает кэш API с диска.
        """
        # unpickle
        return pickle.load(open(self.cache_file_name, 'rb')) if os.path.exists(self.cache_file_name) else {}

    def get_embedding(self, text: str, model: str = default['embedding_model']) -> List[float]:
        """
        Получает внедрение заданного текста с использованием указанной модели.

        Args:
            text (str): Текст для встраивания.
            model (str): Имя модели, используемой для встраивания текста.

        Returns:
            List[float]: Внедрение текста.
        """
        response = self._raw_embedding_model_call(