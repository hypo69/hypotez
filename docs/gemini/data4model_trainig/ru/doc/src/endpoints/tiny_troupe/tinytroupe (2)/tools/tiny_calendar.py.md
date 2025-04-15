# Модуль `tiny_calendar.py`

## Обзор

Модуль `tiny_calendar.py` предоставляет класс `TinyCalendar`, который является инструментом для управления календарем агентов. Он позволяет агентам отслеживать встречи и события.

## Подробней

Модуль содержит класс `TinyCalendar`, который наследуется от класса `TinyTool`. Он предоставляет методы для добавления, поиска и обработки событий в календаре агента. Класс использует словарь `calendar` для хранения событий, где ключом является дата, а значением - список событий на эту дату.

## Классы

### `TinyCalendar`

**Описание**: Класс `TinyCalendar` представляет собой инструмент для управления календарем агентов.

**Наследует**: `TinyTool`

**Атрибуты**:
- `calendar` (dict): Словарь, отображающий дату на список событий. Каждое событие является словарем с ключами: "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time".

**Методы**:
- `__init__(self, owner=None)`: Инициализирует экземпляр класса `TinyCalendar`.
- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет новое событие в календарь.
- `find_events(self, year, month, day, hour=None, minute=None)`: Ищет события в календаре по указанным параметрам.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие, связанное с календарем.
- `actions_definitions_prompt(self) -> str`: Возвращает описание возможных действий с календарем в формате строки.
- `actions_constraints_prompt(self) -> str`: Возвращает ограничения на действия с календарем в формате строки.

#### `__init__(self, owner=None)`

```python
    def __init__(self, owner=None):
        """
        Инициализирует экземпляр класса `TinyCalendar`.

        Args:
            owner (Agent, optional): Владелец календаря. По умолчанию `None`.

        """
```

#### `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`

```python
    def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
        """
        Добавляет новое событие в календарь.

        Args:
            date (str): Дата события.
            title (str): Название события.
            description (str, optional): Описание события. По умолчанию `None`.
            owner (Agent, optional): Владелец события. По умолчанию `None`.
            mandatory_attendees (List[str], optional): Список обязательных участников. По умолчанию `None`.
            optional_attendees (List[str], optional): Список необязательных участников. По умолчанию `None`.
            start_time (str, optional): Время начала события. По умолчанию `None`.
            end_time (str, optional): Время окончания события. По умолчанию `None`.

        """
```

Как работает функция:
- Проверяет, существует ли указанная дата в словаре `calendar`.
- Если даты нет, создает новую запись в словаре с ключом `date` и значением в виде пустого списка.
- Добавляет словарь с информацией о событии в список событий для указанной даты.

#### `find_events(self, year, month, day, hour=None, minute=None)`

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

Как работает функция:
- Функция `find_events` предназначена для поиска событий в календаре на основе предоставленных параметров, таких как год, месяц, день, час и минута.
- В текущей реализации функция содержит только `pass`, что означает, что она не выполняет никаких действий.
- TODO: Необходимо реализовать логику поиска событий в календаре.

#### `_process_action(self, agent, action) -> bool`

```python
    def _process_action(self, agent, action) -> bool:
        """
        Обрабатывает действие, связанное с календарем.

        Args:
            agent (Agent): Агент, выполняющий действие.
            action (dict): Словарь, содержащий информацию о действии.

        Returns:
            bool: `True`, если действие было успешно обработано, `False` в противном случае.

        """
```

Как работает функция:
- Проверяет тип действия (`action['type']`). Если тип действия `CREATE_EVENT` и содержимое действия (`action['content']`) не равно `None`, то выполняется следующая логика:
    - Преобразует содержимое действия из формата JSON в словарь `event_content`.
    - Проверяет, содержит ли словарь `event_content` какие-либо недопустимые ключи, используя функцию `utils.check_valid_fields`.
    - Использует содержимое словаря `event_content` для создания нового события, вызывая метод `self.add_event(event_content)`.
    - Возвращает `True`, указывая, что действие было успешно обработано.
- Если тип действия не `CREATE_EVENT` или содержимое действия равно `None`, функция возвращает `False`.

Внутренние функции:
- В данной функции отсутствуют внутренние функции.

#### `actions_definitions_prompt(self) -> str`

```python
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает описание возможных действий с календарем в формате строки.

        Returns:
            str: Описание возможных действий с календарем.

        """
```

Как работает функция:
- Функция `actions_definitions_prompt` возвращает строку, содержащую описание возможных действий, которые можно выполнить с календарем.
- В текущей реализации функция возвращает строку, описывающую действие `CREATE_EVENT`, которое позволяет создавать новое событие в календаре.
- Описание включает информацию о полях, которые можно использовать для создания события, таких как `title`, `description`, `mandatory_attendees`, `optional_attendees`, `start_time` и `end_time`.
- TODO: Необходимо проработать вопрос об обработке списка участников и уведомлении их о приглашении.

#### `actions_constraints_prompt(self) -> str`

```python
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает ограничения на действия с календарем в формате строки.

        Returns:
            str: Ограничения на действия с календарем.

        """
```

Как работает функция:
- Функция `actions_constraints_prompt` возвращает строку, содержащую ограничения на действия, которые можно выполнить с календарем.
- В текущей реализации функция возвращает пустую строку.
- TODO: Необходимо определить и добавить ограничения на действия с календарем.

## Примеры
### Инициализация класса `TinyCalendar`

```python
from tinytroupe.tools.tiny_calendar import TinyCalendar

calendar = TinyCalendar()
```

### Добавление события в календарь

```python
from tinytroupe.tools.tiny_calendar import TinyCalendar

calendar = TinyCalendar()
calendar.add_event(date="2024-01-01", title="New Year's Day", description="First day of the year")
```

### Обработка действия `CREATE_EVENT`

```python
from tinytroupe.tools.tiny_calendar import TinyCalendar

calendar = TinyCalendar()
action = {
    "type": "CREATE_EVENT",
    "content": '{"title": "Meeting", "description": "Discuss project progress", "mandatory_attendees": ["John", "Jane"], "start_time": "10:00", "end_time": "11:00"}'
}
agent = None  # Замените на реальный экземпляр агента
result = calendar._process_action(agent, action)
print(result)  # Выведет: True
```