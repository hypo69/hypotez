# Модуль `tiny_calendar.py`

## Обзор

Модуль предоставляет класс `TinyCalendar`, который реализует базовый инструмент календаря для агентов.
Этот инструмент позволяет агентам отслеживать встречи и другие события. 
Функциональность включает добавление событий, поиск событий (в разработке) и обработку действий, связанных с событиями.

## Подробнее

Модуль является частью проекта `hypotez` и предназначен для использования в системе, где взаимодействуют различные агенты.
Календарь позволяет агентам координировать свои действия и планировать задачи.
Он предоставляет методы для создания, поиска и обработки событий, а также определяет структуру данных для хранения информации о событиях.

## Классы

### `TinyCalendar(TinyTool)`

**Описание**: Класс `TinyCalendar` представляет собой инструмент календаря для агентов.
Он позволяет агентам добавлять события в календарь, находить события и обрабатывать действия, связанные с событиями.

**Наследует**:
- `TinyTool`: Класс `TinyCalendar` наследует класс `TinyTool`.

**Атрибуты**:
- `calenar` (dict): Словарь, где ключами являются даты, а значениями — списки событий. Каждое событие представлено в виде словаря с ключами: "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time".

**Методы**:
- `__init__(self, owner=None)`: Конструктор класса.
- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет новое событие в календарь.
- `find_events(self, year, month, day, hour=None, minute=None)`: Ищет события в календаре по указанным параметрам.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие, переданное агентом.
- `actions_definitions_prompt(self) -> str`: Возвращает строку с определениями действий, которые может выполнять агент с помощью календаря.
- `actions_constraints_prompt(self) -> str`: Возвращает строку с ограничениями на действия, которые может выполнять агент с помощью календаря.

### `__init__(self, owner=None)`

```python
def __init__(self, owner=None):
    """
    Инициализирует объект `TinyCalendar`.

    Args:
        owner (Any, optional): Владелец календаря. По умолчанию `None`.
    """
```

### `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`

```python
def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
    """
    Добавляет событие в календарь.

    Args:
        date (Any): Дата события.
        title (str): Название события.
        description (str, optional): Описание события. По умолчанию `None`.
        owner (Any, optional): Владелец события. По умолчанию `None`.
        mandatory_attendees (list, optional): Список обязательных участников. По умолчанию `None`.
        optional_attendees (list, optional): Список необязательных участников. По умолчанию `None`.
        start_time (Any, optional): Время начала события. По умолчанию `None`.
        end_time (Any, optional): Время окончания события. По умолчанию `None`.
    """
```

**Как работает функция**:

- Проверяет, существует ли запись для указанной даты в словаре `self.calendar`.
- Если запись не существует, создает новую запись для указанной даты в виде списка.
- Добавляет в список событий словарь с информацией о событии (название, описание, владелец, участники, время начала и окончания).

**Примеры**:
```python
calendar = TinyCalendar()
calendar.add_event("2024-01-01", "New Year", "Celebration", "John", ["Alice", "Bob"], ["Charlie"], "00:00", "23:59")
```

### `find_events(self, year, month, day, hour=None, minute=None)`

```python
def find_events(self, year, month, day, hour=None, minute=None):
    """
    Ищет события в календаре по указанным параметрам.

    Args:
        year (int): Год.
        month (int): Месяц.
        day (int): День.
        hour (int, optional): Час. По умолчанию `None`.
        minute (int, optional): Минута. По умолчанию `None`.
    """
```

**Как работает функция**:

- Функция в настоящее время не реализована (TODO).
- Предполагается, что она будет искать события в календаре на основе предоставленных параметров даты и времени.

**Примеры**:
```python
calendar = TinyCalendar()
calendar.find_events(2024, 1, 1)
```

### `_process_action(self, agent, action) -> bool`

```python
def _process_action(self, agent, action) -> bool:
    """
    Обрабатывает действие, переданное агентом.

    Args:
        agent (Any): Агент, выполнивший действие.
        action (dict): Словарь с информацией о действии.

    Returns:
        bool: `True`, если действие успешно обработано, `False` в противном случае.
    """
```

**Как работает функция**:

- Проверяет, является ли тип действия `"CREATE_EVENT"` и содержит ли действие содержимое (`action['content']`).
- Если это так, пытается распарсить содержимое как JSON (`event_content`).
- Вызывает функцию `utils.check_valid_fields` для проверки наличия недопустимых ключей в содержимом события.
- Вызывает функцию `self.add_event` для добавления события в календарь.
- Возвращает `True`, если действие успешно обработано, `False` в противном случае.

**Примеры**:
```python
calendar = TinyCalendar()
action = {"type": "CREATE_EVENT", "content": '{"title": "Meeting", "description": "Discuss project", "mandatory_attendees": ["Alice"], "start_time": "10:00", "end_time": "11:00"}'}
calendar._process_action("John", action)
```

### `actions_definitions_prompt(self) -> str`

```python
def actions_definitions_prompt(self) -> str:
    """
    Возвращает строку с определениями действий, которые может выполнять агент с помощью календаря.

    Returns:
        str: Строка с определениями действий.
    """
```

**Как работает функция**:

- Возвращает строку, содержащую определения действий, которые агент может выполнить с помощью инструмента календаря.
- В настоящее время определено только действие `CREATE_EVENT`, которое позволяет агенту создавать новые события в своем календаре.
- Строка содержит описание полей, которые можно указать при создании события (например, название, описание, обязательные участники, время начала и окончания).

**Примеры**:
```python
calendar = TinyCalendar()
prompt = calendar.actions_definitions_prompt()
print(prompt)
```

### `actions_constraints_prompt(self) -> str`

```python
def actions_constraints_prompt(self) -> str:
    """
    Возвращает строку с ограничениями на действия, которые может выполнять агент с помощью календаря.

    Returns:
        str: Строка с ограничениями на действия.
    """
```

**Как работает функция**:

- Функция в настоящее время возвращает пустую строку.
- Предполагается, что она будет содержать ограничения на действия, которые может выполнять агент с помощью календаря.

**Примеры**:
```python
calendar = TinyCalendar()
prompt = calendar.actions_constraints_prompt()
print(prompt)
```