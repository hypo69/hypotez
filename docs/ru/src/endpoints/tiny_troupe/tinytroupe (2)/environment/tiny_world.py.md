# Модуль `tiny_world`

## Обзор

Модуль `tiny_world` предназначен для моделирования окружения, в котором действуют агенты (представленные классом `TinyPerson`). Он предоставляет базовый класс `TinyWorld`, который управляет агентами, временем, взаимодействиями и событиями в смоделированном мире.

## Подробней

`TinyWorld` является основой для создания симуляций, где агенты могут взаимодействовать друг с другом и с окружением. Он позволяет добавлять агентов, управлять временем симуляции, обрабатывать действия агентов и транслировать сообщения между ними. Класс также поддерживает применение "интервенций" - событий, которые могут влиять на ход симуляции. Модуль предоставляет инструменты для сохранения и восстановления состояния окружения, что позволяет создавать сложные и продолжительные симуляции.

## Классы

### `TinyWorld`

**Описание**: Базовый класс для моделирования окружения.

**Атрибуты**:
- `all_environments (dict)`: Словарь, содержащий все созданные окружения (`name -> environment`).
- `communication_display (bool)`: Флаг, определяющий, отображать ли сообщения окружения.
- `name (str)`: Имя окружения.
- `current_datetime (datetime)`: Текущее время в окружении.
- `broadcast_if_no_target (bool)`: Если `True`, действия транслируются, если цель не найдена.
- `simulation_id (Any)`: Идентификатор симуляции, к которой принадлежит окружение.
- `agents (list)`: Список агентов в окружении.
- `name_to_agent (dict)`: Словарь, сопоставляющий имена агентов с их экземплярами (`{agent_name: agent}`).
- `_interventions (list)`: Список интервенций, применяемых в окружении.
- `_displayed_communications_buffer (list)`: Буфер для хранения отображенных сообщений.
- `_target_display_communications_buffer (list)`: Временный буфер для целей сообщений.
- `_max_additional_targets_to_display (int)`: Максимальное количество дополнительных целей для отображения в сообщении.
- `console (Console)`: Объект консоли для вывода сообщений.

**Методы**:

- `__init__(self, name: str="A TinyWorld", agents=[], initial_datetime=datetime.now(), interventions=[], broadcast_if_no_target=True, max_additional_targets_to_display=3)`:
  Инициализирует окружение.

- `_step(self, timedelta_per_step=None)`:
  Выполняет один шаг в окружении, заставляя всех агентов действовать и обрабатывая их действия.

- `_advance_datetime(self, timedelta)`:
  Увеличивает текущее время в окружении на заданный интервал.

- `run(self, steps: int, timedelta_per_step=None, return_actions=False)`:
  Запускает симуляцию на заданное количество шагов.

- `skip(self, steps: int, timedelta_per_step=None)`:
  Пропускает заданное количество шагов в симуляции, не выполняя никаких действий.

- `run_minutes(self, minutes: int)`:
  Запускает симуляцию на заданное количество минут.

- `skip_minutes(self, minutes: int)`:
  Пропускает заданное количество минут в симуляции.

- `run_hours(self, hours: int)`:
  Запускает симуляцию на заданное количество часов.

- `skip_hours(self, hours: int)`:
  Пропускает заданное количество часов в симуляции.

- `run_days(self, days: int)`:
  Запускает симуляцию на заданное количество дней.

- `skip_days(self, days: int)`:
  Пропускает заданное количество дней в симуляции.

- `run_weeks(self, weeks: int)`:
  Запускает симуляцию на заданное количество недель.

- `skip_weeks(self, weeks: int)`:
  Пропускает заданное количество недель в симуляции.

- `run_months(self, months: int)`:
  Запускает симуляцию на заданное количество месяцев.

- `skip_months(self, months: int)`:
  Пропускает заданное количество месяцев в симуляции.

- `run_years(self, years: int)`:
  Запускает симуляцию на заданное количество лет.

- `skip_years(self, years: int)`:
  Пропускает заданное количество лет в симуляции.

- `add_agents(self, agents: list)`:
  Добавляет список агентов в окружение.

- `add_agent(self, agent: TinyPerson)`:
  Добавляет агента в окружение. Имена агентов должны быть уникальными.

- `remove_agent(self, agent: TinyPerson)`:
  Удаляет агента из окружения.

- `remove_all_agents(self)`:
  Удаляет всех агентов из окружения.

- `get_agent_by_name(self, name: str) -> TinyPerson`:
  Возвращает агента по имени.

- `add_intervention(self, intervention)`:
  Добавляет интервенцию в окружение.

- `_handle_actions(self, source: TinyPerson, actions: list)`:
  Обрабатывает действия, инициированные агентами.

- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`:
  Обрабатывает действие `REACH_OUT`, позволяющее агентам устанавливать доступность друг для друга.

- `_handle_talk(self, source_agent: TinyPerson, content: str, target: str)`:
  Обрабатывает действие `TALK`, доставляя сообщение указанному агенту.

- `broadcast(self, speech: str, source: AgentOrWorld=None)`:
  Доставляет сообщение всем агентам в окружении.

- `broadcast_thought(self, thought: str, source: AgentOrWorld=None)`:
  Транслирует мысль всем агентам в окружении.

- `broadcast_internal_goal(self, internal_goal: str)`:
  Транслирует внутреннюю цель всем агентам в окружении.

- `broadcast_context_change(self, context: list)`:
  Транслирует изменение контекста всем агентам в окружении.

- `make_everyone_accessible(self)`:
  Делает всех агентов в окружении доступными друг для друга.

- `_display_step_communication(self, cur_step, total_steps, timedelta_per_step=None)`:
  Отображает информацию о текущем шаге симуляции.

- `_display_intervention_communication(self, intervention)`:
  Отображает информацию об интервенции.

- `_push_and_display_latest_communication(self, communication)`:
  Добавляет сообщение в буфер и отображает его.

- `pop_and_display_latest_communications(self)`:
  Извлекает и отображает последние сообщения из буфера.

- `_display(self, communication: dict)`:
  Отображает сообщение в консоли.

- `clear_communications_buffer(self)`:
  Очищает буфер сообщений.

- `__repr__(self)`:
  Возвращает строковое представление объекта `TinyWorld`.

- `_pretty_step(self, cur_step, total_steps, timedelta_per_step=None)`:
  Форматирует строку для отображения текущего шага симуляции.

- `_pretty_intervention(self, intervention)`:
  Форматирует строку для отображения информации об интервенции.

- `pp_current_interactions(self, simplified=True, skip_system=True)`:
  Отображает текущие сообщения от агентов в окружении в удобном формате.

- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info: bool=True)`:
  Возвращает строку с текущими сообщениями агентов в окружении.

- `encode_complete_state(self) -> dict`:
  Кодирует полное состояние окружения в словарь.

- `decode_complete_state(self, state: dict)`:
  Декодирует состояние окружения из словаря.

- `add_environment(environment)`:
  Добавляет окружение в список всех окружений.

- `set_simulation_for_free_environments(simulation)`:
  Назначает симуляцию для свободных окружений.

- `get_environment_by_name(name: str)`:
  Возвращает окружение по имени.

- `clear_environments()`:
  Очищает список всех окружений.

**Принцип работы**:

1.  **Инициализация**: При создании экземпляра `TinyWorld` задается имя окружения, список агентов, начальное время и список интервенций.
2.  **Управление временем**: Методы `run_*` и `skip_*` позволяют управлять временем в симуляции, выполняя шаги или пропуская их.
3.  **Действия агентов**: Метод `_step` выполняет один шаг симуляции, заставляя каждого агента выполнить действие. Действия агентов обрабатываются методом `_handle_actions`.
4.  **Взаимодействие агентов**: Методы `broadcast`, `_handle_talk` и `_handle_reach_out` позволяют агентам взаимодействовать друг с другом, обмениваясь сообщениями и устанавливая доступность.
5.  **Интервенции**: Интервенции - это события, которые могут влиять на ход симуляции. Они применяются на каждом шаге, если выполняются их условия.
6.  **Сохранение и восстановление состояния**: Методы `encode_complete_state` и `decode_complete_state` позволяют сохранять и восстанавливать состояние окружения, что полезно для создания продолжительных симуляций.
7.  **Отображение информации**: Методы `_display_*` позволяют отображать информацию о ходе симуляции, действиях агентов и интервенциях.

```
          Начало
          ↓
  → Проверка предусловий интервенций
  │       ↓
  │       Да → Применение эффектов интервенций
  │       ↓
  │       Нет
  │       ↓
  → Действия агентов (вызов agent.act())
          ↓
  → Обработка действий агентов (_handle_actions)
          ↓
          Конец
```

**Примеры**:

```python
from datetime import datetime, timedelta
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Создание окружения
world = TinyWorld(name='MyWorld', initial_datetime=datetime(2024, 1, 1))

# Создание агентов
agent1 = TinyPerson(name='Alice')
agent2 = TinyPerson(name='Bob')

# Добавление агентов в окружение
world.add_agents([agent1, agent2])

# Запуск симуляции на 10 шагов с интервалом в 1 день
world.run(steps=10, timedelta_per_step=timedelta(days=1))

# Вывод текущего времени в окружении
print(world.current_datetime)

# Получение агента по имени
alice = world.get_agent_by_name('Alice')
print(alice)
```

## Функции

### `add_environment`

```python
 @staticmethod
 def add_environment(environment):
    """
    Adds an environment to the list of all environments. Environment names must be unique,
    so if an environment with the same name already exists, an error is raised.
    """
```

**Назначение**: Добавляет окружение в статический список всех окружений, проверяя уникальность имени.

**Параметры**:
- `environment`: Экземпляр окружения `TinyWorld`, который нужно добавить.

**Возвращает**: Ничего.

**Вызывает исключения**:
- `ValueError`: Если окружение с таким именем уже существует.

**Как работает функция**:

1.  Проверяет, существует ли уже окружение с таким же именем в статическом словаре `TinyWorld.all_environments`.
2.  Если окружение с таким именем уже существует, выбрасывает исключение `ValueError` с соответствующим сообщением.
3.  Если имя уникально, добавляет окружение в словарь `TinyWorld.all_environments`, где ключом является имя окружения, а значением - сам объект окружения.

```
  Начало
  ↓
→ Проверка наличия окружения с таким же именем
  ↓
  Да → Выброс исключения ValueError
  ↓
  Нет
  ↓
→ Добавление окружения в TinyWorld.all_environments
  ↓
  Конец
```

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world1 = TinyWorld(name='World1')

# Добавление окружения
TinyWorld.add_environment(world1)

# Попытка добавления окружения с тем же именем вызовет ошибку
try:
    world2 = TinyWorld(name='World1')
    TinyWorld.add_environment(world2)
except ValueError as ex:
    print(f"Ошибка: {ex}")
```

### `set_simulation_for_free_environments`

```python
    @staticmethod
    def set_simulation_for_free_environments(simulation):
        """
        Sets the simulation if it is None. This allows free environments to be captured by specific simulation scopes
        if desired.
        """
```

**Назначение**: Устанавливает связь между всеми "свободными" (не привязанными к конкретной симуляции) окружениями и заданной симуляцией.

**Параметры**:
- `simulation`: Объект симуляции, который нужно связать со свободными окружениями.

**Возвращает**: Ничего.

**Как работает функция**:

1.  Перебирает все окружения, хранящиеся в статическом словаре `TinyWorld.all_environments`.
2.  Для каждого окружения проверяет, установлено ли у него значение `simulation_id` в `None`. Это означает, что окружение "свободно" и не привязано к конкретной симуляции.
3.  Если окружение свободно, вызывает метод `add_environment` объекта симуляции, передавая текущее окружение в качестве аргумента. Таким образом, окружение привязывается к данной симуляции.

```
  Начало
  ↓
→ Перебор всех окружений в TinyWorld.all_environments
  ↓
→ Проверка simulation_id == None
  ↓
  Да → simulation.add_environment(environment)
  ↓
  Нет
  ↓
  Конец
```

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

class MockSimulation:
    def __init__(self):
        self.environments = []

    def add_environment(self, env):
        self.environments.append(env)

# Создание окружений
world1 = TinyWorld(name='World1')
world2 = TinyWorld(name='World2')

# Создание симуляции
simulation = MockSimulation()

# Привязка свободных окружений к симуляции
TinyWorld.set_simulation_for_free_environments(simulation)

# Проверка, что окружения были добавлены в симуляцию
print(len(simulation.environments))
```

### `get_environment_by_name`

```python
    @staticmethod
    def get_environment_by_name(name: str):
        """
        Returns the environment with the specified name. If no environment with that name exists, 
        returns None.

        Args:
            name (str): The name of the environment to return.

        Returns:
            TinyWorld: The environment with the specified name.
        """
```

**Назначение**: Получает окружение из статического списка всех окружений по имени.

**Параметры**:
- `name (str)`: Имя искомого окружения.

**Возвращает**:
- `TinyWorld`: Объект окружения, если он найден.
- `None`: Если окружение с указанным именем не найдено.

**Как работает функция**:

1.  Проверяет, существует ли окружение с указанным именем в статическом словаре `TinyWorld.all_environments`.
2.  Если окружение с указанным именем существует, возвращает соответствующий объект окружения.
3.  Если окружение с указанным именем не существует, возвращает `None`.

```
  Начало
  ↓
→ Проверка наличия окружения с именем name в TinyWorld.all_environments
  ↓
  Да → Возврат окружения
  ↓
  Нет
  ↓
→ Возврат None
  ↓
  Конец
```

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world1 = TinyWorld(name='World1')
TinyWorld.add_environment(world1)

# Получение окружения по имени
retrieved_world = TinyWorld.get_environment_by_name('World1')
print(retrieved_world)

# Попытка получения окружения с несуществующим именем
non_existent_world = TinyWorld.get_environment_by_name('NonExistentWorld')
print(non_existent_world)
```

### `clear_environments`

```python
    @staticmethod
    def clear_environments():
        """
        Clears the list of all environments.
        """
```

**Назначение**: Очищает статический список всех окружений.

**Параметры**: Отсутствуют.

**Возвращает**: Ничего.

**Как работает функция**:

1.  Присваивает статическому словарю `TinyWorld.all_environments` пустой словарь, удаляя все существующие окружения.

```
  Начало
  ↓
→ TinyWorld.all_environments = {}
  ↓
  Конец
```

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Создание окружения
world1 = TinyWorld(name='World1')
TinyWorld.add_environment(world1)

# Очистка всех окружений
TinyWorld.clear_environments()

# Проверка, что список окружений пуст
retrieved_world = TinyWorld.get_environment_by_name('World1')
print(retrieved_world)