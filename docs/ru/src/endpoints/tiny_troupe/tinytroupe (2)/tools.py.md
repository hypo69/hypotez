# Модуль `tools.py`

## Обзор

Модуль `tools.py` предназначен для определения и управления инструментами, которые могут использовать агенты `tinytroupe` для выполнения специализированных задач. В модуле определены базовый класс `TinyTool` и его подклассы, реализующие конкретные инструменты, такие как календарь (`TinyCalendar`) и текстовый процессор (`TinyWordProcessor`).

## Подробнее

Модуль предоставляет основу для создания инструментов, которые могут быть использованы агентами в среде `tinytroupe`. Инструменты позволяют агентам выполнять различные действия, такие как запись документов, планирование событий и т.д. Каждый инструмент имеет имя, описание, владельца и флаг, указывающий на наличие реальных побочных эффектов в реальном мире.

## Классы

### `TinyTool`

**Описание**: Базовый класс для всех инструментов. Определяет основные атрибуты и методы, которые должны быть реализованы в подклассах.

**Атрибуты**:
- `name` (str): Имя инструмента.
- `description` (str): Краткое описание инструмента.
- `owner` (str): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом.
- `real_world_side_effects` (bool): Флаг, указывающий на наличие реальных побочных эффектов.
- `exporter` (ArtifactExporter): Экспортер для сохранения результатов работы инструмента.
- `enricher` (TinyEnricher): Обогатитель для улучшения результатов работы инструмента.

**Методы**:
- `__init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None)`: Инициализирует новый инструмент.
- `_process_action(self, agent, action: dict) -> bool`: Абстрактный метод, который должен быть реализован в подклассах. Определяет логику обработки действия агента.
- `_protect_real_world(self)`: Предупреждает о наличии реальных побочных эффектов.
- `_enforce_ownership(self, agent)`: Проверяет, имеет ли агент право на использование инструмента.
- `set_owner(self, owner)`: Устанавливает владельца инструмента.
- `actions_definitions_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах. Возвращает описание действий, которые может выполнять инструмент.
- `actions_constraints_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах. Возвращает ограничения на действия, которые может выполнять инструмент.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие агента, проверяя наличие побочных эффектов и права на использование инструмента.

### `TinyCalendar`

**Описание**: Инструмент для ведения календаря. Позволяет агентам создавать и находить события.

**Наследует**:
- `TinyTool`: Расширяет базовый класс `TinyTool`.

**Атрибуты**:
- `calendar` (dict): Словарь, отображающий дату в список событий. Каждое событие является словарем с ключами "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time".

**Методы**:
- `__init__(self, owner=None)`: Инициализирует новый календарь.
- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет новое событие в календарь.
- `find_events(self, year, month, day, hour=None, minute=None)`: Находит события в календаре.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие агента. Поддерживает действие "CREATE_EVENT" для создания новых событий.
- `actions_definitions_prompt(self) -> str`: Возвращает описание действия "CREATE_EVENT".
- `actions_constraints_prompt(self) -> str`: Возвращает ограничения на действия, которые может выполнять инструмент.

### `TinyWordProcessor`

**Описание**: Инструмент для обработки текстов. Позволяет агентам создавать и экспортировать документы.

**Наследует**:
- `TinyTool`: Расширяет базовый класс `TinyTool`.

**Атрибуты**:
- Отсутствуют специфические атрибуты, кроме тех, что наследуются от `TinyTool`.

**Методы**:
- `__init__(self, owner=None, exporter=None, enricher=None)`: Инициализирует новый текстовый процессор.
- `write_document(self, title, content, author=None)`: Создает новый документ. Использует `enricher` для обогащения контента и `exporter` для сохранения документа в различных форматах.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие агента. Поддерживает действие "WRITE_DOCUMENT" для создания новых документов.
- `actions_definitions_prompt(self) -> str`: Возвращает описание действия "WRITE_DOCUMENT".
- `actions_constraints_prompt(self) -> str`: Возвращает ограничения на действия, которые может выполнять инструмент.

## Функции

### `TinyTool.__init__`

```python
def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
    """
    Инициализирует новый инструмент.

    Args:
        name (str): Имя инструмента.
        description (str): Краткое описание инструмента.
        owner (str): Агент, владеющий инструментом. Если None, инструмент может использоваться любым агентом.
        real_world_side_effects (bool): Флаг, указывающий, имеет ли инструмент реальные побочные эффекты.
        exporter (ArtifactExporter): Экспортер для сохранения результатов работы инструмента.
        enricher (Enricher): Обогатитель для улучшения результатов работы инструмента.
    """
```

**Назначение**: Инициализация экземпляра класса `TinyTool`.

**Параметры**:
- `name` (str): Имя инструмента.
- `description` (str): Описание инструмента.
- `owner` (str, optional): Владелец инструмента. По умолчанию `None`.
- `real_world_side_effects` (bool, optional): Признак наличия побочных эффектов. По умолчанию `False`.
- `exporter` (ArtifactExporter, optional): Экспортер артефактов. По умолчанию `None`.
- `enricher` (Enricher, optional): Обогатитель контента. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция устанавливает значения атрибутов экземпляра класса `TinyTool` на основе переданных аргументов. Она также инициализирует атрибуты `name`, `description`, `owner`, `real_world_side_effects`, `exporter` и `enricher`.

**Примеры**:
```python
tool = TinyTool(name="example_tool", description="An example tool")
```

### `TinyTool._process_action`

```python
def _process_action(self, agent, action: dict) -> bool:
    """
    Обрабатывает действие агента.

    Args:
        agent: Агент, выполняющий действие.
        action (dict): Словарь, описывающий действие.

    Returns:
        bool: True, если действие было успешно обработано, False в противном случае.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.
    """
```

**Назначение**: Абстрактный метод, предназначенный для обработки действия, выполняемого агентом с использованием данного инструмента.

**Параметры**:

- `agent`: Агент, выполняющий действие. Тип агента не указан.
- `action` (dict): Словарь, содержащий информацию о действии, которое необходимо выполнить.

**Возвращает**:

- `bool`: Возвращает `True`, если действие успешно обработано, и `False` в противном случае.

**Вызывает исключения**:

- `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:

- Этот метод должен быть переопределен в каждом подклассе `TinyTool` для реализации логики обработки конкретных действий, которые может выполнять инструмент. Если метод не переопределен, он вызывает исключение `NotImplementedError`.

**Примеры**:

Поскольку это абстрактный метод, примеры его вызова напрямую невозможны. Однако, вот пример реализации в подклассе:

```python
class MyTool(TinyTool):
    def _process_action(self, agent, action: dict) -> bool:
        if action['type'] == 'SOME_ACTION':
            # Логика обработки действия
            return True
        return False
```

### `TinyTool._protect_real_world`

```python
def _protect_real_world(self):
    """
    Предупреждает о наличии реальных побочных эффектов.
    """
```

**Назначение**: Вывод предупреждения в лог, если инструмент имеет реальные побочные эффекты.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция проверяет атрибут `real_world_side_effects`. Если он `True`, выводит предупреждение в лог с использованием модуля `logger` из `src.logger`.

**Примеры**:
```python
tool = TinyTool(name="example_tool", description="An example tool", real_world_side_effects=True)
tool._protect_real_world()
```

### `TinyTool._enforce_ownership`

```python
def _enforce_ownership(self, agent):
    """
    Проверяет, имеет ли агент право на использование инструмента.

    Args:
        agent: Агент, пытающийся использовать инструмент.

    Raises:
        ValueError: Если агент не является владельцем инструмента.
    """
```

**Назначение**: Проверка, является ли указанный агент владельцем инструмента.

**Параметры**:
- `agent`: Агент, для которого выполняется проверка владения инструментом.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `ValueError`: Если инструмент имеет владельца и переданный агент не совпадает с владельцем инструмента.

**Как работает функция**:
- Функция проверяет, установлен ли владелец для инструмента (`self.owner`).
- Если владелец установлен, функция сравнивает имя переданного агента (`agent.name`) с именем владельца инструмента (`self.owner.name`).
- Если имена не совпадают, вызывается исключение `ValueError` с сообщением о том, что агент не имеет права использовать инструмент, так как он принадлежит другому агенту.

**Примеры**:
```python
class Agent:
    def __init__(self, name):
        self.name = name

agent1 = Agent("Alice")
agent2 = Agent("Bob")

tool = TinyTool(name="example_tool", description="An example tool", owner=agent1)

tool._enforce_ownership(agent1)  # Успешно, Alice - владелец инструмента
try:
    tool._enforce_ownership(agent2)  # Вызовет ValueError, Bob не является владельцем
except ValueError as ex:
    print(ex)
```

### `TinyTool.set_owner`

```python
def set_owner(self, owner):
    """
    Устанавливает владельца инструмента.

    Args:
        owner: Новый владелец инструмента.
    """
```

**Назначение**: Устанавливает владельца для инструмента.

**Параметры**:
- `owner`: Новый владелец инструмента.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция устанавливает атрибут `owner` экземпляра класса `TinyTool` на переданное значение `owner`.

**Примеры**:
```python
tool = TinyTool(name="example_tool", description="An example tool")
tool.set_owner("new_owner")
```

### `TinyTool.actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Возвращает описание действий, которые может выполнять инструмент.
    """
```

**Назначение**: Абстрактный метод, который должен быть реализован в подклассах и возвращать описание действий, которые может выполнять инструмент.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Описание действий, которые может выполнять инструмент.

**Вызывает исключения**:
- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:
- Этот метод должен быть переопределен в каждом подклассе `TinyTool` для предоставления информации о возможных действиях, которые агент может запросить у инструмента. Если метод не переопределен, он вызывает исключение `NotImplementedError`.

**Примеры**:

Поскольку это абстрактный метод, примеры его вызова напрямую невозможны. Однако, вот пример реализации в подклассе:

```python
class MyTool(TinyTool):
    def actions_definitions_prompt(self) -> str:
        return "SOME_ACTION: Do something."
```

### `TinyTool.actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Возвращает ограничения на действия, которые может выполнять инструмент.
    """
```

**Назначение**: Абстрактный метод, который должен быть реализован в подклассах и возвращать ограничения на действия, которые может выполнять инструмент.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Ограничения на действия, которые может выполнять инструмент.

**Вызывает исключения**:
- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:
- Этот метод должен быть переопределен в каждом подклассе `TinyTool` для предоставления информации об ограничениях на возможные действия, которые агент может запросить у инструмента. Если метод не переопределен, он вызывает исключение `NotImplementedError`.

**Примеры**:

Поскольку это абстрактный метод, примеры его вызова напрямую невозможны. Однако, вот пример реализации в подклассе:

```python
class MyTool(TinyTool):
    def actions_constraints_prompt(self) -> str:
        return "SOME_ACTION: You can only do this once."
```

### `TinyTool.process_action`

```python
def process_action(self, agent, action: dict) -> bool:
    """
    Обрабатывает действие агента.

    Args:
        agent: Агент, выполняющий действие.
        action (dict): Словарь, описывающий действие.

    Returns:
        bool: True, если действие было успешно обработано, False в противном случае.
    """
```

**Назначение**: Обработка действия, выполняемого агентом.

**Параметры**:
- `agent`: Агент, выполняющий действие.
- `action` (dict): Словарь, описывающий действие.

**Возвращает**:
- `bool`: `True`, если действие было успешно обработано, `False` в противном случае.

**Как работает функция**:
- Сначала вызывает метод `_protect_real_world()` для проверки наличия реальных побочных эффектов и вывода предупреждения, если они есть.
- Затем вызывает метод `_enforce_ownership()` для проверки, имеет ли агент право на использование инструмента.
- Если обе проверки пройдены успешно, вызывает метод `_process_action()` для фактической обработки действия.

**Примеры**:
```python
class MyTool(TinyTool):
    def _process_action(self, agent, action: dict) -> bool:
        if action['type'] == 'SOME_ACTION':
            # Логика обработки действия
            return True
        return False

agent = ...  # Некоторый агент
action = {'type': 'SOME_ACTION'}
tool = MyTool(name="example_tool", description="An example tool")
result = tool.process_action(agent, action)
```

### `TinyCalendar.__init__`

```python
def __init__(self, owner=None):
    """
    Инициализирует новый календарь.

    Args:
        owner: Владелец календаря.
    """
```

**Назначение**: Инициализация экземпляра класса `TinyCalendar`.

**Параметры**:
- `owner` (optional): Владелец календаря. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция вызывает конструктор родительского класса `TinyTool` с именем "calendar", описанием "A basic calendar tool that allows agents to keep track meetings and appointments.", владельцем `owner`, и флагом `real_world_side_effects=False`.
- Инициализирует атрибут `calendar` как пустой словарь, который будет использоваться для хранения событий календаря.

**Примеры**:
```python
calendar = TinyCalendar(owner="Alice")
```

### `TinyCalendar.add_event`

```python
def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
    """
    Добавляет новое событие в календарь.

    Args:
        date: Дата события.
        title: Название события.
        description (optional): Описание события. По умолчанию None.
        owner (optional): Владелец события. По умолчанию None.
        mandatory_attendees (optional): Список обязательных участников. По умолчанию None.
        optional_attendees (optional): Список необязательных участников. По умолчанию None.
        start_time (optional): Время начала события. По умолчанию None.
        end_time (optional): Время окончания события. По умолчанию None.
    """
```

**Назначение**: Добавление нового события в календарь.

**Параметры**:
- `date`: Дата события.
- `title`: Название события.
- `description` (optional): Описание события. По умолчанию `None`.
- `owner` (optional): Владелец события. По умолчанию `None`.
- `mandatory_attendees` (optional): Список обязательных участников. По умолчанию `None`.
- `optional_attendees` (optional): Список необязательных участников. По умолчанию `None`.
- `start_time` (optional): Время начала события. По умолчанию `None`.
- `end_time` (optional): Время окончания события. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
- Проверяет, существует ли запись для указанной даты в календаре (`self.calendar`). Если нет, создает новую запись в виде списка.
- Добавляет словарь с информацией о событии в список событий для указанной даты.

**Примеры**:
```python
calendar = TinyCalendar()
calendar.add_event(
    date="2024-01-01",
    title="New Year's Party",
    description="A party to celebrate the new year",
    mandatory_attendees=["Alice", "Bob"]
)
```

### `TinyCalendar.find_events`

```python
def find_events(self, year, month, day, hour=None, minute=None):
    """
    Находит события в календаре.

    Args:
        year: Год события.
        month: Месяц события.
        day: День события.
        hour (optional): Час события. По умолчанию None.
        minute (optional): Минута события. По умолчанию None.
    """
```

**Назначение**: Поиск событий в календаре по указанной дате и времени.

**Параметры**:
- `year`: Год события.
- `month`: Месяц события.
- `day`: День события.
- `hour` (optional): Час события. По умолчанию `None`.
- `minute` (optional): Минута события. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция пока не реализована (`pass`). TODO: Добавить логику поиска событий в календаре по указанным параметрам.

**Примеры**:
```python
calendar = TinyCalendar()
events = calendar.find_events(year=2024, month=1, day=1)
```

### `TinyCalendar._process_action`

```python
def _process_action(self, agent, action) -> bool:
    """
    Обрабатывает действие агента.

    Args:
        agent: Агент, выполняющий действие.
        action: Словарь, описывающий действие.

    Returns:
        bool: True, если действие было успешно обработано, False в противном случае.
    """
```

**Назначение**: Обрабатывает действие агента, связанное с календарем.

**Параметры**:
- `agent`: Агент, выполняющий действие (тип не указан).
- `action`: Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Возвращает `True`, если действие успешно обработано, и `False` в противном случае.

**Как работает функция**:
- Проверяет, что тип действия (`action['type']`) равен `"CREATE_EVENT"` и что в действии содержится контент (`action['content'] is not None`).
- Если условие выполняется, пытается распарсить контент действия как JSON (`json.loads(action['content'])`) и сохранить его в переменной `event_content`.
- Выполняет проверку наличия недопустимых ключей в `event_content` с использованием функции `utils.check_valid_fields`. Допустимые ключи: `"title"`, `"description"`, `"mandatory_attendees"`, `"optional_attendees"`, `"start_time"`, `"end_time"`.
- Использует полученные данные для создания нового события с помощью метода `self.add_event(event_content)`.
- Возвращает `True`, если действие успешно обработано.
- Если тип действия не `"CREATE_EVENT"` или контент отсутствует, возвращает `False`.

**Примеры**:
```python
calendar = TinyCalendar()
agent = ...  # Некоторый агент

# Пример действия для создания события
action = {
    'type': "CREATE_EVENT",
    'content': json.dumps({
        'date': '2024-01-01',
        'title': 'New Year',
        'description': 'description'
    })
}

success = calendar._process_action(agent, action)
print(success)  # Выведет: True
```

### `TinyCalendar.actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Возвращает описание действия "CREATE_EVENT".
    """
```

**Назначение**: Предоставляет описание доступных действий для календаря в формате, пригодном для использования в запросах к языковой модели.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка с описанием действия `CREATE_EVENT` и его параметров в формате Markdown.

**Как работает функция**:
- Функция возвращает строку, содержащую описание действия `CREATE_EVENT` и его возможных параметров в формате Markdown.
- Описание включает информацию о том, что действие позволяет создать новое событие в календаре, и перечисляет возможные поля для события (title, description, mandatory_attendees, optional_attendees, start_time, end_time) с указанием, какие из них являются обязательными, а какие - опциональными.

**Примеры**:
```python
calendar = TinyCalendar()
prompt = calendar.actions_definitions_prompt()
print(prompt)
```

### `TinyCalendar.actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Возвращает ограничения на действия, которые может выполнять инструмент.
    """
```

**Назначение**: Возвращает строку с описанием ограничений на действия, которые могут быть выполнены с использованием календаря.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка с описанием ограничений на действия.

**Как работает функция**:
- В текущей реализации функция возвращает пустую строку (`prompt = ""`).
- TODO: Добавить логику для определения и возврата ограничений на действия с календарем.

**Примеры**:
```python
calendar = TinyCalendar()
prompt = calendar.actions_constraints_prompt()
print(prompt)  # Выведет:
```

### `TinyWordProcessor.__init__`

```python
def __init__(self, owner=None, exporter=None, enricher=None):
    """
    Инициализирует новый текстовый процессор.

    Args:
        owner: Владелец текстового процессора.
        exporter: Экспортер для сохранения документов.
        enricher: Обогатитель для улучшения контента.
    """
```

**Назначение**: Инициализация экземпляра класса `TinyWordProcessor`.

**Параметры**:
- `owner` (optional): Владелец текстового процессора. По умолчанию `None`.
- `exporter` (optional): Экспортер для сохранения документов. По умолчанию `None`.
- `enricher` (optional): Обогатитель для улучшения контента. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция вызывает конструктор родительского класса `TinyTool` с именем "wordprocessor", описанием "A basic word processor tool that allows agents to write documents.", владельцем `owner`, флагом `real_world_side_effects=False`, и переданными значениями `exporter` и `enricher`.

**Примеры**:
```python
word_processor = TinyWordProcessor(owner="Alice", exporter=my_exporter, enricher=my_enricher)
```

### `TinyWordProcessor.write_document`

```python
def write_document(self, title, content, author=None):
    """
    Создает новый документ.

    Args:
        title: Название документа.
        content: Содержание документа.
        author (optional): Автор документа. По умолчанию None.
    """
```

**Назначение**: Создание нового документа с указанным названием, содержимым и автором.

**Параметры**:
- `title` (str): Название документа.
- `content` (str): Содержание документа.
- `author` (str, optional): Автор документа. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Логирует информацию о создании документа с указанием названия и содержания.
2. Если установлен `enricher` (обогатитель контента), применяет его к содержимому документа. `enricher` используется для улучшения и расширения контента, делая его более детальным и информативным.
3. Если установлен `exporter` (экспортер артефактов), экспортирует документ в различных форматах (Markdown, DOCX, JSON).

**Примеры**:
```python
word_processor = TinyWordProcessor(exporter=my_exporter, enricher=my_enricher)
word_processor.write_document(title="My Document", content="This is the content of my document.", author="Alice")
```

### `TinyWordProcessor._process_action`

```python
def _process_action(self, agent, action) -> bool:
    """
    Обрабатывает действие агента.

    Args:
        agent: Агент, выполняющий действие.
        action: Словарь, описывающий действие.

    Returns:
        bool: True, если действие было успешно обработано, False в противном случае.
    """
```

**Назначение**: Обрабатывает действие агента, связанное с созданием документа.

**Параметры**:
- `agent`: Агент, выполняющий действие (тип не указан).
- `action`: Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Возвращает `True`, если действие успешно обработано, и `False` в противном случае.

**Как работает функция**:
1. Пытается выполнить следующие действия в блоке `try`:
   - Проверяет, что тип действия (`action['type']`) равен `"WRITE_DOCUMENT"` и что в действии содержится контент (`action['content'] is not None`).
   - Если условие выполняется, пытается распарсить контент действия как JSON (`json.loads(action['content'])`) и сохранить его в переменной `doc_spec`.
   - Выполняет проверку наличия недопустимых ключей в `doc_spec` с использованием функции `utils.check_valid_fields`. Допустимые ключи: `"title"`, `"content"`, `"author"`.
   - Использует полученные данные для создания нового документа с помощью метода `self.write_document(**doc_spec)`.
   - Возвращает `True`, если действие успешно обработано.
   - Если тип действия не `"WRITE_DOCUMENT"` или контент отсутствует, возвращает `False`.
2. Если в процессе обработки возникает ошибка `json.JSONDecodeError` (ошибка при парсинге JSON), перехватывает исключение в блоке `except`:
   - Логирует информацию об ошибке с использованием `logger.error`, указывая на то, что произошла ошибка при парсинге JSON, и выводит оригинальный контент.
   - Возвращает `False`.

**Примеры**:
```python
word_processor = TinyWordProcessor(exporter=my_exporter, enricher=my_enricher)
agent = ...  # Некоторый агент

# Пример действия для создания документа
action = {
    'type': "WRITE_DOCUMENT",
    'content': json.dumps({
        'title': 'My Document',
        'content': 'This is the content of my document.',
        'author': 'Alice'
    })
}

success = word_processor._process_action(agent, action)
print(success)  # Выведет: True
```

### `TinyWordProcessor.actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Возвращает описание действия "WRITE_DOCUMENT".
    """
```

**Назначение**: Предоставляет описание доступных действий для текстового процессора в формате, пригодном для использования в запросах к языковой модели.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка с описанием действия `WRITE_DOCUMENT` и его параметров в формате Markdown.

**Как работает функция**:
- Функция возвращает строку, содержащую описание действия `WRITE_DOCUMENT` и его возможных параметров в формате Markdown.
- Описание включает информацию о том, что действие позволяет создать новый документ, и перечисляет возможные поля для документа (title, content, author) с указанием, какие из них являются обязательными, а какие - опциональными.

**Примеры**:
```python
word_processor = TinyWordProcessor()
prompt = word_processor.actions_definitions_prompt()
print(prompt)
```

### `TinyWordProcessor.actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Возвращает ограничения на действия, которые может выполнять инструмент.
    """
```

**Назначение**: Предоставляет рекомендации и ограничения для действия `WRITE_DOCUMENT`.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка, содержащая рекомендации и ограничения для действия `WRITE_DOCUMENT`.

**Как работает функция**:
- Функция возвращает строку, содержащую рекомендации и ограничения для действия `WRITE_DOCUMENT`.
- Ограничения включают:
  - `WRITE_DOCUMENT` должно записывать весь контент сразу.
  - Контент должен быть длинным и подробным, если нет веских причин для обратного.
  - При упоминании этапов или сроков следует указывать конкретных владельцев или партнерские команды, если нет веских причин не делать этого.

**Примеры**:
```python
word_processor = TinyWordProcessor()
prompt = word_processor.actions_constraints_prompt()
print(prompt)