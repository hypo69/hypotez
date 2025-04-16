### **Анализ кода модуля `results_extractor.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на отдельные методы, что облегчает его понимание и поддержку.
  - Присутствуют docstring для большинства методов, что помогает понять их назначение и параметры.
  - Использование `chevron` для шаблонизации промптов.
- **Минусы**:
  - Отсутствуют аннотации типов для параметров и возвращаемых значений в некоторых методах.
  - В некоторых местах используется смешанный стиль кавычек (где-то одинарные, где-то двойные).
  - Не все docstring соответствуют требуемому формату (отсутствуют примеры использования, не все параметры описаны).
  - Не используется модуль `logger` из `src.logger.logger` для логирования ошибок.

#### **Рекомендации по улучшению**:
1. **Добавить docstring модуля**:
   - В начале файла добавить docstring с описанием модуля, его назначения и примерами использования.

2. **Добавить аннотации типов**:
   - Добавить аннотации типов для всех параметров и возвращаемых значений функций и методов.

3. **Унифицировать стиль кавычек**:
   - Использовать только одинарные кавычки (`'`) для строк.

4. **Доработать docstring**:
   - Привести docstring к единому формату, включающему описание параметров, возвращаемых значений, возможных исключений и примеров использования.
   - Перевести все docstring на русский язык.

5. **Использовать `logger`**:
   - Заменить `print` на `logger.debug` для отладочных сообщений.
   - Добавить обработку исключений с использованием `logger.error` для логирования ошибок.

6. **Улучшить читаемость**:
   - Добавить пробелы вокруг операторов присваивания.

#### **Оптимизированный код**:
```python
"""
Модуль для извлечения результатов из взаимодействий агентов и окружения
=====================================================================

Модуль содержит класс :class:`ResultsExtractor`, который используется для извлечения информации из истории взаимодействий агентов
в TinyTroupe. Он использует шаблоны для формирования запросов к языковой модели и извлекает результаты в формате JSON.

Пример использования
----------------------

>>> extractor = ResultsExtractor()
>>> results = extractor.extract_results_from_agents(agents=[agent1, agent2])
>>> print(results)
"""
import os
import json
import chevron
import pandas as pd
from typing import Union, List, Optional

from src.logger import logger
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

from tinytroupe import openai_utils
import tinytroupe.utils as utils


class ResultsExtractor:
    """
    Извлекает результаты из взаимодействий агентов и окружения.
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
        verbose: bool = False,
    ) -> None:
        """
        Инициализирует ResultsExtractor с параметрами по умолчанию.

        Args:
            extraction_prompt_template_path (str): Путь к шаблону промпта для извлечения.
            extraction_objective (str): Цель извлечения по умолчанию.
            situation (str): Ситуация для рассмотрения по умолчанию.
            fields (Optional[List[str]]): Поля для извлечения по умолчанию.
            fields_hints (Optional[dict]): Подсказки для полей для извлечения по умолчанию.
            verbose (bool): Флаг для вывода отладочных сообщений по умолчанию.
        """
        self._extraction_prompt_template_path = extraction_prompt_template_path

        # Параметры по умолчанию
        self.default_extraction_objective = extraction_objective
        self.default_situation = situation
        self.default_fields = fields
        self.default_fields_hints = fields_hints
        self.default_verbose = verbose

        # Кэш для последних результатов извлечения
        self.agent_extraction = {}
        self.world_extraction = {}

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
            fields (Optional[list]): Поля для извлечения. Если `None`, извлекатель решит, какие имена использовать.
            fields_hints (Optional[dict]): Подсказки для полей для извлечения. Сопоставляет имена полей со строками с подсказками.
            verbose (Optional[bool]): Флаг для вывода отладочных сообщений.

        Returns:
            list: Список извлеченных результатов.
        """
        results = []
        for agent in agents:
            result = self.extract_results_from_agent(
                agent, extraction_objective, situation, fields, fields_hints, verbose
            )
            results.append(result)

        return results

    def extract_results_from_agent(
        self,
        tinyperson: TinyPerson,
        extraction_objective: str = "The main points present in the agent's interactions history.",
        situation: str = "",
        fields: Optional[list] = None,
        fields_hints: Optional[dict] = None,
        verbose: bool = None,
    ) -> dict | None:
        """
        Извлекает результаты из экземпляра TinyPerson.

        Args:
            tinyperson (TinyPerson): Экземпляр TinyPerson для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация для рассмотрения.
            fields (Optional[list]): Поля для извлечения. Если `None`, извлекатель решит, какие имена использовать.
            fields_hints (Optional[dict]): Подсказки для полей для извлечения. Сопоставляет имена полей со строками с подсказками.
            verbose (bool): Флаг для вывода отладочных сообщений.

        Returns:
            dict | None: Извлеченные результаты в формате словаря или `None` в случае ошибки.
        """
        extraction_objective, situation, fields, fields_hints, verbose = (
            self._get_default_values_if_necessary(
                extraction_objective, situation, fields, fields_hints, verbose
            )
        )

        messages = []

        rendering_configs = {}
        if fields is not None:
            rendering_configs['fields'] = ', '.join(fields)

        if fields_hints is not None:
            rendering_configs['fields_hints'] = list(fields_hints.items())

        messages.append(
            {
                'role': 'system',
                'content': chevron.render(
                    open(self._extraction_prompt_template_path).read(), rendering_configs
                ),
            }
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
            next_message = openai_utils.client().send_message(
                messages, temperature=0.0, frequency_penalty=0.0, presence_penalty=0.0
            )
        except Exception as ex:
            logger.error('Ошибка при отправке сообщения в OpenAI', ex, exc_info=True)
            return None

        debug_msg = f'Extraction raw result message: {next_message}'
        logger.debug(debug_msg)
        if verbose:
            print(debug_msg)

        if next_message is not None:
            result = utils.extract_json(next_message['content'])
        else:
            result = None

        # кэшируем результат
        self.agent_extraction[tinyperson.name] = result

        return result

    def extract_results_from_world(
        self,
        tinyworld: TinyWorld,
        extraction_objective: str = "The main points that can be derived from the agents conversations and actions.",
        situation: str = "",
        fields: Optional[list] = None,
        fields_hints: Optional[dict] = None,
        verbose: bool = None,
    ) -> dict | None:
        """
        Извлекает результаты из экземпляра TinyWorld.

        Args:
            tinyworld (TinyWorld): Экземпляр TinyWorld для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация для рассмотрения.
            fields (Optional[list]): Поля для извлечения. Если `None`, извлекатель решит, какие имена использовать.
            fields_hints (Optional[dict]): Подсказки для полей для извлечения. Сопоставляет имена полей со строками с подсказками.
            verbose (bool): Флаг для вывода отладочных сообщений.

        Returns:
            dict | None: Извлеченные результаты в формате словаря или `None` в случае ошибки.
        """
        extraction_objective, situation, fields, fields_hints, verbose = (
            self._get_default_values_if_necessary(
                extraction_objective, situation, fields, fields_hints, verbose
            )
        )

        messages = []

        rendering_configs = {}
        if fields is not None:
            rendering_configs['fields'] = ', '.join(fields)

        if fields_hints is not None:
            rendering_configs['fields_hints'] = list(fields_hints.items())

        messages.append(
            {
                'role': 'system',
                'content': chevron.render(
                    open(self._extraction_prompt_template_path).read(), rendering_configs
                ),
            }
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
        except Exception as ex:
            logger.error('Ошибка при отправке сообщения в OpenAI', ex, exc_info=True)
            return None

        debug_msg = f'Extraction raw result message: {next_message}'
        logger.debug(debug_msg)
        if verbose:
            print(debug_msg)

        if next_message is not None:
            result = utils.extract_json(next_message['content'])
        else:
            result = None

        # кэшируем результат
        self.world_extraction[tinyworld.name] = result

        return result

    def save_as_json(self, filename: str, verbose: bool = False) -> None:
        """
        Сохраняет последние результаты извлечения в формате JSON.

        Args:
            filename (str): Имя файла для сохранения JSON.
            verbose (bool): Флаг для вывода отладочных сообщений.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(
                    {'agent_extractions': self.agent_extraction, 'world_extraction': self.world_extraction},
                    f,
                    indent=4,
                )
        except Exception as ex:
            logger.error('Ошибка при сохранении в JSON', ex, exc_info=True)

        if verbose:
            print(f'Saved extraction results to {filename}')

    def _get_default_values_if_necessary(
        self,
        extraction_objective: str,
        situation: str,
        fields: List[str],
        fields_hints: dict,
        verbose: bool,
    ) -> tuple[str, str, List[str], dict, bool]:
        """
        Возвращает значения по умолчанию, если необходимо.

        Args:
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация.
            fields (List[str]): Поля.
            fields_hints (dict): Подсказки для полей.
            verbose (bool): Флаг для вывода отладочных сообщений.

        Returns:
            tuple[str, str, List[str], dict, bool]: Кортеж значений.
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