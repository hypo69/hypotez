### **Анализ кода модуля `tiny_world.py`**

=========================================================================================

Модуль определяет класс `TinyWorld`, представляющий собой базовый класс для моделирования окружений в контексте TinyTroupe. Он предоставляет функциональность для управления агентами, временем, событиями и взаимодействиями между агентами в смоделированном мире.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура класса и методов.
    - Использование логирования для отладки и мониторинга.
    - Реализация основных методов управления окружением и агентами.
- **Минусы**:
    - Некоторые docstring написаны на английском языке.
    - Не все переменные аннотированы типами.
    - Не хватает более подробных комментариев в некоторых местах.

**Рекомендации по улучшению**:

1.  **Документация**:
    *   Перевести все docstring на русский язык, соблюдая формат, указанный в инструкции.
    *   Добавить примеры использования для основных методов и классов.

2.  **Аннотации типов**:
    *   Убедиться, что все переменные и параметры функций аннотированы типами.

3.  **Комментарии**:
    *   Добавить больше комментариев для пояснения сложных участков кода.
    *   Улучшить описания в комментариях, избегая расплывчатых формулировок. Использовать более точные термины.

4.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках обработки исключений.
    *   Логировать ошибки с использованием `logger.error`, передавая исключение в качестве второго аргумента и `exc_info=True`.

5.  **Использование `Union`**:
    *   Заменить `Union[]` на `|` для аннотаций типов.

**Оптимизированный код**:

```python
"""
Модуль для создания и управления виртуальным миром TinyWorld
=============================================================

Модуль содержит класс :class:`TinyWorld`, который представляет собой виртуальное окружение,
в котором могут взаимодействовать агенты. Он предоставляет методы для управления временем,
добавления и удаления агентов, обработки действий и трансляции сообщений.

Пример использования
----------------------

>>> world = TinyWorld(name='MyWorld')
>>> agent = TinyPerson(name='Alice')
>>> world.add_agent(agent)
>>> world.run_minutes(10)
"""

from tinytroupe.environment import logger, default  # Импорт логгера и настроек по умолчанию

import copy  # Импорт модуля для создания копий объектов
from datetime import datetime, timedelta  # Импорт классов для работы с датой и временем
import textwrap  # Импорт модуля для форматирования текста

from tinytroupe.agent import *  # Импорт всех классов из модуля agent
from tinytroupe.utils import name_or_empty, pretty_datetime  # Импорт утилитных функций
import tinytroupe.control as control  # Импорт модуля control
from tinytroupe.control import transactional  # Импорт декоратора transactional
from tinytroupe import utils  # Импорт модуля utils

from rich.console import Console  # Импорт класса Console из библиотеки rich

from typing import Any, TypeVar, Union  # Импорт классов для аннотаций типов
AgentOrWorld = Union["TinyPerson", "TinyWorld"]  # Определение типа для агента или мира


class TinyWorld:
    """
    Базовый класс для виртуальных окружений.

    Атрибуты:
        all_environments (dict): Словарь всех созданных окружений (имя -> окружение).
        communication_display (bool): Флаг, определяющий, отображать ли сообщения окружения.

    Args:
        name (str): Имя окружения. По умолчанию "A TinyWorld".
        agents (list): Список агентов для добавления в окружение. По умолчанию пустой список.
        initial_datetime (datetime): Начальное время окружения. По умолчанию текущее время.
        interventions (list): Список интервенций для применения на каждом шаге симуляции. По умолчанию пустой список.
        broadcast_if_no_target (bool): Если True, действия транслируются, если цель не найдена. По умолчанию True.
        max_additional_targets_to_display (int): Максимальное количество дополнительных целей для отображения в сообщении.
            Если None, отображаются все цели. По умолчанию 3.

    """

    # Словарь всех созданных окружений.
    all_environments: dict = {}  # name -> environment

    # Определяет, отображать ли коммуникации окружений или нет, для всех окружений.
    communication_display: bool = True

    def __init__(self, name: str = "A TinyWorld", agents: list = [],
                 initial_datetime: datetime = datetime.now(),
                 interventions: list = [],
                 broadcast_if_no_target: bool = True,
                 max_additional_targets_to_display: int = 3) -> None:
        """
        Инициализирует окружение.

        Args:
            name (str): Имя окружения.
            agents (list): Список агентов для добавления в окружение.
            initial_datetime (datetime): Начальное время окружения, или None (т.е., явное время не обязательно).
                По умолчанию текущее время в реальном мире.
            interventions (list): Список интервенций для применения в окружении на каждом шаге симуляции.
            broadcast_if_no_target (bool): Если True, транслировать действия, если цель действия не найдена.
            max_additional_targets_to_display (int): Максимальное количество дополнительных целей для отображения в коммуникации. Если None,
                отображаются все дополнительные цели.
        """

        self.name: str = name  # Имя окружения
        self.current_datetime: datetime = initial_datetime  # Текущее время в окружении
        self.broadcast_if_no_target: bool = broadcast_if_no_target  # Флаг трансляции при отсутствии цели
        self.simulation_id: str | None = None  # Идентификатор симуляции, будет установлен позже
        # будет сброшен позже, если агент используется в рамках определенной области симуляции

        self.agents: list[TinyPerson] = []  # Список агентов в окружении
        self.name_to_agent: dict[str, TinyPerson] = {}  # {agent_name: agent, agent_name_2: agent_2, ...}

        self._interventions: list = interventions  # Список интервенций

        # Буфер коммуникаций, которые были отображены, используется для сохранения этих коммуникаций
        # для последующего использования (например, кэширования)
        self._displayed_communications_buffer: list = []

        # Временный буфер для целей коммуникаций, чтобы упростить отображение
        self._target_display_communications_buffer: list = []
        self._max_additional_targets_to_display: int = max_additional_targets_to_display

        self.console: Console = Console()  # Консоль для вывода

        # Добавляем окружение в список всех окружений
        TinyWorld.add_environment(self)

        self.add_agents(agents)  # Добавляем агентов в окружение

    #######################################################################
    # Методы управления симуляцией
    #######################################################################
    @transactional
    def _step(self, timedelta_per_step: timedelta | None = None) -> dict:
        """
        Выполняет один шаг в окружении. Эта реализация по умолчанию просто вызывает действия
        всех агентов в окружении и обрабатывает результирующие действия. Подклассы могут переопределить
        этот метод для реализации других политик.

        Args:
            timedelta_per_step (timedelta | None): Временной интервал для шага.

        Returns:
            dict: Словарь действий агентов.
        """
        # увеличиваем текущее время, если задан timedelta. Это должно произойти до
        # любых других обновлений симуляции, чтобы убедиться, что агенты действуют
        # в правильное время, особенно если выполняется только один шаг.
        self._advance_datetime(timedelta_per_step)

        # применяем интервенции
        for intervention in self._interventions:
            should_apply_intervention: bool = intervention.check_precondition()
            if should_apply_intervention:
                if TinyWorld.communication_display:
                    self._display_intervention_communication(intervention)
                intervention.apply_effect()

                logger.debug(f"[{self.name}] Intervention \'{intervention.name}\' was applied.")

        # агенты могут действовать
        agents_actions: dict = {}
        for agent in self.agents:
            logger.debug(f"[{self.name}] Agent {name_or_empty(agent)} is acting.")
            actions: list = agent.act(return_actions=True)
            agents_actions[agent.name] = actions

            self._handle_actions(agent, agent.pop_latest_actions())

        return agents_actions

    def _advance_datetime(self, timedelta: timedelta | None) -> None:
        """
        Увеличивает текущее время окружения на указанный timedelta.

        Args:
            timedelta (timedelta): Значение, на которое нужно увеличить текущее время.
        """
        if timedelta is not None:
            self.current_datetime += timedelta
        else:
            logger.info(f"[{self.name}] No timedelta provided, so the datetime was not advanced.")

    @transactional
    def run(self, steps: int, timedelta_per_step: timedelta | None = None, return_actions: bool = False) -> list | None:
        """
        Запускает окружение на заданное количество шагов.

        Args:
            steps (int): Количество шагов для запуска окружения.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию None.
            return_actions (bool, optional): Если True, возвращает действия, предпринятые агентами. По умолчанию False.

        Returns:
            list: Список действий, предпринятых агентами во времени, если return_actions имеет значение True.
                  Список имеет следующий формат:
                  [{agent_name: [action_1, action_2, ...]}, {agent_name_2: [action_1, action_2, ...]}, ...]
        """
        agents_actions_over_time: list = []
        for i in range(steps):
            logger.info(f"[{self.name}] Running world simulation step {i + 1} of {steps}.")

            if TinyWorld.communication_display:
                self._display_step_communication(cur_step=i + 1, total_steps=steps,
                                                  timedelta_per_step=timedelta_per_step)

            agents_actions: dict = self._step(timedelta_per_step=timedelta_per_step)
            agents_actions_over_time.append(agents_actions)

        if return_actions:
            return agents_actions_over_time

    @transactional
    def skip(self, steps: int, timedelta_per_step: timedelta | None = None) -> None:
        """
        Пропускает заданное количество шагов в окружении. То есть время должно пройти, но никакие действия не будут предприняты
        агентами или каким-либо другим лицом в окружении.

        Args:
            steps (int): Количество шагов для пропуска.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию None.
        """
        self._advance_datetime(steps * timedelta_per_step)

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
    def add_agents(self, agents: list) -> "TinyWorld":
        """
        Добавляет список агентов в окружение.

        Args:
            agents (list): Список агентов для добавления в окружение.
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
            ValueError: Если имя агента не уникально в пределах окружения.
        """

        # проверяем, что агента еще нет в окружении
        if agent not in self.agents:
            logger.debug(f"Adding agent {agent.name} to the environment.")

            # Имена агентов должны быть уникальными в окружении.
            # Проверяем, что имени агента еще нет.
            if agent.name not in self.name_to_agent:
                agent.environment: TinyWorld = self
                self.agents.append(agent)
                self.name_to_agent[agent.name] = agent
            else:
                raise ValueError(f"Agent names must be unique, but \'{agent.name}\' is already in the environment.")
        else:
            logger.warn(f"Agent {agent.name} is already in the environment.")

        return self  # для связывания

    def remove_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Удаляет агента из окружения.

        Args:
            agent (TinyPerson): Агент для удаления из окружения.
        """
        logger.debug(f"Removing agent {agent.name} from the environment.")
        self.agents.remove(agent)
        del self.name_to_agent[agent.name]

        return self  # для связывания

    def remove_all_agents(self) -> "TinyWorld":
        """
        Удаляет всех агентов из окружения.
        """
        logger.debug(f"Removing all agents from the environment.")
        self.agents: list = []
        self.name_to_agent: dict = {}

        return self  # для связывания

    def get_agent_by_name(self, name: str) -> TinyPerson | None:
        """
        Возвращает агента с указанным именем. Если агента с таким именем не существует в окружении,
        возвращает None.

        Args:
            name (str): Имя агента для возврата.

        Returns:
            TinyPerson: Агент с указанным именем.
        """
        if name in self.name_to_agent:
            return self.name_to_agent[name]
        else:
            return None

    #######################################################################
    # Методы управления интервенциями
    #######################################################################

    def add_intervention(self, intervention: Any) -> None:
        """
        Добавляет интервенцию в окружение.

        Args:
            intervention: Интервенция для добавления в окружение.
        """
        self._interventions.append(intervention)

    #######################################################################
    # Обработчики действий
    #
    # Определенные действия, выпущенные агентами, обрабатываются окружением,
    # потому что они имеют последствия за пределами самого агента.
    #######################################################################
    @transactional
    def _handle_actions(self, source: TinyPerson, actions: list) -> None:
        """
        Обрабатывает действия, выпущенные агентами.

        Args:
            source (TinyPerson): Агент, выпустивший действия.
            actions (list): Список действий, выпущенных агентами. Каждое действие фактически является
              JSON-спецификацией.

        """
        for action in actions:
            action_type: str = action["type"]  # это единственное обязательное поле
            content: str | None = action["content"] if "content" in action else None
            target: str | None = action["target"] if "target" in action else None

            logger.debug(
                f"[{self.name}] Handling action {action_type} from agent {name_or_empty(source)}. Content: {content}, target: {target}.")

            # только некоторые действия требуют вмешательства окружения
            if action_type == "REACH_OUT":
                self._handle_reach_out(source, content, target)
            elif action_type == "TALK":
                self._handle_talk(source, content, target)

    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str) -> None:
        """
        Обрабатывает действие REACH_OUT. Эта реализация по умолчанию всегда позволяет REACH_OUT пройти успешно.
        Подклассы могут переопределить этот метод для реализации других политик.

        Args:
            source_agent (TinyPerson): Агент, выпустивший действие REACH_OUT.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """

        # Эта реализация по умолчанию всегда позволяет REACH_OUT пройти успешно.
        target_agent: TinyPerson | None = self.get_agent_by_name(target)

        if target_agent is not None:
            source_agent.make_agent_accessible(target_agent)
            target_agent.make_agent_accessible(source_agent)

            source_agent.socialize(f"{name_or_empty(target_agent)} was successfully reached out, and is now available for interaction.",
                                  source=self)
            target_agent.socialize(f"{name_or_empty(source_agent)} reached out to you, and is now available for interaction.",
                                  source=self)

        else:
            logger.debug(f"[{self.name}] REACH_OUT action failed: target agent \'{target}\' not found.")

    @transactional
    def _handle_talk(self, source_agent: TinyPerson, content: str, target: str) -> None:
        """
        Обрабатывает действие TALK, доставляя указанное содержимое указанной цели.

        Args:
            source_agent (TinyPerson): Агент, выпустивший действие TALK.
            content (str): Содержимое сообщения.
            target (str, optional): Цель сообщения.
        """
        target_agent: TinyPerson | None = self.get_agent_by_name(target)

        logger.debug(
            f"[{self.name}] Delivering message from {name_or_empty(source_agent)} to {name_or_empty(target_agent)}.")

        if target_agent is not None:
            target_agent.listen(content, source=source_agent)
        elif self.broadcast_if_no_target:
            self.broadcast(content, source=source_agent)

    #######################################################################
    # Методы взаимодействия
    #######################################################################
    @transactional
    def broadcast(self, speech: str, source: AgentOrWorld | None = None) -> None:
        """
        Доставляет речь всем агентам в окружении.

        Args:
            speech (str): Содержимое сообщения.
            source (AgentOrWorld, optional): Агент или окружение, выпустившее сообщение. По умолчанию None.
        """
        logger.debug(f"[{self.name}] Broadcasting message: \'{speech}\'.")

        for agent in self.agents:
            # не доставляем сообщение источнику
            if agent != source:
                agent.listen(speech, source=source)

    @transactional
    def broadcast_thought(self, thought: str, source: AgentOrWorld | None = None) -> None:
        """
        Транслирует мысль всем агентам в окружении.

        Args:
            thought (str): Содержимое мысли.
        """
        logger.debug(f"[{self.name}] Broadcasting thought: \'{thought}\'.")

        for agent in self.agents:
            agent.think(thought)

    @transactional
    def broadcast_internal_goal(self, internal_goal: str) -> None:
        """
        Транслирует внутреннюю цель всем агентам в окружении.

        Args:
            internal_goal (str): Содержимое внутренней цели.
        """
        logger.debug(f"[{self.name}] Broadcasting internal goal: \'{internal_goal}\'.")

        for agent in self.agents:
            agent.internalize_goal(internal_goal)

    @transactional
    def broadcast_context_change(self, context: list) -> None:
        """
        Транслирует изменение контекста всем агентам в окружении.

        Args:
            context (list): Содержимое изменения контекста.
        """
        logger.debug(f"[{self.name}] Broadcasting context change: \'{context}\'.")

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

    # TODO better names for these "display" methods
    def _display_step_communication(self, cur_step: int, total_steps: int, timedelta_per_step: timedelta | None = None) -> None:
        """
        Отображает текущую коммуникацию и сохраняет ее в буфере для последующего использования.
        """
        rendering: str = self._pretty_step(cur_step=cur_step, total_steps=total_steps,
                                            timedelta_per_step=timedelta_per_step)

        self._push_and_display_latest_communication(
            {"kind": 'step', "rendering": rendering, "content": None, "source": None, "target": None})

    def _display_intervention_communication(self, intervention: Any) -> None:
        """
        Отображает текущую коммуникацию интервенции и сохраняет ее в буфере для последующего использования.
        """
        rendering: str = self._pretty_intervention(intervention)
        self._push_and_display_latest_communication(
            {"kind": 'intervention', "rendering": rendering, "content": None, "source": None, "target": None})

    def _push_and_display_latest_communication(self, communication: dict) -> None:
        """
        Помещает последние коммуникации в буфер агента.
        """
        #
        # проверяем, что коммуникация просто повторяет последнюю для другой цели
        #
        if len(self._displayed_communications_buffer) > 0:
            # получаем значения из последней коммуникации
            last_communication: dict = self._displayed_communications_buffer[-1]
            last_kind: str | None = last_communication["kind"]
            last_target: str | None = last_communication["target"]
            last_source: str | None = last_communication["source"]
            if last_kind == 'action':
                last_content: str | None = last_communication["content"]["action"]["content"]
                last_type: str | None = last_communication["content"]["action"]["type"]
            elif last_kind == 'stimulus':
                last_content: str | None = last_communication["content"]["stimulus"]["content"]
                last_type: str | None = last_communication["content"]["stimulus"]["type"]
            elif last_kind == 'stimuli':
                last_stimulus: dict = last_communication["content"]["stimuli"][0]
                last_content: str | None = last_stimulus["content"]
                last_type: str | None = last_stimulus["type"]
            else:
                last_content: str | None = None
                last_type: str | None = None

            # получаем значения из текущей коммуникации
            current_kind: str | None = communication["kind"]
            current_target: str | None = communication["target"]
            current_source: str | None = communication["source"]
            if current_kind == 'action':
                current_content: str | None = communication["content"]["action"]["content"]
                current_type: str | None = communication["content"]["action"]["type"]
            elif current_kind == 'stimulus':
                current_content: str | None = communication["content"]["stimulus"]["content"]
                current_type: str | None = communication["content"]["stimulus"]["type"]
            elif current_kind == 'stimuli':
                current_stimulus: dict = communication["content"]["stimuli"][0]
                current_content: str | None = current_stimulus["content"]
                current_type: str | None = current_stimulus["type"]
            else:
                current_content: str | None = None
                current_type: str | None = None

            # если мы повторяем последнюю коммуникацию, давайте упростим рендеринг
            if (last_source == current_source) and (last_type == current_type) and (last_kind == current_kind) and \
                    (last_content is not None) and (last_content == current_content) and \
                    (current_target is not None):

                self._target_display_communications_buffer.append(current_target)

                rich_style: str = utils.RichTextStyle.get_style_for(last_kind, last_type)

                # выводим дополнительную цель ограниченное количество раз, если установлено максимальное значение, или
                # всегда, если максимальное значение не установлено.
                if (self._max_additional_targets_to_display is None) or \
                        len(self._target_display_communications_buffer) < self._max_additional_targets_to_display:
                    communication["rendering"] = " " * len(
                        last_source) + f"[{rich_style}]       + --> [underline]{current_target}[/][/]"

                elif len(self._target_display_communications_buffer) == self._max_additional_targets_to_display:
                    communication["rendering"] = " " * len(
                        last_source) + f"[{rich_style}]       + --> ...others...[/]"

                else:  # больше ничего не выводим
                    communication["rendering"] = None

            else:
                # нет повторения, поэтому просто отображаем коммуникацию и сбрасываем буфер целей
                self._target_display_communications_buffer: list = []  # сбрасывает

        else:
            # нет повторения, поэтому просто отображаем коммуникацию и сбрасываем буфер целей
            self._target_display_communications_buffer: list = []  # сбрасывает

        self._displayed_communications_buffer.append(communication)
        self._display(communication)

    def pop_and_display_latest_communications(self) -> list:
        """
        Извлекает последние коммуникации и отображает их.
        """
        communications: list = self._displayed_communications_buffer
        self._displayed_communications_buffer: list = []

        for communication in communications:
            self._display(communication)

        return communications

    def _display(self, communication: dict) -> None:
        # распаковываем рендеринг, чтобы найти больше информации
        content: str | None = communication["rendering"]
        kind: str | None = communication["kind"]

        if content is not None:
            # рендерим соответствующим образом
            if kind == 'step':
                self.console.rule(content)
            else:
                self.console.print(content)

    def clear_communications_buffer(self) -> None:
        """
        Очищает буфер коммуникаций.
        """
        self._displayed_communications_buffer: list = []

    def __repr__(self) -> str:
        return f"TinyWorld(name=\'{self.name}\')"

    def _pretty_step(self, cur_step: int, total_steps: int, timedelta_per_step: timedelta | None = None) -> str:
        rendering: str = f"{self.name} step {cur_step} of {total_steps}"
        if timedelta_per_step is not None:
            rendering += f" ({pretty_datetime(self.current_datetime)})"

        return rendering

    def _pretty_intervention(self, intervention: Any) -> str:
        indent: str = "          > "
        justification: str = textwrap.fill(
            intervention.precondition_justification(),
            width=TinyPerson.PP_TEXT_WIDTH,
            initial_indent=indent,
            subsequent_indent=indent,
        )

        rich_style: str = utils.RichTextStyle.get_style_for("intervention")
        rendering: str = f"[{rich_style}] :zap: [bold] <<{intervention.name}>> Triggered, effects are being applied...[/] \\n" + \
                         f"[italic]{justification}[/][/]"
        # TODO add details about why the intervention was applied

        return rendering

    def pp_current_interactions(self, simplified: bool = True, skip_system: bool = True) -> None:
        """
        Выводит в удобочитаемом формате текущие сообщения от агентов в этом окружении.
        """
        print(self.pretty_current_interactions(simplified=simplified, skip_system=skip_system))

    def pretty_current_interactions(self, simplified: bool = True, skip_system: bool = True,
                                   max_content_length: int = default["max_content_display_length"], first_n: int | None = None,
                                   last_n: int | None = None, include_omission_info: bool = True) -> str:
        """
        Возвращает красивую, удобочитаемую строку с текущими сообщениями агентов в этом окружении.
        """
        agent_contents: list = []

        for agent in self.agents:
            agent_content: str = f"#### Interactions from the point of view of {agent.name} agent:\\n"
            agent_content += f"**BEGIN AGENT {agent.name} HISTORY.**\\n "
            agent_content += agent.pretty_current_interactions(simplified=simplified, skip_system=skip_system,
                                                                max_content_length=max_content_length, first_n=first_n,
                                                                last_n=last_n,
                                                                include_omission_info=include_omission_info) + "\\n"
            agent_content += f"**FINISHED AGENT {agent.name} HISTORY.**\\n\\n"
            agent_contents.append(agent_content)

        return "\\n".join(agent_contents)

    #######################################################################
    # IO
    #######################################################################

    def encode_complete_state(self) -> dict:
        """
        Кодирует полное состояние среды в словарь.

        Returns:
            dict: словарь, кодирующий полное состояние среды.
        """
        to_copy: dict = copy.copy(self.__dict__)

        # удалите логгер и другие поля
        del to_copy['console']
        del to_copy['agents']