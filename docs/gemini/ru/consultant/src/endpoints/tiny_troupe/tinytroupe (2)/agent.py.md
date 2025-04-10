### **Анализ кода модуля `agent.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/agent.py

Модуль предоставляет основные классы и функции для агентов TinyTroupe. Агенты являются ключевой абстракцией, используемой в TinyTroupe, представляя собой смоделированных личностей или сущностей, которые могут взаимодействовать друг с другом и с окружающей средой, получая стимулы и производя действия. Агенты обладают когнитивными состояниями, которые обновляются по мере их взаимодействия с окружающей средой и другими агентами.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структурированность и модульность кода.
  - Использование аннотаций типов.
  - Применение `logger` для логирования.
  - Использование `textwrap` для форматирования текста.
- **Минусы**:
  - Местами отсутствует подробная документация и описание назначения переменных.
  - Некоторые docstring на английском языке.
  - Встречаются смешанные стили форматирования (где-то есть пробелы вокруг оператора `=`, где-то нет).

**Рекомендации по улучшению:**

1.  **Документация**:
    - Дополнить docstring для всех методов и классов, особенно для тех, где описание отсутствует или является недостаточным.
    - Перевести все docstring на русский язык, при этом сохранив формат UTF-8.
    - Добавить примеры использования для наиболее важных методов.

2.  **Комментарии**:
    - Добавить больше комментариев для пояснения сложных участков кода, особенно там, где выполняются важные логические операции или вычисления.
    - Убедиться, что все комментарии соответствуют назначению кода и не являются устаревшими.

3.  **Форматирование**:
    - Привести весь код к единому стилю форматирования, в частности, добавить пробелы вокруг оператора `=`, как указано в требованиях.

4.  **Использование `j_loads` или `j_loads_ns`**:
    - В данном коде не используются JSON или конфигурационные файлы напрямую, поэтому замена `open` и `json.load` на `j_loads` или `j_loads_ns` не требуется.

5.  **Обработка исключений**:
    - Убедиться, что все блоки `except` содержат логирование ошибок с использованием `logger.error`, передавая исключение как аргумент.

6.  **Аннотации типов**:
    - Проверить все переменные на наличие аннотаций типов, чтобы улучшить читаемость и предотвратить возможные ошибки.

7.  **Удалить неиспользуемые импорты**:
    - Удалить неиспользуемые импорты, такие как `csv`, `ast` и `logging`. Использовать `logger` из модуля `src.logger`.

**Оптимизированный код:**

```python
"""
Модуль для работы с агентами TinyTroupe
========================================

Модуль предоставляет основные классы и функции для агентов TinyTroupe.
Агенты - это ключевые абстракции, представляющие собой моделируемых личностей,
которые могут взаимодействовать друг с другом и с окружающей средой.
Они получают стимулы и производят действия, обладая когнитивными состояниями,
которые обновляются по мере взаимодействия.

Пример использования:
----------------------
>>> person = TinyPerson(name='Alice')
>>> person.define('age', 25)
>>> print(person.get('age'))
25
"""

import os
import json
import textwrap  # для выравнивания строк
import datetime  # для получения текущей даты и времени
import chevron  # для парсинга шаблонов Mustache
import copy
from typing import Any, TypeVar, Union, Optional, List
from pathlib import Path

from rich import print

from src.logger import logger  # Используем logger из src.logger
import tinytroupe.utils as utils
from tinytroupe.utils import post_init, JsonSerializableRegistry
from tinytroupe.control import transactional, current_simulation

# LLaMa-Index configs
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader


Self = TypeVar('Self', bound='TinyPerson')
AgentOrWorld = Union[Self, 'TinyWorld']

###########################################################################
# Default parameter values
###########################################################################
# Используем различные элементы конфигурации
config = utils.read_config_file()


default = {}
default['embedding_model'] = config['OpenAI'].get('EMBEDDING_MODEL', 'text-embedding-3-small')
default['max_content_display_length'] = config['OpenAI'].getint('MAX_CONTENT_DISPLAY_LENGTH', 1024)

## LLaMa-Index configs ########################################################
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
# from llama_index.readers.web import SimpleWebPageReader


# это будет кэшировано локально llama-index, в OS-зависимом месте

## Settings.embed_model = HuggingFaceEmbedding(
##    model_name="BAAI/bge-small-en-v1.5"
## )

llmaindex_openai_embed_model = OpenAIEmbedding(model=default['embedding_model'], embed_batch_size=10)
Settings.embed_model = llmaindex_openai_embed_model
###############################################################################


from tinytroupe import openai_utils
from tinytroupe.utils import name_or_empty, break_text_at_length, repeat_on_error


#######################################################################################################################
# TinyPerson itself
#######################################################################################################################
@post_init
class TinyPerson(JsonSerializableRegistry):
    """
    Симулируемый человек в вселенной TinyTroupe.
    """

    # Максимальное количество действий, которое агенту разрешено выполнить до завершения.
    # Это предотвращает бесконечные действия агента.
    MAX_ACTIONS_BEFORE_DONE: int = 15

    PP_TEXT_WIDTH: int = 100

    serializable_attributes: list = ['name', 'episodic_memory', 'semantic_memory', '_mental_faculties', '_configuration']

    # Словарь всех инстанцированных агентов.
    all_agents: dict = {}  # name -> agent

    # Стиль общения для всех агентов: "simplified" или "full".
    communication_style: str = 'simplified'

    # Отображать ли общение или нет. True для интерактивных приложений, когда мы хотим видеть симуляцию
    # выходы по мере их производства.
    communication_display: bool = True

    def __init__(
        self,
        name: str = None,
        episodic_memory=None,
        semantic_memory=None,
        mental_faculties: Optional[list] = None,
    ):
        """
        Создает TinyPerson.

        Args:
            name (str): Имя TinyPerson. Должно быть указано либо это, либо spec_path.
            episodic_memory (EpisodicMemory, optional): Используемая реализация памяти. По умолчанию EpisodicMemory().
            semantic_memory (SemanticMemory, optional): Используемая реализация памяти. По умолчанию SemanticMemory().
            mental_faculties (list, optional): Список ментальных способностей для добавления агенту. По умолчанию None.
        """

        # NOTE: значения по умолчанию будут заданы в методе _post_init, так как он используется
        #       как для прямой инициализации, так и через десериализацию.

        if episodic_memory is not None:
            self.episodic_memory = episodic_memory

        if semantic_memory is not None:
            self.semantic_memory = semantic_memory

        # Mental faculties
        if mental_faculties is not None:
            self._mental_faculties = mental_faculties

        assert name is not None, 'A TinyPerson must have a name.'
        self.name = name

        # @post_init ensures that _post_init is called after __init__

    def _post_init(self, **kwargs):
        """
        Этот метод будет запущен после __init__, так как класс имеет декоратор @post_init.
        Удобно разделять некоторые процессы инициализации, чтобы упростить десериализацию.
        """

        ############################################################
        # Default values
        ############################################################

        self.current_messages: list = []

        # текущая среда, в которой действует агент
        self.environment = None

        # Список действий, которые этот агент выполнил до сих пор, но которые еще не были
        # потреблены средой.
        self._actions_buffer: list = []

        # Список агентов, с которыми этот агент в настоящее время может взаимодействовать.
        # Это может меняться со временем, поскольку агенты перемещаются по миру.
        self._accessible_agents: list = []

        # буфер сообщений, которые были отображены до сих пор, используется для
        # сохранения этих сообщений в другую выходную форму позже (например, кэширование)
        self._displayed_communications_buffer: list = []

        if not hasattr(self, 'episodic_memory'):
            # Это значение по умолчанию НЕ ДОЛЖНО быть в сигнатуре метода, иначе оно будет использоваться совместно всеми экземплярами.
            self.episodic_memory = EpisodicMemory()

        if not hasattr(self, 'semantic_memory'):
            # Это значение по умолчанию НЕ ДОЛЖНО быть в сигнатуре метода, иначе оно будет использоваться совместно всеми экземплярами.
            self.semantic_memory = SemanticMemory()

        # _mental_faculties
        if not hasattr(self, '_mental_faculties'):
            # Это значение по умолчанию НЕ ДОЛЖНО быть в сигнатуре метода, иначе оно будет использоваться совместно всеми экземплярами.
            self._mental_faculties = []

        # create the configuration dictionary
        if not hasattr(self, '_configuration'):
            self._configuration = {
                'name': self.name,
                'age': None,
                'nationality': None,
                'country_of_residence': None,
                'occupation': None,
                'routines': [],
                'occupation_description': None,
                'personality_traits': [],
                'professional_interests': [],
                'personal_interests': [],
                'skills': [],
                'relationships': [],
                'current_datetime': None,
                'current_location': None,
                'current_context': [],
                'current_attention': None,
                'current_goals': [],
                'current_emotions': 'Currently you feel calm and friendly.',
                'currently_accessible_agents': [],  # [{"agent": agent_1, "relation": "My friend"}, {"agent": agent_2, "relation": "My colleague"}, ...]\
            }

        self._prompt_template_path: str = os.path.join(
            os.path.dirname(__file__), 'prompts/tinyperson.mustache'
        )
        self._init_system_message = None  # initialized later

        ############################################################
        # Special mechanisms used during deserialization
        ############################################################

        # rename agent to some specific name?
        if kwargs.get('new_agent_name') is not None:
            self._rename(kwargs.get('new_agent_name'))

        # If auto-rename, use the given name plus some new number ...
        if kwargs.get('auto_rename') is True:
            new_name = self.name  # start with the current name
            rename_succeeded = False
            while not rename_succeeded:
                try:
                    self._rename(new_name)
                    TinyPerson.add_agent(self)
                    rename_succeeded = True
                except ValueError:
                    new_id = utils.fresh_id()
                    new_name = f'{self.name}_{new_id}'

        # ... otherwise, just register the agent
        else:
            # register the agent in the global list of agents
            TinyPerson.add_agent(self)

        # start with a clean slate
        self.reset_prompt()

        # it could be the case that the agent is being created within a simulation scope, in which case
        # the simulation_id must be set accordingly
        if current_simulation() is not None:
            current_simulation().add_agent(self)
        else:
            self.simulation_id = None

    def _rename(self, new_name: str):
        self.name = new_name
        self._configuration['name'] = self.name

    def generate_agent_prompt(self) -> str:
        with open(self._prompt_template_path, 'r') as f:
            agent_prompt_template = f.read()

        # let's operate on top of a copy of the configuration, because we'll need to add more variables, etc.
        template_variables = self._configuration.copy()

        # Prepare additional action definitions and constraints
        actions_definitions_prompt = ''
        actions_constraints_prompt = ''
        for faculty in self._mental_faculties:
            actions_definitions_prompt += f'{faculty.actions_definitions_prompt()}\\n'
            actions_constraints_prompt += f'{faculty.actions_constraints_prompt()}\\n'

        # make the additional prompt pieces available to the template
        template_variables['actions_definitions_prompt'] = textwrap.indent(actions_definitions_prompt, '')
        template_variables['actions_constraints_prompt'] = textwrap.indent(actions_constraints_prompt, '')

        # RAI prompt components, if requested
        template_variables = utils.add_rai_template_variables_if_enabled(template_variables)

        return chevron.render(agent_prompt_template, template_variables)

    def reset_prompt(self):
        # render the template with the current configuration
        self._init_system_message = self.generate_agent_prompt()

        # TODO actually, figure out another way to update agent state without "changing history"

        # reset system message
        self.current_messages = [
            {'role': 'system', 'content': self._init_system_message}
        ]

        # sets up the actual interaction messages to use for prompting
        self.current_messages += self.episodic_memory.retrieve_recent()

    def get(self, key: str) -> Any:
        """
        Возвращает значение ключа из конфигурации TinyPerson.
        """
        return self._configuration.get(key, None)

    @transactional
    def define(self, key: str, value: Any, group: str = None):
        """
        Определяет значение в конфигурации TinyPerson.
        Если group is None, значение добавляется на верхний уровень конфигурации.
        В противном случае значение добавляется в указанную группу.
        """

        # dedent value if it is a string
        if isinstance(value, str):
            value = textwrap.dedent(value)

        if group is None:
            # logger.debug(f"[{self.name}] Defining {key}={value} in the person.")
            self._configuration[key] = value
        else:
            if key is not None:
                # logger.debug(f"[{self.name}] Adding definition to {group} += [ {key}={value} ] in the person.")
                self._configuration[group].append({key: value})
            else:
                # logger.debug(f"[{self.name}] Adding definition to {group} += [ {value} ] in the person.")
                self._configuration[group].append(value)

        # must reset prompt after adding to configuration
        self.reset_prompt()

    def define_several(self, group: str, records: list):
        """
        Определяет несколько значений в конфигурации TinyPerson, все принадлежащие одной группе.
        """
        for record in records:
            self.define(key=None, value=record, group=group)

    @transactional
    def define_relationships(self, relationships: Union[list, dict], replace: bool = True):
        """
        Определяет или обновляет отношения TinyPerson.

        Args:
            relationships (list or dict): Отношения для добавления или замены. Либо список словарей, сопоставляющих имена агентов с описаниями отношений,
              либо один словарь, сопоставляющий одно имя агента с его описанием отношений.
            replace (bool, optional): Заменять ли текущие отношения или просто добавлять к ним. По умолчанию True.
        """

        if (replace == True) and (isinstance(relationships, list)):
            self._configuration['relationships'] = relationships

        elif replace == False:
            current_relationships = self._configuration['relationships']
            if isinstance(relationships, list):
                for r in relationships:
                    current_relationships.append(r)

            elif isinstance(relationships, dict) and len(relationships) == 2:  # {"Name": ..., "Description": ...}
                current_relationships.append(relationships)

            else:
                raise Exception('Only one key-value pair is allowed in the relationships dict.')

        else:
            raise Exception('Invalid arguments for define_relationships.')

    @transactional
    def clear_relationships(self):
        """
        Очищает отношения TinyPerson.
        """
        self._configuration['relationships'] = []

        return self

    @transactional
    def related_to(self, other_agent, description, symmetric_description=None):
        """
        Определяет отношения между этим агентом и другим агентом.

        Args:
            other_agent (TinyPerson): Другой агент.
            description (str): Описание отношений.
            symmetric (bool): Являются ли отношения симметричными или нет. То есть,
              если отношения определены для обоих агентов.

        Returns:
            TinyPerson: Сам агент, чтобы облегчить связывание.
        """
        self.define_relationships([{'Name': other_agent.name, 'Description': description}], replace=False)
        if symmetric_description is not None:
            other_agent.define_relationships([{'Name': self.name, 'Description': symmetric_description}], replace=False)

        return self

    def add_mental_faculties(self, mental_faculties: list):
        """
        Добавляет список ментальных способностей агенту.
        """
        for faculty in mental_faculties:
            self.add_mental_faculty(faculty)

        return self

    def add_mental_faculty(self, faculty):
        """
        Добавляет ментальную способность агенту.
        """
        # check if the faculty is already there or not
        if faculty not in self._mental_faculties:
            self._mental_faculties.append(faculty)
        else:
            raise Exception(f'The mental faculty {faculty} is already present in the agent.')

        return self

    @transactional
    def act(
        self,
        until_done: bool = True,
        n: Optional[int] = None,
        return_actions: bool = False,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Действует в среде и обновляет свое внутреннее когнитивное состояние.
        Либо действует до тех пор, пока агент не будет завершен и не потребуются дополнительные стимулы, либо действует фиксированное количество раз,
        но не оба варианта.

        Args:
            until_done (bool): Следует ли продолжать действовать, пока агент не будет завершен и не потребуются дополнительные стимулы.
            n (int): Количество действий для выполнения. По умолчанию None.
            return_actions (bool): Следует ли возвращать действия или нет. По умолчанию False.
        """

        # either act until done or act a fixed number of times, but not both
        assert not (until_done and n is not None)
        if n is not None:
            assert n < TinyPerson.MAX_ACTIONS_BEFORE_DONE

        contents = []

        # Aux function to perform exactly one action.
        # Occasionally, the model will return JSON missing important keys, so we just ask it to try again
        @repeat_on_error(retries=5, exceptions=[KeyError])
        def aux_act_once():
            # A quick thought before the action. This seems to help with better model responses, perhaps because
            # it interleaves user with assistant messages.
            self.think('I will now act a bit, and then issue DONE.')

            role, content = self._produce_message()

            self.episodic_memory.store({'role': role, 'content': content, 'simulation_timestamp': self.iso_datetime()})

            cognitive_state = content['cognitive_state']

            action = content['action']

            self._actions_buffer.append(action)
            self._update_cognitive_state(
                goals=cognitive_state['goals'], attention=cognitive_state['attention'], emotions=cognitive_state['emotions']
            )

            contents.append(content)
            if TinyPerson.communication_display:
                self._display_communication(
                    role=role, content=content, kind='action', simplified=True, max_content_length=max_content_length
                )

            #
            # Some actions induce an immediate stimulus or other side-effects. We need to process them here, by means of the mental faculties.
            #
            for faculty in self._mental_faculties:
                faculty.process_action(self, action)

        #
        # How to proceed with a sequence of actions.
        #

        ##### Option 1: run N actions ######
        if n is not None:
            for i in range(n):
                aux_act_once()

        ##### Option 2: run until DONE ######
        elif until_done:
            while (len(contents) == 0) or (not contents[-1]['action']['type'] == 'DONE'):
                # check if the agent is acting without ever stopping
                if len(contents) > TinyPerson.MAX_ACTIONS_BEFORE_DONE:
                    logger.warning(
                        f'[{self.name}] Agent {self.name} is acting without ever stopping. This may be a bug. Let\'s stop it here anyway.'
                    )
                    break
                if len(contents) > 4:  # just some minimum number of actions to check for repetition, could be anything >= 3
                    # if the last three actions were the same, then we are probably in a loop
                    if contents[-1]['action'] == contents[-2]['action'] == contents[-3]['action']:
                        logger.warning(
                            f'[{self.name}] Agent {self.name} is acting in a loop. This may be a bug. Let\'s stop it here anyway.'
                        )
                        break

                aux_act_once()

        if return_actions:
            return contents

    @transactional
    def listen(
        self,
        speech: str,
        source: AgentOrWorld = None,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Слушает другого агента (искусственного или человеческого) и обновляет свое внутреннее когнитивное состояние.

        Args:
            speech (str): Речь для прослушивания.
            source (AgentOrWorld, optional): Источник речи. По умолчанию None.
        """

        return self._observe(
            stimulus={'type': 'CONVERSATION', 'content': speech, 'source': name_or_empty(source)},
            max_content_length=max_content_length,
        )

    def socialize(
        self,
        social_description: str,
        source: AgentOrWorld = None,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Воспринимает социальный стимул через описание и обновляет свое внутреннее когнитивное состояние.

        Args:
            social_description (str): Описание социального стимула.
            source (AgentOrWorld, optional): Источник социального стимула. По умолчанию None.
        """
        return self._observe(
            stimulus={'type': 'SOCIAL', 'content': social_description, 'source': name_or_empty(source)},
            max_content_length=max_content_length,
        )

    def see(
        self,
        visual_description: str,
        source: AgentOrWorld = None,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Воспринимает визуальный стимул через описание и обновляет свое внутреннее когнитивное состояние.

        Args:
            visual_description (str): Описание визуального стимула.
            source (AgentOrWorld, optional): Источник визуального стимула. По умолчанию None.
        """
        return self._observe(
            stimulus={'type': 'VISUAL', 'content': visual_description, 'source': name_or_empty(source)},
            max_content_length=max_content_length,
        )

    def think(self, thought: str, max_content_length: int = default['max_content_display_length']):
        """
        Заставляет агента думать о чем-то и обновляет свое внутреннее когнитивное состояние.
        """
        return self._observe(
            stimulus={'type': 'THOUGHT', 'content': thought, 'source': name_or_empty(self)},
            max_content_length=max_content_length,
        )

    def internalize_goal(
        self, goal: str, max_content_length: int = default['max_content_display_length']
    ):
        """
        Интернализует цель и обновляет свое внутреннее когнитивное состояние.
        """
        return self._observe(
            stimulus={'type': 'INTERNAL_GOAL_FORMULATION', 'content': goal, 'source': name_or_empty(self)},
            max_content_length=max_content_length,
        )

    @transactional
    def _observe(self, stimulus: dict, max_content_length: int = default['max_content_display_length']):
        stimuli = [stimulus]

        content = {'stimuli': stimuli}

        logger.debug(f'[{self.name}] Observing stimuli: {content}')

        # whatever comes from the outside will be interpreted as coming from 'user', simply because
        # this is the counterpart of 'assistant'

        self.episodic_memory.store({'role': 'user', 'content': content, 'simulation_timestamp': self.iso_datetime()})

        if TinyPerson.communication_display:
            self._display_communication(
                role='user',
                content=content,
                kind='stimuli',
                simplified=True,
                max_content_length=max_content_length,
            )

        return self  # allows easier chaining of methods

    @transactional
    def listen_and_act(
        self,
        speech: str,
        return_actions: bool = False,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Удобный метод, который объединяет методы `listen` и `act`.
        """

        self.listen(speech, max_content_length=max_content_length)
        return self.act(return_actions=return_actions, max_content_length=max_content_length)

    @transactional
    def see_and_act(
        self,
        visual_description: str,
        return_actions: bool = False,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Удобный метод, который объединяет методы `see` и `act`.
        """

        self.see(visual_description, max_content_length=max_content_length)
        return self.act(return_actions=return_actions, max_content_length=max_content_length)

    @transactional
    def think_and_act(
        self,
        thought: str,
        return_actions: bool = False,
        max_content_length: int = default['max_content_display_length'],
    ):
        """
        Удобный метод, который объединяет методы `think` и `act`.
        """

        self.think(thought, max_content_length=max_content_length)
        return self.act(return_actions=return_actions, max_content_length=max_content_length)

    def read_documents_from_folder(self, documents_path: str):
        """
        Читает документы из каталога и загружает их в семантическую память.
        """
        logger.info(f'Setting documents path to {documents_path} and loading documents.')

        self.semantic_memory.add_documents_path(documents_path)

    def read_documents_from_web(self, web_urls: list):
        """
        Читает документы из веб-адресов и загружает их в семантическую память.
        """
        logger.info(f'Reading documents from the following web URLs: {web_urls}')

        self.semantic_memory.add_web_urls(web_urls)

    @transactional
    def move_to(self, location, context=[]):
        """
        Перемещается в новое местоположение и обновляет свое внутреннее когнитивное состояние.
        """
        self._configuration['current_location'] = location

        # context must also be updated when moved, since we assume that context is dictated partly by location.
        self.change_context(context)

    @transactional
    def change_context(self, context: list):
        """
        Изменяет контекст и обновляет свое внутреннее когнитивное состояние.
        """
        self._configuration['current_context'] = {'description': item for item in context}

        self._update_cognitive_state(context=context)

    @transactional
    def make_agent_accessible(
        self,
        agent: Self,
        relation_description: str = 'An agent I can currently interact with.',
    ):
        """
        Делает агента доступным для этого агента.
        """
        if agent not in self._accessible_agents:
            self._accessible_agents.append(agent)
            self._configuration['currently_accessible_agents'].append(
                {'name': agent.name, 'relation_description': relation_description}
            )
        else:
            logger.warning(
                f'[{self.name}] Agent {agent.name} is already accessible to {self.name}.'
            )

    @transactional
    def make_agent_inaccessible(self, agent: Self):
        """
        Делает агента недоступным для этого агента.
        """
        if agent in self._accessible_agents:
            self._accessible_agents.remove(agent)
        else:
            logger.warning(
                f'[{self.name}] Agent {agent.name} is already inaccessible to {self.name}.'
            )

    @transactional
    def make_all_agents_inaccessible(self):
        """
        Делает всех агентов недоступными для этого агента.
        """
        self._accessible_agents = []
        self._configuration['currently_accessible_agents'] = []

    @transactional
    def _produce_message(self):
        # logger.debug(f"Current messages: {self.current_messages}")

        # ensure we have the latest prompt (initial system message + selected messages from memory)
        self.reset_prompt()

        messages = [
            {'role': msg['role'], 'content': json.dumps(msg['content'])} for msg in self.current_messages
        ]

        logger.debug(f'[{self.name}] Sending messages to OpenAI API')
        logger.debug(f'[{self.name}] Last interaction: {messages[-1]}')

        next_message = openai_utils.client().send_message(messages)

        logger.debug(f'[{self.name}] Received message: {next_message}')

        return next_message['role'], utils.extract_json(next_message['content'])

    ###########################################################
    # Internal cognitive state changes
    ###########################################################
    @transactional
    def _update_cognitive_state(
        self, goals=None, context=None, attention=None, emotions=None
    ):
        """
        Обновляет когнитивное состояние TinyPerson.
        """

        # Update current datetime. The passage of time is controlled by the environment, if any.
        if self.environment is not None and self.environment.current_datetime is not None:
            self._configuration['current_datetime'] = utils.pretty_datetime(self.environment.current_datetime)

        # update current goals
        if goals is not None:
            self._configuration['current_goals'] = goals

        # update current context
        if context is not None:
            self._configuration['current_context'] = context

        # update current attention
        if attention is not None:
            self._configuration['current_attention'] = attention

        # update current emotions
        if emotions is not None:
            self._configuration['current_emotions'] = emotions

        self.reset_prompt()

    ###########################################################
    # Inspection conveniences
    ###########################################################
    def _display_communication(
        self,
        role,
        content,
        kind,
        simplified=True,
        max_content_length=default['max_content_display_length'],
    ):
        """
        Отображает текущее общение и сохраняет его в буфере для последующего использования.
        """
        if kind == 'stimuli':
            rendering = self._pretty_stimuli(
                role=role,
                content=content,
                simplified=simplified,
                max_content_length=max_content_length,
            )
        elif kind == 'action':
            rendering = self._pretty_action(
                role=role,
                content=content,
                simplified=simplified,
                max_content_length=max_content_length,
            )
        else:
            raise ValueError(f'Unknown communication kind: {kind}')

        # if the agent has no parent environment, then it is a free agent and we can display the communication.
        # otherwise, the environment will display the communication instead. This is important to make sure that
        # the communication is displayed in the correct order, since environments control the flow of their underlying
        # agents.
        if self.environment is None:
            self._push_and_display_latest_communication(rendering)
        else:
            self.environment._push_and_display_latest_communication(rendering)

    def _push_and_display_latest_communication(self, rendering):
        """