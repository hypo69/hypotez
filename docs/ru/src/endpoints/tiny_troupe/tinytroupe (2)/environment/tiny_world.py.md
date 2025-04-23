# Модуль `tiny_world`

## Обзор

Модуль `tiny_world` предоставляет класс `TinyWorld`, который является базовым классом для создания виртуальных сред, в которых взаимодействуют агенты (`TinyPerson`). Он позволяет моделировать поведение агентов во времени, управлять событиями в среде и сохранять/восстанавливать состояние среды.

## Подробнее

Модуль определяет основную логику для управления виртуальным миром, включая добавление и удаление агентов, обработку действий агентов, моделирование течения времени и обеспечение взаимодействия между агентами. `TinyWorld` служит контейнером для агентов и управляет их взаимодействиями, а также предоставляет инструменты для моделирования изменений в среде.

## Классы

### `TinyWorld`

**Описание**: Базовый класс для создания виртуальных сред.

**Атрибуты**:
- `all_environments` (dict): Словарь, содержащий все созданные окружения (`name -> environment`).
- `communication_display` (bool): Флаг, определяющий, отображать ли коммуникации в окружении.
- `name` (str): Имя окружения.
- `current_datetime` (datetime): Текущая дата и время в окружении.
- `broadcast_if_no_target` (bool): Если `True`, действия транслируются, если цель действия не найдена.
- `simulation_id` (Any): Идентификатор симуляции, к которой принадлежит окружение.
- `agents` (list): Список агентов в окружении.
- `name_to_agent` (dict): Словарь, отображающий имена агентов в объекты агентов (`{agent_name: agent, ...}`).
- `_interventions` (list): Список интервенций, применяемых в окружении на каждом шаге симуляции.
- `_displayed_communications_buffer` (list): Буфер отображаемых коммуникаций.
- `_target_display_communications_buffer` (list): Временный буфер для целей коммуникаций.
- `_max_additional_targets_to_display` (int): Максимальное количество дополнительных целей для отображения в коммуникации.
- `console` (Console): Объект консоли для вывода информации.

**Методы**:

- `__init__(self, name: str="A TinyWorld", agents=[], initial_datetime=datetime.now(), interventions=[], broadcast_if_no_target=True, max_additional_targets_to_display=3)`: Инициализирует окружение.
- `_step(self, timedelta_per_step=None)`: Выполняет один шаг в окружении.
- `_advance_datetime(self, timedelta)`: Сдвигает текущую дату и время в окружении на указанный `timedelta`.
- `run(self, steps: int, timedelta_per_step=None, return_actions=False)`: Запускает окружение на заданное количество шагов.
- `skip(self, steps: int, timedelta_per_step=None)`: Пропускает заданное количество шагов в окружении без выполнения действий.
- `run_minutes(self, minutes: int)`: Запускает окружение на заданное количество минут.
- `skip_minutes(self, minutes: int)`: Пропускает заданное количество минут в окружении.
- `run_hours(self, hours: int)`: Запускает окружение на заданное количество часов.
- `skip_hours(self, hours: int)`: Пропускает заданное количество часов в окружении.
- `run_days(self, days: int)`: Запускает окружение на заданное количество дней.
- `skip_days(self, days: int)`: Пропускает заданное количество дней в окружении.
- `run_weeks(self, weeks: int)`: Запускает окружение на заданное количество недель.
- `skip_weeks(self, weeks: int)`: Пропускает заданное количество недель в окружении.
- `run_months(self, months: int)`: Запускает окружение на заданное количество месяцев.
- `skip_months(self, months: int)`: Пропускает заданное количество месяцев в окружении.
- `run_years(self, years: int)`: Запускает окружение на заданное количество лет.
- `skip_years(self, years: int)`: Пропускает заданное количество лет в окружении.
- `add_agents(self, agents: list)`: Добавляет список агентов в окружение.
- `add_agent(self, agent: TinyPerson)`: Добавляет агента в окружение.
- `remove_agent(self, agent: TinyPerson)`: Удаляет агента из окружения.
- `remove_all_agents(self)`: Удаляет всех агентов из окружения.
- `get_agent_by_name(self, name: str) -> TinyPerson`: Возвращает агента по имени.
- `add_intervention(self, intervention)`: Добавляет интервенцию в окружение.
- `_handle_actions(self, source: TinyPerson, actions: list)`: Обрабатывает действия, выполняемые агентами.
- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `REACH_OUT`.
- `_handle_talk(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `TALK`.
- `broadcast(self, speech: str, source: AgentOrWorld=None)`: Отправляет сообщение всем агентам в окружении.
- `broadcast_thought(self, thought: str, source: AgentOrWorld=None)`: Отправляет мысль всем агентам в окружении.
- `broadcast_internal_goal(self, internal_goal: str)`: Отправляет внутреннюю цель всем агентам в окружении.
- `broadcast_context_change(self, context: list)`: Отправляет изменение контекста всем агентам в окружении.
- `make_everyone_accessible(self)`: Делает всех агентов в окружении доступными друг для друга.
- `_display_step_communication(self, cur_step, total_steps, timedelta_per_step=None)`: Отображает текущий шаг симуляции.
- `_display_intervention_communication(self, intervention)`: Отображает коммуникацию об интервенции.
- `_push_and_display_latest_communication(self, communication)`: Добавляет и отображает последнюю коммуникацию.
- `pop_and_display_latest_communications(self)`: Извлекает и отображает последние коммуникации.
- `_display(self, communication: dict)`: Отображает коммуникацию.
- `clear_communications_buffer(self)`: Очищает буфер коммуникаций.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyWorld`.
- `_pretty_step(self, cur_step, total_steps, timedelta_per_step=None)`: Форматирует отображение шага симуляции.
- `_pretty_intervention(self, intervention)`: Форматирует отображение интервенции.
- `pp_current_interactions(self, simplified=True, skip_system=True)`: Выводит текущие взаимодействия агентов в отформатированном виде.
- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info: bool=True)`: Возвращает строку с текущими взаимодействиями агентов в отформатированном виде.
- `encode_complete_state(self) -> dict`: Кодирует полное состояние окружения в словарь.
- `decode_complete_state(self, state: dict)`: Декодирует полное состояние окружения из словаря.
- `add_environment(environment)`: Добавляет окружение в список всех окружений.
- `set_simulation_for_free_environments(simulation)`: Устанавливает симуляцию для свободных окружений.
- `get_environment_by_name(name: str)`: Возвращает окружение по имени.
- `clear_environments()`: Очищает список всех окружений.

### `__init__`
```python
def __init__(self, name: str="A TinyWorld", agents=[], 
                 initial_datetime=datetime.now(),
                 interventions=[],
                 broadcast_if_no_target=True,
                 max_additional_targets_to_display=3):
```
**Назначение**: Инициализирует окружение `TinyWorld`.

**Параметры**:
- `name` (str, optional): Имя окружения. По умолчанию "A TinyWorld".
- `agents` (list, optional): Список агентов для добавления в окружение. По умолчанию пустой список.
- `initial_datetime` (datetime, optional): Начальная дата и время окружения. По умолчанию текущее время.
- `interventions` (list, optional): Список интервенций для применения в окружении. По умолчанию пустой список.
- `broadcast_if_no_target` (bool, optional): Флаг, определяющий, следует ли транслировать действия, если цель не найдена. По умолчанию `True`.
- `max_additional_targets_to_display` (int, optional): Максимальное количество дополнительных целей для отображения в коммуникациях. По умолчанию 3.

**Как работает функция**:
- Функция инициализирует атрибуты окружения, такие как имя, текущее время, список агентов и интервенций.
- Добавляет окружение в общий список окружений `TinyWorld.all_environments`.
- Добавляет переданных агентов в окружение, используя метод `add_agents`.

**Примеры**:
```python
from datetime import datetime
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения с именем "MyWorld" и начальным временем 1 января 2024
initial_datetime = datetime(2024, 1, 1)
world = TinyWorld(name="MyWorld", initial_datetime=initial_datetime)

# Создание окружения с двумя агентами
from tinytroupe.agent.agent import TinyPerson
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
world = TinyWorld(agents=[agent1, agent2])
```

### `_step`
```python
@transactional
def _step(self, timedelta_per_step=None):
```
**Назначение**: Выполняет один шаг симуляции в окружении.

**Параметры**:
- `timedelta_per_step` (timedelta, optional): Временной интервал для одного шага. По умолчанию `None`.

**Как работает функция**:
1. **Сдвиг времени**: Увеличивает текущее время окружения на `timedelta_per_step`, если он указан.
2. **Применение интервенций**: Проверяет и применяет интервенции, если выполнены их предусловия.
3. **Действия агентов**: Каждый агент в окружении выполняет свои действия, и результаты этих действий обрабатываются.
4. **Возвращает действия агентов**: Функция возвращает словарь, содержащий действия, выполненные каждым агентом на этом шаге.

**Примеры**:
```python
from datetime import timedelta
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Выполнение одного шага с интервалом в 1 час
actions = world._step(timedelta_per_step=timedelta(hours=1))
print(actions)
```

### `_advance_datetime`
```python
def _advance_datetime(self, timedelta):
```
**Назначение**: Увеличивает текущее время окружения на указанный временной интервал.

**Параметры**:
- `timedelta` (timedelta): Временной интервал для увеличения текущего времени.

**Как работает функция**:
- Если указан `timedelta`, текущее время окружения увеличивается на этот интервал.
- Если `timedelta` не указан, функция логирует информационное сообщение о том, что время не было увеличено.

**Примеры**:
```python
from datetime import timedelta
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Увеличение времени на 30 минут
world._advance_datetime(timedelta=timedelta(minutes=30))
print(world.current_datetime)
```

### `run`
```python
@transactional
def run(self, steps: int, timedelta_per_step=None, return_actions=False):
```
**Назначение**: Запускает симуляцию в окружении на указанное количество шагов.

**Параметры**:
- `steps` (int): Количество шагов для выполнения симуляции.
- `timedelta_per_step` (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.
- `return_actions` (bool, optional): Если `True`, возвращает список действий, выполненных агентами. По умолчанию `False`.

**Как работает функция**:
1. **Инициализация**: Создает пустой список `agents_actions_over_time` для хранения действий агентов, если `return_actions` равен `True`.
2. **Цикл по шагам**: Для каждого шага в диапазоне `steps`:
   - Логирует информацию о текущем шаге симуляции.
   - Отображает коммуникацию о текущем шаге, если `TinyWorld.communication_display` равен `True`.
   - Выполняет один шаг симуляции, вызывая метод `_step` с указанным `timedelta_per_step`.
   - Если `return_actions` равен `True`, добавляет действия агентов в список `agents_actions_over_time`.
3. **Возврат результатов**: Если `return_actions` равен `True`, возвращает список действий агентов `agents_actions_over_time`.

**Примеры**:
```python
from datetime import timedelta
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск симуляции на 5 шагов с интервалом в 1 день и возвратом действий агентов
actions = world.run(steps=5, timedelta_per_step=timedelta(days=1), return_actions=True)
print(actions)

# Запуск симуляции на 10 шагов без возврата действий агентов
world.run(steps=10)
```

### `skip`
```python
@transactional
def skip(self, steps: int, timedelta_per_step=None):
```
**Назначение**: Пропускает заданное количество шагов в окружении, увеличивая текущее время, но не выполняя никаких действий агентов.

**Параметры**:
- `steps` (int): Количество шагов для пропуска.
- `timedelta_per_step` (timedelta, optional): Временной интервал между шагами. По умолчанию `None`.

**Как работает функция**:
- Увеличивает текущее время окружения на `steps * timedelta_per_step`, используя метод `_advance_datetime`.

**Примеры**:
```python
from datetime import timedelta
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 7 дней
world.skip(steps=7, timedelta_per_step=timedelta(days=1))
print(world.current_datetime)
```

### `run_minutes`
```python
def run_minutes(self, minutes: int):
```
**Назначение**: Запускает окружение на заданное количество минут.

**Параметры**:
- `minutes` (int): Количество минут для запуска окружения.

**Как работает функция**:
- Вызывает метод `run` с количеством шагов, равным `minutes`, и временным интервалом в 1 минуту.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск окружения на 60 минут
world.run_minutes(minutes=60)
```

### `skip_minutes`
```python
def skip_minutes(self, minutes: int):
```
**Назначение**: Пропускает заданное количество минут в окружении.

**Параметры**:
- `minutes` (int): Количество минут для пропуска.

**Как работает функция**:
- Вызывает метод `skip` с количеством шагов, равным `minutes`, и временным интервалом в 1 минуту.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 120 минут
world.skip_minutes(minutes=120)
```

### `run_hours`
```python
def run_hours(self, hours: int):
```
**Назначение**: Запускает окружение на заданное количество часов.

**Параметры**:
- `hours` (int): Количество часов для запуска окружения.

**Как работает функция**:
- Вызывает метод `run` с количеством шагов, равным `hours`, и временным интервалом в 1 час.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск окружения на 24 часа
world.run_hours(hours=24)
```

### `skip_hours`
```python
def skip_hours(self, hours: int):
```
**Назначение**: Пропускает заданное количество часов в окружении.

**Параметры**:
- `hours` (int): Количество часов для пропуска.

**Как работает функция**:
- Вызывает метод `skip` с количеством шагов, равным `hours`, и временным интервалом в 1 час.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 48 часов
world.skip_hours(hours=48)
```

### `run_days`
```python
def run_days(self, days: int):
```
**Назначение**: Запускает окружение на заданное количество дней.

**Параметры**:
- `days` (int): Количество дней для запуска окружения.

**Как работает функция**:
- Вызывает метод `run` с количеством шагов, равным `days`, и временным интервалом в 1 день.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск окружения на 7 дней
world.run_days(days=7)
```

### `skip_days`
```python
def skip_days(self, days: int):
```
**Назначение**: Пропускает заданное количество дней в окружении.

**Параметры**:
- `days` (int): Количество дней для пропуска.

**Как работает функция**:
- Вызывает метод `skip` с количеством шагов, равным `days`, и временным интервалом в 1 день.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 14 дней
world.skip_days(days=14)
```

### `run_weeks`
```python
def run_weeks(self, weeks: int):
```
**Назначение**: Запускает окружение на заданное количество недель.

**Параметры**:
- `weeks` (int): Количество недель для запуска окружения.

**Как работает функция**:
- Вызывает метод `run` с количеством шагов, равным `weeks`, и временным интервалом в 1 неделю.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск окружения на 4 недели
world.run_weeks(weeks=4)
```

### `skip_weeks`
```python
def skip_weeks(self, weeks: int):
```
**Назначение**: Пропускает заданное количество недель в окружении.

**Параметры**:
- `weeks` (int): Количество недель для пропуска.

**Как работает функция**:
- Вызывает метод `skip` с количеством шагов, равным `weeks`, и временным интервалом в 1 неделю.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 8 недель
world.skip_weeks(weeks=8)
```

### `run_months`
```python
def run_months(self, months: int):
```
**Назначение**: Запускает окружение на заданное количество месяцев.

**Параметры**:
- `months` (int): Количество месяцев для запуска окружения.

**Как работает функция**:
- Вызывает метод `run` с количеством шагов, равным `months`, и временным интервалом в 4 недели (приблизительно месяц).

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск окружения на 6 месяцев
world.run_months(months=6)
```

### `skip_months`
```python
def skip_months(self, months: int):
```
**Назначение**: Пропускает заданное количество месяцев в окружении.

**Параметры**:
- `months` (int): Количество месяцев для пропуска.

**Как работает функция**:
- Вызывает метод `skip` с количеством шагов, равным `months`, и временным интервалом в 4 недели (приблизительно месяц).

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 12 месяцев
world.skip_months(months=12)
```

### `run_years`
```python
def run_years(self, years: int):
```
**Назначение**: Запускает окружение на заданное количество лет.

**Параметры**:
- `years` (int): Количество лет для запуска окружения.

**Как работает функция**:
- Вызывает метод `run` с количеством шагов, равным `years`, и временным интервалом в 365 дней (приблизительно год).

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Запуск окружения на 2 года
world.run_years(years=2)
```

### `skip_years`
```python
def skip_years(self, years: int):
```
**Назначение**: Пропускает заданное количество лет в окружении.

**Параметры**:
- `years` (int): Количество лет для пропуска.

**Как работает функция**:
- Вызывает метод `skip` с количеством шагов, равным `years`, и временным интервалом в 365 дней (приблизительно год).

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld

# Создание окружения
world = TinyWorld()

# Пропуск 5 лет
world.skip_years(years=5)
```

### `add_agents`
```python
def add_agents(self, agents: list):
```
**Назначение**: Добавляет список агентов в окружение.

**Параметры**:
- `agents` (list): Список агентов для добавления в окружение.

**Как работает функция**:
- Перебирает список агентов и добавляет каждого агента в окружение с помощью метода `add_agent`.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")

# Добавление агентов в окружение
world.add_agents([agent1, agent2])
print(world.agents)
```

### `add_agent`
```python
def add_agent(self, agent: TinyPerson):
```
**Назначение**: Добавляет агента в окружение.

**Параметры**:
- `agent` (TinyPerson): Агент для добавления в окружение.

**Как работает функция**:
1. **Проверка уникальности имени**:
   - Проверяет, существует ли агент с таким же именем в окружении. Если да, вызывает исключение `ValueError`.
2. **Добавление агента**:
   - Устанавливает свойство `environment` агента равным текущему окружению.
   - Добавляет агента в список `agents` окружения.
   - Добавляет агента в словарь `name_to_agent`, где ключом является имя агента.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агента
agent = TinyPerson(name="Alice")

# Добавление агента в окружение
world.add_agent(agent)
print(world.agents)
```

### `remove_agent`
```python
def remove_agent(self, agent: TinyPerson):
```
**Назначение**: Удаляет агента из окружения.

**Параметры**:
- `agent` (TinyPerson): Агент для удаления из окружения.

**Как работает функция**:
1. **Удаление из списков**:
   - Удаляет агента из списка `agents` окружения.
   - Удаляет агента из словаря `name_to_agent` окружения.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агента
agent = TinyPerson(name="Alice")

# Добавление агента в окружение
world.add_agent(agent)

# Удаление агента из окружения
world.remove_agent(agent)
print(world.agents)
```

### `remove_all_agents`
```python
def remove_all_agents(self):
```
**Назначение**: Удаляет всех агентов из окружения.

**Как работает функция**:
1. **Очистка списков**:
   - Очищает список `agents` окружения.
   - Очищает словарь `name_to_agent` окружения.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")

# Добавление агентов в окружение
world.add_agents([agent1, agent2])

# Удаление всех агентов из окружения
world.remove_all_agents()
print(world.agents)
```

### `get_agent_by_name`
```python
def get_agent_by_name(self, name: str) -> TinyPerson:
```
**Назначение**: Возвращает агента из окружения по его имени.

**Параметры**:
- `name` (str): Имя агента, которого необходимо получить.

**Возвращает**:
- `TinyPerson`: Агент с указанным именем, или `None`, если агент не найден.

**Как работает функция**:
- Проверяет, существует ли агент с указанным именем в словаре `name_to_agent`.
- Если агент существует, возвращает его.
- Если агент не существует, возвращает `None`.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агента
agent = TinyPerson(name="Alice")

# Добавление агента в окружение
world.add_agent(agent)

# Получение агента по имени
retrieved_agent = world.get_agent_by_name("Alice")
print(retrieved_agent)

# Попытка получения агента с несуществующим именем
non_existent_agent = world.get_agent_by_name("Charlie")
print(non_existent_agent)
```

### `add_intervention`
```python
def add_intervention(self, intervention):
```
**Назначение**: Добавляет интервенцию в окружение.

**Параметры**:
- `intervention`: Интервенция для добавления в окружение.

**Как работает функция**:
- Добавляет переданную интервенцию в список `_interventions` окружения.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.intervention import Intervention  # Предполагается, что есть класс Intervention

# Создание окружения
world = TinyWorld()

# Создание интервенции
intervention = Intervention(name="Example Intervention")

# Добавление интервенции в окружение
world.add_intervention(intervention)
print(world._interventions)
```

### `_handle_actions`
```python
@transactional
def _handle_actions(self, source: TinyPerson, actions: list):
```
**Назначение**: Обрабатывает действия, выполненные агентами.

**Параметры**:
- `source` (TinyPerson): Агент, выполнивший действия.
- `actions` (list): Список действий, выполненных агентом. Каждое действие представлено в формате JSON.

**Как работает функция**:
1. **Перебор действий**:
   - Перебирает список действий `actions`.
2. **Определение типа действия**:
   - Для каждого действия определяет его тип (`action_type`).
3. **Обработка действия**:
   - В зависимости от типа действия вызывает соответствующий метод обработки:
     - Если `action_type` равен `"REACH_OUT"`, вызывает метод `_handle_reach_out`.
     - Если `action_type` равен `"TALK"`, вызывает метод `_handle_talk`.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агента
agent = TinyPerson(name="Alice")

# Добавление агента в окружение
world.add_agent(agent)

# Создание действий
actions = [
    {"type": "REACH_OUT", "content": "Hello", "target": "Bob"},
    {"type": "TALK", "content": "How are you?", "target": "Bob"}
]

# Обработка действий агента
world._handle_actions(agent, actions)
```

### `_handle_reach_out`
```python
@transactional
def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
```
**Назначение**: Обрабатывает действие `REACH_OUT`, позволяющее агентам устанавливать связь друг с другом.

**Параметры**:
- `source_agent` (TinyPerson): Агент, инициировавший действие `REACH_OUT`.
- `content` (str): Содержание сообщения (не используется в данной реализации).
- `target` (str): Имя агента, к которому направлено действие `REACH_OUT`.

**Как работает функция**:
1. **Поиск целевого агента**:
   - Получает целевого агента по имени, используя метод `get_agent_by_name`.
2. **Установление доступности**:
   - Если целевой агент найден:
     - Делает исходного агента доступным для целевого агента, вызывая метод `make_agent_accessible` у исходного агента.
     - Делает целевого агента доступным для исходного агента, вызывая метод `make_agent_accessible` у целевого агента.
     - Отправляет сообщения обоим агентам, уведомляющие об успешном установлении связи, используя метод `socialize`.
3. **Обработка ненайденного агента**:
   - Если целевой агент не найден, логирует отладочное сообщение об ошибке.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")

# Добавление агентов в окружение
world.add_agents([agent1, agent2])

# Обработка действия REACH_OUT
world._handle_reach_out(agent1, "Hello", "Bob")
```

### `_handle_talk`
```python
@transactional
def _handle_talk(self, source_agent: TinyPerson, content: str, target: str):
```
**Назначение**: Обрабатывает действие `TALK`, отправляя сообщение от одного агента к другому.

**Параметры**:
- `source_agent` (TinyPerson): Агент, отправляющий сообщение.
- `content` (str): Содержание сообщения.
- `target` (str): Имя агента, которому предназначено сообщение.

**Как работает функция**:
1. **Поиск целевого агента**:
   - Получает целевого агента по имени, используя метод `get_agent_by_name`.
2. **Доставка сообщения**:
   - Если целевой агент найден:
     - Отправляет сообщение целевому агенту, вызывая метод `listen` у целевого агента.
   - Если целевой агент не найден и включена трансляция:
     - Транслирует сообщение всем агентам в окружении, вызывая метод `broadcast`.

**Примеры**:
```python
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.agent.agent import TinyPerson

# Создание окружения
world = TinyWorld()

# Создание агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")

# Добавление агентов в окружение
world.add_agents([agent1, agent2])

# Обработка действия TALK
world._handle_talk(agent1, "Hello, Bob!", "Bob")

# Обработка действия TALK с несуществующим целевым агентом и включенной трансляцией
world._handle_talk(agent1, "Hello, everyone!", "Charlie")
```

### `broadcast`
```python
@transactional
def broadcast(self, speech: str, source: AgentOrWorld=None):
```
**Назначение**: Отправляет сообщение (речь) всем агентам в окружении, исключая источник сообщения.

**Параметры**:
-