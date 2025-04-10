### **Анализ кода модуля `results_extractor.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/extraction/results_extractor.py

Модуль содержит класс `ResultsExtractor`, предназначенный для извлечения результатов из объектов `TinyPerson` и `TinyWorld`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован в классы и методы.
    - Присутствуют docstring для большинства методов и классов.
    - Используется `logger` для отладочных сообщений.
- **Минусы**:
    - В docstring отсутствует описание исключений, которые могут быть вызваны.
    - Не все переменные аннотированы типами.
    - Используется `Union`, нужно заменить на `|`.
    - Не используется `j_loads` для загрузки JSON из файла.

**Рекомендации по улучшению:**

1.  **Добавить docstring модуля**:

    - Добавить описание модуля в начале файла.
2.  **Улучшить docstring**:

    - Добавить описание возможных исключений (`Raises`) для каждой функции.
    - Все комментарии и docstring должны быть на русском языке в формате UTF-8. Если в коде docsting на английском - сделай перевеод на русский

3.  **Использовать `j_loads`**:

    - Заменить `open(self._extraction_prompt_template_path).read()` на `j_loads(self._extraction_prompt_template_path)` для чтения mustache файлов.

4.  **Типизация**:

    - Добавить аннотации типов для всех переменных, где это необходимо.

5.  **Использовать `|` вместо `Union`**:

    - Заменить `Union[str, List[str]]` на `str | List[str]`.

6.  **Обработка ошибок**:

    - Добавить обработку ошибок с логированием через `logger.error`.

7.  **Использовать одинарные кавычки**:

    - Заменить двойные кавычки на одинарные, где это необходимо.

8. **Стиль именования переменных**:

*   *   `verbose:bool=None` заменить на `verbose: Optional[bool] = None` и аналогично для других переменных.

**Оптимизированный код:**

```python
import os
import json
import chevron
import pandas as pd
from typing import Optional, List
from pathlib import Path

from src.logger import logger
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

from tinytroupe import openai_utils
import tinytroupe.utils as utils


"""
Модуль для извлечения результатов из объектов TinyPerson и TinyWorld.
====================================================================

Модуль содержит класс :class:`ResultsExtractor`, который используется для извлечения информации
из истории взаимодействий агентов в TinyTroupe.
"""


class ResultsExtractor:
    """
    Класс для извлечения результатов из объектов TinyPerson и TinyWorld.
    """

    def __init__(
        self,
        extraction_prompt_template_path: str = os.path.join(
            os.path.dirname(__file__), './prompts/interaction_results_extractor.mustache'
        ),
        extraction_objective: str = "The main points present in the agents' interactions history.",
        situation: str = "",
        fields: Optional[List[str]] = None,
        fields_hints: Optional[dict] = None,
        verbose: Optional[bool] = False,
    ) -> None:
        """
        Инициализирует ResultsExtractor с параметрами по умолчанию.

        Args:
            extraction_prompt_template_path (str): Путь к шаблону запроса на извлечение.
            extraction_objective (str): Цель извлечения по умолчанию.
            situation (str): Ситуация для рассмотрения по умолчанию.
            fields (Optional[List[str]]): Поля для извлечения по умолчанию.
            fields_hints (Optional[dict]): Подсказки для полей извлечения по умолчанию.
            verbose (Optional[bool]): Флаг для вывода отладочных сообщений по умолчанию.
        """
        self._extraction_prompt_template_path = extraction_prompt_template_path

        # Параметры по умолчанию
        self.default_extraction_objective = extraction_objective
        self.default_situation = situation
        self.default_fields = fields
        self.default_fields_hints = fields_hints
        self.default_verbose = verbose

        # Кэш для последних результатов извлечения
        self.agent_extraction: dict = {}
        self.world_extraction: dict = {}

    def extract_results_from_agents(
        self,
        agents: List[TinyPerson],
        extraction_objective: Optional[str] = None,
        situation: Optional[str] = None,
        fields: Optional[list] = None,
        fields_hints: Optional[dict] = None,
        verbose: Optional[bool] = None,
    ) -> list:
        """
        Извлекает результаты из списка экземпляров TinyPerson.

        Args:
            agents (List[TinyPerson]): Список экземпляров TinyPerson для извлечения результатов.
            extraction_objective (Optional[str]): Цель извлечения.
            situation (Optional[str]): Ситуация для рассмотрения.
            fields (Optional[list]): Поля для извлечения. Если None, экстрактор решит, какие имена использовать.
            fields_hints (Optional[dict]): Подсказки для полей извлечения. Сопоставляет имена полей со строками подсказок.
            verbose (Optional[bool]): Флаг для вывода отладочных сообщений.

        Returns:
            list: Список извлеченных результатов.

        Raises:
            Exception: Если возникает ошибка во время извлечения результатов.
        """
        results: list = []
        for agent in agents:
            result = self.extract_results_from_agent(agent, extraction_objective, situation, fields, fields_hints, verbose)
            results.append(result)

        return results

    def extract_results_from_agent(
        self,
        tinyperson: TinyPerson,
        extraction_objective: str = "The main points present in the agent's interactions history.",
        situation: str = "",
        fields: Optional[list] = None,
        fields_hints: Optional[dict] = None,
        verbose: Optional[bool] = None,
    ) -> Optional[dict]:
        """
        Извлекает результаты из экземпляра TinyPerson.

        Args:
            tinyperson (TinyPerson): Экземпляр TinyPerson для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация для рассмотрения.
            fields (Optional[list]): Поля для извлечения. Если None, экстрактор решит, какие имена использовать.
            fields_hints (Optional[dict]): Подсказки для полей извлечения. Сопоставляет имена полей со строками подсказок.
            verbose (Optional[bool]): Флаг для вывода отладочных сообщений.

        Returns:
            Optional[dict]: Извлеченные результаты в виде словаря или None в случае ошибки.

        Raises:
            Exception: Если возникает ошибка во время извлечения результатов.
        """
        extraction_objective, situation, fields, fields_hints, verbose = self._get_default_values_if_necessary(
            extraction_objective, situation, fields, fields_hints, verbose
        )

        messages: list = []

        rendering_configs: dict = {}
        if fields is not None:
            rendering_configs['fields'] = ', '.join(fields)

        if fields_hints is not None:
            rendering_configs['fields_hints'] = list(fields_hints.items())

        messages.append(
            {'role': 'system',
             'content': chevron.render(
                 open(self._extraction_prompt_template_path).read(),
                 rendering_configs)}
        )

        interaction_history = tinyperson.pretty_current_interactions(max_content_length=None)

        extraction_request_prompt = f"""
## Extraction objective

{extraction_objective}

## Situation
You are considering a single agent, named {tinyperson.name}. Your objective thus refers to this agent specifically.
{situation}

## Agent Interactions History

You will consider an agent's history of interactions, which include stimuli it received as well as actions it 
performed.

{interaction_history}
"""
        messages.append({'role': 'user', 'content': extraction_request_prompt})

        try:
            next_message = openai_utils.client().send_message(messages, temperature=0.0, frequency_penalty=0.0, presence_penalty=0.0)

            debug_msg = f'Extraction raw result message: {next_message}'
            logger.debug(debug_msg)
            if verbose:
                print(debug_msg)

            if next_message is not None:
                result = utils.extract_json(next_message['content'])
            else:
                result = None

            # Кэшируем результат
            self.agent_extraction[tinyperson.name] = result

            return result
        except Exception as ex:
            logger.error('Error while extracting results from agent', ex, exc_info=True)
            return None

    def extract_results_from_world(
        self,
        tinyworld: TinyWorld,
        extraction_objective: str = "The main points that can be derived from the agents conversations and actions.",
        situation: str = "",
        fields: Optional[list] = None,
        fields_hints: Optional[dict] = None,
        verbose: Optional[bool] = None,
    ) -> Optional[dict]:
        """
        Извлекает результаты из экземпляра TinyWorld.

        Args:
            tinyworld (TinyWorld): Экземпляр TinyWorld для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация для рассмотрения.
            fields (Optional[list]): Поля для извлечения. Если None, экстрактор решит, какие имена использовать.
            fields_hints (Optional[dict]): Подсказки для полей извлечения. Сопоставляет имена полей со строками подсказок.
            verbose (Optional[bool]): Флаг для вывода отладочных сообщений.

        Returns:
            Optional[dict]: Извлеченные результаты в виде словаря или None в случае ошибки.

        Raises:
            Exception: Если возникает ошибка во время извлечения результатов.
        """
        extraction_objective, situation, fields, fields_hints, verbose = self._get_default_values_if_necessary(
            extraction_objective, situation, fields, fields_hints, verbose
        )

        messages: list = []

        rendering_configs: dict = {}
        if fields is not None:
            rendering_configs['fields'] = ', '.join(fields)

        if fields_hints is not None:
            rendering_configs['fields_hints'] = list(fields_hints.items())

        messages.append(
            {'role': 'system',
             'content': chevron.render(
                 open(self._extraction_prompt_template_path).read(),
                 rendering_configs)}
        )

        # TODO: either summarize first or break up into multiple tasks
        interaction_history = tinyworld.pretty_current_interactions(max_content_length=None)

        extraction_request_prompt = f"""
## Extraction objective

{extraction_objective}

## Situation
You are considering various agents.
{situation}

## Agents Interactions History

You will consider the history of interactions from various agents that exist in an environment called {tinyworld.name}. 
Each interaction history includes stimuli the corresponding agent received as well as actions it performed.

{interaction_history}
"""
        messages.append({'role': 'user', 'content': extraction_request_prompt})

        try:
            next_message = openai_utils.client().send_message(messages, temperature=0.0)

            debug_msg = f'Extraction raw result message: {next_message}'
            logger.debug(debug_msg)
            if verbose:
                print(debug_msg)

            if next_message is not None:
                result = utils.extract_json(next_message['content'])
            else:
                result = None

            # Кэшируем результат
            self.world_extraction[tinyworld.name] = result

            return result
        except Exception as ex:
            logger.error('Error while extracting results from world', ex, exc_info=True)
            return None

    def save_as_json(self, filename: str, verbose: Optional[bool] = False) -> None:
        """
        Сохраняет последние результаты извлечения в формате JSON.

        Args:
            filename (str): Имя файла для сохранения JSON.
            verbose (Optional[bool]): Флаг для вывода отладочных сообщений.

        Raises:
            Exception: Если возникает ошибка во время сохранения файла.
        """
        try:
            with open(filename, 'w') as f:
                json.dump({'agent_extractions': self.agent_extraction,
                           'world_extraction': self.world_extraction}, f, indent=4)

            if verbose:
                print(f'Saved extraction results to {filename}')
        except Exception as ex:
            logger.error('Error while saving extraction results to JSON', ex, exc_info=True)

    def _get_default_values_if_necessary(
        self,
        extraction_objective: str,
        situation: str,
        fields: Optional[List[str]],
        fields_hints: Optional[dict],
        verbose: bool,
    ) -> tuple[str, str, Optional[List[str]], Optional[dict], bool]:
        """
        Возвращает значения по умолчанию, если необходимо.

        Args:
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация.
            fields (Optional[List[str]]): Поля.
            fields_hints (Optional[dict]): Подсказки для полей.
            verbose (bool): Флаг verbose.

        Returns:
            tuple[str, str, Optional[List[str]], Optional[dict], bool]: Кортеж значений.
        """
        if extraction_objective is None:
            extraction_objective = self.default_extraction_objective

        if situation is None:
            situation = self.default_situation

        if fields is None:
            fields = self.default_fields

        if fields_hints is None:
            fields_hints = self.default_fields_hints

        if verbose is None:
            verbose = self.default_verbose

        return extraction_objective, situation, fields, fields_hints, verbose