# Модуль tinytroupe.tools.tiny_tool

## Обзор

Модуль определяет базовый класс `TinyTool`, предназначенный для создания инструментов, используемых агентами в рамках системы `tinytroupe`. Он предоставляет основу для реализации различных действий, выполняемых агентами, и обеспечивает механизмы контроля доступа и защиты от нежелательных побочных эффектов.

## Подробней

Модуль содержит класс `TinyTool`, который является базовым классом для всех инструментов. Он определяет основные атрибуты и методы, необходимые для работы инструмента, такие как имя, описание, владелец, наличие побочных эффектов, экспортер и обогатитель.

## Классы

### `TinyTool`

**Описание**: Базовый класс для создания инструментов, используемых агентами.

**Наследует**: `JsonSerializableRegistry`

**Атрибуты**:

-   `name` (str): Имя инструмента.
-   `description` (str): Краткое описание инструмента.
-   `owner` (str): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом.
-   `real_world_side_effects` (bool): Указывает, имеет ли инструмент побочные эффекты, влияющие на реальный мир.
-   `exporter` (ArtifactExporter): Экспортер для сохранения результатов работы инструмента.
-   `enricher` (Enricher): Обогатитель для расширения результатов работы инструмента.

**Методы**:

-   `__init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None)`: Инициализирует новый инструмент.
-   `_process_action(self, agent, action: dict) -> bool`: Абстрактный метод, который должен быть реализован в подклассах.
-   `_protect_real_world(self)`: Предупреждает о наличии побочных эффектов, влияющих на реальный мир.
-   `_enforce_ownership(self, agent)`: Проверяет, имеет ли агент право на использование инструмента.
-   `set_owner(self, owner)`: Устанавливает владельца инструмента.
-   `actions_definitions_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах.
-   `actions_constraints_prompt(self) -> str`: Абстрактный метод, который должен быть реализован в подклассах.
-   `process_action(self, agent, action: dict) -> bool`: Выполняет действие инструмента, предварительно проверяя наличие побочных эффектов и права доступа.

### `__init__`

```python
def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
```

**Назначение**: Инициализация экземпляра класса `TinyTool`.

**Параметры**:

-   `name` (str): Имя инструмента.
-   `description` (str): Описание инструмента.
-   `owner` (str, optional): Владелец инструмента. По умолчанию `None`.
-   `real_world_side_effects` (bool, optional): Флаг, указывающий на наличие реальных побочных эффектов. По умолчанию `False`.
-   `exporter` (ArtifactExporter, optional): Экспортер артефактов. По умолчанию `None`.
-   `enricher` (Enricher, optional): Обогатитель. По умолчанию `None`.

**Возвращает**: `None`

**Как работает функция**:

-   Функция инициализирует атрибуты экземпляра класса `TinyTool` значениями, переданными в качестве аргументов.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool
from tinytroupe.tools import logger
from tinytroupe.utils import JsonSerializableRegistry

# Пример создания экземпляра TinyTool
tool = TinyTool(name="MyTool", description="A simple tool", real_world_side_effects=False)
logger.info(f"Tool created: {tool.name}")
```

### `_process_action`

```python
def _process_action(self, agent, action: dict) -> bool:
```

**Назначение**: Абстрактный метод, предназначенный для переопределения в подклассах.

**Параметры**:

-   `agent` (Any): Агент, выполняющий действие.
-   `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:
-   `bool`: Возвращает `True` или `False` в зависимости от успешности выполнения действия.

**Вызывает исключения**:

-   `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:

-   Функция предназначена для выполнения конкретного действия инструмента.

**Примеры**:

```python
class MyTool(TinyTool):
    def _process_action(self, agent, action: dict) -> bool:
        """
        Пример реализации метода _process_action.
        """
        logger.info(f"Agent {agent.name} is processing action: {action}")
        return True

# Пример создания экземпляра MyTool и вызова метода _process_action
my_tool = MyTool(name="MyTool", description="A simple tool", real_world_side_effects=False)
# my_tool._process_action(agent, action) # вызовет исключение, так как метод защищенный
```

### `_protect_real_world`

```python
def _protect_real_world(self):
```

**Назначение**: Вывод предупреждения в лог, если инструмент имеет побочные эффекты, влияющие на реальный мир.

**Параметры**:

-   `self` (TinyTool): Экземпляр класса `TinyTool`.

**Возвращает**: `None`

**Как работает функция**:

-   Функция проверяет атрибут `real_world_side_effects`. Если он `True`, выводится предупреждение в лог.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool
from tinytroupe.tools import logger
from tinytroupe.utils import JsonSerializableRegistry

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        """
        Пример реализации метода _process_action.
        """
        logger.info(f"Agent {agent.name} is processing action: {action}")
        return True

# Пример создания экземпляра MyTool с real_world_side_effects=True
my_tool = MyTool(name="MyTool", description="A tool with real-world side effects", real_world_side_effects=True)
my_tool._protect_real_world()  # Выведет предупреждение в лог
```

### `_enforce_ownership`

```python
def _enforce_ownership(self, agent):
```

**Назначение**: Проверка, имеет ли агент право на использование инструмента.

**Параметры**:

-   `agent` (Any): Агент, пытающийся использовать инструмент.

**Возвращает**: `None`

**Вызывает исключения**:

-   `ValueError`: Если агент не является владельцем инструмента.

**Как работает функция**:

-   Функция проверяет, установлен ли владелец инструмента (`self.owner`). Если владелец установлен, функция проверяет, совпадает ли имя агента с именем владельца. Если имена не совпадают, выбрасывается исключение `ValueError`.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool
from tinytroupe.tools import logger
from tinytroupe.utils import JsonSerializableRegistry

class Agent:
    def __init__(self, name):
        self.name = name

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        """
        Пример реализации метода _process_action.
        """
        logger.info(f"Agent {agent.name} is processing action: {action}")
        return True

# Пример создания экземпляра MyTool с владельцем
owner = Agent(name="OwnerAgent")
my_tool = MyTool(name="MyTool", description="A tool with an owner", owner=owner)

# Пример создания агента, который не является владельцем
agent = Agent(name="OtherAgent")

try:
    my_tool._enforce_ownership(agent)  # Вызовет исключение ValueError
except ValueError as ex:
    logger.error("Agent does not own the tool", ex, exc_info=True)
```

### `set_owner`

```python
def set_owner(self, owner):
```

**Назначение**: Устанавливает владельца инструмента.

**Параметры**:

-   `owner` (str): Агент, который будет владельцем инструмента.

**Возвращает**: `None`

**Как работает функция**:

-   Функция устанавливает атрибут `self.owner` равным значению аргумента `owner`.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool
from tinytroupe.tools import logger
from tinytroupe.utils import JsonSerializableRegistry

class Agent:
    def __init__(self, name):
        self.name = name

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        """
        Пример реализации метода _process_action.
        """
        logger.info(f"Agent {agent.name} is processing action: {action}")
        return True

# Пример создания экземпляра MyTool без владельца
my_tool = MyTool(name="MyTool", description="A tool without an owner")

# Пример установки владельца
owner = Agent(name="OwnerAgent")
my_tool.set_owner(owner)
logger.info(f"Tool owner set to: {my_tool.owner.name}")
```

### `actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
```

**Назначение**:  Абстрактный метод, который должен быть реализован в подклассах.

**Параметры**:

-   `self` (TinyTool): Экземпляр класса `TinyTool`.

**Возвращает**:
-   `str`: Возвращает строку.

**Вызывает исключения**:

-   `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:

-   Метод возвращает определения действий.

**Примеры**:

```python
class MyTool(TinyTool):
    def actions_definitions_prompt(self) -> str:
        """
        Пример реализации метода actions_definitions_prompt.
        """
        return "This is the actions definitions prompt."

# Пример создания экземпляра MyTool и вызова метода actions_definitions_prompt
my_tool = MyTool(name="MyTool", description="A simple tool", real_world_side_effects=False)
# result = my_tool.actions_definitions_prompt() # Переопределено в дочернем классе.
```

### `actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
```

**Назначение**: Абстрактный метод, который должен быть реализован в подклассах.

**Параметры**:

-   `self` (TinyTool): Экземпляр класса `TinyTool`.

**Возвращает**:
-   `str`: Возвращает строку.

**Вызывает исключения**:

-   `NotImplementedError`: Вызывается, если метод не переопределен в подклассе.

**Как работает функция**:

-   Метод возвращает ограничения действия.

**Примеры**:

```python
class MyTool(TinyTool):
    def actions_constraints_prompt(self) -> str:
        """
        Пример реализации метода actions_constraints_prompt.
        """
        return "This is the actions constraints prompt."

# Пример создания экземпляра MyTool и вызова метода actions_constraints_prompt
my_tool = MyTool(name="MyTool", description="A simple tool", real_world_side_effects=False)
# result = my_tool.actions_constraints_prompt() # Переопределено в дочернем классе.
```

### `process_action`

```python
def process_action(self, agent, action: dict) -> bool:
```

**Назначение**: Выполняет действие инструмента, предварительно проверяя наличие побочных эффектов и права доступа.

**Параметры**:

-   `agent` (Any): Агент, выполняющий действие.
-   `action` (dict): Словарь, содержащий информацию о действии.

**Возвращает**:

-   `bool`: Возвращает `True` или `False` в зависимости от успешности выполнения действия.

**Как работает функция**:

1.  Вызывает метод `_protect_real_world()` для проверки и предупреждения о побочных эффектах.
2.  Вызывает метод `_enforce_ownership()` для проверки прав доступа агента к инструменту.
3.  Вызывает метод `_process_action()` для выполнения конкретного действия инструмента.

**Примеры**:

```python
from tinytroupe.tools.tiny_tool import TinyTool
from tinytroupe.tools import logger
from tinytroupe.utils import JsonSerializableRegistry

class Agent:
    def __init__(self, name):
        self.name = name

class MyTool(TinyTool):
    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        """
        Пример реализации метода _process_action.
        """
        logger.info(f"Agent {agent.name} is processing action: {action}")
        return True

# Пример создания экземпляра MyTool и вызова метода process_action
agent = Agent(name="TestAgent")
my_tool = MyTool(name="MyTool", description="A simple tool", real_world_side_effects=False)
action = {"action_type": "test_action"}
result = my_tool.process_action(agent, action)
logger.info(f"Action processed: {result}")