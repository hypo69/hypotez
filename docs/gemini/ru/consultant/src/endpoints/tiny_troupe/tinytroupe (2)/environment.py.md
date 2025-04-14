### **Анализ кода модуля `environment.py`**

## \file hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/environment.py

Модуль содержит классы для определения окружения, в котором взаимодействуют агенты, включая базовый класс `TinyWorld` и его расширение `TinySocialNetwork`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая организация кода, классы и методы четко структурированы.
  - Использование логирования для отслеживания действий агентов и изменений в окружении.
  - Наличие базовой реализации методов для управления временем и взаимодействием агентов.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных в некоторых местах.
  - Смешанный стиль кавычек (используются как одинарные, так и двойные).
  - Docstring в основном на английском языке.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и возвращаемых значений функций.
2.  **Исправить стиль кавычек**:
    - Заменить все двойные кавычки на одинарные.
3.  **Перевести docstring на русский язык**:
    - Перевести все docstring на русский язык, чтобы соответствовать требованиям.
4.  **Использовать `logger` из `src.logger`**:
    - Заменить текущий `logger` на `logger` из модуля `src.logger.logger`.
5.  **Документировать все методы и классы**:
    - Добавить docstring для всех методов и классов, включая описание аргументов, возвращаемых значений и возможных исключений.
6.  **Использовать `ex` в блоках `except`**:
    - Переименовать переменную исключения с `e` на `ex` в блоках `except`.
7.  **Улучшить обработку исключений**:
    - Добавить логирование ошибок с использованием `logger.error` в блоках `except`.
8.  **Удалить неиспользуемые импорты**:
    - Проверить и удалить неиспользуемые импорты.

**Оптимизированный код:**

```python
"""
Модуль для определения окружения, в котором взаимодействуют агенты.
==================================================================

Модуль содержит классы для определения окружения, в котором взаимодействуют агенты,
включая базовый класс :class:`TinyWorld` и его расширение :class:`TinySocialNetwork`.

Пример использования
----------------------

>>> world = TinyWorld(name='MyWorld')
>>> agent = TinyPerson(name='Alice')
>>> world.add_agent(agent)
>>> world.run(steps=1)
"""

import copy
from datetime import datetime, timedelta
from typing import Any, TypeVar, Union, List, Optional

from rich.console import Console

from src.logger.logger import logger
from tinytroupe.agent import TinyPerson
from tinytroupe.utils import name_or_empty, pretty_datetime
import tinytroupe.control as control
from tinytroupe.control import transactional

AgentOrWorld = Union["TinyPerson", "TinyWorld"]


class TinyWorld:
    """
    Базовый класс для окружений.
    """

    # Словарь всех созданных окружений.
    all_environments: dict = {}  # name -> environment

    # Отображать ли коммуникации окружений или нет, для всех окружений.
    communication_display: bool = True

    def __init__(
        self,
        name: str = "A TinyWorld",
        agents: Optional[List[TinyPerson]] = None,
        initial_datetime: Optional[datetime] = None,
        broadcast_if_no_target: bool = True,
    ) -> None:
        """
        Инициализирует окружение.

        Args:
            name (str): Имя окружения. По умолчанию "A TinyWorld".
            agents (Optional[List[TinyPerson]]): Список агентов для добавления в окружение. По умолчанию пустой список.
            initial_datetime (Optional[datetime]): Начальное время окружения.
                Если `None`, используется текущее время. По умолчанию `datetime.now()`.
            broadcast_if_no_target (bool): Если `True`, рассылает действия, если цель действия не найдена.
        """

        self.name: str = name
        self.current_datetime: datetime = initial_datetime if initial_datetime else datetime.now()
        self.broadcast_if_no_target: bool = broadcast_if_no_target
        self.simulation_id: Optional[str] = None  # будет сброшен позже, если агент используется в определенной области моделирования

        self.agents: List[TinyPerson] = []
        self.name_to_agent: dict = {}  # {agent_name: agent, agent_name_2: agent_2, ...}

        # буфер коммуникаций, которые были отображены, используется для
        # сохранения этих коммуникаций в другом формате позже (например, для кэширования)
        self._displayed_communications_buffer: list = []

        self.console: Console = Console()

        # добавить окружение в список всех окружений
        TinyWorld.add_environment(self)

        self.add_agents(agents if agents else [])

    #######################################################################
    # Методы управления моделированием
    #######################################################################
    @transactional
    def _step(self, timedelta_per_step: Optional[timedelta] = None) -> dict:
        """
        Выполняет один шаг в окружении. Эта реализация по умолчанию
        просто заставляет всех агентов в окружении действовать и правильно
        обрабатывает полученные действия. Подклассы могут переопределять этот метод для реализации
        различных политик.

        Args:
            timedelta_per_step (Optional[timedelta]): Временной интервал для каждого шага. По умолчанию `None`.

        Returns:
            dict: Словарь действий агентов.
        """
        # увеличить текущее время, если задан timedelta. Это должно произойти до
        # любых других обновлений моделирования, чтобы убедиться, что агенты действуют
        # в правильное время, особенно если выполняется только один шаг.
        self._advance_datetime(timedelta_per_step)

        # агенты могут действовать
        agents_actions: dict = {}
        for agent in self.agents:
            logger.debug(f"[{self.name}] Агент {name_or_empty(agent)} действует.")
            actions: list = agent.act(return_actions=True)
            agents_actions[agent.name] = actions

            self._handle_actions(agent, agent.pop_latest_actions())

        return agents_actions

    def _advance_datetime(self, timedelta: Optional[timedelta]) -> None:
        """
        Продвигает текущее время окружения на указанный timedelta.

        Args:
            timedelta (Optional[timedelta]): Временной интервал для продвижения текущего времени.
        """
        if timedelta is not None:
            self.current_datetime += timedelta
        else:
            logger.info(
                f"[{self.name}] Не указан timedelta, поэтому время не было продвинуто."
            )

    @transactional
    def run(
        self,
        steps: int,
        timedelta_per_step: Optional[timedelta] = None,
        return_actions: bool = False,
    ) -> Optional[List[dict]]:
        """
        Запускает окружение на заданное количество шагов.

        Args:
            steps (int): Количество шагов для запуска окружения.
            timedelta_per_step (Optional[timedelta], optional): Временной интервал между шагами. По умолчанию None.
            return_actions (bool, optional): Если True, возвращает действия, предпринятые агентами. По умолчанию False.

        Returns:
            Optional[List[dict]]: Список действий, предпринятых агентами с течением времени, если return_actions имеет значение True.
            Список имеет следующий формат: [{agent_name: [action_1, action_2, ...]}, {agent_name_2: [action_1, action_2, ...]}, ...]
        """
        agents_actions_over_time: list = []
        for i in range(steps):
            logger.info(
                f"[{self.name}] Запуск шага {i+1} из {steps} моделирования мира."
            )

            if TinyWorld.communication_display:
                self._display_communication(
                    cur_step=i + 1,
                    total_steps=steps,
                    kind="step",
                    timedelta_per_step=timedelta_per_step,
                )

            agents_actions: dict = self._step(timedelta_per_step=timedelta_per_step)
            agents_actions_over_time.append(agents_actions)

        if return_actions:
            return agents_actions_over_time
        else:
            return None

    @transactional
    def skip(self, steps: int, timedelta_per_step: Optional[timedelta] = None) -> None:
        """
        Пропускает заданное количество шагов в окружении. То есть время должно пройти, но никаких действий не будет предпринято
        агентами или любой другой сущностью в окружении.

        Args:
            steps (int): Количество шагов для пропуска.
            timedelta_per_step (Optional[timedelta], optional): Временной интервал между шагами. По умолчанию None.
        """
        if timedelta_per_step:
            self._advance_datetime(steps * timedelta_per_step)
        else:
            logger.info(
                f"[{self.name}] Не указан timedelta_per_step, поэтому время не было пропущено."
            )

    def run_minutes(self, minutes: int) -> None:
        """
        Запускает окружение на заданное количество минут.

        Args:
            minutes (int): Количество минут для запуска окружения.
        """
        self.run(steps=minutes, timedelta_per_step=timedelta(minutes=1))

    def skip_minutes(self, minutes: int) -> None:
        """
        Пропускает заданное количество минут в окружении.

        Args:
            minutes (int): Количество минут для пропуска.
        """
        self.skip(steps=minutes, timedelta_per_step=timedelta(minutes=1))

    def run_hours(self, hours: int) -> None:
        """
        Запускает окружение на заданное количество часов.

        Args:
            hours (int): Количество часов для запуска окружения.
        """
        self.run(steps=hours, timedelta_per_step=timedelta(hours=1))

    def skip_hours(self, hours: int) -> None:
        """
        Пропускает заданное количество часов в окружении.

        Args:
            hours (int): Количество часов для пропуска.
        """
        self.skip(steps=hours, timedelta_per_step=timedelta(hours=1))

    def run_days(self, days: int) -> None:
        """
        Запускает окружение на заданное количество дней.

        Args:
            days (int): Количество дней для запуска окружения.
        """
        self.run(steps=days, timedelta_per_step=timedelta(days=1))

    def skip_days(self, days: int) -> None:
        """
        Пропускает заданное количество дней в окружении.

        Args:
            days (int): Количество дней для пропуска.
        """
        self.skip(steps=days, timedelta_per_step=timedelta(days=1))

    def run_weeks(self, weeks: int) -> None:
        """
        Запускает окружение на заданное количество недель.

        Args:
            weeks (int): Количество недель для запуска окружения.
        """
        self.run(steps=weeks, timedelta_per_step=timedelta(weeks=1))

    def skip_weeks(self, weeks: int) -> None:
        """
        Пропускает заданное количество недель в окружении.

        Args:
            weeks (int): Количество недель для пропуска.
        """
        self.skip(steps=weeks, timedelta_per_step=timedelta(weeks=1))

    def run_months(self, months: int) -> None:
        """
        Запускает окружение на заданное количество месяцев.

        Args:
            months (int): Количество месяцев для запуска окружения.
        """
        self.run(steps=months, timedelta_per_step=timedelta(weeks=4))

    def skip_months(self, months: int) -> None:
        """
        Пропускает заданное количество месяцев в окружении.

        Args:
            months (int): Количество месяцев для пропуска.
        """
        self.skip(steps=months, timedelta_per_step=timedelta(weeks=4))

    def run_years(self, years: int) -> None:
        """
        Запускает окружение на заданное количество лет.

        Args:
            years (int): Количество лет для запуска окружения.
        """
        self.run(steps=years, timedelta_per_step=timedelta(days=365))

    def skip_years(self, years: int) -> None:
        """
        Пропускает заданное количество лет в окружении.

        Args:
            years (int): Количество лет для пропуска.
        """
        self.skip(steps=years, timedelta_per_step=timedelta(days=365))

    #######################################################################
    # Методы управления агентами
    #######################################################################
    def add_agents(self, agents: List[TinyPerson]) -> "TinyWorld":
        """
        Добавляет список агентов в окружение.

        Args:
            agents (List[TinyPerson]): Список агентов для добавления в окружение.

        Returns:
            TinyWorld: self для связывания.
        """
        for agent in agents:
            self.add_agent(agent)

        return self  # для связывания

    def add_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Добавляет агента в окружение. У агента должно быть уникальное имя в пределах окружения.

        Args:
            agent (TinyPerson): Агент для добавления в окружение.

        Raises:
            ValueError: Если имя агента не является уникальным в пределах окружения.

        Returns:
            TinyWorld: self для связывания.
        """

        # проверить, нет ли агента уже в окружении
        if agent not in self.agents:
            logger.debug(f"Добавление агента {agent.name} в окружение.")

            # Имена агентов должны быть уникальными в окружении.
            # Проверить, есть ли уже имя агента.
            if agent.name not in self.name_to_agent:
                agent.environment = self
                self.agents.append(agent)
                self.name_to_agent[agent.name] = agent
            else:
                raise ValueError(
                    f"Имена агентов должны быть уникальными, но '{agent.name}' уже есть в окружении."
                )
        else:
            logger.warn(f"Агент {agent.name} уже есть в окружении.")

        return self  # для связывания

    def remove_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Удаляет агента из окружения.

        Args:
            agent (TinyPerson): Агент для удаления из окружения.

        Returns:
            TinyWorld: self для связывания.
        """
        logger.debug(f"Удаление агента {agent.name} из окружения.")
        self.agents.remove(agent)
        del self.name_to_agent[agent.name]

        return self  # для связывания

    def remove_all_agents(self) -> "TinyWorld":
        """
        Удаляет всех агентов из окружения.

        Returns:
            TinyWorld: self для связывания.
        """
        logger.debug("Удаление всех агентов из окружения.")
        self.agents = []
        self.name_to_agent = {}

        return self  # для связывания

    def get_agent_by_name(self, name: str) -> Optional[TinyPerson]:
        """
        Возвращает агента с указанным именем. Если в окружении нет агента с таким именем,
        возвращает None.

        Args:
            name (str): Имя агента для возврата.

        Returns:
            Optional[TinyPerson]: Агент с указанным именем или None.
        """
        if name in self.name_to_agent:
            return self.name_to_agent[name]
        else:
            return None

    #######################################################################
    # Обработчики действий
    #
    # Конкретные действия, выполняемые агентами, обрабатываются окружением,
    # потому что они имеют последствия, выходящие за рамки самого агента.
    #######################################################################
    @transactional
    def _handle_actions(self, source: TinyPerson, actions: list) -> None:
        """
        Обрабатывает действия, выполняемые агентами.

        Args:
            source (TinyPerson): Агент, выполнивший действия.
            actions (list): Список действий, выполняемых агентами. Каждое действие на самом деле является
              JSON-спецификацией.
        """
        for action in actions:
            action_type: str = action["type"]  # это единственное обязательное поле
            content: Optional[str] = action.get("content")
            target: Optional[str] = action.get("target")

            logger.debug(
                f"[{self.name}] Обработка действия {action_type} от агента {name_or_empty(source)}. Содержимое: {content}, цель: {target}."
            )

            # только некоторые действия требуют вмешательства окружения
            if action_type == "REACH_OUT":
                self._handle_reach_out(source, content, target)
            elif action_type == "TALK":
                self._handle_talk(source, content, target)

    @transactional
    def _handle_reach_out(
        self, source_agent: TinyPerson, content: str, target: str
    ) -> None:
        """
        Обрабатывает действие REACH_OUT. Эта реализация по умолчанию всегда позволяет REACH_OUT выполнить успешно.
        Подклассы могут переопределять этот метод для реализации различных политик.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие REACH_OUT.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """

        # Эта реализация по умолчанию всегда позволяет REACH_OUT выполнить успешно.
        target_agent: Optional[TinyPerson] = self.get_agent_by_name(target)

        if target_agent:
            source_agent.make_agent_accessible(target_agent)
            target_agent.make_agent_accessible(source_agent)

            source_agent.socialize(
                f"{name_or_empty(target_agent)} был успешно достигнут и теперь доступен для взаимодействия.",
                source=self,
            )
            target_agent.socialize(
                f"{name_or_empty(source_agent)} связался с вами и теперь доступен для взаимодействия.",
                source=self,
            )
        else:
            logger.warning(
                f"Агент {target} не найден в окружении при попытке REACH_OUT от агента {source_agent.name}."
            )

    @transactional
    def _handle_talk(self, source_agent: TinyPerson, content: str, target: str) -> None:
        """
        Обрабатывает действие TALK, доставляя указанное содержимое указанной цели.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие TALK.
            content (str): Содержимое сообщения.
            target (str, optional): Цель сообщения.
        """
        target_agent: Optional[TinyPerson] = self.get_agent_by_name(target)

        logger.debug(
            f"[{self.name}] Доставка сообщения от {name_or_empty(source_agent)} к {name_or_empty(target_agent)}."
        )

        if target_agent is not None:
            target_agent.listen(content, source=source_agent)
        elif self.broadcast_if_no_target:
            self.broadcast(content, source=source_agent)

    #######################################################################
    # Методы взаимодействия
    #######################################################################
    @transactional
    def broadcast(self, speech: str, source: AgentOrWorld = None) -> None:
        """
        Доставляет речь всем агентам в окружении.

        Args:
            speech (str): Содержимое сообщения.
            source (AgentOrWorld, optional): Агент или окружение, выполнившее сообщение. По умолчанию None.
        """
        logger.debug(f"[{self.name}] Широковещательное сообщение: '{speech}'.")

        for agent in self.agents:
            # не доставлять сообщение источнику
            if agent != source:
                agent.listen(speech, source=source)

    @transactional
    def broadcast_thought(self, thought: str, source: AgentOrWorld = None) -> None:
        """
        Широковещательное распространение мысли всем агентам в окружении.

        Args:
            thought (str): Содержимое мысли.
        """
        logger.debug(f"[{self.name}] Широковещательная мысль: '{thought}'.")

        for agent in self.agents:
            agent.think(thought)

    @transactional
    def broadcast_internal_goal(self, internal_goal: str) -> None:
        """
        Широковещательное распространение внутренней цели всем агентам в окружении.

        Args:
            internal_goal (str): Содержимое внутренней цели.
        """
        logger.debug(f"[{self.name}] Широковещательная внутренняя цель: '{internal_goal}'.")

        for agent in self.agents:
            agent.internalize_goal(internal_goal)

    @transactional
    def broadcast_context_change(self, context: list) -> None:
        """
        Широковещательное распространение изменения контекста всем агентам в окружении.

        Args:
            context (list): Содержимое изменения контекста.
        """
        logger.debug(f"[{self.name}] Широковещательное изменение контекста: '{context}'.")

        for agent in self.agents:
            agent.change_context(context)

    def make_everyone_accessible(self) -> None:
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
        self, cur_step: int, total_steps: int, kind: str, timedelta_per_step: Optional[timedelta] = None
    ) -> None:
        """
        Отображает текущую коммуникацию и сохраняет ее в буфере для дальнейшего использования.
        """
        if kind == "step":
            rendering: str = self._pretty_step(
                cur_step=cur_step,
                total_steps=total_steps,
                timedelta_per_step=timedelta_per_step,
            )
        else:
            raise ValueError(f"Неизвестный вид коммуникации: {kind}")

        self._push_and_display_latest_communication({"content": rendering, "kind": kind})

    def _push_and_display_latest_communication(self, rendering: dict) -> None:
        """
        Помещает последние коммуникации в буфер агента.
        """
        self._displayed_communications_buffer.append(rendering)
        self._display(rendering)

    def pop_and_display_latest_communications(self) -> list:
        """
        Извлекает последние коммуникации и отображает их.
        """
        communications: list = self._displayed_communications_buffer
        self._displayed_communications_buffer = []

        for communication in communications:
            self._display(communication)

        return communications

    def _display(self, communication: dict | str) -> None:
        """Отображает коммуникацию"""
        # unpack the rendering to find more info
        if isinstance(communication, dict):
            content: str = communication["content"]
            kind: str = communication["kind"]
        else:
            content: str = communication
            kind: Optional[str] = None

        # render as appropriate
        if kind == "step":
            self.console.rule(content)
        else:
            self.console.print(content)

    def clear_communications_buffer(self) -> None:
        """
        Очищает буфер коммуникаций.
        """
        self._displayed_communications_buffer = []

    def __repr__(self) -> str:
        return f"TinyWorld(name='{self.name}')"

    def _pretty_step(
        self, cur_step: int, total_steps: int, timedelta_per_step: Optional[timedelta] = None
    ) -> str:
        """Форматирует шаг симуляции"""
        rendering: str = f"{self.name} шаг {cur_step} из {total_steps}"
        if timedelta_per_step is not None:
            rendering += f" ({pretty_datetime(self.current_datetime)})"

        return rendering

    def pp_current_interactions(self, simplified: bool = True, skip_system: bool = True) -> None:
        """
        Красиво печатает текущие сообщения от агентов в этом окружении.
        """
        print(
            self.pretty_current_interactions(simplified=simplified, skip_system=skip_system)
        )

    def pretty_current_interactions(
        self,
        simplified: bool = True,
        skip_system: bool = True,
        max_content_length: int = default["max_content_display_length"],
        first_n: Optional[int] = None,
        last_n: Optional[int] = None,
        include_omission_info: bool = True,
    ) -> str:
        """
        Возвращает красивую, удобочитаемую строку с текущими сообщениями агентов в этом окружении.
        """
        agent_contents: list = []

        for agent in self.agents:
            agent_content: str = (
                f"#### Взаимодействия с точки зрения агента {agent.name}:\\n"
            )
            agent_content += f"**НАЧАЛО ИСТОРИИ АГЕНТА {agent.name}.**\\n "
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
            agent_content += f"**КОНЕЦ ИСТОРИИ АГЕНТА {agent.name}.**\\n\\n"

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

        # удалить logger и другие поля
        del to_copy["console"]
        del to_copy["agents"]
        del to_copy["name_to_agent"]
        del to_copy["current_datetime"]

        state: dict = copy.deepcopy(to_copy)

        # агенты кодируются отдельно
        state["agents"] = [agent.encode_complete_state() for agent in self.agents]

        # datetime также должен быть закодирован отдельно
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
        # восстановить агентов на месте
        #################################
        self.remove_all_agents()
        for agent_state in state["agents"]:
            try:
                try:
                    agent: TinyPerson = TinyPerson.get_agent_by_name(agent_state["name"])
                except Exception as ex:
                    raise ValueError(
                        f"Не удалось найти агента {agent_state['name']} для окружения {self.name}."
                    ) from ex

                agent.decode_complete_state(agent_state)
                self.add_agent(agent)

            except Exception as ex:
                raise ValueError(
                    f"Не удалось декодировать агента {agent_state['name']} для окружения {self.name}."
                ) from ex

        # удалить состояния агентов, чтобы обновить остальную часть окружения
        del state["agents"]

        # восстановить datetime
        state["current_datetime"] = datetime.datetime.fromisoformat(
            state["current_datetime"]
        )

        # восстановить другие поля
        self.__dict__.update(state)

        return self

    @staticmethod
    def add_environment(environment: "TinyWorld") -> None:
        """
        Добавляет окружение в список всех окружений. Имена окружений должны быть уникальными,
        поэтому, если окружение с таким же именем уже существует, возникает ошибка.
        """
        if environment.name in TinyWorld.all_environments:
            raise ValueError(
                f"Имена окружений должны быть уникальными, но '{environment.name}' уже определено."
            )
        else:
            TinyWorld.all_environments[environment.name] = environment

    @staticmethod
    def set_simulation_for_free_environments(simulation) -> None:
        """
        Устанавливает моделирование, если оно равно None. Это позволяет захватывать свободные окружения конкретными областями моделирования
        при желании.
        """
        for environment in TinyWorld.all_environments.values():
            if environment.simulation_id is None:
                simulation.add_environment(environment)

    @staticmethod
    def get_environment_by_name(name: str) -> Optional["TinyWorld"]:
        """
        Возвращает окружение с указанным именем. Если окружение с таким именем не существует,
        возвращает None.

        Args:
            name (str): Имя окружения для возврата.

        Returns:
            Optional[TinyWorld]: Окружение с указанным именем или None.
        """
        if name in TinyWorld.all_environments:
            return TinyWorld.all_environments[name]
        else:
            return None

    @staticmethod
    def clear_environments() -> None:
        """
        Очищает список всех окружений.
        """
        TinyWorld.all_environments = {}


class TinySocialNetwork(TinyWorld):
    """Реализация класса для социальных сетей"""

    def __init__(self, name: str, broadcast_if_no_target: bool = True) -> None:
        """
        Создает новую среду TinySocialNetwork.

        Args:
            name (str): Имя окружения.
            broadcast_if_no_target (bool): Если True, транслировать действия через доступные отношения агента
              если цель действия не найдена.
        """

        super().__init__(name, broadcast_if_no_target=broadcast_if_no_target)

        self.relations: dict = {}

    @transactional
    def add_relation(
        self, agent_1: TinyPerson, agent_2: TinyPerson, name: str = "default"
    ) -> "TinySocialNetwork":
        """
        Добавляет отношение между двумя агентами.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент.
            name (str): Имя отношения.

        Returns:
            TinySocialNetwork: self для связывания.
        """

        logger.debug(f"Добавление отношения {name} между {agent_1.name} и {agent_2.name}.")

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
    def _update_agents_contexts(self) -> None:
        """
        Обновляет наблюдения агентов на основе текущего состояния мира.
        """

        # сначала очистить всю доступность
        for agent in self.agents:
            agent.make_all_agents_inaccessible()

        # теперь обновить доступность на основе отношений
        for relation_name, relation in self.relations.items():
            logger.debug(f"Обновление наблюдений агентов для отношения {relation_name}.")
            for agent_1, agent_2 in relation:
                agent_1.make_agent_accessible(agent_2)
                agent_2.make_agent_accessible(agent_1)

    @transactional
    def _step(self) -> None:
        """Выполняет шаг в социальной сети"""
        self._update_agents_contexts()

        # вызвать super
        super()._step()

    @transactional
    def _handle_reach_out(
        self, source_agent: TinyPerson, content: str, target: str
    ) -> None:
        """
        Обрабатывает действие REACH_OUT. Эта реализация социальной сети позволяет