# Модуль для определения и управления ментальными способностями агента
==================================================================

Модуль содержит классы для представления и управления ментальными способностями агента, такими как память, доступ к файлам и использование инструментов.

## Обзор

Этот модуль предоставляет абстракции для представления ментальных способностей агента в системе.
Он включает базовый класс `TinyMentalFaculty`, который служит основой для создания конкретных ментальных способностей,
таких как `CustomMentalFaculty`, `RecallFaculty`, `FilesAndWebGroundingFaculty` и `TinyToolUse`.
Эти классы позволяют агенту выполнять различные действия, такие как вспоминание информации, доступ к локальным файлам и веб-страницам, а также использование внешних инструментов.

## Подробнее

Модуль предоставляет инструменты для определения когнитивных способностей агента, управления ими и интеграции с другими частями системы.
Он позволяет создавать гибкие и настраиваемые ментальные модели, которые могут быть адаптированы к различным задачам и требованиям.
В частности, модуль предоставляет возможность определять действия, которые может выполнять агент, а также ограничения на эти действия.

## Классы

### `TinyMentalFaculty`

**Описание**:
Представляет собой ментальную способность агента. Ментальные способности - это когнитивные возможности, которыми обладает агент.

**Атрибуты**:
- `name` (str): Название ментальной способности.
- `requires_faculties` (list): Список ментальных способностей, необходимых для функционирования данной способности.

**Методы**:
- `__init__(self, name: str, requires_faculties: list = None) -> None`:
    Инициализирует ментальную способность.
- `__str__(self) -> str`:
    Возвращает строковое представление ментальной способности.
- `__eq__(self, other) -> bool`:
    Сравнивает две ментальные способности на равенство.
- `process_action(self, agent, action: dict) -> bool`:
    Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`:
    Возвращает подсказку для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`:
    Возвращает подсказку для определения ограничений на действия, связанные с этой способностью.

### `CustomMentalFaculty`

**Описание**:
Представляет собой пользовательскую ментальную способность агента. Пользовательские ментальные способности - это когнитивные способности, которые агент имеет и которые определены пользователем просто путем указания действий, которые способность может выполнять, или ограничений, которые способность вводит. Ограничения могут быть связаны с действиями, которые способность может выполнять, или быть независимыми, более общими ограничениями, которым агент должен следовать.
**Наследует**:
`TinyMentalFaculty`

**Атрибуты**:
- `actions_configs` (dict): Словарь с конфигурацией действий, которые может выполнять эта способность.
- `constraints` (dict): Список ограничений, введенных этой способностью.

**Методы**:
- `__init__(self, name: str, requires_faculties: list = None, actions_configs: dict = None, constraints: dict = None)`:
    Инициализирует пользовательскую ментальную способность.
- `add_action(self, action_name: str, description: str, function: Callable = None)`:
    Добавляет действие в конфигурацию действий.
- `add_actions(self, actions: dict)`:
    Добавляет несколько действий в конфигурацию действий.
- `add_action_constraint(self, constraint: str)`:
    Добавляет ограничение на действие.
- `add_actions_constraints(self, constraints: list)`:
    Добавляет несколько ограничений на действия.
- `process_action(self, agent, action: dict) -> bool`:
    Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`:
    Возвращает подсказку для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`:
    Возвращает подсказку для определения ограничений на действия, связанные с этой способностью.

### `RecallFaculty`

**Описание**:
Представляет собой ментальную способность агента к вспоминанию информации.

**Наследует**:
`TinyMentalFaculty`

**Методы**:
- `__init__(self)`:
    Инициализирует способность к вспоминанию.
- `process_action(self, agent, action: dict) -> bool`:
    Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`:
    Возвращает подсказку для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`:
    Возвращает подсказку для определения ограничений на действия, связанные с этой способностью.

### `FilesAndWebGroundingFaculty`

**Описание**:
Позволяет агенту получать доступ к локальным файлам и веб-страницам, чтобы обосновать свои знания.

**Наследует**:
`TinyMentalFaculty`

**Атрибуты**:
- `local_files_grounding_connector` (LocalFilesGroundingConnector): Коннектор для доступа к локальным файлам.
- `web_grounding_connector` (WebPagesGroundingConnector): Коннектор для доступа к веб-страницам.

**Методы**:
- `__init__(self, folders_paths: list = None, web_urls: list = None)`:
    Инициализирует способность к доступу к файлам и веб-страницам.
- `process_action(self, agent, action: dict) -> bool`:
    Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`:
    Возвращает подсказку для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`:
    Возвращает подсказку для определения ограничений на действия, связанные с этой способностью.

### `TinyToolUse`

**Описание**:
Позволяет агенту использовать инструменты для выполнения задач. Использование инструментов - один из важнейших когнитивных навыков, которым обладают люди и приматы, как мы знаем.

**Наследует**:
`TinyMentalFaculty`

**Атрибуты**:
- `tools` (list): Список инструментов, доступных агенту.

**Методы**:
- `__init__(self, tools: list) -> None`:
    Инициализирует способность к использованию инструментов.
- `process_action(self, agent, action: dict) -> bool`:
    Обрабатывает действие, связанное с этой способностью.
- `actions_definitions_prompt(self) -> str`:
    Возвращает подсказку для определения действий, связанных с этой способностью.
- `actions_constraints_prompt(self) -> str`:
    Возвращает подсказку для определения ограничений на действия, связанные с этой способностью.

## Методы классов

### `TinyMentalFaculty`

#### `__init__(self, name: str, requires_faculties: list = None) -> None`

```python
def __init__(self, name: str, requires_faculties: list = None) -> None:
    """
    Инициализирует ментальную способность.

    Args:
        name (str): Название ментальной способности.
        requires_faculties (list): Список ментальных способностей, необходимых для функционирования данной способности.
    """
```

**Назначение**:
Инициализирует объект `TinyMentalFaculty`. Принимает название способности и список способностей, от которых она зависит.

**Параметры**:
- `name` (str): Название ментальной способности.
- `requires_faculties` (list, optional): Список названий ментальных способностей, от которых зависит данная способность. По умолчанию `None`.

**Как работает функция**:
- Устанавливает атрибут `name` равным переданному значению.
- Если `requires_faculties` не указан, инициализирует `self.requires_faculties` пустым списком.
- Если `requires_faculties` указан, устанавливает `self.requires_faculties` равным переданному списку.

**Примеры**:

```python
faculty = TinyMentalFaculty("Reasoning")
print(faculty.name)  # Вывод: Reasoning
print(faculty.requires_faculties)  # Вывод: []

faculty = TinyMentalFaculty("Planning", ["Reasoning", "Memory"])
print(faculty.name)  # Вывод: Planning
print(faculty.requires_faculties)  # Вывод: ['Reasoning', 'Memory']
```

#### `__str__(self) -> str`

```python
def __str__(self) -> str:
    """
    Возвращает строковое представление ментальной способности.
    """
```

**Назначение**:
Возвращает строковое представление объекта `TinyMentalFaculty`.

**Возвращает**:
- `str`: Строковое представление ментальной способности в формате "Mental Faculty: {name}".

**Как работает функция**:
Формирует строку, включающую название способности.

**Примеры**:

```python
faculty = TinyMentalFaculty("Reasoning")
print(str(faculty))  # Вывод: Mental Faculty: Reasoning
```

#### `__eq__(self, other) -> bool`

```python
def __eq__(self, other):
    """
    Сравнивает две ментальные способности на равенство.
    """
```

**Назначение**:
Сравнивает текущий объект `TinyMentalFaculty` с другим объектом на равенство.

**Параметры**:
- `other` (Any): Объект для сравнения.

**Возвращает**:
- `bool`: `True`, если объекты равны (имеют одинаковое название), `False` в противном случае.

**Как работает функция**:
- Проверяет, является ли `other` экземпляром класса `TinyMentalFaculty`.
- Если да, сравнивает атрибут `name` текущего объекта с атрибутом `name` объекта `other`.
- Возвращает `True`, если названия совпадают, и `False` в противном случае.
- Если `other` не является экземпляром класса `TinyMentalFaculty`, возвращает `False`.

**Примеры**:

```python
faculty1 = TinyMentalFaculty("Reasoning")
faculty2 = TinyMentalFaculty("Reasoning")
faculty3 = TinyMentalFaculty("Planning")

print(faculty1 == faculty2)  # Вывод: True
print(faculty1 == faculty3)  # Вывод: False
print(faculty1 == "Reasoning")  # Вывод: False
```

#### `process_action(self, agent, action: dict) -> bool`

```python
def process_action(self, agent, action: dict) -> bool:
    """
    Processes an action related to this faculty.

    Args:
        action (dict): The action to process.
    
    Returns:
        bool: True if the action was successfully processed, False otherwise.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**:
Обрабатывает действие, связанное с данной ментальной способностью. Этот метод должен быть переопределен в подклассах.

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, представляющий действие.

**Возвращает**:
- `bool`: `True`, если действие было успешно обработано, `False` в противном случае.

**Вызывает исключения**:
- `NotImplementedError`: Если метод не переопределен в подклассе.

**Как работает функция**:
Вызывает исключение `NotImplementedError`, указывающее на то, что метод должен быть реализован в подклассах.

#### `actions_definitions_prompt(self) -> str`

```python
def actions_definitions_prompt(self) -> str:
    """
    Returns the prompt for defining a actions related to this faculty.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**:
Возвращает подсказку для определения действий, связанных с данной ментальной способностью. Этот метод должен быть переопределен в подклассах.

**Возвращает**:
- `str`: Подсказка для определения действий.

**Вызывает исключения**:
- `NotImplementedError`: Если метод не переопределен в подклассе.

**Как работает функция**:
Вызывает исключение `NotImplementedError`, указывающее на то, что метод должен быть реализован в подклассах.

#### `actions_constraints_prompt(self) -> str`

```python
def actions_constraints_prompt(self) -> str:
    """
    Returns the prompt for defining constraints on actions related to this faculty.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**:
Возвращает подсказку для определения ограничений на действия, связанные с данной ментальной способностью. Этот метод должен быть переопределен в подклассах.

**Возвращает**:
- `str`: Подсказка для определения ограничений на действия.

**Вызывает исключения**:
- `NotImplementedError`: Если метод не переопределен в подклассе.

**Как работает функция**:
Вызывает исключение `NotImplementedError`, указывающее на то, что метод должен быть реализован в подклассах.

### `CustomMentalFaculty`

#### `__init__(self, name: str, requires_faculties: list = None, actions_configs: dict = None, constraints: dict = None)`

```python
def __init__(self, name: str, requires_faculties: list = None,
                 actions_configs: dict = None, constraints: dict = None):
    """
    Initializes the custom mental faculty.

    Args:
        name (str): The name of the mental faculty.
        requires_faculties (list): A list of mental faculties that this faculty requires to function properly. 
          Format is ["faculty1", "faculty2", ...]
        actions_configs (dict): A dictionary with the configuration of actions that this faculty can perform.
          Format is {<action_name>: {"description": <description>, "function": <function>}}
        constraints (dict): A list with the constraints introduced by this faculty.
          Format is [<constraint1>, <constraint2>, ...]
    """
    super().__init__(name, requires_faculties)

    # {<action_name>: {"description": <description>, "function": <function>}}
    if actions_configs is None:
        self.actions_configs = {}
    else:
        self.actions_configs = actions_configs
    
    # [<constraint1>, <constraint2>, ...]
    if constraints is None:
        self.constraints = {}
    else:
        self.constraints = constraints
```

**Назначение**:
Инициализирует объект `CustomMentalFaculty`.

**Параметры**:
- `name` (str): Название пользовательской ментальной способности.
- `requires_faculties` (list, optional): Список названий ментальных способностей, от которых зависит данная способность. По умолчанию `None`.
- `actions_configs` (dict, optional): Словарь, содержащий конфигурацию действий, которые может выполнять данная способность. По умолчанию `None`.
- `constraints` (dict, optional): Список ограничений, введенных данной способностью. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `TinyMentalFaculty` для инициализации атрибутов `name` и `requires_faculties`.
- Инициализирует атрибут `actions_configs` либо пустым словарем, если `actions_configs` не указан, либо переданным словарем.
- Инициализирует атрибут `constraints` либо пустым списком, если `constraints` не указан, либо переданным списком.

**Примеры**:

```python
faculty = CustomMentalFaculty("DecisionMaking")
print(faculty.name)  # Вывод: DecisionMaking
print(faculty.actions_configs)  # Вывод: {}
print(faculty.constraints)  # Вывод: {}

actions = {"ChooseAction": {"description": "Choose the best action", "function": None}}
constraints = ["Must choose an action", "Action must be relevant"]
faculty = CustomMentalFaculty("Planning", ["Reasoning"], actions, constraints)
print(faculty.name)  # Вывод: Planning
print(faculty.actions_configs)
# Вывод: {'ChooseAction': {'description': 'Choose the best action', 'function': None}}
print(faculty.constraints)  # Вывод: ['Must choose an action', 'Action must be relevant']
```

#### `add_action(self, action_name: str, description: str, function: Callable = None)`

```python
def add_action(self, action_name: str, description: str, function: Callable=None):
    self.actions_configs[action_name] = {"description": description, "function": function}
```

**Назначение**:
Добавляет новое действие в конфигурацию действий данной ментальной способности.

**Параметры**:
- `action_name` (str): Название добавляемого действия.
- `description` (str): Описание добавляемого действия.
- `function` (Callable, optional): Функция, выполняемая при вызове данного действия. По умолчанию `None`.

**Как работает функция**:
Добавляет в словарь `self.actions_configs` новую запись, где ключом является `action_name`, а значением - словарь с ключами "description" и "function", соответствующими переданным параметрам.

**Примеры**:

```python
faculty = CustomMentalFaculty("DecisionMaking")
faculty.add_action("ChooseAction", "Choose the best action", None)
print(faculty.actions_configs)
# Вывод: {'ChooseAction': {'description': 'Choose the best action', 'function': None}}
```

#### `add_actions(self, actions: dict)`

```python
def add_actions(self, actions: dict):
    for action_name, action_config in actions.items():
        self.add_action(action_name, action_config['description'], action_config['function'])
```

**Назначение**:
Добавляет несколько действий в конфигурацию действий данной ментальной способности.

**Параметры**:
- `actions` (dict): Словарь, содержащий конфигурацию добавляемых действий. Ключом является название действия, а значением - словарь с ключами "description" и "function".

**Как работает функция**:
Перебирает элементы словаря `actions` и вызывает метод `self.add_action` для каждого действия.

**Примеры**:

```python
faculty = CustomMentalFaculty("DecisionMaking")
actions = {
    "ChooseAction": {"description": "Choose the best action", "function": None},
    "EvaluateAction": {"description": "Evaluate the chosen action", "function": None}
}
faculty.add_actions(actions)
print(faculty.actions_configs)
# Вывод:
# {'ChooseAction': {'description': 'Choose the best action', 'function': None},
#  'EvaluateAction': {'description': 'Evaluate the chosen action', 'function': None}}
```

#### `add_action_constraint(self, constraint: str)`

```python
def add_action_constraint(self, constraint: str):
    self.constraints.append(constraint)
```

**Назначение**:
Добавляет новое ограничение на действия данной ментальной способности.

**Параметры**:
- `constraint` (str): Добавляемое ограничение.

**Как работает функция**:
Добавляет переданное ограничение в список `self.constraints`.

**Примеры**:

```python
faculty = CustomMentalFaculty("DecisionMaking")
faculty.add_action_constraint("Must choose an action")
print(faculty.constraints)  # Вывод: ['Must choose an action']
```

#### `add_actions_constraints(self, constraints: list)`

```python
def add_actions_constraints(self, constraints: list):
    for constraint in constraints:
        self.add_action_constraint(constraint)
```

**Назначение**:
Добавляет несколько ограничений на действия данной ментальной способности.

**Параметры**:
- `constraints` (list): Список добавляемых ограничений.

**Как работает функция**:
Перебирает элементы списка `constraints` и вызывает метод `self.add_action_constraint` для каждого ограничения.

**Примеры**:

```python
faculty = CustomMentalFaculty("DecisionMaking")
constraints = ["Must choose an action", "Action must be relevant"]
faculty.add_actions_constraints(constraints)
print(faculty.constraints)  # Вывод: ['Must choose an action', 'Action must be relevant']
```

#### `process_action(self, agent, action: dict) -> bool`

```python
def process_action(self, agent, action: dict) -> bool:
    agent.logger.debug(f"Processing action: {action}")

    action_type = action['type']
    if action_type in self.actions_configs:
        action_config = self.actions_configs[action_type]
        action_function = action_config.get("function", None)

        if action_function is not None:
            action_function(agent, action)
        
        # one way or another, the action was processed
        return True 
    
    else:
        return False
```

**Назначение**:
Обрабатывает действие, связанное с данной ментальной способностью.

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, представляющий действие.

**Возвращает**:
- `bool`: `True`, если действие было успешно обработано, `False` в противном случае.

**Как работает функция**:
- Логирует отладочное сообщение о начале обработки действия.
- Извлекает тип действия из словаря `action`.
- Проверяет, содержится ли тип действия в словаре `self.actions_configs`.
- Если да, извлекает конфигурацию действия из словаря `self.actions_configs`.
- Извлекает функцию действия из конфигурации действия.
- Если функция действия существует, вызывает ее, передавая ей агента и действие.
- Возвращает `True`, если действие было успешно обработано, `False` в противном случае.

#### `actions_definitions_prompt(self) -> str`

```python
def actions_definitions_prompt(self) -> str:
    prompt = ""
    for action_name, action_config in self.actions_configs.items():
        prompt += f"  - {action_name.upper()}: {action_config['description']}\\n"
    
    return prompt
```

**Назначение**:
Возвращает подсказку для определения действий, связанных с данной ментальной способностью.

**Возвращает**:
- `str`: Подсказка для определения действий.

**Как работает функция**:
- Создает пустую строку `prompt`.
- Перебирает элементы словаря `self.actions_configs`.
- Для каждого действия добавляет в строку `prompt` строку в формате "  - {action_name.upper()}: {action_config['description']}\n".
- Возвращает строку `prompt`.

#### `actions_constraints_prompt(self) -> str`

```python
def actions_constraints_prompt(self) -> str:
    prompt = ""
    for constraint in self.constraints:
        prompt += f"  - {constraint}\\n"
    
    return prompt
```

**Назначение**:
Возвращает подсказку для определения ограничений на действия, связанные с данной ментальной способностью.

**Возвращает**:
- `str`: Подсказка для определения ограничений на действия.

**Как работает функция**:
- Создает пустую строку `prompt`.
- Перебирает элементы списка `self.constraints`.
- Для каждого ограничения добавляет в строку `prompt` строку в формате "  - {constraint}\n".
- Возвращает строку `prompt`.

### `RecallFaculty`

#### `__init__(self)`

```python
def __init__(self):
    super().__init__("Memory Recall")
```

**Назначение**:
Инициализирует объект `RecallFaculty`.

**Как работает функция**:
Вызывает конструктор родительского класса `TinyMentalFaculty` с названием "Memory Recall".

**Примеры**:

```python
faculty = RecallFaculty()
print(faculty.name)  # Вывод: Memory Recall
```

#### `process_action(self, agent, action: dict) -> bool`

```python
def process_action(self, agent, action: dict) -> bool:
    agent.logger.debug(f"Processing action: {action}")

    if action['type'] == "RECALL" and action['content'] is not None:
        content = action['content']

        semantic_memories = agent.retrieve_relevant_memories(relevance_target=content)

        agent.logger.info(f"Recalling information related to '{content}'. Found {len(semantic_memories)} relevant memories.")

        if len(semantic_memories) > 0:
            # a string with each element in the list in a new line starting with a bullet point
            agent.think("I have remembered the following information from my semantic memory and will use it to guide me in my subsequent actions: \\n" + \\
                    "\\n".join([f"  - {item}" for item in semantic_memories]))
        else:
            agent.think(f"I can't remember anything about '{content}'.")
        
        return True
    
    else:
        return False
```

**Назначение**:
Обрабатывает действие, связанное с вспоминанием информации.

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, представляющий действие.

**Возвращает**:
- `bool`: `True`, если действие было успешно обработано, `False` в противном случае.

**Как работает функция**:
- Логирует отладочное сообщение о начале обработки действия.
- Проверяет, является ли тип действия "RECALL" и содержит ли действие непустой контент.
- Если да, извлекает контент из словаря `action`.
- Вызывает метод `agent.retrieve_relevant_memories` для извлечения релевантных воспоминаний.
- Логирует информационное сообщение о количестве найденных релевантных воспоминаний.
- Если релевантные воспоминания найдены, вызывает метод `agent.think` для добавления информации о них в сознание агента.
- Возвращает `True`, если действие было успешно обработано, `False` в противном случае.

#### `actions_definitions_prompt(self) -> str`

```python
def actions_definitions_prompt(self) -> str:
    prompt = """
              - RECALL: you can recall information from your memory. To do, you must specify a "mental query" to locate the desired memory. If the memory is found, it is brought to your conscience.
            """

    return textwrap.dedent(prompt)
```

**Назначение**:
Возвращает подсказку для определения действия "RECALL".

**Возвращает**:
- `str`: Подсказка для определения действия "RECALL".

**Как работает функция**:
Формирует строку, содержащую описание действия "RECALL".

#### `actions_constraints_prompt(self) -> str`

```python
def actions_constraints_prompt(self) -> str:
    prompt = """
            - Before concluding you don't know something or don't have access to some information, you **must** try to RECALL it from your memory.
            - You try to RECALL information from your semantic/factual memory, so that you can have more relevant elements to think and talk about, whenever such an action would be likely
                to enrich the current interaction. To do so, you must specify able "mental query" that is related to the things you've been thinking, listening and talking about.
                Example:
                ```
                <THINK A>
                <RECALL B, which is something related to A>
                <THINK about A and B>
                <TALK about A and B>
                DONE
                ```
            - If you RECALL:
                * you use a "mental query" that describe the elements you are looking for, you do not use a question. It is like a keyword-based search query.
                For example, instead of "What are the symptoms of COVID-19?", you would use "COVID-19 symptoms".
                * you use keywords likely to be found in the text you are looking for. For example, instead of "Brazil economic outlook", you would use "Brazil economy", "Brazil GPD", "Brazil inflation", etc.
            - It may take several tries of RECALL to get the relevant information you need. If you don't find what you are looking for, you can try again with a **very** different "mental query".
                Be creative: you can use synonyms, related concepts, or any other strategy you think might help you to find the information you need. Avoid using the same terms in different queries, as it is likely to return the same results. Whenever necessary, you should retry RECALL a couple of times before giving up the location of more information.
                Example:
                ```
                <THINK something>
                <RECALL "cat products">
                <THINK something>
                <RECALL "feline artifacts">
                <THINK something>
                <RECALL "pet store">
                <THINK something>
                <TALK something>
                DONE
                ```
            - You **may** interleave THINK and RECALL so that you can better reflect on the information you are trying to recall.
            - If you need information about a specific document, you **must** use CONSULT instead of RECALL. This is because RECALL **does not** allow you to select the specific document, and only brings small 
                relevant parts of variious documents - while CONSULT brings the precise document requested for your inspection, with its full content. 
                Example:
                ```
                LIST_DOCUMENTS
                <CONSULT some document name>
                <THINK something about the retrieved document>
                <TALK something>
                DONE
                ``` 
          """

    return textwrap.dedent(prompt)
```

**Назначение**:
Возвращает подсказку для определения ограничений на действие "RECALL".

**Возвращает**:
- `str`: Подсказка для определения ограничений на действие "RECALL".

**Как работает функция**:
Формирует строку, содержащую описание ограничений на действие "RECALL".

### `FilesAndWebGroundingFaculty`

#### `__init__(self, folders_paths: list = None, web_urls: list = None)`

```python
def __init__(self, folders_paths: list=None, web_urls: list=None):
    super().__init__("Local Files and Web Grounding")

    self.local_files_grounding_connector = LocalFilesGroundingConnector(folders_paths=folders_paths)
    self.web_grounding_connector = WebPagesGroundingConnector(web_urls=web_urls)
```

**Назначение**:
Инициализирует объект `FilesAndWebGroundingFaculty`.

**Параметры**:
- `folders_paths` (list, optional): Список путей к локальным папкам. По умолчанию `None`.
- `web_urls` (list, optional): Список URL-адресов веб-страниц. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `TinyMentalFaculty` с названием "Local Files and Web Grounding".
- Создает объекты `LocalFilesGroundingConnector` и `WebPagesGroundingConnector` с переданными параметрами.

#### `process_action(self, agent, action: dict) -> bool`

```python
def process_action(self, agent, action: dict) -> bool:
    if action['type'] == "CONSULT" and action['content'] is not None:
        target_name = action['content']

        results = []
        results.append(self.local_files_grounding_connector.retrieve_by_name(target_name))
        results.append(self.web_grounding_connector.retrieve_by_name(target_name))

        if len(results) > 0:
            agent.think(f"I have read the following document: \\n{results}")
        else:
            agent.think(f"I can't find any document with the name '{target_name}'.")
        
        return True
    
    elif action['type'] == "LIST_DOCUMENTS" and action['content'] is not None:
        available_names = []
        available_names += self.local_files_grounding_connector.list_sources()
        available_names += self.web_grounding_connector.list_sources()

        if len(available_names) > 0:
            agent.think(f"I have the following documents available to me: {available_names}")
        else:
            agent.think(f"I don't have any documents available for inspection.")
        
        return True

    else:
        return False
```

**Назначение**:
Обрабатывает действия "CONSULT" (консультация с документом) и "LIST_DOCUMENTS" (получение списка доступных документов).

**Параметры**:
- `agent` (Any): Агент, выполняющий действие.
- `action` (dict): Словарь, представляющий действие.

**Возвращает**:
- `bool`: `True`, если действие было успешно обработано, `False` в противном случае.

**Как работает функция**:
- Если тип действия "CONSULT" и указано имя документа:
    - Извлекает имя документа из словаря `action`.
    - Получает контент документа из локальных файлов и веб-страниц с использованием соответствующих коннекторов.
    - Если документ найден, добавляет информацию о нем в сознание агента с помощью метода `agent.think`.
    - Если документ не найден, сообщает агенту об этом.
- Если тип действия "LIST_DOCUMENTS":
    - Получает список доступных документов из локальных файлов и веб-страниц с использованием соответствующих коннекторов.
    - Если документы найдены, добавляет информацию о них в сознание агента с помощью метода `agent.think`.
    - Если документы не найдены, сообщает агенту об этом.
- Возвращает `True`, если действие было успешно обработано, `False` в противном случае.

#### `actions_definitions_prompt(self) -> str`

```python
def actions_definitions_prompt(self) -> str:
    prompt = """
            - LIST_DOCUMENTS: you can list the names of the documents you have access to, so that you can decide which to access, if any, to accomplish your goals. Documents is a generic term and includes any 
                kind of "packaged" information you can access, such as emails, files, chat messages, calendar events, etc. It also includes, in particular, web pages.
                The order of in which the documents are listed is not relevant.
            - CONSULT: you can retrieve and consult a specific document, so that you can access its content and accomplish your goals. To do so, you specify the name of the document you want to consult.
            """

    return textwrap.dedent(prompt)
```

**Назначение**:
Возвращает подсказку для определения действий "LIST_DOCUMENTS" и "CONSULT".

**Возвращает**: