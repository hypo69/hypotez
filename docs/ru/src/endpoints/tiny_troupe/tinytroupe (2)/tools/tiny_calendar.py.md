# Модуль `tiny_calendar.py`

## Обзор

Модуль предоставляет класс `TinyCalendar`, который представляет собой инструмент для работы с календарем. Этот инструмент позволяет агентам отслеживать встречи и события.

## Подробней

Модуль `tiny_calendar.py` является частью проекта `hypotez` и предназначен для организации работы с календарем. Он предоставляет базовый функционал для создания и поиска событий в календаре агентов. Класс `TinyCalendar` наследуется от класса `TinyTool` и расширяет его функциональность, добавляя возможность управления событиями.

## Классы

### `TinyCalendar`

**Описание**: Класс `TinyCalendar` представляет собой инструмент календаря, который позволяет агентам отслеживать встречи и события.

**Наследует**: `TinyTool`

**Атрибуты**:
- `calendar` (dict): Словарь, где ключи - это даты, а значения - списки событий. Каждое событие представлено в виде словаря с ключами: "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time".

**Принцип работы**:
Класс `TinyCalendar` предоставляет методы для добавления и поиска событий в календаре. Он использует словарь `calendar` для хранения информации о событиях, где ключом является дата, а значением - список событий в этот день.

**Методы**:
- `__init__(self, owner=None)`: Инициализирует объект `TinyCalendar`.
- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет событие в календарь.
- `find_events(self, year, month, day, hour=None, minute=None)`: Ищет события в календаре.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие, связанное с календарем.
- `actions_definitions_prompt(self) -> str`: Возвращает строку с описанием действий, которые можно выполнять с календарем.
- `actions_constraints_prompt(self) -> str`: Возвращает строку с ограничениями на действия, которые можно выполнять с календарем.

### `__init__`

```python
def __init__(self, owner=None):
    """
    Инициализирует объект `TinyCalendar`.

    Args:
        owner (Any, optional): Владелец календаря. По умолчанию `None`.
    """
```
**Описание**:
Конструктор класса `TinyCalendar`. Инициализирует атрибуты класса, в том числе словарь `calendar`, который будет хранить события.

**Параметры**:
- `owner` (Any, optional): Владелец календаря. По умолчанию `None`.

**Примеры**:
```python
calendar = TinyCalendar(owner="Agent1")
print(calendar.calendar)  # Выведет: {}
```

### `add_event`

```python
def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
    """
    Добавляет событие в календарь.

    Args:
        date (Any): Дата события.
        title (str): Название события.
        description (str, optional): Описание события. По умолчанию `None`.
        owner (Any, optional): Владелец события. По умолчанию `None`.
        mandatory_attendees (List[Any], optional): Список обязательных участников. По умолчанию `None`.
        optional_attendees (List[Any], optional): Список необязательных участников. По умолчанию `None`.
        start_time (Any, optional): Время начала события. По умолчанию `None`.
        end_time (Any, optional): Время окончания события. По умолчанию `None`.
    """
```
**Описание**:
Метод добавляет новое событие в календарь. Если для указанной даты еще нет событий, создается новый список. Затем событие добавляется в список событий для указанной даты.

**Параметры**:
- `date` (Any): Дата события.
- `title` (str): Название события.
- `description` (str, optional): Описание события. По умолчанию `None`.
- `owner` (Any, optional): Владелец события. По умолчанию `None`.
- `mandatory_attendees` (List[Any], optional): Список обязательных участников. По умолчанию `None`.
- `optional_attendees` (List[Any], optional): Список необязательных участников. По умолчанию `None`.
- `start_time` (Any, optional): Время начала события. По умолчанию `None`.
- `end_time` (Any, optional): Время окончания события. По умолчанию `None`.

**Примеры**:
```python
calendar = TinyCalendar()
calendar.add_event("2024-01-01", "New Year", description="New Year celebration")
print(calendar.calendar)
# Выведет: {'2024-01-01': [{'title': 'New Year', 'description': 'New Year celebration', 'owner': None, 'mandatory_attendees': None, 'optional_attendees': None, 'start_time': None, 'end_time': None}]}
```

### `find_events`

```python
def find_events(self, year, month, day, hour=None, minute=None):
    """
    Ищет события в календаре.

    Args:
        year (int): Год.
        month (int): Месяц.
        day (int): День.
        hour (int, optional): Час. По умолчанию `None`.
        minute (int, optional): Минута. По умолчанию `None`.
    """
```
**Описание**:
Метод предназначен для поиска событий в календаре по указанным параметрам даты и времени. 

**Параметры**:
- `year` (int): Год.
- `month` (int): Месяц.
- `day` (int): День.
- `hour` (int, optional): Час. По умолчанию `None`.
- `minute` (int, optional): Минута. По умолчанию `None`.

### `_process_action`

```python
def _process_action(self, agent, action) -> bool:
    """
    Обрабатывает действие, связанное с календарем.

    Args:
        agent (Any): Агент, выполняющий действие.
        action (dict): Словарь, содержащий информацию о действии.

    Returns:
        bool: `True`, если действие успешно обработано, `False` в противном случае.
    """
```
**Описание**:
Метод обрабатывает действие, переданное агентом. Если тип действия "CREATE_EVENT", он извлекает содержимое события из JSON, проверяет наличие недопустимых ключей и использует полученные данные для создания нового события с помощью метода `add_event`.

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: `True`, если действие успешно обработано, `False` в противном случае.

**Внутренние функции**:
Внутри данного метода нет внутренних функций.

**Примеры**:
```python
calendar = TinyCalendar()
action = {
    'type': "CREATE_EVENT",
    'content': '{"title": "Meeting", "description": "Discuss project progress", "date": "2024-01-05"}'
}
result = calendar._process_action("Agent1", action)
print(result)  # Выведет: True
print(calendar.calendar)
# Выведет: {'2024-01-05': [{'title': 'Meeting', 'description': 'Discuss project progress', 'owner': None, 'mandatory_attendees': None, 'optional_attendees': None, 'start_time': None, 'end_time': None, 'date': '2024-01-05'}]}
```

### `actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Возвращает строку с описанием действий, которые можно выполнять с календарем.

    Returns:
        str: Строка с описанием действий.
    """
```

**Описание**:
Метод возвращает строку с описанием возможных действий, которые агент может выполнить с календарем. В данном случае, определено только действие "CREATE_EVENT", которое позволяет создавать новые события. Строка содержит описание полей, которые можно указать при создании события.

**Возвращает**:
- `str`: Строка с описанием действий.

**Примеры**:
```python
calendar = TinyCalendar()
prompt = calendar.actions_definitions_prompt()
print(prompt)
# Выведет:
# - CREATE_EVENT: You can create a new event in your calendar. The content of the event has many fields, and you should use a JSON format to specify them. Here are the possible fields:
# * title: The title of the event. Mandatory.
# * description: A brief description of the event. Optional.
# * mandatory_attendees: A list of agent names who must attend the event. Optional.
# * optional_attendees: A list of agent names who are invited to the event, but are not required to attend. Optional.
# * start_time: The start time of the event. Optional.
# * end_time: The end time of the event. Optional.
```

### `actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Возвращает строку с ограничениями на действия, которые можно выполнять с календарем.

    Returns:
        str: Строка с ограничениями на действия.
    """
```
**Описание**:
Метод возвращает строку с описанием ограничений на действия, которые можно выполнять с календарем. В текущей реализации строка пустая, так как ограничения не определены.

**Возвращает**:
- `str`: Строка с ограничениями на действия.

**Примеры**:
```python
calendar = TinyCalendar()
prompt = calendar.actions_constraints_prompt()
print(prompt)  # Выведет: ""
```