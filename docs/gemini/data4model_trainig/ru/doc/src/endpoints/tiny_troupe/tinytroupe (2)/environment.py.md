# Модуль environment

## Обзор

Модуль предоставляет классы для моделирования окружения, в котором взаимодействуют агенты, такие как `TinyWorld` и `TinySocialNetwork`. Он определяет базовую логику для управления агентами, обработки их действий и моделирования течения времени.

## Подробней

Модуль содержит классы для создания виртуальных миров, в которых "живут" и взаимодействуют агенты (`TinyPerson`). Здесь определены основные механизмы управления временем в этих мирах, добавления и удаления агентов, а также обработки действий, которые агенты предпринимают.
`TinyWorld` предоставляет базовый функционал, а `TinySocialNetwork` расширяет его, добавляя возможность моделирования социальных связей между агентами.

## Классы

### `TinyWorld`

**Описание**: Базовый класс для создания виртуальных сред.

**Атрибуты**:

- `all_environments (dict)`: Словарь, содержащий все созданные окружения, где ключ - имя окружения, а значение - сам объект окружения.
- `communication_display (bool)`: Определяет, отображать ли сообщения агентов в консоли (по умолчанию `True`).
- `name (str)`: Название окружения.
- `current_datetime (datetime)`: Текущее время в окружении.
- `broadcast_if_no_target (bool)`: Если `True`, то действия агента, направленные на несуществующего агента, будут транслироваться всем агентам в окружении.
- `simulation_id (Any)`: Идентификатор симуляции, к которой принадлежит окружение.
- `agents (list)`: Список агентов, находящихся в окружении.
- `name_to_agent (dict)`: Словарь, связывающий имена агентов с их объектами для быстрого доступа.
- `_displayed_communications_buffer (list)`: Буфер для хранения сообщений агентов, отображаемых в консоли.
- `console (Console)`: Объект консоли `rich`, используемый для отображения информации.

**Методы**:

- `__init__(self, name: str="A TinyWorld", agents=[], initial_datetime=datetime.datetime.now(), broadcast_if_no_target=True)`: Инициализирует окружение, задает его имя, добавляет агентов, устанавливает начальное время и определяет политику трансляции действий.
- `_step(self, timedelta_per_step=None)`: Выполняет один шаг симуляции, заставляя каждого агента действовать и обрабатывая результаты их действий.
- `_advance_datetime(self, timedelta)`: Увеличивает текущее время окружения на заданный интервал.
- `run(self, steps: int, timedelta_per_step=None, return_actions=False)`: Запускает симуляцию на заданное количество шагов.
- `skip(self, steps: int, timedelta_per_step=None)`: Пропускает заданное количество шагов симуляции, просто сдвигая время, без выполнения действий агентов.
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
- `_handle_actions(self, source: TinyPerson, actions: list)`: Обрабатывает действия, совершенные агентами.
- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `REACH_OUT`, позволяющее агентам устанавливать связь друг с другом.
- `_handle_talk(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `TALK`, доставляя сообщение от одного агента к другому.
- `broadcast(self, speech: str, source: AgentOrWorld=None)`: Рассылает сообщение всем агентам в окружении.
- `broadcast_thought(self, thought: str, source: AgentOrWorld=None)`: Рассылает мысль всем агентам в окружении.
- `broadcast_internal_goal(self, internal_goal: str)`: Рассылает внутреннюю цель всем агентам в окружении.
- `broadcast_context_change(self, context:list)`: Рассылает изменение контекста всем агентам в окружении.
- `make_everyone_accessible(self)`: Делает всех агентов доступными друг для друга.
- `_display_communication(self, cur_step, total_steps, kind, timedelta_per_step=None)`: Отображает текущее состояние симуляции.
- `_push_and_display_latest_communication(self, rendering)`: Добавляет сообщение в буфер и отображает его.
- `pop_and_display_latest_communications(self)`: Извлекает и отображает все накопленные сообщения.
- `_display(self, communication)`: Отображает сообщение в консоли.
- `clear_communications_buffer(self)`: Очищает буфер сообщений.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyWorld`.
- `_pretty_step(self, cur_step, total_steps, timedelta_per_step=None)`: Форматирует сообщение о текущем шаге симуляции.
- `pp_current_interactions(self, simplified=True, skip_system=True)`: Выводит в консоль текущие взаимодействия между агентами.
- `pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info:bool=True)`: Возвращает отформатированную строку с текущими сообщениями агентов в этом окружении.
- `encode_complete_state(self) -> dict`: Кодирует полное состояние окружения в словарь.
- `decode_complete_state(self, state:dict) -> Self`: Декодирует состояние окружения из словаря.
- `add_environment(environment)`: Добавляет окружение в список всех окружений.
- `set_simulation_for_free_environments(simulation)`: Устанавливает симуляцию для свободных окружений.
- `get_environment_by_name(name: str)`: Возвращает окружение по имени.
- `clear_environments()`: Очищает список всех окружений.

### `TinySocialNetwork`

**Описание**: Подкласс `TinyWorld`, представляющий социальную сеть, где агенты связаны отношениями.

**Наследует**:

- `TinyWorld`: Расширяет функциональность базового класса `TinyWorld`, добавляя возможность моделирования социальных связей между агентами.

**Атрибуты**:

- `relations (dict)`: Словарь, хранящий отношения между агентами, где ключ - название отношения, а значение - список пар агентов, связанных этим отношением.

**Методы**:

- `__init__(self, name, broadcast_if_no_target=True)`: Инициализирует социальную сеть, вызывая конструктор родительского класса и инициализируя словарь отношений.
- `add_relation(self, agent_1, agent_2, name="default")`: Добавляет отношение между двумя агентами.
- `_update_agents_contexts(self)`: Обновляет контексты агентов на основе текущих отношений в сети.
- `_step(self)`: Выполняет шаг симуляции, предварительно обновляя контексты агентов.
- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `REACH_OUT`, разрешая его только если целевой агент находится в тех же отношениях, что и инициатор.
- `is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool`: Проверяет, находятся ли два агента в каких-либо отношениях.

## Функции

### `_step`

```python
@transactional
def _step(self, timedelta_per_step=None) -> dict:
    """
    Выполняет один шаг в окружении. По умолчанию заставляет всех агентов действовать и обрабатывает их действия.

    Args:
        timedelta_per_step (timedelta, optional): Временной интервал для одного шага. По умолчанию `None`.

    Returns:
        dict: Словарь, содержащий действия, выполненные агентами на этом шаге.

    Как работает функция:
    - Увеличивает текущее время в окружении, если задан `timedelta_per_step`.
    - Для каждого агента вызывает метод `act()` для выполнения действия.
    - Обрабатывает действия, возвращенные агентом, с помощью метода `_handle_actions()`.
    """
```
### `_advance_datetime`

```python
def _advance_datetime(self, timedelta):
    """
    Увеличивает текущую дату и время окружения на заданный интервал.

    Args:
        timedelta (timedelta): Временной интервал для увеличения текущей даты и времени.
    """
```

### `run`

```python
@transactional
def run(self, steps: int, timedelta_per_step=None, return_actions=False) -> list | None:
    """
    Запускает окружение на заданное количество шагов.

    Args:
        steps (int): Количество шагов для запуска окружения.
        timedelta_per_step (timedelta, optional): Временной интервал для каждого шага. По умолчанию `None`.
        return_actions (bool, optional): Если `True`, возвращает список действий, выполненных агентами. По умолчанию `False`.

    Returns:
        list | None: Список действий агентов, если `return_actions` is `True`, иначе `None`.

    Как работает функция:
    - Выполняет заданное количество шагов симуляции.
    - На каждом шаге вызывает метод `_step()`.
    - Если `return_actions` is `True`, собирает действия агентов в список и возвращает его.
    """
```

### `skip`

```python
@transactional
def skip(self, steps: int, timedelta_per_step=None):
    """
    Пропускает заданное количество шагов в окружении, увеличивая время, но не выполняя действий агентов.

    Args:
        steps (int): Количество шагов для пропуска.
        timedelta_per_step (timedelta, optional): Временной интервал для каждого шага. По умолчанию `None`.

    Как работает функция:
    - Увеличивает текущее время в окружении на заданный интервал, умноженный на количество шагов.
    """
```

### `run_minutes`

```python
def run_minutes(self, minutes: int):
    """
    Запускает окружение на заданное количество минут.

    Args:
        minutes (int): Количество минут для запуска окружения.

    Как работает функция:
    - Вызывает метод `run()` с заданным количеством шагов и временным интервалом в 1 минуту.
    """
```

### `skip_minutes`

```python
def skip_minutes(self, minutes: int):
    """
    Пропускает заданное количество минут в окружении.

    Args:
        minutes (int): Количество минут для пропуска.

    Как работает функция:
    - Вызывает метод `skip()` с заданным количеством шагов и временным интервалом в 1 минуту.
    """
```

### `run_hours`

```python
def run_hours(self, hours: int):
    """
    Запускает окружение на заданное количество часов.

    Args:
        hours (int): Количество часов для запуска окружения.

    Как работает функция:
    - Вызывает метод `run()` с заданным количеством шагов и временным интервалом в 1 час.
    """
```

### `skip_hours`

```python
def skip_hours(self, hours: int):
    """
    Пропускает заданное количество часов в окружении.

    Args:
        hours (int): Количество часов для пропуска.

    Как работает функция:
    - Вызывает метод `skip()` с заданным количеством шагов и временным интервалом в 1 час.
    """
```

### `run_days`

```python
def run_days(self, days: int):
    """
    Запускает окружение на заданное количество дней.

    Args:
        days (int): Количество дней для запуска окружения.

    Как работает функция:
    - Вызывает метод `run()` с заданным количеством шагов и временным интервалом в 1 день.
    """
```

### `skip_days`

```python
def skip_days(self, days: int):
    """
    Пропускает заданное количество дней в окружении.

    Args:
        days (int): Количество дней для пропуска.

    Как работает функция:
    - Вызывает метод `skip()` с заданным количеством шагов и временным интервалом в 1 день.
    """
```

### `run_weeks`

```python
def run_weeks(self, weeks: int):
    """
    Запускает окружение на заданное количество недель.

    Args:
        weeks (int): Количество недель для запуска окружения.

    Как работает функция:
    - Вызывает метод `run()` с заданным количеством шагов и временным интервалом в 1 неделю.
    """
```

### `skip_weeks`

```python
def skip_weeks(self, weeks: int):
    """
    Пропускает заданное количество недель в окружении.

    Args:
        weeks (int): Количество недель для пропуска.

    Как работает функция:
    - Вызывает метод `skip()` с заданным количеством шагов и временным интервалом в 1 неделю.
    """
```

### `run_months`

```python
def run_months(self, months: int):
    """
    Запускает окружение на заданное количество месяцев.

    Args:
        months (int): Количество месяцев для запуска окружения.

    Как работает функция:
    - Вызывает метод `run()` с заданным количеством шагов и временным интервалом в 4 недели (приблизительно месяц).
    """
```

### `skip_months`

```python
def skip_months(self, months: int):
    """
    Пропускает заданное количество месяцев в окружении.

    Args:
        months (int): Количество месяцев для пропуска.

    Как работает функция:
    - Вызывает метод `skip()` с заданным количеством шагов и временным интервалом в 4 недели (приблизительно месяц).
    """
```

### `run_years`

```python
def run_years(self, years: int):
    """
    Запускает окружение на заданное количество лет.

    Args:
        years (int): Количество лет для запуска окружения.

    Как работает функция:
    - Вызывает метод `run()` с заданным количеством шагов и временным интервалом в 365 дней (приблизительно год).
    """
```

### `skip_years`

```python
def skip_years(self, years: int):
    """
    Пропускает заданное количество лет в окружении.

    Args:
        years (int): Количество лет для пропуска.

    Как работает функция:
    - Вызывает метод `skip()` с заданным количеством шагов и временным интервалом в 365 дней (приблизительно год).
    """
```

### `add_agents`

```python
def add_agents(self, agents: list) -> Self:
    """
    Добавляет список агентов в окружение.

    Args:
        agents (list): Список агентов для добавления в окружение.

    Returns:
        Self: Ссылка на текущий объект окружения для возможности chaining.

    Как работает функция:
    - Итерируется по списку агентов и добавляет каждого агента с помощью метода `add_agent()`.
    """
```

### `add_agent`

```python
def add_agent(self, agent: TinyPerson) -> Self:
    """
    Добавляет агента в окружение.

    Args:
        agent (TinyPerson): Агент для добавления в окружение.

    Returns:
        Self: Ссылка на текущий объект окружения для возможности chaining.

    Raises:
        ValueError: Если имя агента уже существует в окружении.

    Как работает функция:
    - Проверяет, не добавлен ли уже агент в окружение.
    - Проверяет, не существует ли уже агент с таким именем в окружении.
    - Если имя уникально, добавляет агента в списки `agents` и `name_to_agent`.
    """
```

### `remove_agent`

```python
def remove_agent(self, agent: TinyPerson) -> Self:
    """
    Удаляет агента из окружения.

    Args:
        agent (TinyPerson): Агент для удаления из окружения.

    Returns:
        Self: Ссылка на текущий объект окружения для возможности chaining.

    Как работает функция:
    - Удаляет агента из списка `agents`.
    - Удаляет агента из словаря `name_to_agent`.
    """
```

### `remove_all_agents`

```python
def remove_all_agents(self) -> Self:
    """
    Удаляет всех агентов из окружения.

    Returns:
        Self: Ссылка на текущий объект окружения для возможности chaining.

    Как работает функция:
    - Очищает списки `agents` и `name_to_agent`.
    """
```

### `get_agent_by_name`

```python
def get_agent_by_name(self, name: str) -> TinyPerson | None:
    """
    Возвращает агента по имени.

    Args:
        name (str): Имя агента для поиска.

    Returns:
        TinyPerson | None: Агент с заданным именем или `None`, если агент не найден.

    Как работает функция:
    - Ищет агента в словаре `name_to_agent` по заданному имени.
    """
```

### `_handle_actions`

```python
@transactional
def _handle_actions(self, source: TinyPerson, actions: list):
    """
    Обрабатывает действия, совершенные агентами.

    Args:
        source (TinyPerson): Агент, выполнивший действия.
        actions (list): Список действий для обработки.

    Как работает функция:
    - Итерируется по списку действий.
    - Определяет тип действия и вызывает соответствующий обработчик.
    - Поддерживает действия `REACH_OUT` и `TALK`.
    """
```

### `_handle_reach_out`

```python
@transactional
def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
    """
    Обрабатывает действие `REACH_OUT`.

    Args:
        source_agent (TinyPerson): Агент, инициировавший действие.
        content (str): Содержание действия.
        target (str): Имя целевого агента.

    Как работает функция:
    - Получает целевого агента по имени.
    - Делает агентов доступными друг для друга.
    - Отправляет сообщения агентам об успешном установлении связи.
    """
```

### `_handle_talk`

```python
@transactional
def _handle_talk(self, source_agent: TinyPerson, content: str, target: str):
    """
    Обрабатывает действие `TALK`, доставляя сообщение от одного агента к другому.

    Args:
        source_agent (TinyPerson): Агент, отправивший сообщение.
        content (str): Содержание сообщения.
        target (str): Имя целевого агента.

    Как работает функция:
    - Получает целевого агента по имени.
    - Если целевой агент найден, отправляет ему сообщение.
    - Если целевой агент не найден, и включена трансляция, отправляет сообщение всем агентам в окружении.
    """
```

### `broadcast`

```python
@transactional
def broadcast(self, speech: str, source: AgentOrWorld=None):
    """
    Рассылает сообщение всем агентам в окружении.

    Args:
        speech (str): Содержание сообщения.
        source (AgentOrWorld, optional): Агент или окружение, отправившее сообщение. По умолчанию `None`.

    Как работает функция:
    - Итерируется по списку агентов.
    - Отправляет сообщение каждому агенту, исключая отправителя.
    """
```

### `broadcast_thought`

```python
@transactional
def broadcast_thought(self, thought: str, source: AgentOrWorld=None):
    """
    Рассылает мысль всем агентам в окружении.

    Args:
        thought (str): Содержание мысли.

    Как работает функция:
    - Итерируется по списку агентов.
    - Отправляет мысль каждому агенту.
    """
```

### `broadcast_internal_goal`

```python
@transactional
def broadcast_internal_goal(self, internal_goal: str):
    """
    Рассылает внутреннюю цель всем агентам в окружении.

    Args:
        internal_goal (str): Содержание внутренней цели.

    Как работает функция:
    - Итерируется по списку агентов.
    - Отправляет внутреннюю цель каждому агенту.
    """
```

### `broadcast_context_change`

```python
@transactional
def broadcast_context_change(self, context:list):
    """
    Рассылает изменение контекста всем агентам в окружении.

    Args:
        context (list): Содержание изменения контекста.

    Как работает функция:
    - Итерируется по списку агентов.
    - Отправляет изменение контекста каждому агенту.
    """
```

### `make_everyone_accessible`

```python
def make_everyone_accessible(self):
    """
    Делает всех агентов в окружении доступными друг для друга.

    Как работает функция:
    - Итерируется по списку агентов.
    - Для каждой пары агентов делает их доступными друг для друга.
    """
```

### `_display_communication`

```python
def _display_communication(self, cur_step, total_steps, kind, timedelta_per_step=None):
    """
    Отображает текущее состояние симуляции.

    Args:
        cur_step (int): Текущий шаг симуляции.
        total_steps (int): Общее количество шагов симуляции.
        kind (str): Тип отображаемой информации.
        timedelta_per_step (timedelta, optional): Временной интервал для каждого шага. По умолчанию `None`.

    Raises:
        ValueError: Если `kind` имеет неизвестное значение.

    Как работает функция:
    - Форматирует сообщение о текущем шаге симуляции.
    - Добавляет сообщение в буфер и отображает его.
    """
```

### `_push_and_display_latest_communication`

```python
def _push_and_display_latest_communication(self, rendering):
    """
    Добавляет сообщение в буфер и отображает его.

    Args:
        rendering (dict): Сообщение для отображения.

    Как работает функция:
    - Добавляет сообщение в буфер `_displayed_communications_buffer`.
    - Вызывает метод `_display()` для отображения сообщения.
    """
```

### `pop_and_display_latest_communications`

```python
def pop_and_display_latest_communications(self):
    """
    Извлекает и отображает все накопленные сообщения.

    Returns:
        list: Список извлеченных сообщений.

    Как работает функция:
    - Извлекает все сообщения из буфера `_displayed_communications_buffer`.
    - Очищает буфер.
    - Отображает каждое сообщение с помощью метода `_display()`.
    """
```

### `_display`

```python
def _display(self, communication):
    """
    Отображает сообщение в консоли.

    Args:
        communication (dict): Сообщение для отображения.

    Как работает функция:
    - Извлекает содержимое и тип сообщения из словаря.
    - Отображает сообщение в консоли с использованием объекта `console`.
    """
```

### `clear_communications_buffer`

```python
def clear_communications_buffer(self):
    """
    Очищает буфер сообщений.

    Как работает функция:
    - Очищает список `_displayed_communications_buffer`.
    """
```

### `__repr__`

```python
def __repr__(self) -> str:
    """
    Возвращает строковое представление объекта `TinyWorld`.

    Returns:
        str: Строковое представление объекта.

    Как работает функция:
    - Форматирует строку с именем окружения.
    """
```

### `_pretty_step`

```python
def _pretty_step(self, cur_step, total_steps, timedelta_per_step=None) -> str:
    """
    Форматирует сообщение о текущем шаге симуляции.

    Args:
        cur_step (int): Текущий шаг симуляции.
        total_steps (int): Общее количество шагов симуляции.
        timedelta_per_step (timedelta, optional): Временной интервал для каждого шага. По умолчанию `None`.

    Returns:
        str: Отформатированное сообщение о текущем шаге.

    Как работает функция:
    - Форматирует строку с именем окружения, текущим шагом и общим количеством шагов.
    - Добавляет информацию о текущем времени, если задан `timedelta_per_step`.
    """
```

### `pp_current_interactions`

```python
def pp_current_interactions(self, simplified=True, skip_system=True):
    """
    Выводит в консоль текущие взаимодействия между агентами.

    Args:
        simplified (bool, optional): Упрощенный вывод. По умолчанию `True`.
        skip_system (bool, optional): Пропускать системные сообщения. По умолчанию `True`.

    Как работает функция:
    - Вызывает метод `pretty_current_interactions()` и выводит результат в консоль.
    """
```

### `pretty_current_interactions`

```python
def pretty_current_interactions(self, simplified=True, skip_system=True, max_content_length=default["max_content_display_length"], first_n=None, last_n=None, include_omission_info:bool=True) -> str:
    """
    Возвращает отформатированную строку с текущими сообщениями агентов в этом окружении.

    Args:
        simplified (bool, optional): Упрощенный вывод. По умолчанию `True`.
        skip_system (bool, optional): Пропускать системные сообщения. По умолчанию `True`.
        max_content_length (int, optional): Максимальная длина содержимого сообщения. По умолчанию значение из `default`.
        first_n (int, optional): Выводить первые N сообщений. По умолчанию `None`.
        last_n (int, optional): Выводить последние N сообщений. По умолчанию `None`.
        include_omission_info (bool, optional): Включать информацию о пропущенных сообщениях. По умолчанию `True`.

    Returns:
        str: Отформатированная строка с сообщениями агентов.

    Как работает функция:
    - Итерируется по списку агентов.
    - Для каждого агента получает его историю взаимодействий.
    - Форматирует историю взаимодействий агента и добавляет ее в общий вывод.
    """
```

### `encode_complete_state`

```python
def encode_complete_state(self) -> dict:
    """
    Кодирует полное состояние окружения в словарь.

    Returns:
        dict: Словарь, содержащий состояние окружения.

    Как работает функция:
    - Создает копию словаря `__dict__` окружения.
    - Удаляет из копии поля, которые не нужно сохранять (например, `console`, `agents`, `name_to_agent`, `current_datetime`).
    - Кодирует состояние каждого агента с помощью метода `encode_complete_state()` и добавляет его в словарь.
    - Кодирует дату и время с помощью метода `isoformat()` и добавляет их в словарь.
    """
```

### `decode_complete_state`

```python
def decode_complete_state(self, state:dict) -> Self:
    """
    Декодирует состояние окружения из словаря.

    Args:
        state (dict): Словарь, содержащий состояние окружения.

    Returns:
        Self: Объект окружения с восстановленным состоянием.

    Как работает функция:
    - Создает копию словаря `state`.
    - Восстанавливает состояние каждого агента с помощью метода `decode_complete_state()` и добавляет его в окружение.
    - Восстанавливает дату и время с помощью метода `fromisoformat()`.
    - Обновляет `__dict__` окружения значениями из словаря `state`.
    """
```

### `add_environment`

```python
@staticmethod
def add_environment(environment):
    """
    Добавляет окружение в список всех окружений.

    Args:
        environment (TinyWorld): Окружение для добавления.

    Raises:
        ValueError: Если имя окружения уже существует.

    Как работает функция:
    - Проверяет, не существует ли уже окружение с таким именем.
    - Если имя уникально, добавляет окружение в словарь `TinyWorld.all_environments`.
    """
```

### `set_simulation_for_free_environments`

```python
@staticmethod
def set_simulation_for_free_environments(simulation):
    """
    Устанавливает симуляцию для свободных окружений.

    Args:
        simulation (Simulation): Симуляция для установки.

    Как работает функция:
    - Итерируется по всем окружениям в словаре `TinyWorld.all_environments`.
    - Если окружение не принадлежит ни одной симуляции, добавляет его в заданную симуляцию.
    """
```

### `get_environment_by_name`

```python
@staticmethod
def get_environment_by_name(name: str) -> TinyWorld | None:
    """
    Возвращает окружение по имени.

    Args:
        name (str): Имя окружения для поиска.

    Returns:
        TinyWorld | None: Окружение с заданным именем или `None`, если окружение не найдено.

    Как работает функция:
    - Ищет окружение в словаре `TinyWorld.all_environments` по заданному имени.
    """
```

### `clear_environments`

```python
@staticmethod
def clear_environments():
    """
    Очищает список всех окружений.

    Как работает функция:
    - Очищает словарь `TinyWorld.all_environments`.
    """
```

### `add_relation`

```python
@transactional
def add_relation(self, agent_1, agent_2, name="default") -> Self:
    """
    Добавляет отношение между двумя агентами.

    Args:
        agent_1 (TinyPerson): Первый агент.
        agent_2 (TinyPerson): Второй агент.
        name (str, optional): Название отношения. По умолчанию "default".

    Returns:
        Self: Ссылка на текущий объект окружения для возможности chaining.

    Как работает функция:
    - Добавляет агентов в окружение, если их там еще нет.
    - Добавляет пару агентов в список отношений с заданным именем.
    """
```

### `_update_agents_contexts`

```python
@transactional
def _update_agents_contexts(self):
    """
    Обновляет контексты агентов на основе текущих отношений в сети.

    Как работает функция:
    - Сначала делает всех агентов недоступными друг для друга.
    - Затем, на основе списка отношений, делает связанных агентов доступными друг для друга.
    """
```

### `_handle_reach_out`

```python
@transactional
def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
    """
    Обрабатывает действие `REACH_OUT` в социальной сети.

    Args:
        source_agent (TinyPerson): Агент, инициировавший действие.
        content (str): Содержание действия.
        target (str): Имя целевого агента.

    Как работает функция:
    - Проверяет, находится ли целевой агент в тех же отношениях, что и инициатор.
    - Если да, то выполняет стандартную обработку действия `REACH_OUT`.
    - Если нет, то отправляет сообщение инициатору о невозможности установить связь.
    """
```

### `is_in_relation_with`

```python
def is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool:
    """
    Проверяет, находятся ли два агента в каких-либо отношениях.

    Args:
        agent_1 (TinyPerson): Первый агент.
        agent_2 (TinyPerson): Второй агент.
        relation_name (str, optional): Название отношения для проверки. Если `None`, проверяется наличие любых отношений. По умолчанию `None`.

    Returns:
        bool: `True`, если агенты находятся в заданном отношении, иначе `False`.

    Как работает