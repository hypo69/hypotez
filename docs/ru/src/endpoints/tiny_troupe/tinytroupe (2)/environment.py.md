# Модуль `environment`

## Обзор

Модуль `environment` предоставляет инструменты для создания и управления виртуальными средами, в которых взаимодействуют агенты (например, `TinyPerson`) и внешние сущности. Он содержит базовый класс `TinyWorld`, представляющий собой абстракцию мира, в котором живут и действуют агенты. Также включает подкласс `TinySocialNetwork`, расширяющий `TinyWorld` для моделирования социальных связей между агентами.

## Подробней

Этот модуль является ключевым компонентом системы моделирования, позволяя создавать различные сценарии взаимодействия между агентами. Он предоставляет механизмы для управления временем, добавления и удаления агентов, обработки действий агентов и организации коммуникации между ними. `TinyWorld` служит основой для более сложных сред, таких как `TinySocialNetwork`, которая учитывает социальные отношения между агентами. Модуль также предоставляет инструменты для сохранения и восстановления состояния среды, что позволяет воспроизводить и анализировать результаты моделирования.

## Классы

### `TinyWorld`

**Описание**:
Базовый класс для создания виртуальных сред, в которых взаимодействуют агенты.

**Принцип работы**:
Класс `TinyWorld` предоставляет основу для моделирования окружения агентов. Он управляет списком агентов, временем, обработкой действий и коммуникацией между агентами. `TinyWorld` может быть расширен для создания более сложных и специализированных сред.

**Атрибуты**:
- `all_environments (dict)`: Словарь, содержащий все созданные окружения. Ключ - имя окружения, значение - экземпляр `TinyWorld`.
- `communication_display (bool)`: Флаг, определяющий, отображать ли коммуникации в окружении.
- `name (str)`: Имя окружения.
- `current_datetime (datetime)`: Текущее время в окружении.
- `broadcast_if_no_target (bool)`: Флаг, определяющий, транслировать ли действия, если цель не найдена.
- `simulation_id (Any)`: Идентификатор симуляции, к которой принадлежит окружение.
- `agents (list)`: Список агентов в окружении.
- `name_to_agent (dict)`: Словарь, отображающий имена агентов в экземпляры агентов.
- `_displayed_communications_buffer (list)`: Буфер для хранения отображаемых сообщений.
- `console (Console)`: Консоль для вывода сообщений.

**Методы**:

- `__init__(self, name: str="A TinyWorld", agents=[], initial_datetime=datetime.datetime.now(), broadcast_if_no_target=True)`
    ```python
    def __init__(self, name: str="A TinyWorld", agents=[], 
                 initial_datetime=datetime.datetime.now(),
                 broadcast_if_no_target=True):
        """
        Инициализирует окружение.

        Args:
            name (str): Имя окружения.
            agents (list): Список агентов для добавления в окружение.
            initial_datetime (datetime): Начальное время окружения. По умолчанию - текущее время.
            broadcast_if_no_target (bool): Если `True`, транслирует действия, если цель не найдена.
        """
        ...
    ```
- `_step(self, timedelta_per_step=None)`
    ```python
    @transactional
    def _step(self, timedelta_per_step=None):
        """
        Выполняет один шаг в окружении.

        Args:
            timedelta_per_step (timedelta, optional): Временной интервал для одного шага. По умолчанию `None`.
        """
        ...
    ```
- `_advance_datetime(self, timedelta)`
    ```python
    def _advance_datetime(self, timedelta):
        """
        Сдвигает текущее время в окружении на заданный интервал.

        Args:
            timedelta (timedelta): Временной интервал для сдвига.
        """
        ...
    ```
- `run(self, steps: int, timedelta_per_step=None, return_actions=False)`
    ```python
    @transactional
    def run(self, steps: int, timedelta_per_step=None, return_actions=False):
        """
        Запускает окружение на заданное количество шагов.

        Args:
            steps (int): Количество шагов для запуска.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.
            return_actions (bool, optional): Если `True`, возвращает действия агентов. По умолчанию `False`.

        Returns:
            list: Список действий агентов за время выполнения, если `return_actions` равен `True`.
        """
        ...
    ```
- `skip(self, steps: int, timedelta_per_step=None)`
    ```python
    @transactional
    def skip(self, steps: int, timedelta_per_step=None):
        """
        Пропускает заданное количество шагов в окружении.

        Args:
            steps (int): Количество шагов для пропуска.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.
        """
        ...
    ```
- `run_minutes(self, minutes: int)`
    ```python
    def run_minutes(self, minutes: int):
        """
        Запускает окружение на заданное количество минут.

        Args:
            minutes (int): Количество минут для запуска.
        """
        ...
    ```
- `skip_minutes(self, minutes: int)`
    ```python
    def skip_minutes(self, minutes: int):
        """
        Пропускает заданное количество минут в окружении.

        Args:
            minutes (int): Количество минут для пропуска.
        """
        ...
    ```
- `run_hours(self, hours: int)`
    ```python
    def run_hours(self, hours: int):
        """
        Запускает окружение на заданное количество часов.

        Args:
            hours (int): Количество часов для запуска.
        """
        ...
    ```
- `skip_hours(self, hours: int)`
    ```python
    def skip_hours(self, hours: int):
        """
        Пропускает заданное количество часов в окружении.

        Args:
            hours (int): Количество часов для пропуска.
        """
        ...
    ```
- `run_days(self, days: int)`
    ```python
    def run_days(self, days: int):
        """
        Запускает окружение на заданное количество дней.

        Args:
            days (int): Количество дней для запуска.
        """
        ...
    ```
- `skip_days(self, days: int)`
    ```python
    def skip_days(self, days: int):
        """
        Пропускает заданное количество дней в окружении.

        Args:
            days (int): Количество дней для пропуска.
        """
        ...
    ```
- `run_weeks(self, weeks: int)`
    ```python
    def run_weeks(self, weeks: int):
        """
        Запускает окружение на заданное количество недель.

        Args:
            weeks (int): Количество недель для запуска.
        """
        ...
    ```
- `skip_weeks(self, weeks: int)`
    ```python
    def skip_weeks(self, weeks: int):
        """
        Пропускает заданное количество недель в окружении.

        Args:
            weeks (int): Количество недель для пропуска.
        """
        ...
    ```
- `run_months(self, months: int)`
    ```python
    def run_months(self, months: int):
        """
        Запускает окружение на заданное количество месяцев.

        Args:
            months (int): Количество месяцев для запуска.
        """
        ...
    ```
- `skip_months(self, months: int)`
    ```python
    def skip_months(self, months: int):
        """
        Пропускает заданное количество месяцев в окружении.

        Args:
            months (int): Количество месяцев для пропуска.
        """
        ...
    ```
- `run_years(self, years: int)`
    ```python
    def run_years(self, years: int):
        """
        Запускает окружение на заданное количество лет.

        Args:
            years (int): Количество лет для запуска.
        """
        ...
    ```
- `skip_years(self, years: int)`
    ```python
    def skip_years(self, years: int):
        """
        Пропускает заданное количество лет в окружении.

        Args:
            years (int): Количество лет для пропуска.
        """
        ...
    ```
- `add_agents(self, agents: list)`
    ```python
    def add_agents(self, agents: list):
        """
        Добавляет список агентов в окружение.

        Args:
            agents (list): Список агентов для добавления.

        Returns:
            self: Для цепочки вызовов.
        """
        ...
    ```
- `add_agent(self, agent: TinyPerson)`
    ```python
    def add_agent(self, agent: TinyPerson):
        """
        Добавляет агента в окружение.

        Args:
            agent (TinyPerson): Агент для добавления.

        Raises:
            ValueError: Если имя агента не уникально в окружении.

        Returns:
            self: Для цепочки вызовов.
        """
        ...
    ```
- `remove_agent(self, agent: TinyPerson)`
    ```python
    def remove_agent(self, agent: TinyPerson):
        """
        Удаляет агента из окружения.

        Args:
            agent (TinyPerson): Агент для удаления.

        Returns:
            self: Для цепочки вызовов.
        """
        ...
    ```
- `remove_all_agents(self)`
    ```python
    def remove_all_agents(self):
        """
        Удаляет всех агентов из окружения.

        Returns:
            self: Для цепочки вызовов.
        """
        ...
    ```
- `get_agent_by_name(self, name: str) -> TinyPerson`
    ```python
    def get_agent_by_name(self, name: str) -> TinyPerson:
        """
        Возвращает агента по имени.

        Args:
            name (str): Имя агента.

        Returns:
            TinyPerson: Агент с указанным именем.
        """
        ...
    ```
- `_handle_actions(self, source: TinyPerson, actions: list)`
    ```python
    @transactional
    def _handle_actions(self, source: TinyPerson, actions: list):
        """
        Обрабатывает действия агентов.

        Args:
            source (TinyPerson): Агент, выполнивший действия.
            actions (list): Список действий.
        """
        ...
    ```
- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`
    ```python
    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие REACH_OUT.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """
        ...
    ```
- `_handle_talk(self, source_agent: TinyPerson, content: str, target: str)`
    ```python
    @transactional
    def _handle_talk(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие TALK.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """
        ...
    ```
- `broadcast(self, speech: str, source: AgentOrWorld=None)`
    ```python
    @transactional
    def broadcast(self, speech: str, source: AgentOrWorld=None):
        """
        Отправляет сообщение всем агентам в окружении.

        Args:
            speech (str): Содержимое сообщения.
            source (AgentOrWorld, optional): Источник сообщения. По умолчанию `None`.
        """
        ...
    ```
- `broadcast_thought(self, thought: str, source: AgentOrWorld=None)`
    ```python
    @transactional
    def broadcast_thought(self, thought: str, source: AgentOrWorld=None):
        """
        Отправляет мысль всем агентам в окружении.

        Args:
            thought (str): Содержимое мысли.
        """
        ...
    ```
- `broadcast_internal_goal(self, internal_goal: str)`
    ```python
    @transactional
    def broadcast_internal_goal(self, internal_goal: str):
        """
        Отправляет внутреннюю цель всем агентам в окружении.

        Args:
            internal_goal (str): Содержимое внутренней цели.
        """
        ...
    ```
- `broadcast_context_change(self, context: list)`
    ```python
    @transactional
    def broadcast_context_change(self, context:list):
        """
        Отправляет изменение контекста всем агентам в окружении.

        Args:
            context (list): Содержимое изменения контекста.
        """
        ...
    ```
- `make_everyone_accessible(self)`
    ```python
    def make_everyone_accessible(self):
        """
        Делает всех агентов в окружении доступными друг для друга.
        """
        ...
    ```
- `_display_communication(self, cur_step, total_steps, kind, timedelta_per_step=None)`
    ```python
    def _display_communication(self, cur_step, total_steps, kind, timedelta_per_step=None):
        """
        Отображает текущую коммуникацию и сохраняет ее в буфере.

        Args:
            cur_step (int): Текущий шаг.
            total_steps (int): Общее количество шагов.
            kind (str): Тип коммуникации.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.
        """
        ...
    ```
- `_push_and_display_latest_communication(self, rendering)`
    ```python
    def _push_and_display_latest_communication(self, rendering):
        """
        Добавляет последнюю коммуникацию в буфер агента.

        Args:
            rendering (dict): Отображаемая информация.
        """
        ...
    ```
- `pop_and_display_latest_communications(self)`
    ```python
    def pop_and_display_latest_communications(self):
        """
        Извлекает последние коммуникации и отображает их.
        """
        ...
    ```
- `_display(self, communication)`
    ```python
    def _display(self, communication):
        """
        Отображает коммуникацию.

        Args:
            communication (dict): Коммуникация для отображения.
        """
        ...
    ```
- `clear_communications_buffer(self)`
    ```python
    def clear_communications_buffer(self):
        """
        Очищает буфер коммуникаций.
        """
        ...
    ```
- `__repr__(self)`
    ```python
    def __repr__(self):
        return f"TinyWorld(name=\'{self.name}\')"
    ```
- `_pretty_step(self, cur_step, total_steps, timedelta_per_step=None)`
    ```python
    def _pretty_step(self, cur_step, total_steps, timedelta_per_step=None):
        """
        Форматирует сообщение для отображения текущего шага.

        Args:
            cur_step (int): Текущий шаг.
            total_steps (int): Общее количество шагов.
            timedelta_per_step (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.

        Returns:
            str: Отформатированное сообщение.
        """
        ...
    ```
- `pp_current_interactions(self, simplified=True, skip_system=True)`
    ```python
    def pp_current_interactions(self, simplified=True, skip_system=True):
        """
        Выводит текущие взаимодействия агентов в окружении.

        Args:
            simplified (bool, optional): Упрощенный вывод. По умолчанию `True`.
            skip_system (bool, optional): Пропускать системные сообщения. По умолчанию `True`.
        """
        ...
    ```
- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info:bool=True)`
    ```python
    def pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info:bool=True):
      """
      Возвращает отформатированную строку с текущими сообщениями агентов в этой среде.
      """
      ...
    ```
- `encode_complete_state(self) -> dict`
    ```python
    def encode_complete_state(self) -> dict:
        """
        Кодирует полное состояние окружения в словарь.

        Returns:
            dict: Словарь, содержащий состояние окружения.
        """
        ...
    ```
- `decode_complete_state(self, state: dict) -> Self`
    ```python
    def decode_complete_state(self, state:dict) -> Self:
        """
        Декодирует полное состояние окружения из словаря.

        Args:
            state (dict): Словарь, содержащий состояние окружения.

        Returns:
            Self: Окружение, декодированное из словаря.
        """
        ...
    ```

**Статические методы**:

- `add_environment(environment)`
    ```python
    @staticmethod
    def add_environment(environment):
        """
        Добавляет окружение в список всех окружений.

        Args:
            environment (TinyWorld): Окружение для добавления.

        Raises:
            ValueError: Если имя окружения не уникально.
        """
        ...
    ```
- `set_simulation_for_free_environments(simulation)`
    ```python
    @staticmethod
    def set_simulation_for_free_environments(simulation):
        """
        Устанавливает симуляцию для свободных окружений.
        """
        ...
    ```
- `get_environment_by_name(name: str)`
    ```python
    @staticmethod
    def get_environment_by_name(name: str):
        """
        Возвращает окружение по имени.

        Args:
            name (str): Имя окружения.

        Returns:
            TinyWorld: Окружение с указанным именем.
        """
        ...
    ```
- `clear_environments()`
    ```python
    @staticmethod
    def clear_environments():
        """
        Очищает список всех окружений.
        """
        ...
    ```

### `TinySocialNetwork`

**Описание**:
Подкласс `TinyWorld`, представляющий собой социальную сеть агентов.

**Наследует**:
`TinyWorld`: Расширяет базовый класс `TinyWorld`, добавляя функциональность для моделирования социальных связей между агентами.

**Атрибуты**:
- `relations (dict)`: Словарь, хранящий отношения между агентами.

**Методы**:

- `__init__(self, name, broadcast_if_no_target=True)`
    ```python
    def __init__(self, name, broadcast_if_no_target=True):
        """
        Создает новую среду TinySocialNetwork.

        Args:
            name (str): Имя окружения.
            broadcast_if_no_target (bool): Если `True`, транслирует действия через доступные связи агента, если цель не найдена.
        """
        ...
    ```
- `add_relation(self, agent_1, agent_2, name="default")`
    ```python
    @transactional
    def add_relation(self, agent_1, agent_2, name="default"):
        """
        Добавляет отношение между двумя агентами.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент.
            name (str): Имя отношения.

        Returns:
            self: Для цепочки вызовов.
        """
        ...
    ```
- `_update_agents_contexts(self)`
    ```python
    @transactional
    def _update_agents_contexts(self):
        """
        Обновляет контексты агентов на основе текущего состояния мира.
        """
        ...
    ```
- `_step(self)`
    ```python
    @transactional
    def _step(self):
        """
        Выполняет один шаг в социальной сети.
        """
        ...
    ```
- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`
    ```python
    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие REACH_OUT.

        Args:
            source_agent (TinyPerson): Агент, выполнивший действие.
            content (str): Содержимое сообщения.
            target (str): Цель сообщения.
        """
        ...
    ```
- `is_in_relation_with(self, agent_1: TinyPerson, agent_2: TinyPerson, relation_name=None) -> bool`
    ```python
    def is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool:
        """
        Проверяет, находятся ли два агента в отношении.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент.
            relation_name (str, optional): Имя отношения для проверки. Если `None`, проверяется наличие любого отношения.

        Returns:
            bool: `True`, если агенты находятся в отношении, `False` в противном случае.
        """
        ...
    ```

## Функции

В данном модуле нет отдельных функций, не являющихся методами классов.

## Как работает `TinyWorld`

1.  **Инициализация окружения**:
    *   Создается экземпляр класса `TinyWorld` с заданным именем, списком агентов, начальным временем и флагом трансляции действий.
    *   Окружение добавляется в статический словарь `all_environments`, где хранятся все созданные окружения.
    *   Агенты добавляются в окружение с помощью метода `add_agents`.

2.  **Запуск симуляции**:
    *   Метод `run` запускает симуляцию на заданное количество шагов.
    *   На каждом шаге вызывается метод `_step`.

3.  **Выполнение шага симуляции (`_step`)**:
    *   Если задан временной интервал (`timedelta_per_step`), текущее время окружения увеличивается на этот интервал.
    *   Для каждого агента в окружении вызывается метод `act`, который определяет действия агента.
    *   Действия агента обрабатываются методом `_handle_actions`.

4.  **Обработка действий агентов (`_handle_actions`)**:
    *   Для каждого действия определяется его тип (`action_type`), содержимое (`content`) и цель (`target`).
    *   В зависимости от типа действия вызывается соответствующий метод обработки:
        *   `REACH_OUT`: `_handle_reach_out` (устанавливает доступность между агентами).
        *   `TALK`: `_handle_talk` (доставляет сообщение целевому агенту или транслирует его).

5.  **Коммуникация между агентами**:
    *   Метод `broadcast` отправляет сообщение всем агентам в окружении, кроме отправителя.
    *   Метод `listen` используется агентом для получения сообщений.

6.  **Управление временем**:
    *   Методы `run_minutes`, `run_hours`, `run_days`, `run_weeks`, `run_months`, `run_years` позволяют запускать симуляцию на заданный период времени.
    *   Аналогичные методы `skip_...` позволяют пропускать определенный период времени без выполнения действий агентов.

7.  **Сохранение и восстановление состояния**:
    *   Метод `encode_complete_state` кодирует состояние окружения в словарь.
    *   Метод `decode_complete_state` восстанавливает состояние окружения из словаря.

## Как работает функция `_step`

Функция `_step` выполняет один шаг в симуляции окружения. Она отвечает за обновление времени в окружении и запуск действий каждого агента.

```
    Начало
    │
    ├──► Обновление времени: Если timedelta_per_step задан, current_datetime увеличивается на timedelta_per_step
    │   (advance_datetime)
    │
    ├──► Действия агентов: Для каждого агента в окружении:
    │   │
    │   ├──► Агент действует: Вызывается метод act() агента, который возвращает список действий
    │   │   (agent.act(return_actions=True))
    │   │
    │   ├──► Обработка действий: Действия агента обрабатываются функцией _handle_actions()
    │   │   (_handle_actions(agent, agent.pop_latest_actions()))
    │   │
    │   └──► Запись действий: Действия агента записываются в словарь agents_actions
    │
    └──► Возврат действий: Возвращается словарь agents_actions, содержащий действия всех агентов
         (return agents_actions)
    │
    Конец
```

## Примеры

### Создание и запуск `TinyWorld`

```python
import datetime
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание агентов
agent1 = TinyPerson(name='Alice')
agent2 = TinyPerson(name='Bob')

# Создание окружения
world = TinyWorld(name='MyWorld', agents=[agent1, agent2], initial_datetime=datetime.datetime(2024, 1, 1))

# Запуск симуляции на 10 шагов с интервалом в 1 час
world.run(steps=10, timedelta_per_step=datetime.timedelta(hours=1))

# Вывод текущего времени в окружении
print(world.current_datetime)
```

### Создание и использование `TinySocialNetwork`

```python
from tinytroupe.environment import TinySocialNetwork
from tinytroupe.agent import TinyPerson

# Создание агентов
agent1 = TinyPerson(name='Alice')
agent2 = TinyPerson(name='Bob')
agent3 = TinyPerson(name='Charlie')

# Создание социальной сети
network = TinySocialNetwork(name='MyNetwork')

# Добавление агентов в сеть
network.add_agents([agent1, agent2, agent3])

# Установка отношений между агентами
network.add_relation(agent1, agent2, name='friends')

# Запуск симуляции
network.run(steps=5)