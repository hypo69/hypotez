### **Анализ кода модуля `agent.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура классов и функций.
    - Использование `logger` для логирования.
    - Наличие документации для большинства функций и классов.
    - Использование `textwrap` для форматирования текста.
    - Использование `chevron` для шаблонизации.
- **Минусы**:
    - Встречаются docstring на английском языке.
    - Не все переменные аннотированы типами.
    - Не везде используется `logger.error` для логирования ошибок.
    - Есть устаревшие комментарии.
    - Местами отсутствует подробное описание в комментариях.

#### **Рекомендации по улучшению**:
1.  **Документация**:
    *   Перевести все docstring на русский язык.
    *   Добавить более подробные комментарии к функциям и классам, объясняя их назначение и использование.
    *   Уточнить описание параметров и возвращаемых значений в docstring.
2.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где это необходимо.
    *   Убедиться, что все параметры функций и методов аннотированы типами.
3.  **Логирование**:
    *   Использовать `logger.error` для логирования ошибок и исключений.
    *   Добавить `exc_info=True` при логировании ошибок для получения полной информации об исключении.
4.  **Комментарии**:
    *   Избавиться от устаревших или неинформативных комментариев.
    *   Заменить общие формулировки в комментариях на более конкретные и понятные описания.
5.  **Использование констант**:
    *   Вместо магических чисел использовать константы с понятными именами (например, `MAX_ACTIONS_BEFORE_DONE`).
6.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках `except`.
7.  **Форматирование**:
    *   Убедиться, что код соответствует PEP8, особенно в части пробелов вокруг операторов.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с агентами TinyTroupe
========================================

Модуль содержит основные классы и функции для создания и управления агентами в TinyTroupe.
Агенты представляют собой симулированных личностей или сущностей, способных взаимодействовать
друг с другом и с окружающей средой.

Пример использования
----------------------

>>> agent = TinyPerson(name='Alice')
>>> agent.define('occupation', 'Software Engineer')
>>> agent.act()
"""

import os
import textwrap
import datetime
import chevron
import logging
import copy
from typing import Any, TypeVar, Union, List, Optional
from pathlib import Path

from rich import print

# Импортируем модуль логирования из проекта hypotez
from src.logger import logger

import tinytroupe.utils as utils
from tinytroupe.utils import post_init
from tinytroupe.control import transactional
from tinytroupe.control import current_simulation
from tinytroupe.utils import JsonSerializableRegistry
from tinytroupe.utils import name_or_empty, break_text_at_length, repeat_on_error
from tinytroupe import openai_utils

# LLaMa-Index configs
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader

Self = TypeVar("Self", bound="TinyPerson")
AgentOrWorld = Union[Self, "TinyWorld"]

###########################################################################
# Default parameter values
###########################################################################
# Используем различные элементы конфигурации
config = utils.read_config_file()

default = {}
default["embedding_model"] = config["OpenAI"].get("EMBEDDING_MODEL", "text-embedding-3-small")
default["max_content_display_length"] = config["OpenAI"].getint("MAX_CONTENT_DISPLAY_LENGTH", 1024)

llmaindex_openai_embed_model = OpenAIEmbedding(model=default["embedding_model"], embed_batch_size=10)
Settings.embed_model = llmaindex_openai_embed_model

#######################################################################################################################
# TinyPerson itself
#######################################################################################################################
@post_init
class TinyPerson(JsonSerializableRegistry):
    """
    Симулированный персонаж в TinyTroupe.

    Агент является ключевой абстракцией, используемой в TinyTroupe. Агент - это симулированный человек или сущность,
    который может взаимодействовать с другими агентами и окружающей средой, получая стимулы и производя действия.
    Агенты имеют когнитивные состояния, которые обновляются по мере их взаимодействия с окружающей средой и другими агентами.
    Агенты также могут хранить и извлекать информацию из памяти и выполнять действия в окружающей среде.
    В отличие от агентов, целью которых является поддержка AI-ассистентов или других подобных инструментов повышения
    производительности, **агенты TinyTroupe стремятся представлять человеческое поведение**, которое включает в себя
    идиосинкразии, эмоции и другие человеческие черты, которые не ожидаются от инструмента повышения производительности.

    Общий базовый дизайн вдохновлен в основном когнитивной психологией, поэтому агенты имеют различные внутренние
    когнитивные состояния, такие как внимание, эмоции и цели. Именно поэтому память агента, в отличие от других
    платформ агентов на основе LLM, имеет тонкие внутренние разделения, особенно между эпизодической и семантической
    памятью. Некоторые бихевиористские концепции также присутствуют, такие как идея "стимула" и "реакции" в методах
    `listen` и `act`, которые являются ключевыми абстракциями для понимания того, как агенты взаимодействуют с
    окружающей средой и другими агентами.
    """

    # Максимальное количество действий, которое агент может выполнить до завершения.
    # Это предотвращает бесконечные действия агента.
    MAX_ACTIONS_BEFORE_DONE: int = 15

    PP_TEXT_WIDTH: int = 100

    serializable_attributes: list[str] = ["name", "episodic_memory", "semantic_memory", "_mental_faculties", "_configuration"]

    # Словарь всех созданных агентов.
    all_agents: dict[str, Self] = {}  # name -> agent

    # Стиль общения для всех агентов: "simplified" или "full".
    communication_style: str = "simplified"

    # Отображать ли общение или нет. True для интерактивных приложений, когда мы хотим видеть результаты моделирования
    # по мере их создания.
    communication_display: bool = True

    def __init__(self, name: str = None,
                 episodic_memory = None,
                 semantic_memory = None,
                 mental_faculties: Optional[List["TinyMentalFaculty"]] = None):
        """
        Создает TinyPerson.

        Args:
            name (str): Имя TinyPerson.
            episodic_memory: Эпизодическая память.
            semantic_memory: Семантическая память.
            mental_faculties (Optional[List[TinyMentalFaculty]]): Список ментальных способностей агента. По умолчанию None.

        Raises:
            AssertionError: Если имя не указано.
        """

        # Присваиваем значения по умолчанию в методе _post_init,
        # так как он используется как при прямой инициализации, так и при десериализации.

        if episodic_memory is not None:
            self.episodic_memory = episodic_memory

        if semantic_memory is not None:
            self.semantic_memory = semantic_memory

        # Ментальные способности
        if mental_faculties is not None:
            self._mental_faculties = mental_faculties

        assert name is not None, "A TinyPerson must have a name."
        self.name = name

        # @post_init гарантирует, что _post_init будет вызван после __init__

    def _post_init(self, **kwargs):
        """
        Выполняется после __init__, так как класс имеет декоратор @post_init.
        Удобно разделять некоторые процессы инициализации, чтобы упростить десериализацию.
        """

        ############################################################
        # Default values
        ############################################################

        self.current_messages: list[dict] = []

        # Текущее окружение, в котором действует агент
        self.environment = None

        # Список действий, которые этот агент выполнил до сих пор, но которые еще не были
        # использованы окружением.
        self._actions_buffer: list[dict] = []

        # Список агентов, с которыми этот агент может в данный момент взаимодействовать.
        # Это может меняться со временем, так как агенты перемещаются по миру.
        self._accessible_agents: list[Self] = []

        # Буфер коммуникаций, которые были отображены до сих пор, используется для
        # сохранения этих коммуникаций в другую выходную форму позже (например, кэширование)
        self._displayed_communications_buffer: list[str] = []

        if not hasattr(self, 'episodic_memory'):
            # Значение по умолчанию НЕ ДОЛЖНО быть в сигнатуре метода, иначе оно будет общим для всех экземпляров.
            self.episodic_memory = EpisodicMemory()

        if not hasattr(self, 'semantic_memory'):
            # Значение по умолчанию НЕ ДОЛЖНО быть в сигнатуре метода, иначе оно будет общим для всех экземпляров.
            self.semantic_memory = SemanticMemory()

        # _mental_faculties
        if not hasattr(self, '_mental_faculties'):
            # Значение по умолчанию НЕ ДОЛЖНО быть в сигнатуре метода, иначе оно будет общим для всех экземпляров.
            self._mental_faculties: list["TinyMentalFaculty"] = []

        # Создаем словарь конфигурации
        if not hasattr(self, '_configuration'):
            self._configuration: dict[str, Any] = {
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
                "relationships": [],
                "current_datetime": None,
                "current_location": None,
                "current_context": [],
                "current_attention": None,
                "current_goals": [],
                "current_emotions": "Currently you feel calm and friendly.",
                "currently_accessible_agents": [],  # [{"agent": agent_1, "relation": "My friend"}, {"agent": agent_2, "relation": "My colleague"}, ...]
            }

        self._prompt_template_path: str = os.path.join(
            os.path.dirname(__file__), "prompts/tinyperson.mustache"
        )
        self._init_system_message = None  # Инициализируется позже

        ############################################################
        # Special mechanisms used during deserialization
        ############################################################

        # Переименовать агента в какое-то конкретное имя?
        if kwargs.get("new_agent_name") is not None:
            self._rename(kwargs.get("new_agent_name"))

        # Если автоматическое переименование, используйте данное имя плюс новый номер ...
        if kwargs.get("auto_rename") is True:
            new_name: str = self.name  # Начинаем с текущего имени
            rename_succeeded: bool = False
            while not rename_succeeded:
                try:
                    self._rename(new_name)
                    TinyPerson.add_agent(self)
                    rename_succeeded = True
                except ValueError:
                    new_id: str = utils.fresh_id()
                    new_name = f"{self.name}_{new_id}"

        # ... иначе, просто регистрируем агента
        else:
            # Регистрируем агента в глобальном списке агентов
            TinyPerson.add_agent(self)

        # Начинаем с чистого листа
        self.reset_prompt()

        # Может случиться так, что агент создается в рамках области моделирования, и в этом случае
        # simulation_id должен быть установлен соответствующим образом
        if current_simulation() is not None:
            current_simulation().add_agent(self)
        else:
            self.simulation_id = None

    def _rename(self, new_name: str):
        """
        Переименовывает агента.

        Args:
            new_name (str): Новое имя агента.
        """
        self.name = new_name
        self._configuration["name"] = self.name

    def generate_agent_prompt(self) -> str:
        """
        Генерирует prompt агента на основе mustache шаблона.

        Returns:
            str: Prompt агента.
        """
        with open(self._prompt_template_path, "r") as f:
            agent_prompt_template: str = f.read()

        # Будем оперировать поверх копии конфигурации, потому что нам нужно будет добавить больше переменных и т.д.
        template_variables: dict[str, Any] = self._configuration.copy()

        # Подготавливаем дополнительные определения действий и ограничения
        actions_definitions_prompt: str = ""
        actions_constraints_prompt: str = ""
        for faculty in self._mental_faculties:
            actions_definitions_prompt += f"{faculty.actions_definitions_prompt()}\\n"
            actions_constraints_prompt += f"{faculty.actions_constraints_prompt()}\\n"

        # Делаем дополнительные части prompt доступными для шаблона
        template_variables['actions_definitions_prompt'] = textwrap.indent(actions_definitions_prompt, "")
        template_variables['actions_constraints_prompt'] = textwrap.indent(actions_constraints_prompt, "")

        # RAI prompt components, if requested
        template_variables = utils.add_rai_template_variables_if_enabled(template_variables)

        return chevron.render(agent_prompt_template, template_variables)

    def reset_prompt(self):
        """
        Сбрасывает prompt агента, перегенерируя его из шаблона и текущей конфигурации.
        """

        # Рендерим шаблон с текущей конфигурацией
        self._init_system_message: str = self.generate_agent_prompt()

        # TODO на самом деле, придумать другой способ обновления состояния агента без "изменения истории"

        # Сбрасываем системное сообщение
        self.current_messages: list[dict] = [
            {"role": "system", "content": self._init_system_message}
        ]

        # Настраиваем фактические сообщения взаимодействия для использования при запросе
        self.current_messages += self.episodic_memory.retrieve_recent()

    def get(self, key: str) -> Any:
        """
        Возвращает определение ключа в конфигурации TinyPerson.

        Args:
            key (str): Ключ для поиска.

        Returns:
            Any: Значение ключа или None, если ключ не найден.
        """
        return self._configuration.get(key, None)

    @transactional
    def define(self, key: str, value: Any, group: str = None):
        """
        Определяет значение в конфигурации TinyPerson.

        Args:
            key (str): Ключ для определения.
            value (Any): Значение для установки.
            group (str, optional): Группа, к которой принадлежит значение. Defaults to None.
        """

        # Удаляем отступ, если это строка
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

        # Необходимо сбросить prompt после добавления в конфигурацию
        self.reset_prompt()

    def define_several(self, group: str, records: list[dict]):
        """
        Определяет несколько значений в конфигурации TinyPerson, принадлежащих к одной группе.

        Args:
            group (str): Группа, к которой принадлежат значения.
            records (list[dict]): Список записей для определения.
        """
        for record in records:
            self.define(key=None, value=record, group=group)

    @transactional
    def define_relationships(self, relationships: Union[list[dict], dict], replace: bool = True):
        """
        Определяет или обновляет отношения TinyPerson.

        Args:
            relationships (list[dict] or dict): Отношения для добавления или замены.
            replace (bool, optional): Заменять текущие отношения или просто добавлять к ним. Defaults to True.

        Raises:
            Exception: Если аргументы недействительны.
        """

        if (replace == True) and (isinstance(relationships, list)):
            self._configuration['relationships'] = relationships

        elif replace == False:
            current_relationships: list[dict] = self._configuration['relationships']
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
        self._configuration['relationships'] = []

        return self

    @transactional
    def related_to(self, other_agent: Self, description: str, symmetric_description: str = None) -> Self:
        """
        Определяет связь между этим агентом и другим агентом.

        Args:
            other_agent (TinyPerson): Другой агент.
            description (str): Описание связи.
            symmetric_description (str, optional): Симметричное описание. Defaults to None.

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
        """
        self.define_relationships([{"Name": other_agent.name, "Description": description}], replace=False)
        if symmetric_description is not None:
            other_agent.define_relationships([{"Name": self.name, "Description": symmetric_description}], replace=False)

        return self

    def add_mental_faculties(self, mental_faculties: list["TinyMentalFaculty"]) -> Self:
        """
        Добавляет список ментальных способностей агенту.

        Args:
            mental_faculties (list[TinyMentalFaculty]): Список ментальных способностей.

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
        """
        for faculty in mental_faculties:
            self.add_mental_faculty(faculty)

        return self

    def add_mental_faculty(self, faculty: "TinyMentalFaculty") -> Self:
        """
        Добавляет ментальную способность агенту.

        Args:
            faculty (TinyMentalFaculty): Ментальная способность для добавления.

        Raises:
            Exception: Если ментальная способность уже присутствует.

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
        """
        # Проверяем, есть ли уже эта способность или нет
        if faculty not in self._mental_faculties:
            self._mental_faculties.append(faculty)
        else:
            raise Exception(f"The mental faculty {faculty} is already present in the agent.")

        return self

    @transactional
    def act(
        self,
        until_done: bool = True,
        n: int = None,
        return_actions: bool = False,
        max_content_length: int = default["max_content_display_length"],
    ) -> Optional[list[dict]]:
        """
        Действует в окружающей среде и обновляет свое внутреннее когнитивное состояние.
        Либо действует до тех пор, пока агент не закончит и не потребуются дополнительные стимулы, либо действует фиксированное количество раз,
        но не оба варианта одновременно.

        Args:
            until_done (bool): Продолжать ли действовать, пока агент не будет завершен и не потребуются дополнительные стимулы.
            n (int, optional): Количество действий для выполнения. Defaults to None.
            return_actions (bool, optional): Возвращать ли действия. Defaults to False.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            Optional[list[dict]]: Список действий, если `return_actions` имеет значение True, иначе None.
        """

        # Либо действовать до тех пор, пока не будет выполнено, либо действовать фиксированное количество раз, но не оба варианта одновременно
        assert not (until_done and n is not None)
        if n is not None:
            assert n < TinyPerson.MAX_ACTIONS_BEFORE_DONE

        contents: list[dict] = []

        # Вспомогательная функция для выполнения ровно одного действия.
        # Иногда модель возвращает JSON с отсутствующими важными ключами, поэтому мы просто просим ее попробовать еще раз
        @repeat_on_error(retries=5, exceptions=[KeyError])
        def aux_act_once():
            """
            Вспомогательная функция для выполнения одного действия.
            """
            # Небольшая мысль перед действием. Это, кажется, помогает с лучшими ответами модели, возможно, потому что
            # это перемежает сообщения пользователя с сообщениями помощника.
            self.think("I will now act a bit, and then issue DONE.")

            role: str, content: dict = self._produce_message()

            self.episodic_memory.store({'role': role, 'content': content, 'simulation_timestamp': self.iso_datetime()})

            cognitive_state: dict = content["cognitive_state"]

            action: dict = content['action']

            self._actions_buffer.append(action)
            self._update_cognitive_state(goals=cognitive_state['goals'],
                                        attention=cognitive_state['attention'],
                                        emotions=cognitive_state['emotions'])

            contents.append(content)
            if TinyPerson.communication_display:
                self._display_communication(role=role, content=content, kind='action', simplified=True, max_content_length=max_content_length)

            #
            # Некоторые действия вызывают немедленный стимул или другие побочные эффекты. Мы должны обработать их здесь, с помощью умственных способностей.
            #
            for faculty in self._mental_faculties:
                faculty.process_action(self, action)

        #
        # Как поступить с последовательностью действий.
        #

        ##### Option 1: run N actions ######
        if n is not None:
            for i in range(n):
                aux_act_once()

        ##### Option 2: run until DONE ######
        elif until_done:
            while (len(contents) == 0) or (
                not contents[-1]["action"]["type"] == "DONE"
            ):

                # Проверяем, действует ли агент, не останавливаясь
                if len(contents) > TinyPerson.MAX_ACTIONS_BEFORE_DONE:
                    logger.warning(f"[{self.name}] Agent {self.name} is acting without ever stopping. This may be a bug. Let\'s stop it here anyway.")
                    break
                if len(contents) > 4:  # Just some minimum number of actions to check for repetition, could be anything >= 3
                    # Если последние три действия были одинаковыми, то мы, вероятно, находимся в цикле
                    if contents[-1]['action'] == contents[-2]['action'] == contents[-3]['action']:
                        logger.warning(f"[{self.name}] Agent {self.name} is acting in a loop. This may be a bug. Let\'s stop it here anyway.")
                        break

                aux_act_once()

        if return_actions:
            return contents
        
        return None

    @transactional
    def listen(
        self,
        speech: str,
        source: AgentOrWorld = None,
        max_content_length: int = default["max_content_display_length"],
    ) -> Self:
        """
        Слушает другого агента (искусственного или человеческого) и обновляет свое внутреннее когнитивное состояние.

        Args:
            speech (str): Речь для прослушивания.
            source (AgentOrWorld, optional): Источник речи. Defaults to None.

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
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
            source (AgentOrWorld, optional): Источник социального стимула. Defaults to None.

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
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
            source (AgentOrWorld, optional): Источник визуального стимула. Defaults to None.

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
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

        Args:
            thought (str): Мысль.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
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

        Args:
            goal (str): Цель.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
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
        Наблюдает за стимулом и обновляет внутреннее когнитивное состояние.

        Args:
            stimulus (dict): Стимул для наблюдения.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            TinyPerson: Агент, для облегчения цепочки.
        """
        stimuli: list[dict] = [stimulus]

        content: dict = {"stimuli": stimuli}

        logger.debug(f"[{self.name}] Observing stimuli: {content}")

        # Все, что приходит извне, будет интерпретироваться как приходящее от "user", просто потому, что
        # это аналог "assistant"

        self.episodic_memory.store({'role': 'user', 'content': content, 'simulation_timestamp': self.iso_datetime()})

        if TinyPerson.communication_display:
            self._display_communication(
                role="user",
                content=content,
                kind="stimuli",
                simplified=True,
                max_content_length=max_content_length,
            )

        return self  # Allows easier chaining of methods

    @transactional
    def listen_and_act(
        self,
        speech: str,
        return_actions: bool = False,
        max_content_length: int = default["max_content_display_length"],
    ) -> Optional[list[dict]]:
        """
        Удобный метод, который объединяет методы `listen` и `act`.

        Args:
            speech (str): Речь для прослушивания.
            return_actions (bool, optional): Возвращать ли действия. Defaults to False.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            Optional[list[dict]]: Список действий, если `return_actions` имеет значение True, иначе None.
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
    ) -> Optional[list[dict]]:
        """
        Удобный метод, который объединяет методы `see` и `act`.

        Args:
            visual_description (str): Описание визуального стимула.
            return_actions (bool, optional): Возвращать ли действия. Defaults to False.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            Optional[list[dict]]: Список действий, если `return_actions` имеет значение True, иначе None.
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
    ) -> Optional[list[dict]]:
        """
        Удобный метод, который объединяет методы `think` и `act`.

        Args:
            thought (str): Мысль.
            return_actions (bool, optional): Возвращать ли действия. Defaults to False.
            max_content_length (int, optional): Максимальная длина контента. Defaults to default["max_content_display_length"].

        Returns:
            Optional[list[dict]]: Список действий, если `return_actions` имеет значение True, иначе None.
        """

        self.think(thought, max_content_length=max_content_length)
        return self.act(return_actions=return_actions, max_content_length=max_content_length)

    def read_documents_from_folder(self, documents_path: str):
        """
        Читает документы из каталога и загружает их в семантическую память.

        Args:
            documents_path (str): Путь к каталогу с документами.
        """
        logger.info(f"Setting documents path to {documents_path} and loading documents.")

        self.semantic_memory.add_documents_path(documents_path)

    def read_documents_from_web(self, web_urls: list[str]):
        """
        Читает документы из веб-URL и загружает их в семантическую память.

        Args:
            web_urls (list[str]): Список веб-URL.
        """
        logger.info(f"Reading documents from the following web URLs: {web_urls}")

        self.semantic_memory.add_web_urls(web_urls)

    @transactional
    def move_to(self, location: str, context: list[str] = []):
        """
        Перемещается в новое местоположение и обновляет свое внутреннее когнитивное состояние.

        Args:
            location (str): Новое местоположение.
            context (list[str], optional): Контекст. Defaults to [].
        """
        self._configuration["current_location"] = location