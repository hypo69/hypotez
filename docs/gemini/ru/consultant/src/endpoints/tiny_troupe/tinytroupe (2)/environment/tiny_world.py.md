### **Анализ кода модуля `tiny_world.py`**

=========================================================================================

Модуль содержит класс `TinyWorld`, представляющий собой базовый класс для создания виртуальных сред, в которых могут взаимодействовать агенты. Класс управляет агентами, временем, событиями и коммуникациями между агентами.

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структурированность класса `TinyWorld`.
  - Наличие документации для большинства методов.
  - Использование логирования для отслеживания работы среды.
  - Реализация методов для управления временем и агентами.
- **Минусы**:
  - Отсутствие документации модуля.
  - Использование `Union` вместо `|` для аннотаций типов.
  - Не все методы имеют подробные docstring.
  - Не везде используется `logger.error` с передачей исключения `ex`.
  - Встречаются смешанные стили форматирования строк (использование `f""` и `""`).

**Рекомендации по улучшению**:

1.  **Добавить документацию модуля**:
    - Добавить заголовок с описанием модуля и примером использования.
    
2.  **Улучшить аннотации типов**:
    - Заменить `Union` на `|` для аннотаций типов.

3.  **Дополнить документацию методов**:
    - Добавить подробные описания для всех методов, включая аргументы, возвращаемые значения и возможные исключения.
    - Перевести docstring на русский язык.

4.  **Улучшить обработку исключений**:
    - Использовать `logger.error` с передачей исключения `ex` и `exc_info=True` в блоках `except`.

5.  **Унифицировать стиль форматирования строк**:
    - Использовать только одинарные кавычки (`'`) для строк.

6.  **Переименовать переменные**:
    - Переименовать переменную `e` в блоках `except` на `ex`.

**Оптимизированный код**:

```python
"""
Модуль для создания и управления виртуальными средами TinyWorld
=================================================================

Модуль содержит класс :class:`TinyWorld`, который представляет собой базовый класс для создания виртуальных сред,
в которых могут взаимодействовать агенты. Класс управляет агентами, временем, событиями и коммуникациями между ними.

Пример использования
----------------------

>>> world = TinyWorld(name='MyWorld')
>>> agent = TinyPerson(name='Agent1')
>>> world.add_agent(agent)
>>> world.run_minutes(10)
"""
from tinytroupe.environment import logger, default

import copy
from datetime import datetime, timedelta
import textwrap

from tinytroupe.agent import *
from tinytroupe.utils import name_or_empty, pretty_datetime
import tinytroupe.control as control
from tinytroupe.control import transactional
from tinytroupe import utils
 
from rich.console import Console

from typing import Any, TypeVar, Optional, Union, List
AgentOrWorld = Union["TinyPerson", "TinyWorld"]

class TinyWorld:
    """
    Базовый класс для виртуальных сред.
    """

    # Словарь всех созданных сред.
    all_environments: dict = {} # name -> environment

    # Флаг отображения коммуникаций в среде.
    communication_display: bool = True

    def __init__(
        self,
        name: str = "A TinyWorld",
        agents: Optional[List[TinyPerson]] = None,
        initial_datetime: datetime = datetime.now(),
        interventions: Optional[List[Any]] = None,
        broadcast_if_no_target: bool = True,
        max_additional_targets_to_display: Optional[int] = 3
    ):
        """
        Инициализирует виртуальную среду.

        Args:
            name (str): Имя среды. По умолчанию "A TinyWorld".
            agents (Optional[List[TinyPerson]]): Список агентов для добавления в среду. По умолчанию пустой список.
            initial_datetime (datetime): Начальное время среды. По умолчанию текущее время.
            interventions (Optional[List[Any]]): Список интервенций для применения в среде на каждом шаге симуляции. По умолчанию пустой список.
            broadcast_if_no_target (bool): Если True, действия транслируются, если цель действия не найдена. По умолчанию True.
            max_additional_targets_to_display (Optional[int]): Максимальное количество дополнительных целей для отображения в коммуникации.
                Если None, отображаются все дополнительные цели. По умолчанию 3.
        """

        self.name: str = name
        self.current_datetime: datetime = initial_datetime
        self.broadcast_if_no_target: bool = broadcast_if_no_target
        self.simulation_id: Optional[str] = None # будет сброшен позже, если агент используется в определенной области симуляции
        
        self.agents: List[TinyPerson] = []
        self.name_to_agent: dict[str, TinyPerson] = {} # {agent_name: agent, agent_name_2: agent_2, ...}

        self._interventions: list = interventions if interventions is not None else []

        # Буфер отображаемых коммуникаций, используемый для сохранения этих коммуникаций
        # для последующего вывода (например, кэширования).
        self._displayed_communications_buffer: list = []

        # Временный буфер для целей коммуникаций для упрощения рендеринга.
        self._target_display_communications_buffer: list = []
        self._max_additional_targets_to_display: Optional[int] = max_additional_targets_to_display

        self.console: Console = Console()

        # Добавить среду в список всех сред
        TinyWorld.add_environment(self)
        
        self.add_agents(agents if agents is not None else [])
        
    #######################################################################
    # Методы управления симуляцией
    #######################################################################
    @transactional
    def _step(self, timedelta_per_step: Optional[timedelta] = None) -> dict:
        """
        Выполняет один шаг в среде. Эта реализация по умолчанию просто вызывает действия всех агентов в среде
        и обрабатывает результирующие действия. Подклассы могут переопределять этот метод для реализации
        других политик.

        Args:
            timedelta_per_step (Optional[timedelta]): Временной интервал для продвижения времени на каждом шаге. По умолчанию None.

        Returns:
            dict: Словарь действий агентов.
        """
        # Увеличить текущее время, если задано значение timedelta. Это должно произойти до
        # любых других обновлений симуляции, чтобы убедиться, что агенты действуют
        # в правильное время, особенно если выполняется только один шаг.
        self._advance_datetime(timedelta_per_step)

        # Применить интервенции
        for intervention in self._interventions:
            should_apply_intervention = intervention.check_precondition()
            if should_apply_intervention:
                if TinyWorld.communication_display:
                    self._display_intervention_communication(intervention)
                intervention.apply_effect()
                
                logger.debug(f'[{self.name}] Intervention \'{intervention.name}\' was applied.')

        # Агенты могут действовать
        agents_actions: dict = {}
        for agent in self.agents:
            logger.debug(f'[{self.name}] Agent {name_or_empty(agent)} is acting.')
            actions = agent.act(return_actions=True)
            agents_actions[agent.name] = actions

            self._handle_actions(agent, agent.pop_latest_actions())
        
        return agents_actions
        

    def _advance_datetime(self, timedelta: Optional[timedelta]):
        """
        Увеличивает текущее время среды на указанное значение timedelta.

        Args:
            timedelta (timedelta): Значение timedelta для увеличения текущего времени.
        """
        if timedelta is not None:
            self.current_datetime += timedelta
        else:
            logger.info(f'[{self.name}] No timedelta provided, so the datetime was not advanced.')

    @transactional
    def run(self, steps: int, timedelta_per_step: Optional[timedelta] = None, return_actions: bool = False) -> Optional[List[dict]]:
        """
        Запускает среду на заданное количество шагов.

        Args:
            steps (int): Количество шагов для запуска среды.
            timedelta_per_step (Optional[timedelta], optional): Временной интервал между шагами. По умолчанию None.
            return_actions (bool, optional): Если True, возвращает действия, предпринятые агентами. По умолчанию False.
        
        Returns:
            Optional[List[dict]]: Список действий, предпринятых агентами с течением времени, если return_actions имеет значение True.
            Список имеет следующий формат:
            [{agent_name: [action_1, action_2, ...]}, {agent_name_2: [action_1, action_2, ...]}, ...]
        """
        agents_actions_over_time: list = []
        for i in range(steps):
            logger.info(f'[{self.name}] Running world simulation step {i+1} of {steps}.')

            if TinyWorld.communication_display:
                self._display_step_communication(cur_step=i+1, total_steps=steps, timedelta_per_step=timedelta_per_step)

            agents_actions = self._step(timedelta_per_step=timedelta_per_step)
            agents_actions_over_time.append(agents_actions)
        
        if return_actions:
            return agents_actions_over_time
    
    @transactional
    def skip(self, steps: int, timedelta_per_step: Optional[timedelta] = None):
        """
        Пропускает заданное количество шагов в среде. Время проходит, но никакие действия не предпринимаются
        агентами или другими сущностями в среде.

        Args:
            steps (int): Количество шагов для пропуска.
            timedelta_per_step (Optional[timedelta], optional): Временной интервал между шагами. По умолчанию None.
        """
        self._advance_datetime(steps * timedelta_per_step)

    def run_minutes(self, minutes: int):
        """
        Запускает среду на заданное количество минут.

        Args:
            minutes (int): Количество минут для запуска среды.
        """
        self.run(steps=minutes, timedelta_per_step=timedelta(minutes=1))
    
    def skip_minutes(self, minutes: int):
        """
        Пропускает заданное количество минут в среде.

        Args:
            minutes (int): Количество минут для пропуска.
        """
        self.skip(steps=minutes, timedelta_per_step=timedelta(minutes=1))
    
    def run_hours(self, hours: int):
        """
        Запускает среду на заданное количество часов.

        Args:
            hours (int): Количество часов для запуска среды.
        """
        self.run(steps=hours, timedelta_per_step=timedelta(hours=1))
    
    def skip_hours(self, hours: int):
        """
        Пропускает заданное количество часов в среде.

        Args:
            hours (int): Количество часов для пропуска.
        """
        self.skip(steps=hours, timedelta_per_step=timedelta(hours=1))
    
    def run_days(self, days: int):
        """
        Запускает среду на заданное количество дней.

        Args:
            days (int): Количество дней для запуска среды.
        """
        self.run(steps=days, timedelta_per_step=timedelta(days=1))
    
    def skip_days(self, days: int):
        """
        Пропускает заданное количество дней в среде.

        Args:
            days (int): Количество дней для пропуска.
        """
        self.skip(steps=days, timedelta_per_step=timedelta(days=1))
    
    def run_weeks(self, weeks: int):
        """
        Запускает среду на заданное количество недель.

        Args:
            weeks (int): Количество недель для запуска среды.
        """
        self.run(steps=weeks, timedelta_per_step=timedelta(weeks=1))
    
    def skip_weeks(self, weeks: int):
        """
        Пропускает заданное количество недель в среде.

        Args:
            weeks (int): Количество недель для пропуска.
        """
        self.skip(steps=weeks, timedelta_per_step=timedelta(weeks=1))
    
    def run_months(self, months: int):
        """
        Запускает среду на заданное количество месяцев.

        Args:
            months (int): Количество месяцев для запуска среды.
        """
        self.run(steps=months, timedelta_per_step=timedelta(weeks=4))
    
    def skip_months(self, months: int):
        """
        Пропускает заданное количество месяцев в среде.

        Args:
            months (int): Количество месяцев для пропуска.
        """
        self.skip(steps=months, timedelta_per_step=timedelta(weeks=4))
    
    def run_years(self, years: int):
        """
        Запускает среду на заданное количество лет.

        Args:
            years (int): Количество лет для запуска среды.
        """
        self.run(steps=years, timedelta_per_step=timedelta(days=365))
    
    def skip_years(self, years: int):
        """
        Пропускает заданное количество лет в среде.

        Args:
            years (int): Количество лет для пропуска.
        """
        self.skip(steps=years, timedelta_per_step=timedelta(days=365))

    #######################################################################
    # Методы управления агентами
    #######################################################################
    def add_agents(self, agents: List[TinyPerson]) -> "TinyWorld":
        """
        Добавляет список агентов в среду.

        Args:
            agents (list): Список агентов для добавления в среду.

        Returns:
            TinyWorld: Ссылка на текущий экземпляр класса для возможности chaining.
        """
        for agent in agents:
            self.add_agent(agent)
        
        return self # для chaining

    def add_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Добавляет агента в среду. Имя агента должно быть уникальным в пределах среды.

        Args:
            agent (TinyPerson): Агент для добавления в среду.
        
        Raises:
            ValueError: Если имя агента не является уникальным в пределах среды.

        Returns:
            TinyWorld: Ссылка на текущий экземпляр класса для возможности chaining.
        """

        # проверить, нет ли агента уже в среде
        if agent not in self.agents:
            logger.debug(f'Adding agent {agent.name} to the environment.')
            
            # Имена агентов должны быть уникальными в среде.
            # Проверить, есть ли имя агента уже там.
            if agent.name not in self.name_to_agent:
                agent.environment = self
                self.agents.append(agent)
                self.name_to_agent[agent.name] = agent
            else:
                raise ValueError(f'Agent names must be unique, but \'{agent.name}\' is already in the environment.')
        else:
            logger.warn(f'Agent {agent.name} is already in the environment.')
        
        return self # для chaining

    def remove_agent(self, agent: TinyPerson) -> "TinyWorld":
        """
        Удаляет агента из среды.

        Args:
            agent (TinyPerson): Агент для удаления из среды.

        Returns:
            TinyWorld: Ссылка на текущий экземпляр класса для возможности chaining.
        """
        logger.debug(f'Removing agent {agent.name} from the environment.')
        self.agents.remove(agent)
        del self.name_to_agent[agent.name]

        return self # для chaining
    
    def remove_all_agents(self) -> "TinyWorld":
        """
        Удаляет всех агентов из среды.

        Returns:
            TinyWorld: Ссылка на текущий экземпляр класса для возможности chaining.
        """
        logger.debug(f'Removing all agents from the environment.')
        self.agents = []
        self.name_to_agent = {}

        return self # для chaining

    def get_agent_by_name(self, name: str) -> Optional[TinyPerson]:
        """
        Возвращает агента с указанным именем. Если агента с таким именем не существует в среде,
        возвращает None.

        Args:
            name (str): Имя агента для возврата.

        Returns:
            Optional[TinyPerson]: Агент с указанным именем.
        """
        if name in self.name_to_agent:
            return self.name_to_agent[name]
        else:
            return None
    
    #######################################################################
    # Методы управления интервенциями
    #######################################################################

    def add_intervention(self, intervention: Any):
        """
        Добавляет интервенцию в среду.

        Args:
            intervention: Интервенция для добавления в среду.
        """
        self._interventions.append(intervention)

    #######################################################################
    # Обработчики действий
    #
    # Определенные действия, выполняемые агентами, обрабатываются средой,
    # поскольку они оказывают влияние за пределами самого агента.
    #######################################################################
    @transactional
    def _handle_actions(self, source: TinyPerson, actions: list):
        """
        Обрабатывает действия, выполняемые агентами.

        Args:
            source (TinyPerson): Агент, который выполнил действия.
            actions (list): Список действий, выполняемых агентами. Каждое действие фактически является
              спецификацией JSON.
        """
        for action in actions:
            action_type = action['type'] # это единственное обязательное поле
            content = action['content'] if 'content' in action else None
            target = action['target'] if 'target' in action else None

            logger.debug(f'[{self.name}] Handling action {action_type} from agent {name_or_empty(source)}. Content: {content}, target: {target}.')

            # Только некоторые действия требуют вмешательства среды
            if action_type == 'REACH_OUT':
                self._handle_reach_out(source, content, target)
            elif action_type == 'TALK':
                self._handle_talk(source, content, target)

    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие REACH_OUT. Эта реализация по умолчанию всегда позволяет REACH_OUT выполниться успешно.
        Подклассы могут переопределять этот метод для реализации других политик.

        Args:
            source_agent (TinyPerson): Агент, который выполнил действие REACH_OUT.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """

        # Эта реализация по умолчанию всегда позволяет REACH_OUT выполниться успешно.
        target_agent = self.get_agent_by_name(target)

        if target_agent is not None:
            source_agent.make_agent_accessible(target_agent)
            target_agent.make_agent_accessible(source_agent)

            source_agent.socialize(f'{name_or_empty(target_agent)} was successfully reached out, and is now available for interaction.', source=self)
            target_agent.socialize(f'{name_or_empty(source_agent)} reached out to you, and is now available for interaction.', source=self)
        
        else:
            logger.debug(f'[{self.name}] REACH_OUT action failed: target agent \'{target}\' not found.')

    @transactional
    def _handle_talk(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие TALK, доставляя указанное содержимое указанной цели.

        Args:
            source_agent (TinyPerson): Агент, который выполнил действие TALK.
            content (str): Содержимое сообщения.
            target (str, optional): Цель сообщения.
        """
        target_agent = self.get_agent_by_name(target)

        logger.debug(f'[{self.name}] Delivering message from {name_or_empty(source_agent)} to {name_or_empty(target_agent)}.')

        if target_agent is not None:
            target_agent.listen(content, source=source_agent)
        elif self.broadcast_if_no_target:
            self.broadcast(content, source=source_agent)

    #######################################################################
    # Методы взаимодействия
    #######################################################################
    @transactional
    def broadcast(self, speech: str, source: AgentOrWorld = None):
        """
        Доставляет речь всем агентам в среде.

        Args:
            speech (str): Содержимое сообщения.
            source (AgentOrWorld, optional): Агент или среда, которые выполнили сообщение. По умолчанию None.
        """
        logger.debug(f'[{self.name}] Broadcasting message: \'{speech}\'.')

        for agent in self.agents:
            # Не доставлять сообщение источнику
            if agent != source:
                agent.listen(speech, source=source)
    
    @transactional
    def broadcast_thought(self, thought: str, source: AgentOrWorld = None):
        """
        Транслирует мысль всем агентам в среде.

        Args:
            thought (str): Содержимое мысли.
        """
        logger.debug(f'[{self.name}] Broadcasting thought: \'{thought}\'.')

        for agent in self.agents:
            agent.think(thought)
    
    @transactional
    def broadcast_internal_goal(self, internal_goal: str):
        """
        Транслирует внутреннюю цель всем агентам в среде.

        Args:
            internal_goal (str): Содержимое внутренней цели.
        """
        logger.debug(f'[{self.name}] Broadcasting internal goal: \'{internal_goal}\'.')

        for agent in self.agents:
            agent.internalize_goal(internal_goal)
    
    @transactional
    def broadcast_context_change(self, context: list):
        """
        Транслирует изменение контекста всем агентам в среде.

        Args:
            context (list): Содержимое изменения контекста.
        """
        logger.debug(f'[{self.name}] Broadcasting context change: \'{context}\'.')

        for agent in self.agents:
            agent.change_context(context)

    def make_everyone_accessible(self):
        """
        Делает всех агентов в среде доступными друг для друга.
        """
        for agent_1 in self.agents:
            for agent_2 in self.agents:
                if agent_1 != agent_2:
                    agent_1.make_agent_accessible(agent_2)
            

    ###########################################################
    # Удобства форматирования
    ###########################################################

    # TODO: лучшие имена для этих "display" методов
    def _display_step_communication(self, cur_step: int, total_steps: int, timedelta_per_step: Optional[timedelta] = None):
        """
        Отображает текущую коммуникацию и сохраняет ее в буфере для последующего использования.
        """
        rendering = self._pretty_step(cur_step=cur_step, total_steps=total_steps, timedelta_per_step=timedelta_per_step)

        self._push_and_display_latest_communication({'kind': 'step', 'rendering': rendering, 'content': None, 'source':  None, 'target': None})
    
    def _display_intervention_communication(self, intervention: Any):
        """
        Отображает текущую коммуникацию интервенции и сохраняет ее в буфере для последующего использования.
        """
        rendering = self._pretty_intervention(intervention)
        self._push_and_display_latest_communication({'kind': 'intervention', 'rendering': rendering, 'content': None, 'source':  None, 'target': None})
    
    def _push_and_display_latest_communication(self, communication: dict):
        """
        Добавляет последние коммуникации в буфер агента.
        """
        #
        # Проверить, не повторяет ли коммуникация последнюю для другой цели
        #
        if len(self._displayed_communications_buffer) > 0:
            # Получить значения из последней коммуникации
            last_communication = self._displayed_communications_buffer[-1]
            last_kind = last_communication['kind']
            last_target = last_communication['target']
            last_source = last_communication['source']
            if last_kind == 'action':
                last_content = last_communication['content']['action']['content']
                last_type = last_communication['content']['action']['type']
            elif last_kind == 'stimulus':
                last_content = last_communication['content']['stimulus']['content']
                last_type = last_communication['content']['stimulus']['type']
            elif last_kind == 'stimuli':
                last_stimulus = last_communication['content']['stimuli'][0]
                last_content = last_stimulus['content']
                last_type = last_stimulus['type']
            else:
                last_content = None
                last_type = None
        
            # Получить значения из текущей коммуникации
            current_kind = communication['kind']
            current_target = communication['target']
            current_source = communication['source']
            if current_kind == 'action':
                current_content = communication['content']['action']['content']
                current_type = communication['content']['action']['type']
            elif current_kind == 'stimulus':
                current_content = communication['content']['stimulus']['content']
                current_type = communication['content']['stimulus']['type']
            elif current_kind == 'stimuli':
                current_stimulus = communication['content']['stimuli'][0]
                current_content = current_stimulus['content']
                current_type = current_stimulus['type']
            else:
                current_content = None
                current_type = None

            # Если мы повторяем последнюю коммуникацию, давайте упростим рендеринг
            if (last_source == current_source) and (last_type == current_type) and (last_kind == current_kind) and \
               (last_content is not None) and (last_content == current_content) and \
               (current_target is not None):
               
                self._target_display_communications_buffer.append(current_target)

                rich_style = utils.RichTextStyle.get_style_for(last_kind, last_type)
                
                # Вывести дополнительную цель ограниченное количество раз, если установлено максимальное значение, или
                # всегда, если максимальное значение не установлено.
                if (self._max_additional_targets_to_display is None) or\
                   len(self._target_display_communications_buffer) < self._max_additional_targets_to_display:
                    communication['rendering'] = ' ' * len(last_source) + f'[{rich_style}]       + --> [underline]{current_target}[/][/]'

                elif len(self._target_display_communications_buffer) == self._max_additional_targets_to_display:
                    communication['rendering'] = ' ' * len(last_source) + f'[{rich_style}]       + --> ...others...[/]'
                
                else: # Больше ничего не отображать
                    communication['rendering'] = None
            
            else:
                # Нет повторения, поэтому просто отобразить коммуникацию и сбросить буфер целей
                self._target_display_communications_buffer = [] # сбросить
        
        else:
            # Нет повторения, поэтому просто отобразить коммуникацию и сбросить буфер целей
            self._target_display_communications_buffer = [] # сбросить



        self._displayed_communications_buffer.append(communication)
        self._display(communication)

    def pop_and_display_latest_communications(self) -> list:
        """
        Извлекает последние коммуникации и отображает их.

        Returns:
            list: Список коммуникаций.
        """
        communications = self._displayed_communications_buffer
        self._displayed_communications_buffer = []

        for communication in communications:
            self._display(communication)

        return communications
    
    def _display(self, communication: dict):
        """
        Отображает коммуникацию.
        """
        # Распаковать рендеринг, чтобы найти больше информации
        content = communication['rendering']
        kind = communication['kind']
        
        if content is not None:
            # Рендерить в соответствии с типом
            if kind == 'step':
                self.console.rule(content)
            else:
                self.console.print(content)
    
    def clear_communications_buffer(self):
        """
        Очищает буфер коммуникаций.
        """
        self._displayed_communications_buffer = []

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта TinyWorld.
        """
        return f'TinyWorld(name=\'{self.name}\')'

    def _pretty_step(self, cur_step: int, total_steps: int, timedelta_per_step: Optional[timedelta] = None) -> str:
        """
        Форматирует строку для отображения шага симуляции.
        """
        rendering = f'{self.name} step {cur_step} of {total_steps}'
        if timedelta_per_step is not None:
            rendering += f' ({pretty_datetime(self.current_datetime)})'

        return rendering

    def _pretty_intervention(self, intervention: Any) -> str:
        """
        Форматирует строку для отображения интервенции.
        """
        indent = '          > '
        justification = textwrap.fill(
            intervention.precondition_justification(),
            width=TinyPerson.PP_TEXT_WIDTH,
            initial_indent=indent,
            subsequent_indent=indent,
        )
        
        rich_style = utils.RichTextStyle.get_style_for('intervention')
        rendering = f'[{rich_style}] :zap: [bold] <<{intervention.name}>> Triggered, effects are being applied...[/] \\n' + \
                    f'[italic]{justification}[/][/]'
        # TODO: добавить подробности о том, почему была применена интервенция

        return rendering

    def pp_current_interactions(self, simplified: bool = True, skip_system: bool = True):
        """
        Выводит в консоль текущие сообщения агентов в этой среде в удобочитаемом формате.
        """
        print(self.pretty_current_interactions(simplified=simplified, skip_system=skip_system))

    def pretty_current_interactions(
        self,
        simplified: bool = True,
        skip_system: bool = True,
        max_content_length: int = default['max_content_display_length'],
        first_n: Optional[int] = None,
        last_n: Optional[int] = None,
        include_omission_info: bool = True
    ) -> str:
        """
        Возвращает удобочитаемую строку с текущими сообщениями агентов в этой среде.
        """
        agent_contents: list = []

        for agent in self.agents:
            agent_content = f'#### Interactions from the point of view of {agent.name} agent:\\n'
            agent_content += f'**BEGIN AGENT {agent.name} HISTORY.**\\n '
            agent_content += agent.pretty_current_interactions(simplified=simplified, skip_system=skip_system, max_content_length=max_content_length, first_n=first_n, last_n=last_n, include_omission_info=include_omission_info) + '\\n'
            agent_content += f'**FINISHED AGENT {agent.name} HISTORY.**\\n\\n'
            agent_contents.append(agent_content)
            
        return '\\n'.join(agent_contents)
    
    #######################################################################
    # IO
    #######################################################################

    def encode_complete_state(self) -> dict:
        """
        Кодирует полное состояние среды в словарь.

        Returns:
            dict: Словарь, кодирующий полное состояние среды.
        """
        to_copy = copy.copy(self.__dict__)

        # Удалить логгер и другие поля
        del to_copy['console']
        del to_copy['agents']
        del to_copy['name_to_agent']
        del to_copy['current_datetime']
        del to_copy['_interventions'] # TODO: кодировать интервенции

        state = copy.deepcopy(to_copy)

        # Агенты кодируются отдельно
        state['agents'] = [agent.encode_complete_state() for agent in self.agents]

        # Datetime также должен быть закодирован отдельно
        state['current_datetime'] = self.current_datetime.isoformat()

        return state
    
    def decode_complete_state(self, state: dict) -> "TinyWorld":
        """
        Декодирует полное состояние среды из словаря.

        Args:
            state (dict): Словарь, кодирующий полное состояние среды.

        Returns:
            TinyWorld: Среда, декодированная из словаря.
        """
        state = copy.deepcopy(state)

        #################################
        # Восстановить агентов на месте
        #################################
        self.remove_all_agents()
        for agent_state in state['agents']:
            try:
                try:
                    agent = TinyPerson.get_agent_by_name(agent_state['name'])
                except Exception as ex:
                    raise ValueError(f'Could not find agent {agent_state["name"]} for environment {self.name}.') from ex
                
                agent.decode_complete_state(agent_state)
                self.add_agent(agent)
                
            except