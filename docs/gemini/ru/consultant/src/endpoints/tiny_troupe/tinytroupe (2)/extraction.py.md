### Анализ кода модуля `extraction`

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Код содержит полезные классы для извлечения, сведения и экспорта данных из симуляций TinyTroupe.
     - Присутствуют docstring для большинства методов и классов, что облегчает понимание функциональности кода.
     - Использование `chevron` для шаблонизации prompt-ов.
     - Использование `logger` для отладки и логирования.
   - **Минусы**:
     - В коде присутствуют закомментированные участки кода, которые следует удалить.
     - Некоторые docstring написаны на английском языке.
     - Отсутствуют аннотации типов для параметров функций и переменных.
     - Не везде используется `logger.error` при обработке исключений.
     - Не используется `j_loads` для загрузки JSON файлов.

3. **Рекомендации по улучшению**:
   - Перевести docstring на русский язык.
   - Добавить аннотации типов для всех параметров функций и переменных.
   - Использовать `logger.error` с передачей исключения при обработке исключений.
   - Использовать `j_loads` для загрузки JSON файлов.
   - Описать модуль в соответствии с требованием в задании
   - Избавиться от использования `Union` в пользу `|`
   - Добавить комментарии к логике работы кода

4. **Оптимизированный код**:

```python
"""
Модуль для извлечения, сведения и экспорта данных из симуляций TinyTroupe
========================================================================

Модуль содержит классы:
- :class:`ResultsExtractor`: Извлекает данные из объектов TinyTroupe (агентов и миров).
- :class:`ResultsReducer`: Уменьшает объем извлеченных данных.
- :class:`ArtifactExporter`: Экспортирует артефакты из элементов TinyTroupe.
- :class:`Normalizer`: Нормализует текстовые элементы.

Пример использования
----------------------

>>> extractor = ResultsExtractor()
>>> # Извлечение результатов из агента
>>> agent_results = extractor.extract_results_from_agent(tinyperson, extraction_objective="Main points")
>>> # Сохранение результатов в JSON
>>> extractor.save_as_json("agent_results.json")
"""

import os
import json
import chevron
import pandas as pd
import pypandoc
import markdown
from typing import Union, List, Optional, Callable, Dict
import logging
from pathlib import Path

from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.utils import JsonSerializableRegistry
from tinytroupe import openai_utils
import tinytroupe.utils as utils
from src.logger import logger
from src.utils.file_utils import j_loads

class ResultsExtractor:
    """
    Извлекает результаты из экземпляров TinyPerson и TinyWorld.
    """

    def __init__(self):
        """
        Инициализирует ResultsExtractor.
        """
        self._extraction_prompt_template_path: str = os.path.join(os.path.dirname(__file__), 'prompts/interaction_results_extractor.mustache')

        # Кэшируем последние результаты извлечения для каждого типа, чтобы использовать их для создания отчетов и других выходных данных.
        self.agent_extraction: Dict = {}
        self.world_extraction: Dict = {}

    def extract_results_from_agent(
        self,
        tinyperson: TinyPerson,
        extraction_objective: str = "The main points present in the agent's interactions history.",
        situation: str = "",
        fields: Optional[List[str]] = None,
        fields_hints: Optional[Dict] = None,
        verbose: bool = False
    ) -> Optional[Dict]:
        """
        Извлекает результаты из экземпляра TinyPerson.

        Args:
            tinyperson (TinyPerson): Экземпляр TinyPerson для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация для рассмотрения.
            fields (Optional[List[str]]): Поля для извлечения. Если `None`, экстрактор решит, какие имена использовать. Defaults to None.
            fields_hints (Optional[Dict]):  Словарик с информацией о том, что нужно извлечь.
            verbose (bool): Печатать ли отладочные сообщения. Defaults to False.

        Returns:
            Optional[Dict]: Извлеченные результаты в виде словаря или None в случае ошибки.
        
        Example:
            >>> extractor = ResultsExtractor()
            >>> agent = TinyPerson(name='TestAgent')
            >>> results = extractor.extract_results_from_agent(agent, extraction_objective='Main points')
            >>> print(results)
            {}
        """
        messages: List[Dict] = []

        rendering_configs: Dict = {}
        if fields is not None:
            rendering_configs["fields"] = ", ".join(fields)
        
        if fields_hints is not None:
            rendering_configs["fields_hints"] = list(fields_hints.items())
        
        # Добавляем системное сообщение с шаблоном извлечения
        try:
            with open(self._extraction_prompt_template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            messages.append({"role": "system", 
                             "content": chevron.render(
                                 template, 
                                 rendering_configs)})
        except Exception as ex:
            logger.error(f'Can\'t read template file {self._extraction_prompt_template_path}', ex, exc_info=True)
            return None

        interaction_history: str = tinyperson.pretty_current_interactions(max_content_length=None)

        extraction_request_prompt: str = \
f"""
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
        messages.append({"role": "user", "content": extraction_request_prompt})

        try:
            next_message = openai_utils.client().send_message(messages, temperature=0.0)
        except Exception as ex:
            logger.error('Error while sending message to OpenAI client', ex, exc_info=True)
            return None
        
        debug_msg: str = f"Extraction raw result message: {next_message}"
        logger.debug(debug_msg)
        if verbose:
            print(debug_msg)

        if next_message is not None:
            result: Optional[Dict] = utils.extract_json(next_message["content"])
        else:
            result: Optional[Dict] = None
        
        # Кэшируем результат
        self.agent_extraction[tinyperson.name] = result

        return result
    

    def extract_results_from_world(
        self,
        tinyworld: TinyWorld,
        extraction_objective: str = "The main points that can be derived from the agents conversations and actions.",
        situation: str = "",
        fields: Optional[List[str]] = None,
        fields_hints: Optional[Dict] = None,
        verbose: bool = False
    ) -> Optional[Dict]:
        """
        Извлекает результаты из экземпляра TinyWorld.

        Args:
            tinyworld (TinyWorld): Экземпляр TinyWorld для извлечения результатов.
            extraction_objective (str): Цель извлечения.
            situation (str): Ситуация для рассмотрения.
            fields (Optional[List[str]]): Поля для извлечения. Если `None`, экстрактор решит, какие имена использовать. Defaults to None.
            fields_hints (Optional[Dict]):  Словарик с информацией о том, что нужно извлечь.
            verbose (bool): Печатать ли отладочные сообщения. Defaults to False.

        Returns:
            Optional[Dict]: Извлеченные результаты в виде словаря или None в случае ошибки.
        
        Example:
            >>> extractor = ResultsExtractor()
            >>> world = TinyWorld(name='TestWorld')
            >>> results = extractor.extract_results_from_world(world, extraction_objective='Main points')
            >>> print(results)
            {}
        """
        messages: List[Dict] = []

        rendering_configs: Dict = {}
        if fields is not None:
            rendering_configs["fields"] = ", ".join(fields)
        
        if fields_hints is not None:
            rendering_configs["fields_hints"] = list(fields_hints.items())
        

        try:
            with open(self._extraction_prompt_template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            messages.append({"role": "system", 
                             "content": chevron.render(
                                 template, 
                                 rendering_configs)})
        except Exception as ex:
            logger.error(f'Can\'t read template file {self._extraction_prompt_template_path}', ex, exc_info=True)
            return None

        # TODO: either summarize first or break up into multiple tasks
        interaction_history: str = tinyworld.pretty_current_interactions(max_content_length=None)

        extraction_request_prompt: str = \
f"""
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
        messages.append({"role": "user", "content": extraction_request_prompt})

        try:
            next_message = openai_utils.client().send_message(messages, temperature=0.0)
        except Exception as ex:
            logger.error('Error while sending message to OpenAI client', ex, exc_info=True)
            return None
        
        debug_msg: str = f"Extraction raw result message: {next_message}"
        logger.debug(debug_msg)
        if verbose:
            print(debug_msg)

        if next_message is not None:
            result: Optional[Dict] = utils.extract_json(next_message["content"])
        else:
            result: Optional[Dict] = None
        
        # Кэшируем результат
        self.world_extraction[tinyworld.name] = result

        return result
    
    def save_as_json(self, filename: str, verbose: bool = False) -> None:
        """
        Сохраняет последние результаты извлечения в формате JSON.

        Args:
            filename (str): Имя файла для сохранения JSON.
            verbose (bool): Печатать ли отладочные сообщения. Defaults to False.
        
        Example:
            >>> extractor = ResultsExtractor()
            >>> extractor.agent_extraction = {'agent1': {'key': 'value'}}
            >>> extractor.world_extraction = {'world1': {'key': 'value'}}
            >>> extractor.save_as_json('test.json')
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"agent_extractions": self.agent_extraction, 
                           "world_extraction": self.world_extraction}, f, indent=4)
            if verbose:
                print(f"Saved extraction results to {filename}")
        except Exception as ex:
            logger.error(f'Can\'t save to file {filename}', ex, exc_info=True)


class ResultsReducer:
    """
    Сводит результаты, используя заданные правила.
    """

    def __init__(self):
        """
        Инициализирует ResultsReducer.
        """
        self.results: Dict = {}
        self.rules: Dict = {}
    
    def add_reduction_rule(self, trigger: str, func: Callable) -> None:
        """
        Добавляет правило сведения.

        Args:
            trigger (str): Триггер для правила.
            func (Callable): Функция для выполнения при срабатывании триггера.

        Raises:
            Exception: Если правило для данного триггера уже существует.
        
        Example:
            >>> reducer = ResultsReducer()
            >>> def my_func(agent, event, content): return content
            >>> reducer.add_reduction_rule('stimulus', my_func)
        """
        if trigger in self.rules:
            raise Exception(f"Rule for {trigger} already exists.")
        
        self.rules[trigger] = func
    
    def reduce_agent(self, agent: TinyPerson) -> list:
        """
        Сводит данные агента, используя заданные правила.

        Args:
            agent (TinyPerson): Агент для сведения данных.

        Returns:
            list: Список сведенных данных.
        
        Example:
            >>> reducer = ResultsReducer()
            >>> agent = TinyPerson(name='TestAgent')
            >>> reduction = reducer.reduce_agent(agent)
            >>> print(reduction)
            []
        """
        reduction: List = []
        for message in agent.episodic_memory.retrieve_all():
            if message['role'] == 'system':
                continue # doing nothing for `system` role yet at least

            elif message['role'] == 'user':
                # User role is related to stimuli only
                stimulus_type: str = message['content']['stimuli'][0]['type']
                stimulus_content: str = message['content']['stimuli'][0]['content']
                stimulus_source: str = message['content']['stimuli'][0]['source']
                stimulus_timestamp: str = message['simulation_timestamp']

                if stimulus_type in self.rules:
                    extracted = self.rules[stimulus_type](focus_agent=agent, source_agent=TinyPerson.get_agent_by_name(stimulus_source), target_agent=agent, kind='stimulus', event=stimulus_type, content=stimulus_content, timestamp=stimulus_timestamp)
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
                        extracted = self.rules[action_type](focus_agent=agent, source_agent=agent, target_agent=TinyPerson.get_agent_by_name(action_target), kind='action', event=action_type, content=action_content, timestamp=action_timestamp)
                        if extracted is not None:
                            reduction.append(extracted)
            
        return reduction

    def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list = None) -> pd.DataFrame:
        """
        Сводит данные агента в DataFrame.

        Args:
            agent (TinyPerson): Агент для сведения данных.
            column_names (list): Список имен столбцов для DataFrame.

        Returns:
            pd.DataFrame: DataFrame со сведенными данными.
        
        Example:
            >>> reducer = ResultsReducer()
            >>> agent = TinyPerson(name='TestAgent')
            >>> df = reducer.reduce_agent_to_dataframe(agent, column_names=['event', 'content'])
            >>> print(df)
            Empty DataFrame
            Columns: [event, content]
            Index: []
        """
        reduction: List = self.reduce_agent(agent)
        return pd.DataFrame(reduction, columns=column_names)


class ArtifactExporter(JsonSerializableRegistry):
    """
    Экспортирует артефакты из элементов TinyTroupe.
    """

    def __init__(self, base_output_folder: str) -> None:
        """
        Инициализирует ArtifactExporter.

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
        verbose: bool = False
    ) -> None:
        """
        Экспортирует указанные данные артефакта в файл.

        Args:
            artifact_name (str): Имя артефакта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если dict, то сохраняется как JSON. Если str, то сохраняется как есть.
            content_type (str): Тип контента в артефакте.
            content_format (Optional[str]): Формат контента в артефакте (e.g., md, csv, etc). Defaults to None.
            target_format (str): Формат для экспорта артефакта (e.g., json, txt, docx, etc).
            verbose (bool): Печатать ли отладочные сообщения. Defaults to False.
        
        Example:
            >>> exporter = ArtifactExporter(base_output_folder='output')
            >>> exporter.export(artifact_name='test', artifact_data='test data', content_type='text')
        """
        
        # dedent inputs, just in case
        if isinstance(artifact_data, str):
            artifact_data = utils.dedent(artifact_data)
        elif isinstance(artifact_data, dict):
            artifact_data['content'] = utils.dedent(artifact_data['content'])
        else:
            raise ValueError("The artifact data must be either a string or a dictionary.")
        
        # clean the artifact name of invalid characters
        invalid_chars: List[str] = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\t', '\r', ';']
        for char in invalid_chars:
            # check if the character is in the artifact name
            if char in artifact_name:
                # replace the character with an underscore
                artifact_name = artifact_name.replace(char, "-")
                logger.warning(f"Replaced invalid character {char} with hyphen in artifact name '{artifact_name}'.")
        
        artifact_file_path: str = self._compose_filepath(artifact_data, artifact_name, content_type, target_format, verbose)


        if target_format == "json":
            self._export_as_json(artifact_file_path, artifact_data, content_type, verbose)
        elif target_format == "txt" or target_format == "text" or target_format == "md" or target_format == "markdown":
            self._export_as_txt(artifact_file_path, artifact_data, content_type, verbose)
        elif target_format == "docx":
            self._export_as_docx(artifact_file_path, artifact_data, content_format, verbose)
        else:
            raise ValueError(f"Unsupported target format: {target_format}.")


    def _export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
        """
        Экспортирует указанные данные артефакта в текстовый файл.

        Args:
            artifact_file_path (str): Путь к файлу артефакта.
            artifact_data (Union[dict, str]): Данные артефакта.
            content_type (str): Тип контента.
            verbose (bool): Показывать ли отладочные сообщения.
        """

        try:
            with open(artifact_file_path, 'w', encoding="utf-8") as f:
                if isinstance(artifact_data, dict):
                    content: str = artifact_data['content']
                else:
                    content: str = artifact_data
            
                f.write(content)
        except Exception as ex:
            logger.error(f'Can\'t save to file {artifact_file_path}', ex, exc_info=True)
    
    def _export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
        """
        Экспортирует указанные данные артефакта в JSON-файл.
        Args:
            artifact_file_path (str): Путь к файлу артефакта.
            artifact_data (Union[dict, str]): Данные артефакта.
            content_type (str): Тип контента.
            verbose (bool): Показывать ли отладочные сообщения.
        """

        try:
            with open(artifact_file_path, 'w', encoding="utf-8") as f:
                if isinstance(artifact_data, dict):
                    json.dump(artifact_data, f, indent=4)                
                else:
                    raise ValueError("The artifact data must be a dictionary to export to JSON.")
        except Exception as ex:
            logger.error(f'Can\'t save to file {artifact_file_path}', ex, exc_info=True)
    
    def _export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False) -> None:
        """
        Экспортирует указанные данные артефакта в DOCX-файл.
        Args:
            artifact_file_path (str): Путь к файлу артефакта.
            artifact_data (Union[dict, str]): Данные артефакта.
            content_original_format (str): Оригинальный формат контента.
            verbose (bool): Показывать ли отладочные сообщения.
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
        #html_file_path = artifact_file_path.replace(".docx", ".html")
        #with open(html_file_path, 'w', encoding="utf-8") as f:
        #    f.write(html_content)

        # then, convert to DOCX
        try:
            pypandoc.convert_text(html_content, 'docx', format='html', outputfile=artifact_file_path)
        except Exception as ex:
            logger.error(f'Can\'t convert to docx file {artifact_file_path}', ex, exc_info=True)
    
    ###########################################################
    # IO
    ###########################################################
                  
    def _compose_filepath(self, artifact_data: Union[dict, str], artifact_name: str, content_type: str, target_format: str = None, verbose: bool = False) -> str:
        """
        Составляет путь к файлу для экспорта артефакта.
        Args:
            artifact_data (Union[dict, str]): Данные артефакта.
            artifact_name (str): Имя артефакта.
            content_type (str): Тип контента.
            target_format (str, optional): Формат для экспорта артефакта (e.g., json, txt, docx, etc).
            verbose (bool): Показывать ли отладочные сообщения.
        """        

        # Extension definition: 
        #
        # - If the content format is specified, we use it as the part of the extension.
        # - If artificat_data is a dict, we add .json to the extension. Note that if content format was specified, we'd get <content_format>.json.
        # - If artifact_data is a string and no content format is specified, we add .txt to the extension.
        extension: str = None
        if target_format is not None:
            extension = f"{target_format}"
        elif isinstance(artifact_data, str) and target_format is None:
            extension = "txt"
        
        # content type definition
        if content_type is None:
            subfolder: str = ""
        else:
            subfolder: str = content_type

        # save to the specified file name or path, considering the base output folder.
        artifact_file_path: str = os.path.join(self.base_output_folder, subfolder, f"{artifact_name}.{extension}")    

        # create intermediate directories if necessary
        os.makedirs(os.path.dirname(artifact_file_path), exist_ok=True)

        return artifact_file_path
        
            
class Normalizer:
    """
    Механизм для нормализации фрагментов текста, концепций и других текстовых элементов.
    """

    def __init__(self, elements: List[str], n: int, verbose: bool = False):
        """
        Инициализирует Normalizer.
        Args:
            elements (list): Элементы для нормализации.
            n (int): Количество нормализованных элементов для вывода.
            verbose (bool): Показывать ли отладочные сообщения.
        """
        # ensure elements are unique
        self.elements: List[str] = list(set(elements))
        
        self.n: int = n  
        self.verbose: bool = verbose 
        
        # a JSON-based structure, where each output element is a key to a list of input elements that were merged into it
        self.normalized_elements: Optional[Dict] = None
        # a dict that maps each input element to its normalized output. This will be used as cache later.
        self.normalizing_map: Dict = {}      

        rendering_configs: Dict = {"n": n,
                             "elements": self.elements}

        messages: List[Dict] = utils.compose_initial_LLM_messages_with_templates("normalizer.system.mustache", "normalizer.user.mustache", rendering_configs)
        try:
            next_message = openai_utils.client().send_message(messages, temperature=0.1)
        except Exception as ex:
            logger.error('Error while sending message to OpenAI client', ex, exc_info=True)
            return None
        
        debug_msg: str = f"Normalization result message: {next_message}"
        logger.debug(debug_msg)
        if self.verbose:
            print(debug_msg)

        result: Optional[Dict] = utils.extract_json(next_message["content"])
        logger.debug(result)
        if self.verbose:
            print(result)

        self.normalized_elements = result

    
    def normalize(self, element_or_elements: str | List[str]) -> Union[str, List[str]]:
        """
        Нормализует указанный элемент или элементы.

        Этот метод использует механизм кэширования для повышения производительности. Если элемент был нормализован ранее,
        его нормализованная форма сохраняется в кэше (self.normalizing_map). Когда один и тот же элемент необходимо
        нормализовать снова, метод сначала проверит кэш и использует сохраненную нормализованную форму, если она доступна,
        вместо повторной нормализации элемента.

        Порядок элементов на выходе будет таким же, как и на входе. Это обеспечивается путем обработки
        элементов в том порядке, в котором они появляются на входе, и добавления нормализованных элементов в выходной
        список в том же порядке.

        Args:
            element_or_elements (Union[str, List[str]]): Элемент или элементы для нормализации.

        Returns:
            str: Нормализованный элемент, если на входе была строка.
            list: Нормализованные элементы, если на входе был список, с сохранением порядка элементов на входе.
        
        Example:
            >>> normalizer = Normalizer(elements=['a', 'b'], n=2)
            >>> normalized = normalizer.normalize(element_or_elements='a')
            >>> print(normalized)
            ['a']
        """
        if isinstance(element_or_elements, str):
            denormalized_elements: List[str] = [element_or_elements]
        elif isinstance(element_or_elements, list):
            denormalized_elements: List[str] = element_or_elements
        else:
            raise ValueError("The element_or_elements must be either a string or a list.")
        
        normalized_elements: List[str] = []
        elements_to_normalize: List[str] = []
        for element in denormalized_elements:
            if element not in self.normalizing_map:
                elements_to_normalize.append(element)
        
        if elements_to_normalize:
            rendering_configs: Dict = {"categories": self.normalized_elements,
                                    "elements": elements_to_normalize}
            
            messages: List[Dict] = utils.compose_initial_LLM_messages_with_templates("normalizer.applier.system.mustache", "normalizer.applier.user.mustache", rendering_configs)
            try:
                next_message = openai_utils.client().send_message(messages, temperature=0.1)
            except Exception as ex:
                logger.error('Error while sending message to OpenAI client', ex, exc_info=True)
                return None
            
            debug_msg: str = f"Normalization result message: {next_message}"
            logger.debug(debug_msg)
            if self.verbose:
                print(debug_msg)
    
            normalized_elements_from_llm: List[str] = utils.extract_json(next_message["content"])
            assert isinstance(normalized_elements_from_llm, list), "The normalized element must be a list."
            assert len(normalized_elements_from_llm) == len(elements_to_normalize), "The number of normalized elements must be equal to the number of elements to normalize."
    
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