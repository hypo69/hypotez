### **Анализ кода модуля `environment.py`**

## \file hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/environment.py

Модуль содержит классы для моделирования окружения, в котором взаимодействуют агенты, включая базовый класс `TinyWorld` и его подкласс `TinySocialNetwork`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура классов и методов.
    - Использование логирования для отладки и мониторинга.
    - Реализация основных методов для управления агентами и их взаимодействием.
- **Минусы**:
    - Отсутствуют аннотации типов для некоторых переменных.
    - Не все методы документированы в соответствии с заданным форматом.
    - В некоторых местах используется `Exception` без указания конкретного типа исключения.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавьте аннотации типов для всех переменных и возвращаемых значений функций, где это отсутствует.

2.  **Улучшить документацию**:
    - Приведите все docstring к единому стандарту, включая подробное описание аргументов, возвращаемых значений и возможных исключений.

3.  **Конкретизировать исключения**:
    - Замените общие `Exception` на более конкретные типы исключений, чтобы улучшить обработку ошибок.

4.  **Использовать `logger` из `src.logger`**:
    - Убедитесь, что для логирования используется модуль `logger` из `src.logger`.

5.  **Улучшить обработку ошибок**:
    - Добавьте обработку исключений в тех местах, где это необходимо, и логируйте ошибки с использованием `logger.error`.

6.  **Изменить структуру проекта:**
    - изменить импорт logging на `from src.logger import logger`

7.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные.

**Оптимизированный код:**

```python
"""
Модуль для моделирования окружения, в котором взаимодействуют агенты.
=====================================================================

Модуль содержит классы для моделирования окружения, в котором взаимодействуют агенты,
включая базовый класс :class:`TinyWorld` и его подкласс :class:`TinySocialNetwork`.

Пример использования
----------------------

>>> world = TinyWorld(name='MyWorld')
>>> agent = TinyPerson(name='Agent1')
>>> world.add_agent(agent)
>>> world.run(steps=10)
"""

from src.logger import logger  # Используем logger из src.logger
import copy
from datetime import datetime, timedelta

from tinytroupe.agent import TinyPerson
from tinytroupe.utils import name_or_empty, pretty_datetime
import tinytroupe.control as control
from tinytroupe.control import transactional

from rich.console import Console

from typing import Any, TypeVar, Union

AgentOrWorld = Union["TinyPerson", "TinyWorld"]


class TinyWorld:
    """
    Базовый класс для окружений.
    """

    # Словарь всех созданных окружений.
    all_environments: dict = {}  # name -> environment

    # Отображать ли сообщения окружений или нет, для всех окружений.
    communication_display: bool = True

    def __init__(
        self,
        name: str = "A TinyWorld",
        agents: list = [],
        initial_datetime: datetime = datetime.now(),
        broadcast_if_no_target: bool = True,
    ):
        """
        Инициализирует окружение.

        Args:
            name (str): Имя окружения.
            agents (list): Список агентов для добавления в окружение.
            initial_datetime (datetime): Начальная дата и время окружения, или None (т.е., явное время опционально).
                По умолчанию текущая дата и время в реальном мире.
            broadcast_if_no_target (bool): Если True, транслировать действия, если цель действия не найдена.
        """

        self.name: str = name
        self.current_datetime: datetime = initial_datetime
        self.broadcast_if_no_target: bool = broadcast_if_no_target
        self.simulation_id: str | None = None  # будет сброшен позже, если агент используется в определенной области моделирования

        self.agents: list[TinyPerson] = []
        self.name_to_agent: dict[str, TinyPerson] = {}  # {agent_name: agent, agent_name_2: agent_2, ...}

        # буфер сообщений, которые были отображены до сих пор, используется для
        # сохранения этих сообщений в другую форму вывода позже (например, кэширование)
        self._displayed_communications_buffer: list = []

        self.console: Console = Console()

        # добавить окружение в список всех окружений
        TinyWorld.add_environment(self)

        self.add_agents(agents)

    #######################################################################
    # Методы управления моделированием
    #######################################################################
    @transactional
    def _step(self, timedelta_per_step: timedelta | None = None) -> dict:
        """
        Выполняет один шаг в окружении. Эта реализация по умолчанию
        просто заставляет всех агентов в окружении действовать и правильно
        обрабатывать результирующие действия. Подклассы могут переопределить этот метод для реализации
        различных политик.

        Args:
            timedelta_per_step (timedelta | None, optional): Временной интервал для каждого шага. По умолчанию None.

        Returns:
            dict: Словарь действий агентов.
        """
        # увеличить текущую дату и время, если задан timedelta. Это должно произойти до
        # любых других обновлений моделирования, чтобы убедиться, что агенты действуют
        # в правильное время, особенно если выполняется только один шаг.
        self._advance_datetime(timedelta_per_step)

        # агенты могут действовать
        agents_actions: dict = {}
        for agent in self.agents:
            logger.debug(f"[{self.name}] Agent {name_or_empty(agent)} is acting.")
            actions: list = agent.act(return_actions=True)
            agents_actions[agent.name] = actions

            self._handle_actions(agent, agent.pop_latest_actions())

        return agents_actions

    def _advance_datetime(self, timedelta: timedelta | None):
        """
        Увеличивает текущую дату и время окружения на указанный timedelta.

        Args:
            timedelta (timedelta): Timedelta, на который нужно увеличить текущую дату и время.
        """
        if timedelta is not None:
            self.current_datetime += timedelta
        else:
            logger.info(
                f"[{self.name}] No timedelta provided, so the datetime was not advanced."
            )

    @transactional
    def run(
        self, steps: int, timedelta_per_step: timedelta | None = None, return_actions: bool = False
    ) -> list | None:
        """
        Запускает окружение на заданное количество шагов.

        Args:
            steps (int): Количество шагов для запуска окружения.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию None.
            return_actions (bool, optional): Если True, возвращает действия, предпринятые агентами. По умолчанию False.

        Returns:
            list | None: Список действий, предпринятых агентами с течением времени, если return_actions имеет значение True.
                         Список имеет следующий формат:
                         [{agent_name: [action_1, action_2, ...]}, {agent_name_2: [action_1, action_2, ...]}, ...]
        """
        agents_actions_over_time: list = []
        for i in range(steps):
            logger.info(f"[{self.name}] Running world simulation step {i+1} of {steps}.")

            if TinyWorld.communication_display:
                self._display_communication(
                    cur_step=i + 1,
                    total_steps=steps,
                    kind='step',
                    timedelta_per_step=timedelta_per_step,
                )

            agents_actions: dict = self._step(timedelta_per_step=timedelta_per_step)
            agents_actions_over_time.append(agents_actions)

        if return_actions:
            return agents_actions_over_time
        return None

    @transactional
    def skip(self, steps: int, timedelta_per_step: timedelta | None = None):
        """
        Пропускает заданное количество шагов в окружении. То есть время должно пройти, но никаких действий не будет предпринято
        агентами или каким-либо другим существом в окружении.

        Args:
            steps (int): Количество шагов для пропуска.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию None.
        """
        if timedelta_per_step:
            self._advance_datetime(steps * timedelta_per_step)

    def run_minutes(self, minutes: int):
        """
        Запускает окружение на заданное количество минут.

        Args:
            minutes (int): Количество минут для запуска окружения.
        """
        self.run(steps=minutes, timedelta_per_step=timedelta(minutes=1))

    def skip_minutes(self, minutes: int):
        """
        Пропускает заданное количество минут в окружении.

        Args:
            minutes (int): Количество минут для пропуска.
        """
        self.skip(steps=minutes, timedelta_per_step=timedelta(minutes=1))

    def run_hours(self, hours: int):
        """
        Запускает окружение на заданное количество часов.

        Args:
            hours (int): Количество часов для запуска окружения.
        """
        self.run(steps=hours, timedelta_per_step=timedelta(hours=1))

    def skip_hours(self, hours: int):
        """
        Пропускает заданное количество часов в окружении.

        Args:
            hours (int): Количество часов для пропуска.
        """
        self.skip(steps=hours, timedelta_per_step=timedelta(hours=1))

    def run_days(self, days: int):
        """
        Запускает окружение на заданное количество дней.

        Args:
            days (int): Количество дней для запуска окружения.
        """
        self.run(steps=days, timedelta_per_step=timedelta(days=1))

    def skip_days(self, days: int):
        """
        Пропускает заданное количество дней в окружении.

        Args:
            days (int): Количество дней для пропуска.
        """
        self.skip(steps=days, timedelta_per_step=timedelta(days=1))

    def run_weeks(self, weeks: int):
        """
        Запускает окружение на заданное количество недель.

        Args:
            weeks (int): Количество недель для запуска окружения.
        """
        self.run(steps=weeks, timedelta_per_step=timedelta(weeks=1))

    def skip_weeks(self, weeks: int):
        """
        Пропускает заданное количество недель в окружении.

        Args:
            weeks (int): Количество недель для пропуска.
        """
        self.skip(steps=weeks, timedelta_per_step=timedelta(weeks=1))

    def run_months(self, months: int):
        """
        Запускает окружение на заданное количество месяцев.

        Args:
            months (int): Количество месяцев для запуска окружения.
        """
        self.run(steps=months, timedelta_per_step=timedelta(weeks=4))

    def skip_months(self, months: int):
        """
        Пропускает заданное количество месяцев в окружении.

        Args:
            months (int): Количество месяцев для пропуска.
        """
        self.skip(steps=months, timedelta_per_step=timedelta(weeks=4))

    def run_years(self, years: int):
        """
        Запускает окружение на заданное количество лет.

        Args:
            years (int): Количество лет для запуска окружения.
        """
        self.run(steps=years, timedelta_per_step=timedelta(days=365))

    def skip_years(self, years: int):
        """
        Пропускает заданное количество лет в окружении.

        Args:
            years (int): Количество лет для пропуска.
        """
        self.skip(steps=years, timedelta_per_step=timedelta(days=365))

    #######################################################################
    # Методы управления агентами
    #######################################################################
    def add_agents(self, agents: list) -> "TinyWorld":
        """
        Добавляет список агентов в окружение.

        Args:
            agents (list): Список агентов для добавления в окружение.

        Returns:
            TinyWorld: self для связывания.
        """
        for agent in agents:
            self.add_agent(agent)

        return self  # для связывания

    def add_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Добавляет агента в окружение. У агента должно быть уникальное имя в окружении.

        Args:
            agent (TinyPerson): Агент для добавления в окружение.

        Raises:
            ValueError: Если имя агента не уникально в окружении.

        Returns:
            TinyWorld: self для связывания.
        """

        # проверить, нет ли агента уже в окружении
        if agent not in self.agents:
            logger.debug(f"Adding agent {agent.name} to the environment.")

            # Имена агентов должны быть уникальными в окружении.
            # Проверить, есть ли уже имя агента.
            if agent.name not in self.name_to_agent:
                agent.environment = self
                self.agents.append(agent)
                self.name_to_agent[agent.name] = agent
            else:
                raise ValueError(
                    f"Agent names must be unique, but '{agent.name}' is already in the environment."
                )
        else:
            logger.warn(f"Agent {agent.name} is already in the environment.")

        return self  # для связывания

    def remove_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Удаляет агента из окружения.

        Args:
            agent (TinyPerson): Агент для удаления из окружения.

        Returns:
            TinyWorld: self для связывания.
        """
        logger.debug(f"Removing agent {agent.name} from the environment.")
        self.agents.remove(agent)
        del self.name_to_agent[agent.name]

        return self  # для связывания

    def remove_all_agents(self) -> "TinyWorld":
        """
        Удаляет всех агентов из окружения.

        Returns:
            TinyWorld: self для связывания.
        """
        logger.debug(f"Removing all agents from the environment.")
        self.agents = []
        self.name_to_agent = {}

        return self  # для связывания

    def get_agent_by_name(self, name: str) -> TinyPerson | None:
        """
        Возвращает агента с указанным именем. Если агента с таким именем не существует в окружении,
        возвращает None.

        Args:
            name (str): Имя агента для возврата.

        Returns:
            TinyPerson | None: Агент с указанным именем.
        """
        if name in self.name_to_agent:
            return self.name_to_agent[name]
        else:
            return None

    #######################################################################
    # Обработчики действий
    #
    # Определенные действия, выполняемые агентами, обрабатываются окружением,
    # потому что они имеют последствия, выходящие за рамки самого агента.
    #######################################################################
    @transactional
    def _handle_actions(self, source: TinyPerson, actions: list):
        """
        Обрабатывает действия, выполняемые агентами.

        Args:
            source (TinyPerson): Агент, выполнивший действия.
            actions (list): Список действий, выполняемых агентами. Каждое действие на самом деле является
              JSON-спецификацией.
        """
        for action in actions:
            action_type: str = action["type"]  # это единственное обязательное поле
            content: str | None = action["content"] if "content" in action else None
            target: str | None = action["target"] if "target" in action else None

            logger.debug(
                f"[{self.name}] Handling action {action_type} from agent {name_or_empty(source)}. Content: {content}, target: {target}."
            )

            # только некоторые действия требуют вмешательства окружения
            if action_type == "REACH_OUT":
                self._handle_reach_out(source, content, target)
            elif action_type == "TALK":
                self._handle_talk(source, content, target)

    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие REACH_OUT. Эта реализация по умолчанию всегда позволяет REACH_OUT завершиться успешно.
        Подклассы могут переопределить этот метод для реализации различных политик.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие REACH_OUT.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """

        # Эта реализация по умолчанию всегда позволяет REACH_OUT завершиться успешно.
        target_agent: TinyPerson | None = self.get_agent_by_name(target)

        source_agent.make_agent_accessible(target_agent)
        if target_agent:
            target_agent.make_agent_accessible(source_agent)

        source_agent.socialize(
            f"{name_or_empty(target_agent)} was successfully reached out, and is now available for interaction.",
            source=self,
        )
        if target_agent:
            target_agent.socialize(
                f"{name_or_empty(source_agent)} reached out to you, and is now available for interaction.",
                source=self,
            )

    @transactional
    def _handle_talk(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие TALK, доставляя указанное содержимое указанной цели.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие TALK.
            content (str): Содержимое сообщения.
            target (str, optional): Цель сообщения.
        """
        target_agent: TinyPerson | None = self.get_agent_by_name(target)

        logger.debug(
            f"[{self.name}] Delivering message from {name_or_empty(source_agent)} to {name_or_empty(target_agent)}."
        )

        if target_agent is not None:
            target_agent.listen(content, source=source_agent)
        elif self.broadcast_if_no_target:
            self.broadcast(content, source=source_agent)

    #######################################################################
    # Методы взаимодействия
    #######################################################################
    @transactional
    def broadcast(self, speech: str, source: AgentOrWorld | None = None):
        """
        Доставляет сообщение всем агентам в окружении.

        Args:
            speech (str): Содержимое сообщения.
            source (AgentOrWorld, optional): Агент или окружение, отправившее сообщение. По умолчанию None.
        """
        logger.debug(f"[{self.name}] Broadcasting message: '{speech}'.")

        for agent in self.agents:
            # не доставлять сообщение источнику
            if agent != source:
                agent.listen(speech, source=source)

    @transactional
    def broadcast_thought(self, thought: str, source: AgentOrWorld | None = None):
        """
        Транслирует мысль всем агентам в окружении.

        Args:
            thought (str): Содержимое мысли.
        """
        logger.debug(f"[{self.name}] Broadcasting thought: '{thought}'.")

        for agent in self.agents:
            agent.think(thought)

    @transactional
    def broadcast_internal_goal(self, internal_goal: str):
        """
        Транслирует внутреннюю цель всем агентам в окружении.

        Args:
            internal_goal (str): Содержимое внутренней цели.
        """
        logger.debug(f"[{self.name}] Broadcasting internal goal: '{internal_goal}'.")

        for agent in self.agents:
            agent.internalize_goal(internal_goal)

    @transactional
    def broadcast_context_change(self, context: list):
        """
        Транслирует изменение контекста всем агентам в окружении.

        Args:
            context (list): Содержимое изменения контекста.
        """
        logger.debug(f"[{self.name}] Broadcasting context change: '{context}'.")

        for agent in self.agents:
            agent.change_context(context)

    def make_everyone_accessible(self):
        """
        Делает всех агентов в окружении доступными друг для друга.
        """
        for agent_1 in self.agents:
            for agent_2 in self.agents:
                if agent_1 != agent_2:
                    agent_1.make_agent_accessible(agent_2)

    ###########################################################
    # Удобства форматирования
    ###########################################################

    # TODO лучше имена для этих методов "display"
    def _display_communication(
        self, cur_step: int, total_steps: int, kind: str, timedelta_per_step: timedelta | None = None
    ):
        """
        Отображает текущее сообщение и сохраняет его в буфере для последующего использования.
        """
        if kind == 'step':
            rendering: str = self._pretty_step(
                cur_step=cur_step, total_steps=total_steps, timedelta_per_step=timedelta_per_step
            )
        else:
            raise ValueError(f"Unknown communication kind: {kind}")

        self._push_and_display_latest_communication({"content": rendering, "kind": kind})

    def _push_and_display_latest_communication(self, rendering: dict):
        """
        Помещает последние сообщения в буфер агента.
        """
        self._displayed_communications_buffer.append(rendering)
        self._display(rendering)

    def pop_and_display_latest_communications(self) -> list:
        """
        Извлекает последние сообщения и отображает их.
        """
        communications: list = self._displayed_communications_buffer
        self._displayed_communications_buffer = []

        for communication in communications:
            self._display(communication)

        return communications

    def _display(self, communication: dict | str):
        """Отображает коммуникации"""
        # unpack the rendering to find more info
        if isinstance(communication, dict):
            content: str = communication["content"]
            kind: str | None = communication["kind"]
        else:
            content: str = communication
            kind: str | None = None

        # render as appropriate
        if kind == 'step':
            self.console.rule(content)
        else:
            self.console.print(content)

    def clear_communications_buffer(self):
        """
        Очищает буфер сообщений.
        """
        self._displayed_communications_buffer = []

    def __repr__(self):
        return f"TinyWorld(name='{self.name}')"

    def _pretty_step(self, cur_step: int, total_steps: int, timedelta_per_step: timedelta | None = None) -> str:
        """возвращает строку для шага"""
        rendering: str = f"{self.name} step {cur_step} of {total_steps}"
        if timedelta_per_step is not None:
            rendering += f" ({pretty_datetime(self.current_datetime)})"

        return rendering

    def pp_current_interactions(self, simplified: bool = True, skip_system: bool = True):
        """
        Красиво выводит текущие сообщения от агентов в этом окружении.
        """
        print(
            self.pretty_current_interactions(simplified=simplified, skip_system=skip_system)
        )

    def pretty_current_interactions(
        self,
        simplified: bool = True,
        skip_system: bool = True,
        max_content_length: int = default["max_content_display_length"],
        first_n: int | None = None,
        last_n: int | None = None,
        include_omission_info: bool = True,
    ) -> str:
        """
        Возвращает красивую, читаемую строку с текущими сообщениями агентов в этом окружении.
        """
        agent_contents: list = []

        for agent in self.agents:
            agent_content: str = (
                "#### Interactions from the point of view of {agent.name} agent:\\n"
            )
            agent_content += "**BEGIN AGENT {agent.name} HISTORY.**\\n "
            agent_content += (
                agent.pretty_current_interactions(
                    simplified=simplified,
                    skip_system=skip_system,
                    max_content_length=max_content_length,
                    first_n=first_n,
                    last_n=last_n,
                    include_omission_info=include_omission_info,
                )
                + "\\n"
            )
            agent_content += "**FINISHED AGENT {agent.name} HISTORY.**\\n\\n"

            agent_contents.append(agent_content)

        return "\\n".join(agent_contents)

    #######################################################################
    # IO
    #######################################################################

    def encode_complete_state(self) -> dict:
        """
        Кодирует полное состояние окружения в словарь.

        Returns:
            dict: Словарь, кодирующий полное состояние окружения.
        """
        to_copy: dict = copy.copy(self.__dict__)

        # remove the logger and other fields
        del to_copy['console']
        del to_copy['agents']
        del to_copy['name_to_agent']
        del to_copy['current_datetime']

        state: dict = copy.deepcopy(to_copy)

        # agents are encoded separately
        state["agents"] = [agent.encode_complete_state() for agent in self.agents]

        # datetime also has to be encoded separately
        state["current_datetime"] = self.current_datetime.isoformat()

        return state

    def decode_complete_state(self, state: dict) -> "TinyWorld":
        """
        Декодирует полное состояние окружения из словаря.

        Args:
            state (dict): Словарь, кодирующий полное состояние окружения.

        Returns:
            TinyWorld: Окружение, декодированное из словаря.
        """
        state: dict = copy.deepcopy(state)

        #################################
        # restore agents in-place
        #################################
        self.remove_all_agents()
        for agent_state in state["agents"]:
            try:
                try:
                    agent: TinyPerson = TinyPerson.get_agent_by_name(agent_state["name"])
                except Exception as ex:
                    raise ValueError(
                        f"Could not find agent {agent_state['name']} for environment {self.name}."
                    ) from ex

                agent.decode_complete_state(agent_state)
                self.add_agent(agent)

            except Exception as ex:
                raise ValueError(
                    f"Could not decode agent {agent_state['name']} for environment {self.name}."
                ) from ex

        # remove the agent states to update the rest of the environment
        del state["agents"]

        # restore datetime
        state["current_datetime"] = datetime.datetime.fromisoformat(state["current_datetime"])

        # restore other fields
        self.__dict__.update(state)

        return self

    @staticmethod
    def add_environment(environment: "TinyWorld"):
        """
        Добавляет окружение в список всех окружений. Имена окружений должны быть уникальными,
        поэтому, если окружение с таким же именем уже существует, возникает ошибка.
        """
        if environment.name in TinyWorld.all_environments:
            raise ValueError(
                f"Environment names must be unique, but '{environment.name}' is already defined."
            )
        else:
            TinyWorld.all_environments[environment.name] = environment

    @staticmethod
    def set_simulation_for_free_environments(simulation):
        """
        Устанавливает моделирование, если оно None. Это позволяет захватывать свободные окружения конкретными областями моделирования
        при желании.
        """
        for environment in TinyWorld.all_environments.values():
            if environment.simulation_id is None:
                simulation.add_environment(environment)

    @staticmethod
    def get_environment_by_name(name: str) -> "TinyWorld" | None:
        """
        Возвращает окружение с указанным именем. Если окружения с таким именем не существует,
        возвращает None.

        Args:
            name (str): Имя окружения для возврата.

        Returns:
            TinyWorld | None: Окружение с указанным именем.
        """
        if name in TinyWorld.all_environments:
            return TinyWorld.all_environments[name]
        else:
            return None

    @staticmethod
    def clear_environments():
        """
        Очищает список всех окружений.
        """
        TinyWorld.all_environments = {}


class TinySocialNetwork(TinyWorld):
    """Окружение для моделирования социальных сетей"""

    def __init__(self, name: str, broadcast_if_no_target: bool = True):
        """
        Создает новое окружение TinySocialNetwork.

        Args:
            name (str): Имя окружения.
            broadcast_if_no_target (bool): Если True, транслировать действия через доступные отношения агента,
              если цель действия не найдена.
        """

        super().__init__(name, broadcast_if_no_target=broadcast_if_no_target)

        self.relations: dict = {}

    @transactional
    def add_relation(self, agent_1: TinyPerson, agent_2: TinyPerson, name: str = "default") -> "TinySocialNetwork":
        """
        Добавляет отношение между двумя агентами.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент.
            name (str): Имя отношения.

        Returns:
            TinySocialNetwork: self для связывания.
        """

        logger.debug(f"Adding relation {name} between {agent_1.name} and {agent_2.name}.")

        # агенты должны уже быть в окружении, если нет, они сначала добавляются
        if agent_1 not in self.agents:
            self.agents.append(agent_1)
        if agent_2 not in self.agents:
            self.agents.append(agent_2)

        if name in self.relations:
            self.relations[name].append((agent_1, agent_2))
        else:
            self.relations[name] = [(agent_1, agent_2)]

        return self  # для связывания

    @transactional
    def _update_agents_contexts(self):
        """
        Обновляет наблюдения агентов на основе текущего состояния мира.
        """

        # сначала очистить всю доступность
        for agent in self.agents:
            agent.make_all_agents_inaccessible()

        # теперь обновить доступность на основе отношений
        for relation_name, relation in self.relations.items():
            logger.debug(f"Updating agents' observations for relation {relation_name}.")
            for agent_1, agent_2 in relation:
                agent_1.make_agent_accessible(agent_2)
                agent_2.make_agent_accessible(agent_1)

    @transactional
    def _step(self):
        """Выполняет шаг симуляции"""
        self._update_agents_contexts()

        # call super
        super()._step()

    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие REACH_OUT. Эта реализация социальной сети разрешает
        REACH_OUT завершиться успешно, только если целевой агент находится в том же отношении, что и исходный агент.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие REACH_OUT.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """

        # проверить, находится ли цель в том же отношении, что и источник
        if self.is_in_relation_with(source_agent, self.get_agent_by_name(target)):
            super()._handle_reach_out(source_agent, content, target)

        # если мы дошли до сюда, цель не находится в том же отношении, что и источник
        source_agent.socialize(
            f"{target} is not in the same relation as you, so you cannot reach out to them.",
            source=self,
        )

    # TODO implement _handle_talk using broadcast_if_no_target too

    #######################################################################
    # Утилиты и удобства
    #######################################################################

    def is_in_relation_with(
        self, agent_1: TinyPerson, agent_2: TinyPerson, relation_name: str | None = None
    ) -> bool:
        """
        Проверяет, находятся ли два агента в отношении. Если указано имя отношения, проверить, что
        агенты находятся в этом отношении. Если имя отношения не указано, проверить, что агенты
        находятся в каком-либо отношении. Отношения ненаправленные, поэтому порядок агентов не имеет значения.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент