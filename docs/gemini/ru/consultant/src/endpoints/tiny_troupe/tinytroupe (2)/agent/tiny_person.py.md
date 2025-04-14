### Анализ кода модуля `tiny_person`

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Код хорошо структурирован и содержит множество полезных функций для управления агентами.
     - Использование `logger` для отладки и логирования.
     - Применение декораторов `@transactional` и `@utils.post_init`.
     - Наличие подробных docstring для большинства методов и функций.
   - **Минусы**:
     - Не везде используются аннотации типов.
     - В некоторых местах используется `Union`, следует заменить на `|`.
     - Есть участки кода, требующие более подробных комментариев на русском языке.

3. **Рекомендации по улучшению**:
   - Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
   - Заменить `Union` на `|` для обозначения объединения типов.
   - Перевести все docstring на русский язык и убедиться, что они соответствуют указанному формату.
   - Добавить больше комментариев для пояснения сложных участков кода.

4. **Оптимизированный код**:

```python
from tinytroupe.agent import logger, default, Self, AgentOrWorld, CognitiveActionModel
from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
import tinytroupe.openai_utils as openai_utils
from tinytroupe.utils import JsonSerializableRegistry, repeat_on_error, name_or_empty
import tinytroupe.utils as utils
from tinytroupe.control import transactional, current_simulation

import os
import json
import copy
import textwrap  # to dedent strings
import chevron  # to parse Mustache templates
from typing import Any, Optional, List
from rich import print
from pathlib import Path

#######################################################################################################################
# TinyPerson itself
#######################################################################################################################
@utils.post_init
class TinyPerson(JsonSerializableRegistry):
    """A simulated person in the TinyTroupe universe."""

    # The maximum number of actions that an agent is allowed to perform before DONE.
    # This prevents the agent from acting without ever stopping.
    MAX_ACTIONS_BEFORE_DONE: int = 15

    PP_TEXT_WIDTH: int = 100

    serializable_attributes: List[str] = ["_persona", "_mental_state", "_mental_faculties", "episodic_memory", "semantic_memory"]
    serializable_attributes_renaming: dict = {"_mental_faculties": "mental_faculties", "_persona": "persona", "_mental_state": "mental_state"}

    # A dict of all agents instantiated so far.
    all_agents: dict = {}  # name -> agent

    # The communication style for all agents: "simplified" or "full".
    communication_style: str = "simplified"

    # Whether to display the communication or not. True is for interactive applications, when we want to see simulation
    # outputs as they are produced.
    communication_display: bool = True

    def __init__(self, name: str = None,
                 episodic_memory: Optional[EpisodicMemory] = None,
                 semantic_memory: Optional[SemanticMemory] = None,
                 mental_faculties: Optional[List] = None) -> None:
        """
        Создает TinyPerson.

        Args:
            name (str): Имя TinyPerson. Должно быть указано либо это, либо spec_path.
            episodic_memory (Optional[EpisodicMemory], optional): Используемая реализация памяти. По умолчанию EpisodicMemory().
            semantic_memory (Optional[SemanticMemory], optional): Используемая реализация семантической памяти. По умолчанию SemanticMemory().
            mental_faculties (Optional[List], optional): Список ментальных способностей для добавления агенту. По умолчанию None.
        """

        # NOTE: default values will be given in the _post_init method, as that's shared by
        #       direct initialization as well as via deserialization.

        if episodic_memory is not None:
            self.episodic_memory: EpisodicMemory = episodic_memory

        if semantic_memory is not None:
            self.semantic_memory: SemanticMemory = semantic_memory

        # Mental faculties
        if mental_faculties is not None:
            self._mental_faculties: list = mental_faculties

        assert name is not None, "A TinyPerson must have a name."
        self.name: str = name

        # @post_init makes sure that _post_init is called after __init__

    def _post_init(self, **kwargs) -> None:
        """
        Этот метод будет запущен после __init__, так как у класса есть декоратор @post_init.
        Удобно разделять некоторые процессы инициализации, чтобы упростить десериализацию.
        """

        ############################################################
        # Default values
        ############################################################

        self.current_messages: list = []

        # the current environment in which the agent is acting
        self.environment: Any = None

        # The list of actions that this agent has performed so far, but which have not been
        # consumed by the environment yet.
        self._actions_buffer: list = []

        # The list of agents that this agent can currently interact with.
        # This can change over time, as agents move around the world.
        self._accessible_agents: list = []

        # the buffer of communications that have been displayed so far, used for
        # saving these communications to another output form later (e.g., caching)
        self._displayed_communications_buffer: list = []

        if not hasattr(self, 'episodic_memory'):
            # This default value MUST NOT be in the method signature, otherwise it will be shared across all instances.
            self.episodic_memory: EpisodicMemory = EpisodicMemory()

        if not hasattr(self, 'semantic_memory'):
            # This default value MUST NOT be in the method signature, otherwise it will be shared across all instances.
            self.semantic_memory: SemanticMemory = SemanticMemory()

        # _mental_faculties
        if not hasattr(self, '_mental_faculties'):
            # This default value MUST NOT be in the method signature, otherwise it will be shared across all instances.
            self._mental_faculties: list = []

        # create the persona configuration dictionary
        if not hasattr(self, '_persona'):
            self._persona: dict = {
                "name": self.name,
                "age": None,
                "nationality": None,
                "country_of_residence": None,
                "occupation": None,
                "routines": [],
                "occupation_description": None,
                "personality_traits": [],
                "professional_interests": [],
                "personal_interests": [],
                "skills": [],
                "relationships": []
            }

        if not hasattr(self, 'name'):
            self.name: str = self._persona["name"]

        # create the mental state dictionary
        if not hasattr(self, '_mental_state'):
            self._mental_state: dict = {
                "datetime": None,
                "location": None,
                "context": [],
                "goals": [],
                "attention": None,
                "emotions": "Feeling nothing in particular, just calm.",
                "memory_context": None,
                "accessible_agents": []  # [{"agent": agent_1, "relation": "My friend"}, {"agent": agent_2, "relation": "My colleague"}, ...]
            }

        if not hasattr(self, '_extended_agent_summary'):
            self._extended_agent_summary: Any = None

        self._prompt_template_path: str = os.path.join(
            os.path.dirname(__file__), "prompts/tiny_person.mustache"
        )
        self._init_system_message: Any = None  # initialized later

        ############################################################
        # Special mechanisms used during deserialization
        ############################################################

        # rename agent to some specific name?
        if kwargs.get("new_agent_name") is not None:
            self._rename(kwargs.get("new_agent_name"))

        # If auto-rename, use the given name plus some new number ...
        if kwargs.get("auto_rename") is True:
            new_name: str = self.name  # start with the current name
            rename_succeeded: bool = False
            while not rename_succeeded:
                try:
                    self._rename(new_name)
                    TinyPerson.add_agent(self)
                    rename_succeeded: bool = True
                except ValueError:
                    new_id: str = utils.fresh_id()
                    new_name: str = f"{self.name}_{new_id}"

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
            self.simulation_id: Any = None

    def _rename(self, new_name: str) -> None:
        """
        Переименовывает агента.

        Args:
            new_name (str): Новое имя агента.
        """
        self.name: str = new_name
        self._persona["name"]: str = self.name

    def generate_agent_system_prompt(self) -> str:
        """
        Генерирует системный промпт для агента.

        Returns:
            str: Сгенерированный системный промпт.
        """
        with open(self._prompt_template_path, "r") as f:
            agent_prompt_template: str = f.read()

        # let's operate on top of a copy of the configuration, because we'll need to add more variables, etc.
        template_variables: dict = self._persona.copy()
        template_variables["persona"]: str = json.dumps(self._persona.copy(), indent=4)

        # Prepare additional action definitions and constraints
        actions_definitions_prompt: str = ""
        actions_constraints_prompt: str = ""
        for faculty in self._mental_faculties:
            actions_definitions_prompt += f"{faculty.actions_definitions_prompt()}\\n"
            actions_constraints_prompt += f"{faculty.actions_constraints_prompt()}\\n"

        # Make the additional prompt pieces available to the template.
        # Identation here is to align with the text structure in the template.
        template_variables['actions_definitions_prompt']: str = textwrap.indent(actions_definitions_prompt.strip(), "  ")
        template_variables['actions_constraints_prompt']: str = textwrap.indent(actions_constraints_prompt.strip(), "  ")

        # RAI prompt components, if requested
        template_variables: dict = utils.add_rai_template_variables_if_enabled(template_variables)

        return chevron.render(agent_prompt_template, template_variables)

    def reset_prompt(self) -> None:
        """
        Сбрасывает промпт агента.
        """

        # render the template with the current configuration
        self._init_system_message: str = self.generate_agent_system_prompt()

        # TODO actually, figure out another way to update agent state without "changing history"

        # reset system message
        self.current_messages: list = [
            {"role": "system", "content": self._init_system_message}
        ]

        # sets up the actual interaction messages to use for prompting
        self.current_messages += self.retrieve_recent_memories()

        # add a final user message, which is neither stimuli or action, to instigate the agent to act properly
        self.current_messages.append({"role": "user",
                                      "content": "Now you **must** generate a sequence of actions following your interaction directives, " +
                                                 "and complying with **all** instructions and contraints related to the action you use." +
                                                 "DO NOT repeat the exact same action more than once in a row!" +
                                                 "DO NOT keep saying or doing very similar things, but instead try to adapt and make the interactions look natural." +
                                                 "These actions **MUST** be rendered following the JSON specification perfectly, including all required keys (even if their value is empty), **ALWAYS**."
                                     })

    def get(self, key: str) -> Any:
        """
        Возвращает определение ключа в конфигурации TinyPerson.

        Args:
            key (str): Ключ для получения значения.

        Returns:
            Any: Значение ключа или None, если ключ не найден.
        """
        return self._persona.get(key, None)

    @transactional
    def import_fragment(self, path: str) -> None:
        """
        Импортирует фрагмент конфигурации персонажа из JSON файла.

        Args:
            path (str): Путь к JSON файлу.
        """
        with open(path, "r") as f:
            fragment: dict = json.load(f)

        # check the type is "Fragment" and that there's also a "persona" key
        if fragment.get("type", None) == "Fragment" and fragment.get("persona", None) is not None:
            self.include_persona_definitions(fragment["persona"])
        else:
            raise ValueError("The imported JSON file must be a valid fragment of a persona configuration.")

        # must reset prompt after adding to configuration
        self.reset_prompt()

    @transactional
    def include_persona_definitions(self, additional_definitions: dict) -> None:
        """
        Импортирует набор определений в TinyPerson. Они будут объединены с текущей конфигурацией.
        Это также удобный способ включить несколько связанных определений в агента.

        Args:
            additional_definitions (dict): Дополнительные определения для импорта.
        """

        self._persona: dict = utils.merge_dicts(self._persona, additional_definitions)

        # must reset prompt after adding to configuration
        self.reset_prompt()

    @transactional
    def define(self, key: str, value: Any, merge: bool = True, overwrite_scalars: bool = True) -> None:
        """
        Определяет значение в конфигурации персонажа TinyPerson. Значение может быть скалярным или словарём.
        Если значение является словарём или списком, можно выбрать, следует ли объединять его с существующим значением или заменить его.
        Если значение является скалярным, можно выбрать, следует ли перезаписывать существующее значение или нет.

        Args:
            key (str): Ключ для определения.
            value (Any): Значение для определения.
            merge (bool, optional): Следует ли объединять значения dict/list с существующими значениями или заменить их. По умолчанию True.
            overwrite_scalars (bool, optional): Следует ли перезаписывать скалярные значения или нет. По умолчанию True.
        """

        # dedent value if it is a string
        if isinstance(value, str):
            value: str = textwrap.dedent(value)

        # if the value is a dictionary, we can choose to merge it with the existing value or replace it
        if isinstance(value, dict) or isinstance(value, list):
            if merge:
                self._persona: dict = utils.merge_dicts(self._persona, {key: value})
            else:
                self._persona[key]: Any = value

        # if the value is a scalar, we can choose to overwrite it or not
        elif overwrite_scalars or (key not in self._persona):
            self._persona[key]: Any = value

        else:
            raise ValueError(f"The key '{key}' already exists in the persona configuration and overwrite_scalars is set to False.")

        # must reset prompt after adding to configuration
        self.reset_prompt()

    @transactional
    def define_relationships(self, relationships: list | dict, replace: bool = True) -> None:
        """
        Определяет или обновляет отношения TinyPerson.

        Args:
            relationships (list or dict): Отношения для добавления или замены. Либо список словарей, сопоставляющих имена агентов с описаниями отношений,
              либо один словарь, сопоставляющий одно имя агента с его описанием отношений.
            replace (bool, optional): Следует ли заменять текущие отношения или просто добавлять к ним. По умолчанию True.
        """

        if (replace == True) and (isinstance(relationships, list)):
            self._persona['relationships']: list = relationships

        elif replace == False:
            current_relationships: list = self._persona['relationships']
            if isinstance(relationships, list):
                for r in relationships:
                    current_relationships.append(r)

            elif isinstance(relationships, dict) and len(relationships) == 2:  # {"Name": ..., "Description": ...}
                current_relationships.append(relationships)

            else:
                raise Exception("Only one key-value pair is allowed in the relationships dict.")

        else:
            raise Exception("Invalid arguments for define_relationships.")

    @transactional
    def clear_relationships(self) -> Self:
        """
        Очищает отношения TinyPerson.
        """
        self._persona['relationships']: list = []

        return self

    @transactional
    def related_to(self, other_agent: "TinyPerson", description: str, symmetric_description: Optional[str] = None) -> Self:
        """
        Определяет отношения между этим агентом и другим агентом.

        Args:
            other_agent (TinyPerson): Другой агент.
            description (str): Описание отношения.
            symmetric (bool): Является ли отношение симметричным или нет. То есть,
              если отношение определено для обоих агентов.

        Returns:
            TinyPerson: Сам агент, для облегчения цепочки вызовов.
        """
        self.define_relationships([{"Name": other_agent.name, "Description": description}], replace=False)
        if symmetric_description is not None:
            other_agent.define_relationships([{"Name": self.name, "Description": symmetric_description}], replace=False)

        return self

    def add_mental_faculties(self, mental_faculties: list) -> Self:
        """
        Добавляет список ментальных способностей агенту.
        """
        for faculty in mental_faculties:
            self.add_mental_faculty(faculty)

        return self

    def add_mental_faculty(self, faculty: Any) -> Self:
        """
        Добавляет ментальную способность агенту.
        """
        # check if the faculty is already there or not
        if faculty not in self._mental_faculties:
            self._mental_faculties.append(faculty)
        else:
            raise Exception(f"The mental faculty {faculty} is already present in the agent.")

        return self

    @transactional
    def act(
        self,
        until_done: bool = True,
        n: Optional[int] = None,
        return_actions: bool = False,
        max_content_length: int = default["max_content_display_length"],
    ) -> Optional[list]:
        """
        Действует в среде и обновляет свое внутреннее когнитивное состояние.
        Либо действует до тех пор, пока агент не будет готов и не потребуются дополнительные стимулы, либо действует фиксированное количество раз,
        но не оба варианта.

        Args:
            until_done (bool): Следует ли продолжать действовать до тех пор, пока агент не будет готов и не потребуются дополнительные стимулы.
            n (int): Количество действий для выполнения. По умолчанию None.
            return_actions (bool): Следует ли возвращать действия или нет. По умолчанию False.
        """

        # either act until done or act a fixed number of times, but not both
        assert not (until_done and n is not None)
        if n is not None:
            assert n < TinyPerson.MAX_ACTIONS_BEFORE_DONE

        contents: list = []

        # A separate function to run before each action, which is not meant to be repeated in case of errors.
        def aux_pre_act():
            # TODO maybe we don't need this at all anymore?
            #
            # A quick thought before the action. This seems to help with better model responses, perhaps because
            # it interleaves user with assistant messages.
            pass  # self.think("I will now think, reflect and act a bit, and then issue DONE.")

        # Aux function to perform exactly one action.
        # Occasionally, the model will return JSON missing important keys, so we just ask it to try again
        # Sometimes `content` contains EpisodicMemory's MEMORY_BLOCK_OMISSION_INFO message, which raises a TypeError on line 443
        @repeat_on_error(retries=5, exceptions=[KeyError, TypeError])
        def aux_act_once() -> None:
            """
            Вспомогательная функция для выполнения одного действия.
            """
            role: str, content: dict = self._produce_message()

            cognitive_state: dict = content["cognitive_state"]

            action: dict = content['action']
            logger.debug(f"{self.name}'s action: {action}")

            goals: list = cognitive_state['goals']
            attention: Any = cognitive_state['attention']
            emotions: str = cognitive_state['emotions']

            self.store_in_memory({'role': role, 'content': content,
                                  'type': 'action',
                                  'simulation_timestamp': self.iso_datetime()})

            self._actions_buffer.append(action)
            self._update_cognitive_state(goals=cognitive_state['goals'],
                                        attention=cognitive_state['attention'],
                                        emotions=cognitive_state['emotions'])

            contents.append(content)
            if TinyPerson.communication_display:
                self._display_communication(role=role, content=content, kind='action', simplified=True, max_content_length=max_content_length)

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
                aux_pre_act()
                aux_act_once()

        ##### Option 2: run until DONE ######
        elif until_done:
            while (len(contents) == 0) or (
                not contents[-1]["action"]["type"] == "DONE"
            ):

                # check if the agent is acting without ever stopping
                if len(contents) > TinyPerson.MAX_ACTIONS_BEFORE_DONE:
                    logger.warning(f"[{self.name}] Agent {self.name} is acting without ever stopping. This may be a bug. Let's stop it here anyway.")
                    break
                if len(contents) > 4:  # just some minimum number of actions to check for repetition, could be anything >= 3
                    # if the last three actions were the same, then we are probably in a loop
                    if contents[-1]['action'] == contents[-2]['action'] == contents[-3]['action']:
                        logger.warning(f"[{self.name}] Agent {self.name} is acting in a loop. This may be a bug. Let's stop it here anyway.")
                        break

                aux_pre_act()
                aux_act_once()

        if return_actions:
            return contents

    @transactional
    def listen(
        self,
        speech: str,
        source: AgentOrWorld = None,
        max_content_length: int = default["max_content_display_length"],
    ) -> Self:
        """
        Слушает другого агента (искусственного или человека) и обновляет свое внутреннее когнитивное состояние.

        Args:
            speech (str): Речь для прослушивания.
            source (AgentOrWorld, optional): Источник речи. По умолчанию None.
        """

        return self._observe(
            stimulus={
                "type": "CONVERSATION",
                "content": speech,
                "source": name_or_empty(source),
            },
            max_content_length=max_content_length,
        )

    def socialize(
        self,
        social_description: str,
        source: AgentOrWorld = None,
        max_content_length: int = default["max_content_display_length"],
    ) -> Self:
        """
        Воспринимает социальный стимул через описание и обновляет свое внутреннее когнитивное состояние.

        Args:
            social_description (str): Описание социального стимула.
            source (AgentOrWorld, optional): Источник социального стимула. По умолчанию None.
        """
        return self._observe(
            stimulus={
                "type": "SOCIAL",
                "content": social_description,
                "source": name_or_empty(source),
            },
            max_content_length=max_content_length,
        )

    def see(
        self,
        visual_description: str,
        source: AgentOrWorld = None,
        max_content_length: int = default["max_content_display_length"],
    ) -> Self:
        """
        Воспринимает визуальный стимул через описание и обновляет свое внутреннее когнитивное состояние.

        Args:
            visual_description (str): Описание визуального стимула.
            source (AgentOrWorld, optional): Источник визуального стимула. По умолчанию None.
        """
        return self._observe(
            stimulus={
                "type": "VISUAL",
                "content": visual_description,
                "source": name_or_empty(source),
            },
            max_content_length=max_content_length,
        )

    def think(self, thought: str, max_content_length: int = default["max_content_display_length"]) -> Self:
        """
        Заставляет агента думать о чем-то и обновляет свое внутреннее когнитивное состояние.
        """
        return self._observe(
            stimulus={
                "type": "THOUGHT",
                "content": thought,
                "source": name_or_empty(self),
            },
            max_content_length=max_content_length,
        )

    def internalize_goal(
        self, goal: str, max_content_length: int = default["max_content_display_length"]
    ) -> Self:
        """
        Интернализует цель и обновляет свое внутреннее когнитивное состояние.
        """
        return self._observe(
            stimulus={
                "type": "INTERNAL_GOAL_FORMULATION",
                "content": goal,
                "source": name_or_empty(self),
            },
            max_content_length=max_content_length,
        )

    @transactional
    def _observe(self, stimulus: dict, max_content_length: int = default["max_content_display_length"]) -> Self:
        """
        Наблюдает за стимулом и обновляет внутреннее состояние агента.

        Args:
            stimulus (dict): Стимул для наблюдения.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            Self: Возвращает самого агента.
        """
        stimuli: list = [stimulus]

        content: dict = {"stimuli": stimuli}

        logger.debug(f"[{self.name}] Observing stimuli: {content}")

        # whatever comes from the outside will be interpreted as coming from 'user', simply because
        # this is the counterpart of 'assistant'

        self.store_in_memory({'role': 'user', 'content': content,
                              'type': 'stimulus',
                              'simulation_timestamp': self.iso_datetime()})

        if TinyPerson.communication_display:
            self._display_communication(
                role="user",
                content=content,
                kind="stimuli",
                simplified=True,
                max_content_length=max_content_length,
            )

        return self  # allows easier chaining of methods

    @transactional
    def listen_and_act(
        self,
        speech: str,
        return_actions: bool = False,
        max_content_length: int = default["max_content_display_length"],
    ) -> Optional[list]:
        """
        Удобный метод, который объединяет методы `listen` и `act`.
        """

        self.listen(speech, max_content_length=max_content_length)
        return self.act(
            return_actions=return_actions, max_content_length=max_content_length
        )

    @transactional
    def see_and_act(
        self,
        visual_description: str,
        return_actions: bool = False,
        max_content_length: int = default["max_content_display_length"],
    ) -> Optional[list]:
        """
        Удобный метод, который объединяет методы `see` и `act`.
        """

        self.see(visual_description, max_content_length=max_content_length)
        return self.act(
            return_actions=return_actions, max_content_length=max_content_length
        )

    @transactional
    def think_and_act(
        self,
        thought: str,
        return_actions: bool = False,
        max_content_length: int = default["max_content_display_length"],
    ) -> Optional[list]:
        """
        Удобный метод, который объединяет методы `think` и `act`.
        """

        self.think(thought, max_content_length=max_content_length)
        return self.act(return_actions=return_actions, max_content_length=max_content_length)

    def read_documents_from_folder(self, documents_path: str) -> None:
        """
        Читает документы из каталога и загружает их в семантическую память.
        """
        logger.info(f"Setting documents path to {documents_path} and loading documents.")

        self.semantic_memory.add_documents_path(documents_path)

    def read_document_from_file(self, file_path: str) -> None:
        """
        Читает документ из файла и загружает его в семантическую память.
        """
        logger.info(f"Reading document from file: {file_path}")

        self.semantic_memory.add_document_path(file_path)

    def read_documents_from_web(self, web_urls: list) -> None:
        """
        Читает документы с веб-URL и загружает их в семантическую память.
        """
        logger.info(f"Reading documents from the following web URLs: {web_urls}")

        self.semantic_memory.add_web_urls(web_urls)

    def read_document_from_web(self, web_url: str) -> None:
        """
        Читает документ с веб-URL и загружает его в семантическую память.
        """
        logger.info(f"Reading document from web URL: {web_url}")

        self.semantic_memory.add_web_url(web_url)

    @transactional
    def move_to(self, location: str, context: list = []) -> None:
        """
        Перемещается в новое местоположение и обновляет свое внутреннее когнитивное состояние.
        """
        self._mental_state["location"]: str = location

        # context must also be updated when moved, since we assume that context is dictated partly by location.
        self.change_context(context)

    @transactional
    def change_context(self, context: list) -> None:
        """
        Изменяет контекст и обновляет свое внутреннее когнитивное состояние.
        """
        self._mental_state["context"]: dict = {
            "description": item for item in context
        }

        self._update_cognitive_state(context=context)

    @transactional
    def make_agent_accessible(
        self,
        agent: Self,
        relation_description: str = "An agent I can currently interact with.",
    ) -> None:
        """
        Делает агента доступным для этого агента.
        """
        if agent not in self._accessible_agents:
            self._accessible_agents.append(agent)
            self._mental_state["accessible_agents"].append(
                {"name": agent.name, "relation_description": relation_description}
            )
        else:
            logger.warning(
                f"[{self.name}] Agent {agent.name} is already accessible to {self.name}."
            )

    @transactional
    def make_agent_inaccessible(self, agent: Self) -> None:
        """
        Делает агента недоступным для этого агента.
        """
        if agent in self._accessible_agents:
            self._accessible_agents.remove(agent)
        else:
            logger.warning(
                f"[{self.name}] Agent {agent.name} is already inaccessible to {self.name}."
            )

    @transactional
    def make_all_agents_inaccessible(self) -> None:
        """
        Делает всех агентов недоступными для этого агента.
        """
        self._accessible_agents: list = []
        self._mental_state["accessible_agents"]: list = []

    @transactional
    def _produce_message(self) -> tuple[str, dict]:
        """
        Создает сообщение для отправки в OpenAI API.

        Returns:
            tuple[str, dict]: Роль и контент сообщения.
        """
        # logger.debug(f"Current messages: {self.current_messages}")

        # ensure we have the latest prompt (initial system message + selected messages from memory)
        self.reset_prompt()

        messages: list = [
            {"role": msg["role"], "content": json.dumps(msg["content"])}
            for msg in self.current_messages
        ]

        logger.debug(f"[{self.name}] Sending messages to OpenAI API")
        logger.debug(f"[{self.name}] Last interaction: {messages[-