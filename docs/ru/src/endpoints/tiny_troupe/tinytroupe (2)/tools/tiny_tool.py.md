# Модуль TinyTool

## Обзор

Модуль `TinyTool` предоставляет базовый класс для создания инструментов в проекте `hypotez`. Инструменты используются агентами для выполнения определенных действий. Этот модуль определяет структуру и основные методы, которые должны быть реализованы в подклассах.

## Подробнее

Модуль содержит класс `TinyTool`, который является базовым классом для всех инструментов. Он включает в себя методы для защиты от нежелательных побочных эффектов, проверки права собственности на инструмент и обработки действий агента. Класс использует `JsonSerializableRegistry` для сериализации и десериализации.

## Классы

### `TinyTool`

**Описание**:
Базовый класс для создания инструментов. Инструменты используются агентами для выполнения действий.

**Наследует**:
`JsonSerializableRegistry` - обеспечивает возможность сериализации и десериализации объектов класса в формат JSON.

**Атрибуты**:
- `name` (str): Имя инструмента.
- `description` (str): Краткое описание инструмента.
- `owner` (str): Агент, которому принадлежит инструмент. Если `None`, инструмент может использоваться любым агентом.
- `real_world_side_effects` (bool): Указывает, имеет ли инструмент побочные эффекты в реальном мире.
- `exporter` (ArtifactExporter): Экспортер для сохранения результатов работы инструмента.
- `enricher` (Enricher): Обогатитель для обработки результатов работы инструмента.

**Методы**:
- `__init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None)`: Инициализирует новый инструмент.
- `_process_action(self, agent, action: dict) -> bool`: Абстрактный метод, который должен быть реализован в подклассах для обработки действий агента.
- `_protect_real_world(self)`: Предупреждает о возможных побочных эффектах инструмента в реальном мире.
- `_enforce_ownership(self, agent)`: Проверяет, имеет ли агент право собственности на инструмент.
- `set_owner(self, owner)`: Устанавливает владельца инструмента.
- `actions_definitions_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах для определения действий инструмента.
- `actions_constraints_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах для определения ограничений действий инструмента.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие агента, проверяя побочные эффекты и право собственности.

#### `__init__`
```python
def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
    """
    Initialize a new tool.

    Args:
        name (str): The name of the tool.
        description (str): A brief description of the tool.
        owner (str): The agent that owns the tool. If None, the tool can be used by anyone.
        real_world_side_effects (bool): Whether the tool has real-world side effects. That is to say, if it has the potential to change the 
            state of the world outside of the simulation. If it does, it should be used with caution.
        exporter (ArtifactExporter): An exporter that can be used to export the results of the tool's actions. If None, the tool will not be able to export results.
        enricher (Enricher): An enricher that can be used to enrich the results of the tool's actions. If None, the tool will not be able to enrich results.
    
    """
```

**Назначение**: Инициализирует новый экземпляр класса `TinyTool`.

**Параметры**:
- `name` (str): Имя инструмента.
- `description` (str): Описание инструмента.
- `owner` (str, optional): Владелец инструмента. По умолчанию `None`.
- `real_world_side_effects` (bool, optional): Флаг, указывающий на наличие побочных эффектов в реальном мире. По умолчанию `False`.
- `exporter` (ArtifactExporter, optional): Экспортер для сохранения результатов. По умолчанию `None`.
- `enricher` (Enricher, optional): Обогатитель для обработки результатов. По умолчанию `None`.

**Как работает функция**:
- Присваивает переданные значения атрибутам экземпляра класса, таким как `name`, `description`, `owner`, `real_world_side_effects`, `exporter` и `enricher`.
- Если `owner` не указан, инструмент может использоваться любым агентом.
- Если `real_world_side_effects` установлен в `True`, инструмент следует использовать с осторожностью, так как он может изменять состояние реального мира.
- `exporter` используется для экспорта результатов работы инструмента. Если `None`, экспорт результатов невозможен.
- `enricher` используется для обогащения результатов работы инструмента. Если `None`, обогащение результатов не выполняется.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

# Пример создания инструмента с именем, описанием и без владельца
tool = TinyTool(name='MyTool', description='A simple tool.')

# Пример создания инструмента с именем, описанием и владельцем
tool = TinyTool(name='MyTool', description='A simple tool.', owner='Agent1')

# Пример создания инструмента с реальными побочными эффектами
tool = TinyTool(name='MyTool', description='A tool with side effects.', real_world_side_effects=True)
```

#### `_process_action`
```python
def _process_action(self, agent, action: dict) -> bool:
    """
    Subclasses must implement this method.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Абстрактный метод, предназначенный для переопределения в подклассах. Обрабатывает действия, выполняемые агентом с использованием данного инструмента.

**Параметры**:
- `agent` (Agent): Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о выполняемом действии.

**Возвращает**:
- `bool`: Возвращает `True`, если действие было успешно обработано, и `False` в противном случае.

**Вызывает исключения**:
- `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:
- Вызывает исключение `NotImplementedError`, так как должен быть реализован в подклассах.
- Подклассы должны переопределить этот метод, чтобы определить логику обработки действий агента.

**Примеры**:
Поскольку это абстрактный метод, примеры его вызова не имеют смысла до тех пор, пока он не будет реализован в подклассе.

#### `_protect_real_world`
```python
def _protect_real_world(self):
    """
    ...
    """
    if self.real_world_side_effects:
        logger.warning(f" !!!!!!!!!! Tool {self.name} has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!")
```

**Назначение**: Предупреждает пользователя о возможных побочных эффектах инструмента в реальном мире, если таковые имеются.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Проверяет, установлен ли атрибут `real_world_side_effects` в `True`.
- Если да, выводит предупреждение в лог с использованием модуля `logger` из `src.logger.logger`, указывающее на то, что инструмент имеет побочные эффекты в реальном мире и должен использоваться с осторожностью.

**Примеры**:
```python
from tinytroupe.tools.tiny_tool import TinyTool
from src.logger import logger

# Пример создания инструмента с реальными побочными эффектами
tool = TinyTool(name='DangerousTool', description='A tool with side effects.', real_world_side_effects=True)

# Вызов метода _protect_real_world
tool._protect_real_world()  # Выведет предупреждение в лог
```

#### `_enforce_ownership`
```python
def _enforce_ownership(self, agent):
    """
    ...
    """
    if self.owner is not None and agent.name != self.owner.name:
        raise ValueError(f"Agent {agent.name} does not own tool {self.name}, which is owned by {self.owner.name}.")
```

**Назначение**: Проверяет, имеет ли агент право собственности на инструмент.

**Параметры**:
- `agent` (Agent): Агент, который пытается использовать инструмент.

**Возвращает**:
- Отсутствует.

**Вызывает исключения**:
- `ValueError`: Если агент не является владельцем инструмента.

**Как работает функция**:
- Проверяет, установлен ли атрибут `owner` (владелец) инструмента.
- Если владелец установлен, сравнивает имя агента с именем владельца.
- Если имена не совпадают, вызывает исключение `ValueError` с сообщением о том, что агент не имеет права использовать инструмент.

**Примеры**:
```python
from tinytroupe.tools.tiny_tool import TinyTool

# Пример создания инструмента с владельцем
tool = TinyTool(name='MyTool', description='A simple tool.', owner='Agent1')

class Agent:
    def __init__(self, name):
        self.name = name

# Пример создания агента
agent1 = Agent(name='Agent1')
agent2 = Agent(name='Agent2')

# Вызов метода _enforce_ownership
tool._enforce_ownership(agent1)  # Не вызовет исключение
# tool._enforce_ownership(agent2)  # Вызовет исключение ValueError
```

#### `set_owner`
```python
def set_owner(self, owner):
    """
    ...
    """
    self.owner = owner
```

**Назначение**: Устанавливает владельца инструмента.

**Параметры**:
- `owner` (Agent): Новый владелец инструмента.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Присваивает переданное значение атрибуту `owner` инструмента.

**Примеры**:
```python
from tinytroupe.tools.tiny_tool import TinyTool

# Пример создания инструмента без владельца
tool = TinyTool(name='MyTool', description='A simple tool.')

class Agent:
    def __init__(self, name):
        self.name = name

# Пример создания агента
agent1 = Agent(name='Agent1')

# Вызов метода set_owner
tool.set_owner(agent1)

# Теперь инструмент принадлежит агенту Agent1
```

#### `actions_definitions_prompt`
```python
def actions_definitions_prompt(self) -> str:
    """
    ...
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Абстрактный метод, который должен быть реализован в подклассах. Предназначен для определения возможных действий, которые может выполнять инструмент.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка, содержащая определение действий, которые может выполнять инструмент.

**Вызывает исключения**:
- `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:
- Вызывает исключение `NotImplementedError`, так как должен быть реализован в подклассах.
- Подклассы должны переопределить этот метод, чтобы определить логику определения действий инструмента.

**Примеры**:
Поскольку это абстрактный метод, примеры его вызова не имеют смысла до тех пор, пока он не будет реализован в подклассе.

#### `actions_constraints_prompt`
```python
def actions_constraints_prompt(self) -> str:
    """
    ...
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Абстрактный метод, который должен быть реализован в подклассах. Предназначен для определения ограничений на действия, которые может выполнять инструмент.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка, содержащая ограничения на действия, которые может выполнять инструмент.

**Вызывает исключения**:
- `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:
- Вызывает исключение `NotImplementedError`, так как должен быть реализован в подклассах.
- Подклассы должны переопределить этот метод, чтобы определить логику определения ограничений на действия инструмента.

**Примеры**:
Поскольку это абстрактный метод, примеры его вызова не имеют смысла до тех пор, пока он не будет реализован в подклассе.

#### `process_action`
```python
def process_action(self, agent, action: dict) -> bool:
    """
    ...
    """
    self._protect_real_world()
    self._enforce_ownership(agent)
    self._process_action(agent, action)
```

**Назначение**: Обрабатывает действие агента, проверяя побочные эффекты и право собственности.

**Параметры**:
- `agent` (Agent): Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:
- `bool`: Возвращает `True`, если действие было успешно обработано, и `False` в противном случае.

**Как работает функция**:
- Вызывает метод `_protect_real_world()` для проверки и предупреждения о возможных побочных эффектах инструмента в реальном мире.
- Вызывает метод `_enforce_ownership(agent)` для проверки, имеет ли агент право собственности на инструмент.
- Вызывает метод `_process_action(agent, action)` для обработки действия агента.

**Примеры**:
```python
from tinytroupe.tools.tiny_tool import TinyTool

# Пример создания инструмента с владельцем
tool = TinyTool(name='MyTool', description='A simple tool.', owner='Agent1')

class Agent:
    def __init__(self, name):
        self.name = name

    def process_action(self, agent, action: dict) -> bool:
        """

        Args:
            agent (Agent): 
            action (dict):

        Returns:
            bool:
        """
        raise NotImplementedError

# Пример создания агента
agent1 = Agent(name='Agent1')

# Пример действия
action = {'action': 'do_something'}

# Вызов метода process_action
# tool.process_action(agent1, action)  # Вызовет исключение NotImplementedError, так как _process_action не реализован