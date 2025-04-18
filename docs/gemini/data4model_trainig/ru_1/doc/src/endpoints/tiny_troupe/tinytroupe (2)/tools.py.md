# Модуль `tools.py`

## Обзор

Модуль предоставляет инструменты (`TinyTool` и его подклассы) для агентов, позволяющие им выполнять специализированные задачи в рамках системы `tinytroupe`. Включает базовый класс для инструментов, а также конкретные реализации, такие как `TinyCalendar` (календарь) и `TinyWordProcessor` (текстовый процессор).

## Подробней

Модуль содержит инструменты, которые позволяют агентам выполнять специализированные задачи. Базовый класс `TinyTool` определяет интерфейс для всех инструментов, а подклассы реализуют конкретные функции, такие как ведение календаря (`TinyCalendar`) и обработка текстовых документов (`TinyWordProcessor`). Инструменты могут иметь владельцев, экспортеры и обогатители контента.

## Классы

### `TinyTool`

**Описание**: Базовый класс для всех инструментов. Определяет общие атрибуты и методы, которые должны быть реализованы в подклассах.

**Атрибуты**:
- `name` (str): Имя инструмента.
- `description` (str): Краткое описание инструмента.
- `owner` (str): Агент, которому принадлежит инструмент. Если `None`, инструмент может использоваться любым агентом.
- `real_world_side_effects` (bool): Указывает, имеет ли инструмент реальные побочные эффекты, то есть может ли он изменить состояние мира вне симуляции.
- `exporter` (ArtifactExporter): Экспортер, используемый для экспорта результатов действий инструмента. Если `None`, экспорт невозможен.
- `enricher` (TinyEnricher): Обогатитель, используемый для обогащения результатов действий инструмента. Если `None`, обогащение невозможно.

**Методы**:
- `__init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None)`: Инициализирует новый инструмент.
- `_process_action(self, agent, action: dict) -> bool`: Абстрактный метод, который должен быть реализован в подклассах. Определяет, как инструмент обрабатывает действие агента.
- `_protect_real_world(self)`: Выводит предупреждение в лог, если инструмент имеет реальные побочные эффекты.
- `_enforce_ownership(self, agent)`: Проверяет, имеет ли агент право использовать инструмент. Вызывает исключение, если агент не является владельцем инструмента.
- `set_owner(self, owner)`: Устанавливает владельца инструмента.
- `actions_definitions_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах. Возвращает описание действий, которые может выполнять инструмент.
- `actions_constraints_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах. Возвращает описание ограничений на действия, которые может выполнять инструмент.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие агента, проверяет наличие реальных побочных эффектов и право собственности, а затем вызывает метод `_process_action`.

### `TinyCalendar`

**Описание**: Инструмент календаря, позволяющий агентам отслеживать встречи и события.

**Наследует**:
- `TinyTool`

**Атрибуты**:
- `calendar` (dict): Словарь, отображающий даты в списки событий. Каждое событие представлено словарем с ключами "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time".

**Методы**:
- `__init__(self, owner=None)`: Инициализирует новый календарь.
- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет новое событие в календарь.
- `find_events(self, year, month, day, hour=None, minute=None)`: Находит события в календаре по заданной дате и времени.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие агента. Если действие имеет тип "CREATE_EVENT", создает новое событие в календаре.
- `actions_definitions_prompt(self) -> str`: Возвращает описание действий, которые может выполнять календарь.
- `actions_constraints_prompt(self) -> str`: Возвращает описание ограничений на действия, которые может выполнять календарь.

### `TinyWordProcessor`

**Описание**: Инструмент текстового процессора, позволяющий агентам писать документы.

**Наследует**:
- `TinyTool`

**Методы**:
- `__init__(self, owner=None, exporter=None, enricher=None)`: Инициализирует новый текстовый процессор.
- `write_document(self, title, content, author=None)`: Создает новый документ. Если указан обогатитель контента (`enricher`), он используется для обогащения контента документа. Если указан экспортер (`exporter`), он используется для экспорта документа в различных форматах.
- `_process_action(self, agent, action) -> bool`: Обрабатывает действие агента. Если действие имеет тип "WRITE_DOCUMENT", создает новый документ.
- `actions_definitions_prompt(self) -> str`: Возвращает описание действий, которые может выполнять текстовый процессор.
- `actions_constraints_prompt(self) -> str`: Возвращает описание ограничений на действия, которые может выполнять текстовый процессор.

## Функции

### `TinyTool.__init__`

```python
def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
    """
    Инициализирует новый инструмент.

    Args:
        name (str): Имя инструмента.
        description (str): Краткое описание инструмента.
        owner (str): Агент, которому принадлежит инструмент. Если None, инструмент может использоваться любым агентом.
        real_world_side_effects (bool): Указывает, имеет ли инструмент реальные побочные эффекты, то есть может ли он изменить состояние мира вне симуляции.
        exporter (ArtifactExporter): Экспортер, используемый для экспорта результатов действий инструмента. Если None, экспорт невозможен.
        enricher (Enricher): Обогатитель, используемый для обогащения результатов действий инструмента. Если None, обогащение невозможно.
    """
    ...
```

**Назначение**: Инициализация экземпляра класса `TinyTool`.

**Параметры**:
- `name` (str): Имя инструмента.
- `description` (str): Описание инструмента.
- `owner` (Optional[str], optional): Владелец инструмента. По умолчанию `None`.
- `real_world_side_effects` (bool): Флаг, указывающий на наличие реальных побочных эффектов. По умолчанию `False`.
- `exporter` (Optional[ArtifactExporter], optional): Экспортер артефактов. По умолчанию `None`.
- `enricher` (Optional[TinyEnricher], optional): Обогатитель контента. По умолчанию `None`.

**Как работает функция**:
- Присваивает переданные значения атрибутам экземпляра класса `TinyTool`.

**Примеры**:
```python
tool = TinyTool(name="example_tool", description="This is an example tool.")
tool = TinyTool(name="dangerous_tool", description="This tool can affect the real world!", real_world_side_effects=True)
```

### `TinyTool._process_action`

```python
def _process_action(self, agent, action: dict) -> bool:
    """
    Args:
        agent: <описание агента>
        action (dict): <описание словаря action>

    Returns:
        bool: <описание bool>

    Raises:
        NotImplementedError: <Описание ошибки NotImplementedError>
    """
    ...
```

**Назначение**: Абстрактный метод, предназначенный для обработки действий агента.

**Параметры**:
- `agent`: Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Указывает, было ли успешно обработано действие.

**Вызывает исключения**:
- `NotImplementedError`: Вызывается, если метод не реализован в подклассе.

**Как работает функция**:
- Метод является абстрактным и должен быть реализован в подклассах класса `TinyTool`. Он определяет, как конкретный инструмент обрабатывает действия, выполняемые агентами.

### `TinyTool._protect_real_world`

```python
def _protect_real_world(self):
    """ """
    ...
```

**Назначение**: Выводит предупреждение в лог, если инструмент имеет реальные побочные эффекты.

**Как работает функция**:
- Проверяет значение атрибута `real_world_side_effects`. Если атрибут имеет значение `True`, выводит предупреждение в лог.

### `TinyTool._enforce_ownership`

```python
def _enforce_ownership(self, agent):
    """
    Args:
        agent: <описание agent>

    Raises:
        ValueError: <описание ValueError>
    """
    ...
```

**Назначение**: Проверяет, имеет ли агент право использовать инструмент.

**Параметры**:
- `agent`: Агент, пытающийся использовать инструмент.

**Вызывает исключения**:
- `ValueError`: Вызывается, если агент не является владельцем инструмента.

**Как работает функция**:
- Проверяет, является ли агент владельцем инструмента. Если владелец инструмента не указан (`self.owner is None`), проверка не выполняется. Если владелец указан, проверяется, совпадает ли имя агента с именем владельца. Если имена не совпадают, вызывается исключение `ValueError`.

### `TinyTool.set_owner`

```python
def set_owner(self, owner):
    """
    Args:
        owner: <описание owner>
    """
    ...
```

**Назначение**: Устанавливает владельца инструмента.

**Параметры**:
- `owner`: Новый владелец инструмента.

**Как работает функция**:
- Присваивает переданное значение атрибуту `owner` экземпляра класса `TinyTool`.

### `TinyTool.actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Returns:
        str: <описание str>

    Raises:
        NotImplementedError: <описание NotImplementedError>
    """
    ...
```

**Назначение**: Возвращает описание действий, которые может выполнять инструмент.

**Возвращает**:
- `str`: Описание действий, которые может выполнять инструмент.

**Вызывает исключения**:
- `NotImplementedError`: Вызывается, если метод не реализован в подклассе.

**Как работает функция**:
- Метод является абстрактным и должен быть реализован в подклассах класса `TinyTool`. Он возвращает строку, содержащую описание действий, которые может выполнять конкретный инструмент.

### `TinyTool.actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Returns:
        str: <описание str>

    Raises:
        NotImplementedError: <описание NotImplementedError>
    """
    ...
```

**Назначение**: Возвращает описание ограничений на действия, которые может выполнять инструмент.

**Возвращает**:
- `str`: Описание ограничений на действия, которые может выполнять инструмент.

**Вызывает исключения**:
- `NotImplementedError`: Вызывается, если метод не реализован в подклассе.

**Как работает функция**:
- Метод является абстрактным и должен быть реализован в подклассах класса `TinyTool`. Он возвращает строку, содержащую описание ограничений на действия, которые может выполнять конкретный инструмент.

### `TinyTool.process_action`

```python
def process_action(self, agent, action: dict) -> bool:
    """
    Args:
        agent: <описание agent>
        action (dict): <описание action>

    Returns:
        bool: <описание bool>
    """
    ...
```

**Назначение**: Обрабатывает действие агента.

**Параметры**:
- `agent`: Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Указывает, было ли успешно обработано действие.

**Как работает функция**:
1. Вызывает метод `_protect_real_world` для проверки наличия реальных побочных эффектов.
2. Вызывает метод `_enforce_ownership` для проверки права собственности агента на инструмент.
3. Вызывает метод `_process_action` для обработки действия агента.

### `TinyCalendar.__init__`

```python
def __init__(self, owner=None):
    """
    Args:
        owner: <описание owner>
    """
    ...
```

**Назначение**: Инициализирует новый календарь.

**Параметры**:
- `owner` (Optional[str], optional): Владелец календаря. По умолчанию `None`.

**Как работает функция**:
1. Вызывает конструктор базового класса `TinyTool` с именем "calendar", описанием "A basic calendar tool that allows agents to keep track meetings and appointments." и флагом `real_world_side_effects=False`.
2. Инициализирует атрибут `calendar` пустым словарем.

### `TinyCalendar.add_event`

```python
def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
    """
    Args:
        date: <описание date>
        title: <описание title>
        description: <описание description>
        owner: <описание owner>
        mandatory_attendees: <описание mandatory_attendees>
        optional_attendees: <описание optional_attendees>
        start_time: <описание start_time>
        end_time: <описание end_time>
    """
    ...
```

**Назначение**: Добавляет новое событие в календарь.

**Параметры**:
- `date`: Дата события.
- `title`: Название события.
- `description` (Optional[str], optional): Описание события. По умолчанию `None`.
- `owner` (Optional[str], optional): Владелец события. По умолчанию `None`.
- `mandatory_attendees` (Optional[list], optional): Список обязательных участников. По умолчанию `None`.
- `optional_attendees` (Optional[list], optional): Список необязательных участников. По умолчанию `None`.
- `start_time` (Optional[str], optional): Время начала события. По умолчанию `None`.
- `end_time` (Optional[str], optional): Время окончания события. По умолчанию `None`.

**Как работает функция**:
1. Проверяет, существует ли запись для указанной даты в календаре. Если нет, создает новую запись в виде пустого списка.
2. Создает словарь, содержащий информацию о событии.
3. Добавляет словарь в список событий для указанной даты.

### `TinyCalendar.find_events`

```python
def find_events(self, year, month, day, hour=None, minute=None):
    """
    Args:
        year: <описание year>
        month: <описание month>
        day: <описание day>
        hour: <описание hour>
        minute: <описание minute>
    """
    ...
```

**Назначение**: Находит события в календаре по заданной дате и времени.

**Параметры**:
- `year`: Год события.
- `month`: Месяц события.
- `day`: День события.
- `hour` (Optional[int], optional): Час события. По умолчанию `None`.
- `minute` (Optional[int], optional): Минута события. По умолчанию `None`.

**Как работает функция**:
-  TODO

### `TinyCalendar._process_action`

```python
def _process_action(self, agent, action) -> bool:
    """
    Args:
        agent: <описание agent>
        action: <описание action>

    Returns:
        bool: <описание bool>
    """
    ...
```

**Назначение**: Обрабатывает действие агента.

**Параметры**:
- `agent`: Агент, выполняющий действие.
- `action`: Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Указывает, было ли успешно обработано действие.

**Как работает функция**:
1. Проверяет, имеет ли действие тип "CREATE_EVENT" и содержит ли оно контент.
2. Если оба условия выполнены, пытается распарсить контент действия как JSON.
3. Проверяет, содержит ли контент допустимые ключи.
4. Использует контент для создания нового события в календаре.
5. Возвращает `True`, если действие было успешно обработано.
6. Возвращает `False` в противном случае.

### `TinyCalendar.actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Returns:
        str: <описание str>
    """
    ...
```

**Назначение**: Возвращает описание действий, которые может выполнять календарь.

**Возвращает**:
- `str`: Описание действий, которые может выполнять календарь.

**Как работает функция**:
- Возвращает строку, содержащую описание действия "CREATE_EVENT", которое позволяет создавать новые события в календаре.

### `TinyCalendar.actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Returns:
        str: <описание str>
    """
    ...
```

**Назначение**: Возвращает описание ограничений на действия, которые может выполнять календарь.

**Возвращает**:
- `str`: Описание ограничений на действия, которые может выполнять календарь.

**Как работает функция**:
- TODO

### `TinyWordProcessor.__init__`

```python
def __init__(self, owner=None, exporter=None, enricher=None):
    """
    Args:
        owner: <описание owner>
        exporter: <описание exporter>
        enricher: <описание enricher>
    """
    ...
```

**Назначение**: Инициализирует новый текстовый процессор.

**Параметры**:
- `owner` (Optional[str], optional): Владелец текстового процессора. По умолчанию `None`.
- `exporter` (Optional[ArtifactExporter], optional): Экспортер артефактов. По умолчанию `None`.
- `enricher` (Optional[TinyEnricher], optional): Обогатитель контента. По умолчанию `None`.

**Как работает функция**:
1. Вызывает конструктор базового класса `TinyTool` с именем "wordprocessor", описанием "A basic word processor tool that allows agents to write documents." и флагом `real_world_side_effects=False`.

### `TinyWordProcessor.write_document`

```python
def write_document(self, title, content, author=None):
    """
    Args:
        title: <описание title>
        content: <описание content>
        author: <описание author>
    """
    ...
```

**Назначение**: Создает новый документ.

**Параметры**:
- `title`: Название документа.
- `content`: Содержание документа.
- `author` (Optional[str], optional): Автор документа. По умолчанию `None`.

**Как работает функция**:
1. Записывает отладочное сообщение в лог, содержащее название документа и его содержимое.
2. Если указан обогатитель контента (`enricher`), он используется для обогащения контента документа.
3. Если указан экспортер (`exporter`), он используется для экспорта документа в различных форматах.

### `TinyWordProcessor._process_action`

```python
def _process_action(self, agent, action) -> bool:
    """
    Args:
        agent: <описание agent>
        action: <описание action>

    Returns:
        bool: <описание bool>
    """
    ...
```

**Назначение**: Обрабатывает действие агента.

**Параметры**:
- `agent`: Агент, выполняющий действие.
- `action`: Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Указывает, было ли успешно обработано действие.

**Как работает функция**:
1. Проверяет, имеет ли действие тип "WRITE_DOCUMENT" и содержит ли оно контент.
2. Если оба условия выполнены, пытается распарсить контент действия как JSON.
3. Проверяет, содержит ли контент допустимые ключи.
4. Использует контент для создания нового документа.
5. Возвращает `True`, если действие было успешно обработано.
6. Возвращает `False` в противном случае.
7. Логирует ошибку, если не удается распарсить JSON контент.

### `TinyWordProcessor.actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Returns:
        str: <описание str>
    """
    ...
```

**Назначение**: Возвращает описание действий, которые может выполнять текстовый процессор.

**Возвращает**:
- `str`: Описание действий, которые может выполнять текстовый процессор.

**Как работает функция**:
- Возвращает строку, содержащую описание действия "WRITE_DOCUMENT", которое позволяет создавать новые документы.

### `TinyWordProcessor.actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Returns:
        str: <описание str>
    """
    ...
```

**Назначение**: Возвращает описание ограничений на действия, которые может выполнять текстовый процессор.

**Возвращает**:
- `str`: Описание ограничений на действия, которые может выполнять текстовый процессор.

**Как работает функция**:
- Возвращает строку, содержащую описание ограничений на действие "WRITE_DOCUMENT", включая необходимость писать весь контент сразу, делать его длинным и подробным, а также упоминать конкретных владельцев или партнерские команды для любых упоминаемых вех или временных рамок.