### **Анализ кода модуля `extraction.py`**

**Описание:**
Модуль содержит классы и функции для извлечения, преобразования и экспорта данных из симуляций TinyTroupe. Он предоставляет инструменты для анализа взаимодействий агентов, сведения результатов и экспорта артефактов в различные форматы.

**Расположение:**
Файл находится в директории `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/extraction.py`, что указывает на его роль в подсистеме TinyTroupe для обработки и анализа данных, полученных в результате симуляций.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура классов, разделение ответственности между `ResultsExtractor`, `ResultsReducer` и `ArtifactExporter`.
  - Использование `chevron` для шаблонизации промптов.
  - Логирование с использованием модуля `logger`.
  - Наличие docstring для большинства методов и классов.
- **Минусы**:
  - В некоторых местах отсутствует аннотация типов.
  - Использование `Union` вместо `|` для обозначения нескольких типов.
  - Docstring на английском языке.
  - Не все функции документированы в соответствии с требованиями.
  - Не везде используется `logger.error` для логирования ошибок с передачей исключения.

**Рекомендации по улучшению:**
- Перевести все docstring на русский язык и привести их к требуемому формату.
- Заменить `Union` на `|` в аннотациях типов.
- Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
- Улучшить обработку исключений, используя `logger.error` для логирования ошибок с передачей исключения.
- Добавить больше комментариев для пояснения сложных участков кода.
- Использовать одинарные кавычки для строк.
- Изменить способ открытия файлов, заменив `open` на `j_loads` или `j_loads_ns`.

**Оптимизированный код:**

```python
"""
Модуль для извлечения, преобразования и экспорта данных из симуляций TinyTroupe.
==============================================================================

Модуль содержит классы:
- `ResultsExtractor`: Извлечение результатов из агентов и окружения.
- `ResultsReducer`: Сведение результатов взаимодействий агентов.
- `ArtifactExporter`: Экспорт артефактов в различные форматы.
- `Normalizer`: Нормализация текстовых элементов.

Пример использования
----------------------

>>> extractor = ResultsExtractor()
>>> # Пример извлечения результатов из агента
>>> # agent_results = extractor.extract_results_from_agent(agent, extraction_objective="Some objective")
"""

import os
import json
import chevron
import pandas as pd
import pypandoc
import markdown
from typing import Union, List, Optional, Callable
import logging
from pathlib import Path

from src.logger import logger  # Используем logger из src.logger
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.utils import JsonSerializableRegistry

from tinytroupe import openai_utils
import tinytroupe.utils as utils


class ResultsExtractor:
    """
    Извлекает результаты из экземпляров TinyPerson и TinyWorld.
    Кэширует результаты извлечения для последующего использования.
    """

    def __init__(self) -> None:
        """
        Инициализирует ResultsExtractor, устанавливая путь к шаблону промпта и создавая кэш для результатов извлечения.
        """
        self._extraction_prompt_template_path: str = os.path.join(
            os.path.dirname(__file__), 'prompts/interaction_results_extractor.mustache'
        )

        # Кэш для последних результатов извлечения для каждого типа извлечения
        self.agent_extraction: dict = {}
        self.world_extraction: dict = {}

    def extract_results_from_agent(
        self,
        tinyperson: TinyPerson,
        extraction_objective: str = "The main points present in the agent's interactions history.",
        situation: str = "",
        fields: Optional[List[str]] = None,
        fields_hints: Optional[dict] = None,
        verbose: bool = False,
    ) -> Optional[dict]:
        """
        Извлекает результаты из экземпляра TinyPerson.

        Args:
            tinyperson (TinyPerson): Экземпляр TinyPerson для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Контекст ситуации.
            fields (Optional[List[str]]): Список полей для извлечения. Если `None`, экстрактор сам определит, какие имена использовать.
            fields_hints (Optional[dict]): Словарь с подсказками для полей извлечения.
            verbose (bool): Если `True`, выводятся отладочные сообщения.

        Returns:
            Optional[dict]: Результат извлечения в формате словаря или `None` в случае ошибки.

        Raises:
            Exception: Если возникает ошибка при отправке сообщения или извлечении JSON.

        Example:
            >>> extractor = ResultsExtractor()
            >>> agent = TinyPerson(name='Agent1')
            >>> results = extractor.extract_results_from_agent(agent, extraction_objective='Main points')
            >>> if results:
            ...     print(results)
        """
        messages: list = []

        rendering_configs: dict = {}
        if fields is not None:
            rendering_configs['fields'] = ', '.join(fields)

        if fields_hints is not None:
            rendering_configs['fields_hints'] = list(fields_hints.items())

        # Добавляем системное сообщение с использованием шаблона
        try:
            with open(self._extraction_prompt_template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            messages.append({'role': 'system', 'content': chevron.render(template, rendering_configs)})
        except Exception as ex:
            logger.error('Error while rendering extraction prompt template', ex, exc_info=True)
            return None

        interaction_history: str = tinyperson.pretty_current_interactions(max_content_length=None)

        extraction_request_prompt: str = f"""
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
            next_message: Optional[dict] = openai_utils.client().send_message(messages, temperature=0.0)

            debug_msg: str = f"Extraction raw result message: {next_message}"
            logger.debug(debug_msg)
            if verbose:
                print(debug_msg)

            if next_message is not None:
                result: Optional[dict] = utils.extract_json(next_message['content'])
            else:
                result: Optional[dict] = None

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
        fields: Optional[List[str]] = None,
        fields_hints: Optional[dict] = None,
        verbose: bool = False,
    ) -> Optional[dict]:
        """
        Извлекает результаты из экземпляра TinyWorld.

        Args:
            tinyworld (TinyWorld): Экземпляр TinyWorld для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Контекст ситуации.
            fields (Optional[List[str]]): Список полей для извлечения. Если `None`, экстрактор сам определит, какие имена использовать.
            fields_hints (Optional[dict]): Словарь с подсказками для полей извлечения.
            verbose (bool): Если `True`, выводятся отладочные сообщения.

        Returns:
            Optional[dict]: Результат извлечения в формате словаря или `None` в случае ошибки.

        Raises:
            Exception: Если возникает ошибка при отправке сообщения или извлечении JSON.
        """
        messages: list = []

        rendering_configs: dict = {}
        if fields is not None:
            rendering_configs['fields'] = ', '.join(fields)

        if fields_hints is not None:
            rendering_configs['fields_hints'] = list(fields_hints.items())

        try:
            with open(self._extraction_prompt_template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            messages.append({'role': 'system', 'content': chevron.render(template, rendering_configs)})
        except Exception as ex:
            logger.error('Error while rendering extraction prompt template', ex, exc_info=True)
            return None

        # TODO: either summarize first or break up into multiple tasks
        interaction_history: str = tinyworld.pretty_current_interactions(max_content_length=None)

        extraction_request_prompt: str = f"""
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
            next_message: Optional[dict] = openai_utils.client().send_message(messages, temperature=0.0)

            debug_msg: str = f"Extraction raw result message: {next_message}"
            logger.debug(debug_msg)
            if verbose:
                print(debug_msg)

            if next_message is not None:
                result: Optional[dict] = utils.extract_json(next_message['content'])
            else:
                result: Optional[dict] = None

            # Кэшируем результат
            self.world_extraction[tinyworld.name] = result

            return result
        except Exception as ex:
            logger.error('Error while extracting results from world', ex, exc_info=True)
            return None

    def save_as_json(self, filename: str, verbose: bool = False) -> None:
        """
        Сохраняет последние результаты извлечения в формате JSON.

        Args:
            filename (str): Имя файла для сохранения JSON.
            verbose (bool): Если `True`, выводятся отладочные сообщения.

        Raises:
            Exception: Если возникает ошибка при записи в файл.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(
                    {'agent_extractions': self.agent_extraction, 'world_extraction': self.world_extraction},
                    f,
                    indent=4,
                )

            if verbose:
                print(f"Saved extraction results to {filename}")
        except Exception as ex:
            logger.error('Error while saving extraction results to JSON', ex, exc_info=True)


class ResultsReducer:
    """
    Сокращает результаты взаимодействий агентов на основе заданных правил.
    """

    def __init__(self) -> None:
        """
        Инициализирует ResultsReducer, создавая хранилище для результатов и правил.
        """
        self.results: dict = {}
        self.rules: dict = {}

    def add_reduction_rule(self, trigger: str, func: Callable) -> None:
        """
        Добавляет правило сокращения для указанного триггера.

        Args:
            trigger (str): Триггер, при котором применяется правило.
            func (callable): Функция, выполняющая сокращение.

        Raises:
            Exception: Если правило для указанного триггера уже существует.
        """
        if trigger in self.rules:
            raise Exception(f"Rule for {trigger} already exists.")

        self.rules[trigger] = func

    def reduce_agent(self, agent: TinyPerson) -> list:
        """
        Сокращает историю взаимодействий агента на основе заданных правил.

        Args:
            agent (TinyPerson): Агент, для которого выполняется сокращение.

        Returns:
            list: Список сокращенных данных.
        """
        reduction: list = []
        for message in agent.episodic_memory.retrieve_all():
            if message['role'] == 'system':
                continue  # doing nothing for `system` role yet at least

            elif message['role'] == 'user':
                # User role is related to stimuli only
                stimulus_type: str = message['content']['stimuli'][0]['type']
                stimulus_content: str = message['content']['stimuli'][0]['content']
                stimulus_source: str = message['content']['stimuli'][0]['source']
                stimulus_timestamp: str = message['simulation_timestamp']

                if stimulus_type in self.rules:
                    extracted = self.rules[stimulus_type](
                        focus_agent=agent,
                        source_agent=TinyPerson.get_agent_by_name(stimulus_source),
                        target_agent=agent,
                        kind='stimulus',
                        event=stimulus_type,
                        content=stimulus_content,
                        timestamp=stimulus_timestamp,
                    )
                    if extracted is not None:
                        reduction.append(extracted)

            elif message['role'] == 'assistant':
                # Assistant role is related to actions only
                if 'action' in message['content']:
                    action_type: str = message['content']['action']['type']
                    action_content: str = message['content']['action']['content']
                    action_target: str = message['content']['action']['target']
                    action_timestamp: str = message['simulation_timestamp']

                    if action_type in self.rules:
                        extracted = self.rules[action_type](
                            focus_agent=agent,
                            source_agent=agent,
                            target_agent=TinyPerson.get_agent_by_name(action_target),
                            kind='action',
                            event=action_type,
                            content=action_content,
                            timestamp=action_timestamp,
                        )
                        if extracted is not None:
                            reduction.append(extracted)

        return reduction

    def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: Optional[list] = None) -> pd.DataFrame:
        """
        Сокращает историю взаимодействий агента и преобразует результат в DataFrame.

        Args:
            agent (TinyPerson): Агент, для которого выполняется сокращение.
            column_names (Optional[list]): Список имен столбцов для DataFrame.

        Returns:
            pd.DataFrame: DataFrame с сокращенными данными.
        """
        reduction: list = self.reduce_agent(agent)
        return pd.DataFrame(reduction, columns=column_names)


class ArtifactExporter(JsonSerializableRegistry):
    """
    Экспортер артефактов из элементов TinyTroupe, например, для создания синтетических файлов данных из симуляций.
    """

    def __init__(self, base_output_folder: str) -> None:
        """
        Инициализирует ArtifactExporter с указанием базовой папки для вывода артефактов.

        Args:
            base_output_folder (str): Базовая папка для вывода артефактов.
        """
        self.base_output_folder: str = base_output_folder

    def export(
        self,
        artifact_name: str,
        artifact_data: Union[dict, str],
        content_type: str,
        content_format: Optional[str] = None,
        target_format: str = "txt",
        verbose: bool = False,
    ) -> None:
        """
        Экспортирует указанные данные артефакта в файл.

        Args:
            artifact_name (str): Имя артефакта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если передан словарь, он будет сохранен в формате JSON. Если передана строка, она будет сохранена как есть.
            content_type (str): Тип содержимого артефакта.
            content_format (Optional[str]): Формат содержимого артефакта (например, md, csv и т.д.).
            target_format (str): Формат для экспорта артефакта (например, json, txt, docx и т.д.).
            verbose (bool): Если `True`, выводятся отладочные сообщения.

        Raises:
            ValueError: Если передан неподдерживаемый формат артефакта или данных.
            Exception: Если возникает ошибка при экспорте артефакта.
        """

        # dedent inputs, just in case
        if isinstance(artifact_data, str):
            artifact_data = utils.dedent(artifact_data)
        elif isinstance(artifact_data, dict):
            artifact_data['content'] = utils.dedent(artifact_data['content'])
        else:
            raise ValueError("The artifact data must be either a string or a dictionary.")

        # clean the artifact name of invalid characters
        invalid_chars: list = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\t', '\r', ';']
        for char in invalid_chars:
            # check if the character is in the artifact name
            if char in artifact_name:
                # replace the character with an underscore
                artifact_name = artifact_name.replace(char, "-")
                logger.warning(f"Replaced invalid character {char} with hyphen in artifact name '{artifact_name}'.")

        artifact_file_path: str = self._compose_filepath(artifact_data, artifact_name, content_type, target_format, verbose)

        try:
            if target_format == "json":
                self._export_as_json(artifact_file_path, artifact_data, content_type, verbose)
            elif target_format == "txt" or target_format == "text" or target_format == "md" or target_format == "markdown":
                self._export_as_txt(artifact_file_path, artifact_data, content_type, verbose)
            elif target_format == "docx":
                self._export_as_docx(artifact_file_path, artifact_data, content_format, verbose)
            else:
                raise ValueError(f"Unsupported target format: {target_format}.")
        except Exception as ex:
            logger.error('Error while exporting artifact', ex, exc_info=True)

    def _export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
        """
        Экспортирует указанные данные артефакта в текстовый файл.
        """

        try:
            with open(artifact_file_path, 'w', encoding="utf-8") as f:
                if isinstance(artifact_data, dict):
                    content: str = artifact_data['content']
                else:
                    content: str = artifact_data

                f.write(content)
        except Exception as ex:
            logger.error('Error while exporting artifact as TXT', ex, exc_info=True)

    def _export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
        """
        Экспортирует указанные данные артефакта в JSON-файл.
        """

        try:
            with open(artifact_file_path, 'w', encoding="utf-8") as f:
                if isinstance(artifact_data, dict):
                    json.dump(artifact_data, f, indent=4)
                else:
                    raise ValueError("The artifact data must be a dictionary to export to JSON.")
        except Exception as ex:
            logger.error('Error while exporting artifact as JSON', ex, exc_info=True)

    def _export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False) -> None:
        """
        Экспортирует указанные данные артефакта в DOCX-файл.
        """

        # original format must be 'text' or 'markdown'
        if content_original_format not in ['text', 'txt', 'markdown', 'md']:
            raise ValueError(f"The original format cannot be {content_original_format} to export to DOCX.")
        else:
            # normalize content value
            content_original_format = 'markdown' if content_original_format == 'md' else content_original_format

        # first, get the content to export. If `artifact_date` is a dict, the contant should be under the key `content`.
        # If it is a string, the content is the string itself.
        # using pypandoc
        if isinstance(artifact_data, dict):
            content: str = artifact_data['content']
        else:
            content: str = artifact_data

        # first, convert to HTML. This is necessary because pypandoc does not support a GOOD direct conversion from markdown to DOCX.
        html_content: str = markdown.markdown(content)

        ## write this intermediary HTML to file
        # html_file_path = artifact_file_path.replace(".docx", ".html")
        # with open(html_file_path, 'w', encoding="utf-8") as f:
        #    f.write(html_content)

        # then, convert to DOCX
        try:
            pypandoc.convert_text(html_content, 'docx', format='html', outputfile=artifact_file_path)
        except Exception as ex:
            logger.error('Error while exporting artifact as DOCX', ex, exc_info=True)

    ###########################################################
    # IO
    ###########################################################

    def _compose_filepath(
        self,
        artifact_data: Union[dict, str],
        artifact_name: str,
        content_type: str,
        target_format: Optional[str] = None,
        verbose: bool = False,
    ) -> str:
        """
        Составляет путь к файлу для экспорта артефакта.

        Args:
            artifact_data (Union[dict, str]): Данные для экспорта.
            artifact_name (str): Имя артефакта.
            content_type (str): Тип содержимого артефакта.
            target_format (Optional[str]): Формат содержимого артефакта (например, md, csv и т.д.).
            verbose (bool): Если `True`, выводятся отладочные сообщения.

        Returns:
            str: Полный путь к файлу артефакта.
        """

        # Extension definition:
        #
        # - If the content format is specified, we use it as the part of the extension.
        # - If artificat_data is a dict, we add .json to the extension. Note that if content format was specified, we'd get <content_format>.json.
        # - If artifact_data is a string and no content format is specified, we add .txt to the extension.
        extension: str | None = None
        if target_format is not None:
            extension = f"{target_format}"
        elif isinstance(artifact_data, str) and target_format is None:
            extension = "txt"

        # content type definition
        if content_type is None:
            subfolder: str = ""
        else:
            subfolder = content_type

        # save to the specified file name or path, considering the base output folder.
        artifact_file_path: str = os.path.join(self.base_output_folder, subfolder, f"{artifact_name}.{extension}")

        # create intermediate directories if necessary
        os.makedirs(os.path.dirname(artifact_file_path), exist_ok=True)

        return artifact_file_path


class Normalizer:
    """
    Механизм для нормализации фрагментов текста, концепций и других текстовых элементов.
    """

    def __init__(self, elements: List[str], n: int, verbose: bool = False) -> None:
        """
        Инициализирует Normalizer с указанием элементов для нормализации, количества выходных элементов и режима verbose.

        Args:
            elements (list): Элементы для нормализации.
            n (int): Количество нормализованных элементов для вывода.
            verbose (bool): Если `True`, выводятся отладочные сообщения.
        """
        # ensure elements are unique
        self.elements: list = list(set(elements))

        self.n: int = n
        self.verbose: bool = verbose

        # a JSON-based structure, where each output element is a key to a list of input elements that were merged into it
        self.normalized_elements: Optional[dict] = None
        # a dict that maps each input element to its normalized output. This will be used as cache later.
        self.normalizing_map: dict = {}

        rendering_configs: dict = {"n": n, "elements": self.elements}

        messages: list = utils.compose_initial_LLM_messages_with_templates(
            "normalizer.system.mustache", "normalizer.user.mustache", rendering_configs
        )
        next_message: Optional[dict] = openai_utils.client().send_message(messages, temperature=0.1)

        debug_msg: str = f"Normalization result message: {next_message}"
        logger.debug(debug_msg)
        if self.verbose:
            print(debug_msg)

        result: Optional[dict] = utils.extract_json(next_message["content"])
        logger.debug(result)
        if self.verbose:
            print(result)

        self.normalized_elements = result

    def normalize(self, element_or_elements: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Нормализует указанный элемент или элементы.

        Этот метод использует механизм кэширования для повышения производительности. Если элемент был нормализован ранее,
        его нормализованная форма хранится в кэше (self.normalizing_map). Когда тот же элемент необходимо
        нормализовать снова, метод сначала проверяет кэш и использует сохраненную нормализованную форму,
        вместо повторной нормализации элемента.

        Порядок элементов в выходных данных будет таким же, как и на входе. Это обеспечивается обработкой
        элементов в том порядке, в котором они появляются на входе, и добавлением нормализованных элементов в выходные
        данные в том же порядке.

        Args:
            element_or_elements (Union[str, List[str]]): Элемент или элементы для нормализации.

        Returns:
            str: Нормализованный элемент, если на входе была строка.
            list: Нормализованные элементы, если на входе был список, с сохранением порядка элементов на входе.
        """
        if isinstance(element_or_elements, str):
            denormalized_elements: list = [element_or_elements]
        elif isinstance(element_or_elements, list):
            denormalized_elements: list = element_or_elements
        else:
            raise ValueError("The element_or_elements must be either a string or a list.")

        normalized_elements: list = []
        elements_to_normalize: list = []
        for element in denormalized_elements:
            if element not in self.normalizing_map:
                elements_to_normalize.append(element)

        if elements_to_normalize:
            rendering_configs: dict = {"categories": self.normalized_elements, "elements": elements_to_normalize}

            messages: list = utils.compose_initial_LLM_messages_with_templates(
                "normalizer.applier.system.mustache", "normalizer.applier.user.mustache", rendering_configs
            )
            next_message: Optional[dict] = openai_utils.client().send_message(messages, temperature=0.1)

            debug_msg: str = f"Normalization result message: {next_message}"
            logger.debug(debug_msg)
            if self.verbose:
                print(debug_msg)

            normalized_elements_from_llm: list = utils.extract_json(next_message["content"])
            assert isinstance(normalized_elements_from_llm, list), "The normalized element must be a list."
            assert len(normalized_elements_from_llm) == len(
                elements_to_normalize
            ), "The number of normalized elements must be equal to the number of elements to normalize."

            for i, element in enumerate(elements_to_normalize):
                normalized_element: str = normalized_elements_from_llm[i]
                self.normalizing_map[element] = normalized_element

        for element in denormalized_elements:
            normalized_elements.append(self.normalizing_map[element])

        return normalized_elements


################################################################################
# Convenience mechanisms
################################################################################

# default extractor
default_extractor: ResultsExtractor = ResultsExtractor()