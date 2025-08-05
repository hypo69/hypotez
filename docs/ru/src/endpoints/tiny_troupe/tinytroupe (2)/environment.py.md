# Модуль `environment`

## Обзор

Модуль `environment` предоставляет классы для моделирования окружения, в котором взаимодействуют агенты (`TinyPerson`) и внешние сущности. Он содержит базовый класс `TinyWorld` для представления окружения и класс `TinySocialNetwork` для моделирования социальных сетей. Модуль обеспечивает механизмы для управления агентами, обработки действий, моделирования времени и взаимодействия между агентами.

## Подробнее

Этот модуль является ключевым компонентом для создания симуляций, в которых агенты взаимодействуют друг с другом и с окружением. Он предоставляет абстракции для управления временем, пространством и социальными связями, позволяя моделировать различные сценарии и изучать поведение агентов в этих сценариях.

## Классы

### `TinyWorld`

**Описание**: Базовый класс для представления окружения, в котором находятся агенты.

**Атрибуты**:

-   `all_environments` (dict): Словарь, содержащий все созданные окружения (`name -> environment`).
-   `communication_display` (bool): Флаг, определяющий, отображать ли коммуникации в окружении.
-   `name` (str): Имя окружения.
-   `current_datetime` (datetime): Текущее время в окружении.
-   `broadcast_if_no_target` (bool): Если `True`, действия рассылаются всем, если цель не найдена.
-   `simulation_id` (Any): Идентификатор симуляции, к которой принадлежит окружение.
-   `agents` (list): Список агентов в окружении.
-   `name_to_agent` (dict): Словарь, отображающий имена агентов в объекты агентов (`{agent_name: agent, ...}`).
-   `_displayed_communications_buffer` (list): Буфер для хранения отображаемых коммуникаций.
-   `console` (Console): Объект консоли для вывода информации.

**Методы**:

-   `__init__(self, name: str="A TinyWorld", agents=[], initial_datetime=datetime.datetime.now(), broadcast_if_no_target=True)`: Инициализирует окружение.
-   `_step(self, timedelta_per_step=None)`: Выполняет один шаг симуляции, заставляя агентов действовать и обрабатывая их действия.
-   `_advance_datetime(self, timedelta)`: Сдвигает текущее время в окружении на заданный интервал.
-   `run(self, steps: int, timedelta_per_step=None, return_actions=False)`: Запускает симуляцию на заданное количество шагов.
-   `skip(self, steps: int, timedelta_per_step=None)`: Пропускает заданное количество шагов в симуляции.
-   `run_minutes(self, minutes: int)`: Запускает симуляцию на заданное количество минут.
-   `skip_minutes(self, minutes: int)`: Пропускает заданное количество минут в симуляции.
-   `run_hours(self, hours: int)`: Запускает симуляцию на заданное количество часов.
-   `skip_hours(self, hours: int)`: Пропускает заданное количество часов в симуляции.
-   `run_days(self, days: int)`: Запускает симуляцию на заданное количество дней.
-   `skip_days(self, days: int)`: Пропускает заданное количество дней в симуляции.
-   `run_weeks(self, weeks: int)`: Запускает симуляцию на заданное количество недель.
-   `skip_weeks(self, weeks: int)`: Пропускает заданное количество недель в симуляции.
-   `run_months(self, months: int)`: Запускает симуляцию на заданное количество месяцев.
-   `skip_months(self, months: int)`: Пропускает заданное количество месяцев в симуляции.
-   `run_years(self, years: int)`: Запускает симуляцию на заданное количество лет.
-   `skip_years(self, years: int)`: Пропускает заданное количество лет в симуляции.
-   `add_agents(self, agents: list)`: Добавляет список агентов в окружение.
-   `add_agent(self, agent: TinyPerson)`: Добавляет агента в окружение.
-   `remove_agent(self, agent: TinyPerson)`: Удаляет агента из окружения.
-   `remove_all_agents(self)`: Удаляет всех агентов из окружения.
-   `get_agent_by_name(self, name: str) -> TinyPerson`: Возвращает агента по имени.
-   `_handle_actions(self, source: TinyPerson, actions: list)`: Обрабатывает действия, совершенные агентами.
-   `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `REACH_OUT`.
-   `_handle_talk(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `TALK`.
-   `broadcast(self, speech: str, source: AgentOrWorld=None)`: Рассылает сообщение всем агентам в окружении.
-   `broadcast_thought(self, thought: str, source: AgentOrWorld=None)`: Рассылает мысль всем агентам в окружении.
-   `broadcast_internal_goal(self, internal_goal: str)`: Рассылает внутреннюю цель всем агентам в окружении.
-   `broadcast_context_change(self, context: list)`: Рассылает изменение контекста всем агентам в окружении.
-   `make_everyone_accessible(self)`: Делает всех агентов доступными друг для друга.
-   `_display_communication(self, cur_step, total_steps, kind, timedelta_per_step=None)`: Отображает текущую коммуникацию.
-   `_push_and_display_latest_communication(self, rendering)`: Добавляет последнюю коммуникацию в буфер и отображает ее.
-   `pop_and_display_latest_communications(self)`: Извлекает последние коммуникации из буфера и отображает их.
-   `_display(self, communication)`: Отображает коммуникацию.
-   `clear_communications_buffer(self)`: Очищает буфер коммуникаций.
-   `__repr__(self)`: Возвращает строковое представление объекта `TinyWorld`.
-   `_pretty_step(self, cur_step, total_steps, timedelta_per_step=None)`: Форматирует строку для отображения шага симуляции.
-   `pp_current_interactions(self, simplified=True, skip_system=True)`: Выводит текущие взаимодействия агентов в удобочитаемом формате.
-   `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info: bool=True)`: Возвращает строку с текущими сообщениями агентов.
-   `encode_complete_state(self) -> dict`: Кодирует полное состояние окружения в словарь.
-   `decode_complete_state(self, state: dict) -> Self`: Декодирует полное состояние окружения из словаря.
-   `add_environment(environment)`: Добавляет окружение в список всех окружений.
-   `set_simulation_for_free_environments(simulation)`: Устанавливает симуляцию для свободных окружений.
-   `get_environment_by_name(name: str)`: Возвращает окружение по имени.
-   `clear_environments()`: Очищает список всех окружений.

#### `__init__`

```python
def __init__(self, name: str="A TinyWorld", agents=[], 
                 initial_datetime=datetime.datetime.now(),
                 broadcast_if_no_target=True)
```

**Назначение**: Инициализирует экземпляр класса `TinyWorld`.

**Параметры**:

-   `name` (str): Имя окружения. По умолчанию "A TinyWorld".
-   `agents` (list): Список агентов для добавления в окружение. По умолчанию пустой список.
-   `initial_datetime` (datetime): Начальное время окружения. По умолчанию текущее время.
-   `broadcast_if_no_target` (bool): Флаг, определяющий, следует ли рассылать действия, если цель не найдена. По умолчанию `True`.

**Как работает функция**:

-   Функция инициализирует атрибуты окружения, такие как имя, текущее время, список агентов и словарь для быстрого доступа к агентам по имени.
-   Устанавливает флаг `broadcast_if_no_target`, определяющий, следует ли рассылать действия, если цель не найдена.
-   Добавляет окружение в статический словарь `TinyWorld.all_environments`, чтобы обеспечить к нему глобальный доступ.
-   Вызывает метод `add_agents` для добавления переданных агентов в окружение.

**Примеры**:

```python
import datetime
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Пример 1: Создание окружения с именем и списком агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
world = TinyWorld(name="MyWorld", agents=[agent1, agent2])

# Пример 2: Создание окружения с начальным временем
initial_time = datetime.datetime(2024, 1, 1, 12, 0, 0)
world = TinyWorld(name="MyWorld", initial_datetime=initial_time)

# Пример 3: Создание окружения с отключенной рассылкой действий при отсутствии цели
world = TinyWorld(name="MyWorld", broadcast_if_no_target=False)
```

#### `_step`

```python
@transactional
def _step(self, timedelta_per_step=None)
```

**Назначение**: Выполняет один шаг в симуляции окружения.

**Параметры**:

-   `timedelta_per_step` (timedelta, optional): Временной интервал, на который следует продвинуть симуляцию на этом шаге. По умолчанию `None`.

**Как работает функция**:

1.  Вызывает `_advance_datetime` для обновления текущего времени окружения на основе `timedelta_per_step`.
2.  Итерируется по всем агентам в окружении и вызывает метод `act` для каждого агента, чтобы получить их действия.
3.  Сохраняет действия каждого агента в словарь `agents_actions`.
4.  Вызывает `_handle_actions` для каждого агента, чтобы обработать их действия.
5.  Возвращает словарь `agents_actions`, содержащий действия всех агентов.

**Примеры**:

```python
import datetime
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения
world = TinyWorld(name="MyWorld")

# Создание агента
agent = TinyPerson(name="Alice")
world.add_agent(agent)

# Пример 1: Выполнение одного шага без временного интервала
actions = world._step()

# Пример 2: Выполнение одного шага с временным интервалом в 1 час
time_delta = datetime.timedelta(hours=1)
actions = world._step(timedelta_per_step=time_delta)
```

#### `_advance_datetime`

```python
def _advance_datetime(self, timedelta)
```

**Назначение**: Сдвигает текущее время в окружении на заданный временной интервал.

**Параметры**:

-   `timedelta` (timedelta): Временной интервал, на который нужно сдвинуть время.

**Как работает функция**:

-   Если `timedelta` не равен `None`, добавляет его к текущему времени окружения (`self.current_datetime`).
-   Если `timedelta` равен `None`, записывает информационное сообщение в лог, указывающее, что время не было изменено.

**Примеры**:

```python
import datetime
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пример 1: Сдвиг времени на 1 день
time_delta = datetime.timedelta(days=1)
world._advance_datetime(time_delta)
print(world.current_datetime)

# Пример 2: Сдвиг времени на 30 минут
time_delta = datetime.timedelta(minutes=30)
world._advance_datetime(time_delta)
print(world.current_datetime)

# Пример 3: Отсутствие временного интервала
world._advance_datetime(None)
```

#### `run`

```python
@transactional
def run(self, steps: int, timedelta_per_step=None, return_actions=False)
```

**Назначение**: Запускает симуляцию в окружении на заданное количество шагов.

**Параметры**:

-   `steps` (int): Количество шагов для выполнения симуляции.
-   `timedelta_per_step` (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.
-   `return_actions` (bool, optional): Если `True`, возвращает список действий, выполненных агентами. По умолчанию `False`.

**Возвращает**:

-   `list`: Список действий, выполненных агентами во времени, если `return_actions` равен `True`. Список имеет формат `[{agent_name: [action_1, action_2, ...]}, {agent_name_2: [action_1, action_2, ...]}, ...]`.

**Как работает функция**:

1.  Инициализирует пустой список `agents_actions_over_time` для хранения действий агентов, если `return_actions` равен `True`.
2.  Итерируется `steps` раз, выполняя каждый шаг симуляции:
    -   Записывает информационное сообщение в лог о текущем шаге.
    -   Если `TinyWorld.communication_display` равен `True`, вызывает `_display_communication` для отображения информации о шаге.
    -   Вызывает `_step` для выполнения одного шага симуляции и получения действий агентов.
    -   Добавляет действия агентов в список `agents_actions_over_time`, если `return_actions` равен `True`.
3.  Если `return_actions` равен `True`, возвращает список `agents_actions_over_time`.

**Примеры**:

```python
import datetime
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения
world = TinyWorld(name="MyWorld")

# Создание агента
agent = TinyPerson(name="Alice")
world.add_agent(agent)

# Пример 1: Запуск симуляции на 5 шагов без временного интервала
world.run(steps=5)

# Пример 2: Запуск симуляции на 10 шагов с временным интервалом в 30 минут
time_delta = datetime.timedelta(minutes=30)
world.run(steps=10, timedelta_per_step=time_delta)

# Пример 3: Запуск симуляции на 3 шага с возвратом действий агентов
actions = world.run(steps=3, return_actions=True)
print(actions)
```

#### `skip`

```python
@transactional
def skip(self, steps: int, timedelta_per_step=None)
```

**Назначение**: Пропускает заданное количество шагов в симуляции окружения, не выполняя никаких действий.

**Параметры**:

-   `steps` (int): Количество шагов для пропуска.
-   `timedelta_per_step` (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.

**Как работает функция**:

-   Вызывает метод `_advance_datetime`, чтобы продвинуть время в окружении на `steps * timedelta_per_step`.

**Примеры**:

```python
import datetime
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пример 1: Пропуск 5 шагов без временного интервала
world.skip(steps=5)

# Пример 2: Пропуск 10 шагов с временным интервалом в 1 час
time_delta = datetime.timedelta(hours=1)
world.skip(steps=10, timedelta_per_step=time_delta)
```

#### `run_minutes`

```python
def run_minutes(self, minutes: int)
```

**Назначение**: Запускает симуляцию на заданное количество минут.

**Параметры**:

-   `minutes` (int): Количество минут для запуска симуляции.

**Как работает функция**:

-   Вызывает метод `run` с параметрами `steps=minutes` и `timedelta_per_step=timedelta(minutes=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Запуск симуляции на 60 минут
world.run_minutes(minutes=60)
```

#### `skip_minutes`

```python
def skip_minutes(self, minutes: int)
```

**Назначение**: Пропускает заданное количество минут в симуляции.

**Параметры**:

-   `minutes` (int): Количество минут для пропуска.

**Как работает функция**:

-   Вызывает метод `skip` с параметрами `steps=minutes` и `timedelta_per_step=timedelta(minutes=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пропуск 30 минут в симуляции
world.skip_minutes(minutes=30)
```

#### `run_hours`

```python
def run_hours(self, hours: int)
```

**Назначение**: Запускает симуляцию на заданное количество часов.

**Параметры**:

-   `hours` (int): Количество часов для запуска симуляции.

**Как работает функция**:

-   Вызывает метод `run` с параметрами `steps=hours` и `timedelta_per_step=timedelta(hours=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Запуск симуляции на 24 часа
world.run_hours(hours=24)
```

#### `skip_hours`

```python
def skip_hours(self, hours: int)
```

**Назначение**: Пропускает заданное количество часов в симуляции.

**Параметры**:

-   `hours` (int): Количество часов для пропуска.

**Как работает функция**:

-   Вызывает метод `skip` с параметрами `steps=hours` и `timedelta_per_step=timedelta(hours=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пропуск 12 часов в симуляции
world.skip_hours(hours=12)
```

#### `run_days`

```python
def run_days(self, days: int)
```

**Назначение**: Запускает симуляцию на заданное количество дней.

**Параметры**:

-   `days` (int): Количество дней для запуска симуляции.

**Как работает функция**:

-   Вызывает метод `run` с параметрами `steps=days` и `timedelta_per_step=timedelta(days=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Запуск симуляции на 7 дней
world.run_days(days=7)
```

#### `skip_days`

```python
def skip_days(self, days: int)
```

**Назначение**: Пропускает заданное количество дней в симуляции.

**Параметры**:

-   `days` (int): Количество дней для пропуска.

**Как работает функция**:

-   Вызывает метод `skip` с параметрами `steps=days` и `timedelta_per_step=timedelta(days=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пропуск 3 дня в симуляции
world.skip_days(days=3)
```

#### `run_weeks`

```python
def run_weeks(self, weeks: int)
```

**Назначение**: Запускает симуляцию на заданное количество недель.

**Параметры**:

-   `weeks` (int): Количество недель для запуска симуляции.

**Как работает функция**:

-   Вызывает метод `run` с параметрами `steps=weeks` и `timedelta_per_step=timedelta(weeks=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Запуск симуляции на 2 недели
world.run_weeks(weeks=2)
```

#### `skip_weeks`

```python
def skip_weeks(self, weeks: int)
```

**Назначение**: Пропускает заданное количество недель в симуляции.

**Параметры**:

-   `weeks` (int): Количество недель для пропуска.

**Как работает функция**:

-   Вызывает метод `skip` с параметрами `steps=weeks` и `timedelta_per_step=timedelta(weeks=1)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пропуск 1 недели в симуляции
world.skip_weeks(weeks=1)
```

#### `run_months`

```python
def run_months(self, months: int)
```

**Назначение**: Запускает симуляцию на заданное количество месяцев.

**Параметры**:

-   `months` (int): Количество месяцев для запуска симуляции.

**Как работает функция**:

-   Вызывает метод `run` с параметрами `steps=months` и `timedelta_per_step=timedelta(weeks=4)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Запуск симуляции на 6 месяцев
world.run_months(months=6)
```

#### `skip_months`

```python
def skip_months(self, months: int)
```

**Назначение**: Пропускает заданное количество месяцев в симуляции.

**Параметры**:

-   `months` (int): Количество месяцев для пропуска.

**Как работает функция**:

-   Вызывает метод `skip` с параметрами `steps=months` и `timedelta_per_step=timedelta(weeks=4)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пропуск 3 месяца в симуляции
world.skip_months(months=3)
```

#### `run_years`

```python
def run_years(self, years: int)
```

**Назначение**: Запускает симуляцию на заданное количество лет.

**Параметры**:

-   `years` (int): Количество лет для запуска симуляции.

**Как работает функция**:

-   Вызывает метод `run` с параметрами `steps=years` и `timedelta_per_step=timedelta(days=365)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Запуск симуляции на 1 год
world.run_years(years=1)
```

#### `skip_years`

```python
def skip_years(self, years: int)
```

**Назначение**: Пропускает заданное количество лет в симуляции.

**Параметры**:

-   `years` (int): Количество лет для пропуска.

**Как работает функция**:

-   Вызывает метод `skip` с параметрами `steps=years` и `timedelta_per_step=timedelta(days=365)`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world = TinyWorld(name="MyWorld")

# Пропуск 2 года в симуляции
world.skip_years(years=2)
```

#### `add_agents`

```python
def add_agents(self, agents: list)
```

**Назначение**: Добавляет список агентов в окружение.

**Параметры**:

-   `agents` (list): Список агентов для добавления.

**Возвращает**:

-   `self`: Объект `TinyWorld` для возможности chaining.

**Как работает функция**:

-   Итерируется по списку агентов и вызывает метод `add_agent` для каждого агента.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения
world = TinyWorld(name="MyWorld")

# Создание агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")

# Добавление агентов в окружение
world.add_agents([agent1, agent2])
```

#### `add_agent`

```python
def add_agent(self, agent: TinyPerson)
```

**Назначение**: Добавляет агента в окружение.

**Параметры**:

-   `agent` (TinyPerson): Агент для добавления.

**Возвращает**:

-   `self`: Объект `TinyWorld` для возможности chaining.

**Вызывает исключения**:

-   `ValueError`: Если имя агента не уникально в окружении.

**Как работает функция**:

1.  Проверяет, что агента еще нет в списке агентов окружения.
2.  Проверяет, что имя агента уникально в окружении.
3.  Устанавливает атрибут `environment` агента в текущее окружение.
4.  Добавляет агента в список `agents` и в словарь `name_to_agent`.
5.  Если имя агента уже существует в `name_to_agent`, выбрасывает исключение `ValueError`.
6.  Если агент уже находится в окружении, записывает предупреждение в лог.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения
world = TinyWorld(name="MyWorld")

# Создание агента
agent = TinyPerson(name="Alice")

# Добавление агента в окружение
world.add_agent(agent)
```

#### `remove_agent`

```python
def remove_agent(self, agent: TinyPerson)
```

**Назначение**: Удаляет агента из окружения.

**Параметры**:

-   `agent` (TinyPerson): Агент для удаления.

**Возвращает**:

-   `self`: Объект `TinyWorld` для возможности chaining.

**Как работает функция**:

1.  Записывает отладочное сообщение в лог об удалении агента.
2.  Удаляет агента из списка `self.agents`.
3.  Удаляет агента из словаря `self.name_to_agent`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения и агента
world = TinyWorld(name="MyWorld")
agent = TinyPerson(name="Alice")
world.add_agent(agent)

# Удаление агента из окружения
world.remove_agent(agent)
```

#### `remove_all_agents`

```python
def remove_all_agents(self)
```

**Назначение**: Удаляет всех агентов из окружения.

**Возвращает**:

-   `self`: Объект `TinyWorld` для возможности chaining.

**Как работает функция**:

1.  Записывает отладочное сообщение в лог об удалении всех агентов.
2.  Очищает список `self.agents`.
3.  Очищает словарь `self.name_to_agent`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения и добавление агентов
world = TinyWorld(name="MyWorld")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
world.add_agents([agent1, agent2])

# Удаление всех агентов из окружения
world.remove_all_agents()
```

#### `get_agent_by_name`

```python
def get_agent_by_name(self, name: str) -> TinyPerson
```

**Назначение**: Возвращает агента с указанным именем.

**Параметры**:

-   `name` (str): Имя агента для поиска.

**Возвращает**:

-   `TinyPerson`: Агент с указанным именем или `None`, если агент не найден.

**Как работает функция**:

1.  Проверяет, существует ли агент с указанным именем в словаре `self.name_to_agent`.
2.  Если агент существует, возвращает его.
3.  Если агент не существует, возвращает `None`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения и добавление агента
world = TinyWorld(name="MyWorld")
agent = TinyPerson(name="Alice")
world.add_agent(agent)

# Получение агента по имени
retrieved_agent = world.get_agent_by_name("Alice")
print(retrieved_agent.name)

# Попытка получить несуществующего агента
non_existent_agent = world.get_agent_by_name("Bob")
print(non_existent_agent)
```

#### `_handle_actions`

```python
@transactional
def _handle_actions(self, source: TinyPerson, actions: list)
```

**Назначение**: Обрабатывает действия, выполненные агентами.

**Параметры**:

-   `source` (TinyPerson): Агент, выполнивший действия.
-   `actions` (list): Список действий, выполненных агентом.

**Как работает функция**:

1.  Итерируется по списку действий.
2.  Извлекает тип действия из ключа `type` каждого действия.
3.  Извлекает содержимое действия из ключа `content`, если он существует.
4.  Извлекает цель действия из ключа `target`, если она существует.
5.  Записывает отладочное сообщение в лог об обработке действия.
6.  Вызывает соответствующие методы для обработки конкретных типов действий:
    -   `REACH_OUT`: вызывает `self._handle_reach_out`.
    -   `TALK`: вызывает `self._handle_talk`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения и агентов
world = TinyWorld(name="MyWorld")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
world.add_agents([agent1, agent2])

# Пример действия
actions = [
    {"type": "REACH_OUT", "content": "Hello", "target": "Bob"},
    {"type": "TALK", "content": "How are you?", "target": "Bob"},
]

# Обработка действий
world._handle_actions(agent1, actions)
```

#### `_handle_reach_out`

```python
@transactional
def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)
```

**Назначение**: Обрабатывает действие `REACH_OUT` (попытка установления контакта).

**Параметры**:

-   `source_agent` (TinyPerson): Агент, инициирующий действие.
-   `content` (str): Содержимое сообщения (не используется в данной реализации).
-   `target` (str): Имя агента, к которому обращаются.

**Как работает функция**:

1.  Получает целевого агента по имени с помощью `self.get_agent_by_name(target)`.
2.  Делает целевого агента доступным для исходного агента с помощью `source_agent.make_agent_accessible(target_agent)`.
3.  Делает исходного агента доступным для целевого агента с помощью `target_agent.make_agent_accessible(source_agent)`.
4.  Социализирует исходного агента, сообщая ему об успешном установлении контакта с целевым агентом.
5.  Социализирует целевого агента, сообщая ему об установлении контакта с исходным агентом.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения и агентов
world = TinyWorld(name="MyWorld")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
world.add_agents([agent1, agent2])

# Имитация действия REACH_OUT
world._handle_reach_out(agent1, "Hello", "Bob")
```

#### `_handle_talk`

```python
@transactional
def _handle_talk(self, source_agent: TinyPerson, content: str, target: str)
```

**Назначение**: Обрабатывает действие `TALK` (разговор между агентами).

**Параметры**:

-   `source_agent` (TinyPerson): Агент, инициирующий разговор.
-   `content` (str): Содержимое сообщения.
-   `target` (str): Имя агента, которому адресовано сообщение.

**Как работает функция**:

1.  Получает целевого агента по имени с помощью `self.get_agent_by_name(target)`.
2.  Записывает отладочное сообщение в лог о доставке сообщения.
3.  Если целевой агент найден (`target_agent is not None`):
    -   Вызывает метод `listen` целевого агента, чтобы доставить ему сообщение.