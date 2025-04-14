# Модуль tiny_tool

## Обзор

Модуль содержит базовый класс `TinyTool`, который служит основой для создания различных инструментов, используемых агентами в системе. Он предоставляет общую структуру для определения и выполнения действий, а также механизмы для контроля доступа и обработки побочных эффектов.

## Подробней

Модуль определяет абстрактный класс `TinyTool`, который должен быть унаследован для создания конкретных инструментов. Он включает в себя методы для обработки действий агентов, защиты от нежелательных побочных эффектов и принудительного соблюдения прав собственности на инструменты.

## Классы

### `TinyTool`

**Описание**: Базовый класс для инструментов, используемых агентами.

**Наследует**:

- `JsonSerializableRegistry`: Обеспечивает возможность сериализации и десериализации экземпляров класса в формат JSON.

**Атрибуты**:

- `name` (str): Имя инструмента.
- `description` (str): Краткое описание инструмента.
- `owner` (str): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом.
- `real_world_side_effects` (bool): Указывает, имеет ли инструмент реальные побочные эффекты, то есть может ли он изменять состояние мира вне симуляции.
- `exporter`: Экспортер, используемый для экспорта результатов действий инструмента.
- `enricher`: Обогатитель, используемый для обогащения результатов действий инструмента.

**Методы**:

- `__init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None)`: Инициализирует новый инструмент.
- `_process_action(self, agent, action: dict) -> bool`: Абстрактный метод, который должен быть реализован в подклассах для обработки действий агента.
- `_protect_real_world(self)`: Предупреждает о реальных побочных эффектах инструмента, если они есть.
- `_enforce_ownership(self, agent)`: Проверяет, имеет ли агент право на использование инструмента.
- `set_owner(self, owner)`: Устанавливает владельца инструмента.
- `actions_definitions_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах для предоставления определений действий инструмента в виде текста.
- `actions_constraints_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах для предоставления ограничений действий инструмента в виде текста.
- `process_action(self, agent, action: dict) -> bool`: Обрабатывает действие агента, выполняя защиту от побочных эффектов и проверку прав собственности.

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

**Назначение**: Инициализация экземпляра класса `TinyTool`.

**Параметры**:

- `name` (str): Имя инструмента.
- `description` (str): Описание инструмента.
- `owner` (str, optional): Владелец инструмента. По умолчанию `None`.
- `real_world_side_effects` (bool, optional): Флаг, указывающий на наличие реальных побочных эффектов. По умолчанию `False`.
- `exporter` (optional): Экспортер для результатов действий инструмента. По умолчанию `None`.
- `enricher` (optional): Обогатитель для результатов действий инструмента. По умолчанию `None`.

**Как работает функция**:
- Функция инициализирует атрибуты экземпляра класса `TinyTool` значениями, переданными в качестве аргументов. Она устанавливает имя, описание, владельца, наличие реальных побочных эффектов, экспортер и обогатитель для инструмента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

tool = TinyTool(name='MyTool', description='A simple tool')
print(tool.name, tool.description) # MyTool A simple tool

tool_with_owner = TinyTool(name='RestrictedTool', description='A tool with an owner', owner='Agent007')
print(tool_with_owner.owner) # Agent007
```

#### `_process_action`

```python
def _process_action(self, agent, action: dict) -> bool:
    """
    
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Абстрактный метод, предназначенный для обработки действий агента.

**Параметры**:

- `agent`: Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:

- `bool`: Результат обработки действия.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

- Функция вызывает исключение `NotImplementedError`, указывая на то, что метод должен быть реализован в подклассах для обеспечения конкретной логики обработки действий агента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        print(f"Agent {agent} is performing action: {action}")
        return True

tool = MyTool(name='MyTool', description='A simple tool')
result = tool._process_action(agent='TestAgent', action={'name': 'TestAction'})
print(result) # TestAgent is performing action: {'name': 'TestAction'}
```

#### `_protect_real_world`

```python
def _protect_real_world(self):
    """
    
    """
    if self.real_world_side_effects:
        logger.warning(f" !!!!!!!!!! Tool {self.name} has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!")
```

**Назначение**: Защита от случайного выполнения действий, имеющих реальные побочные эффекты.

**Как работает функция**:

- Если атрибут `real_world_side_effects` установлен в `True`, функция выводит предупреждение в лог, сообщающее о том, что инструмент имеет реальные побочные эффекты и его следует использовать с осторожностью.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool
from tinytroupe.tools import logger  # Corrected import

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

tool = MyTool(name='DangerousTool', description='A tool with real-world side effects', real_world_side_effects=True)
tool._protect_real_world() #  !!!!!!!!! Tool DangerousTool has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!
```

#### `_enforce_ownership`

```python
def _enforce_ownership(self, agent):
    """
    
    """
    if self.owner is not None and agent.name != self.owner.name:
        raise ValueError(f"Agent {agent.name} does not own tool {self.name}, which is owned by {self.owner.name}.")
```

**Назначение**: Обеспечение соблюдения прав собственности на инструмент.

**Параметры**:

- `agent`: Агент, пытающийся использовать инструмент.

**Вызывает исключения**:

- `ValueError`: Если агент не является владельцем инструмента.

**Как работает функция**:

- Если у инструмента есть владелец (атрибут `owner` не `None`) и имя агента не совпадает с именем владельца, функция вызывает исключение `ValueError`, сообщающее о том, что у агента нет прав на использование инструмента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

tool = MyTool(name='MyTool', description='A simple tool', owner='Agent007')

try:
    tool._enforce_ownership(agent=type('Agent', (object,), {'name': 'Agent001'})()) # Agent001 не имеет прав
except ValueError as ex:
    print(ex) # Agent Agent001 does not own tool MyTool, which is owned by Agent007.

tool._enforce_ownership(agent=type('Agent', (object,), {'name': 'Agent007'})()) # Agent007 имеет права
```

#### `set_owner`

```python
def set_owner(self, owner):
    """
    
    """
    self.owner = owner
```

**Назначение**: Установка владельца инструмента.

**Параметры**:

- `owner`: Новый владелец инструмента.

**Как работает функция**:

- Функция устанавливает атрибут `owner` экземпляра класса `TinyTool` равным значению, переданному в качестве аргумента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

tool = MyTool(name='MyTool', description='A simple tool')
print(tool.owner) # None
tool.set_owner(owner='Agent007')
print(tool.owner) # Agent007
```

#### `actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Абстрактный метод, предназначенный для предоставления определений действий инструмента в виде текста.

**Возвращает**:

- `str`: Текстовое представление определений действий инструмента.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

- Функция вызывает исключение `NotImplementedError`, указывая на то, что метод должен быть реализован в подклассах для предоставления конкретных определений действий инструмента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def actions_definitions_prompt(self) -> str:
        return "Action definitions for MyTool"

tool = MyTool(name='MyTool', description='A simple tool')
result = tool.actions_definitions_prompt()
print(result) # Action definitions for MyTool
```

#### `actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Абстрактный метод, предназначенный для предоставления ограничений действий инструмента в виде текста.

**Возвращает**:

- `str`: Текстовое представление ограничений действий инструмента.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

- Функция вызывает исключение `NotImplementedError`, указывая на то, что метод должен быть реализован в подклассах для предоставления конкретных ограничений действий инструмента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def actions_constraints_prompt(self) -> str:
        return "Action constraints for MyTool"

tool = MyTool(name='MyTool', description='A simple tool')
result = tool.actions_constraints_prompt()
print(result) # Action constraints for MyTool
```

#### `process_action`

```python
def process_action(self, agent, action: dict) -> bool:
    """
    
    """
    self._protect_real_world()
    self._enforce_ownership(agent)
    self._process_action(agent, action)
```

**Назначение**: Обработка действия агента с предварительной защитой от побочных эффектов и проверкой прав собственности.

**Параметры**:

- `agent`: Агент, выполняющий действие.
- `action` (dict): Словарь, содержащий информацию о действии.

**Как работает функция**:

- Функция вызывает методы `_protect_real_world` и `_enforce_ownership` для защиты от побочных эффектов и проверки прав собственности. Затем она вызывает метод `_process_action` для обработки действия агента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        print(f"Agent {agent} is performing action: {action}")
        return True

tool = MyTool(name='MyTool', description='A simple tool')
result = tool.process_action(agent='TestAgent', action={'name': 'TestAction'})
print(result) # TestAgent is performing action: {'name': 'TestAction'}