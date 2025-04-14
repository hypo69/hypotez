# Модуль для проведения экспериментов (`experimentation.py`)

## Обзор

Модуль содержит классы для проведения A/B-тестирования и реализации интервенций в рамках экспериментов. Включает класс `ABRandomizer` для рандомизации и дерандомизации вариантов, а также класс `Intervention` для моделирования воздействий на агентов и окружение.

## Подробней

Этот модуль предоставляет инструменты для контролируемого изменения параметров экспериментов и оценки их влияния на поведение агентов. Класс `ABRandomizer` позволяет проводить A/B-тестирование, а класс `Intervention` моделирует различные воздействия на агентов и их окружение.

## Классы

### `ABRandomizer`

**Описание**: Класс для рандомизации и дерандомизации двух вариантов в A/B-тестировании.

**Атрибуты**:
- `choices` (dict): Словарь, хранящий информацию о том, какие варианты были переключены для каждого элемента. Ключом является индекс элемента.
- `real_name_1` (str): Настоящее имя первого варианта.
- `real_name_2` (str): Настоящее имя второго варианта.
- `blind_name_a` (str): Имя первого варианта, отображаемое пользователю.
- `blind_name_b` (str): Имя второго варианта, отображаемое пользователю.
- `passtrough_name` (list): Список имен, которые не должны быть рандомизированы и возвращаются как есть.
- `random_seed` (int): Зерно для генератора случайных чисел.

**Методы**:

- `__init__(self, real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=[], random_seed=42)`
- `randomize(self, i: int, a: str, b: str)`
- `derandomize(self, i: int, a: str, b: str)`
- `derandomize_name(self, i: int, blind_name: str)`

#### `__init__(self, real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name: list = [], random_seed=42)`

```python
def __init__(self, real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B",
                       passtrough_name=[],
                       random_seed=42):
    """
    Args:
        real_name_1 (str): the name of the first option
        real_name_2 (str): the name of the second option
        blind_name_a (str): the name of the first option as seen by the user
        blind_name_b (str): the name of the second option as seen by the user
        passtrough_name (list): a list of names that should not be randomized and are always
                                returned as-is.
        random_seed (int): the random seed to use
    """
    ...
```

**Назначение**: Инициализирует класс `ABRandomizer` с заданными параметрами.

**Параметры**:
- `real_name_1` (str): Настоящее имя первого варианта (по умолчанию "control").
- `real_name_2` (str): Настоящее имя второго варианта (по умолчанию "treatment").
- `blind_name_a` (str): Имя первого варианта, отображаемое пользователю (по умолчанию "A").
- `blind_name_b` (str): Имя второго варианта, отображаемое пользователю (по умолчанию "B").
- `passtrough_name` (list): Список имен, которые не должны быть рандомизированы (по умолчанию пустой список).
- `random_seed` (int): Зерно для генератора случайных чисел (по умолчанию 42).

**Как работает функция**:
- Функция инициализирует атрибуты класса значениями, переданными в качестве аргументов. Она создает словарь `self.choices`, который будет использоваться для хранения информации о переключениях вариантов.

**Примеры**:

```python
randomizer = ABRandomizer(real_name_1='контроль', real_name_2='лечение', blind_name_a='Вариант A', blind_name_b='Вариант B', random_seed=123)
```

#### `randomize(self, i: int, a: str, b: str) -> tuple[str, str]`

```python
def randomize(self, i, a, b):
    """
    Args:
        i (int): index of the item
        a (str): first choice
        b (str): second choice
    """
    ...
```

**Назначение**: Случайным образом переключает два варианта (`a` и `b`) и возвращает их.

**Параметры**:
- `i` (int): Индекс элемента.
- `a` (str): Первый вариант.
- `b` (str): Второй вариант.

**Возвращает**:
- `tuple[str, str]`: Кортеж из двух строк, представляющих переключенные или непереключенные варианты.

**Как работает функция**:
- Функция использует генератор случайных чисел с заданным зерном (`self.random_seed`) для случайного выбора между двумя вариантами. Если случайное число меньше 0.5, варианты возвращаются в исходном порядке, иначе они переключаются. Результат выбора сохраняется в словаре `self.choices` для последующей дерандомизации.

**Примеры**:

```python
randomizer = ABRandomizer(random_seed=42)
option_a = "контрольная группа"
option_b = "экспериментальная группа"
randomized_a, randomized_b = randomizer.randomize(0, option_a, option_b)
print(f"Рандомизированные варианты: A = {randomized_a}, B = {randomized_b}")
```

#### `derandomize(self, i: int, a: str, b: str) -> tuple[str, str]`

```python
def derandomize(self, i, a, b):
    """
    Args:
        i (int): index of the item
        a (str): first choice
        b (str): second choice
    """
    ...
```

**Назначение**: Дерандомизирует варианты для элемента с индексом `i` и возвращает их в исходном порядке.

**Параметры**:
- `i` (int): Индекс элемента.
- `a` (str): Первый вариант.
- `b` (str): Второй вариант.

**Возвращает**:
- `tuple[str, str]`: Кортеж из двух строк, представляющих дерандомизированные варианты.

**Вызывает исключения**:
- `Exception`: Если для элемента `i` не найдена информация о рандомизации.

**Как работает функция**:
- Функция проверяет, были ли переключены варианты для элемента `i` в процессе рандомизации. Если варианты были переключены, функция возвращает их в исходном порядке. Если для элемента `i` не найдена информация о рандомизации, вызывается исключение.

**Примеры**:

```python
randomizer = ABRandomizer(random_seed=42)
option_a = "контрольная группа"
option_b = "экспериментальная группа"
randomized_a, randomized_b = randomizer.randomize(0, option_a, option_b)
derandomized_a, derandomized_b = randomizer.derandomize(0, randomized_a, randomized_b)
print(f"Дерандомизированные варианты: A = {derandomized_a}, B = {derandomized_b}")
```

#### `derandomize_name(self, i: int, blind_name: str) -> str`

```python
def derandomize_name(self, i, blind_name):
    """
    Args:
        i (int): index of the item
        choice_name (str): the choice made by the user
    """
    ...
```

**Назначение**: Декодирует выбор, сделанный пользователем, и возвращает соответствующий вариант.

**Параметры**:
- `i` (int): Индекс элемента.
- `blind_name` (str): Выбор, сделанный пользователем (имя варианта, отображаемое пользователю).

**Возвращает**:
- `str`: Настоящее имя выбранного варианта.

**Вызывает исключения**:
- `Exception`: Если для элемента `i` не найдена информация о рандомизации или если выбор пользователя не распознан.

**Как работает функция**:
- Функция проверяет, был ли рандомизирован элемент `i`. Если элемент был рандомизирован, функция возвращает настоящее имя варианта, противоположного тому, который выбрал пользователь. Если элемент не был рандомизирован, функция возвращает настоящее имя выбранного пользователем варианта. Если выбор пользователя не соответствует ни одному из известных вариантов, вызывается исключение.

**Примеры**:

```python
randomizer = ABRandomizer(real_name_1='контроль', real_name_2='лечение', blind_name_a='Вариант A', blind_name_b='Вариант B', random_seed=42)
randomizer.randomize(0, "Вариант A", "Вариант B")
choice = randomizer.derandomize_name(0, "Вариант A")
print(f"Выбранный вариант: {choice}")
```

### `Intervention`

**Описание**: Класс для моделирования интервенций (воздействий) на агентов и их окружение.

**Атрибуты**:
- `agents` (list | None): Список агентов, на которых оказывается воздействие.
- `environments` (list | None): Список окружений, на которые оказывается воздействие.
- `text_precondition` (str | None): Текстовое условие для применения интервенции.
- `precondition_func` (function | None): Функция-условие для применения интервенции.
- `effect_func` (function | None): Функция, определяющая эффект интервенции.

**Методы**:
- `__init__(self, agent=None, agents: list = None, environment=None, environments: list = None)`
- `check_precondition(self)`
- `apply(self)`
- `set_textual_precondition(self, text: str)`
- `set_functional_precondition(self, func)`
- `set_effect(self, effect_func)`

#### `__init__(self, agent=None, agents: list = None, environment=None, environments: list = None)`

```python
def __init__(self, agent=None, agents:list=None, environment=None, environments:list=None):
    """
    Args:
        agent (TinyPerson): the agent to intervene on
        environment (TinyWorld): the environment to intervene on
    """
    ...
```

**Назначение**: Инициализирует класс `Intervention` с заданными агентами и/или окружениями.

**Параметры**:
- `agent` (TinyPerson | None): Агент, на которого оказывается воздействие.
- `agents` (list | None): Список агентов, на которых оказывается воздействие.
- `environment` (TinyWorld | None): Окружение, на которое оказывается воздействие.
- `environments` (list | None): Список окружений, на которые оказывается воздействие.

**Вызывает исключения**:
- `Exception`: Если не предоставлен ни один агент или окружение, или если предоставлены как единичный агент/окружение, так и список агентов/окружений.

**Как работает функция**:
- Функция проверяет, что передан хотя бы один параметр (агент или окружение). Если переданы и единичный агент/окружение, и список агентов/окружений, вызывается исключение. Функция инициализирует атрибуты `self.agents` и `self.environments` в зависимости от переданных параметров.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

agent1 = TinyPerson()
intervention1 = Intervention(agent=agent1)  # создаем инстанс интервенции с одним агентом
```

```python
from tinytroupe.agent import TinyPerson

agent1 = TinyPerson()
agent2 = TinyPerson()
agents_list = [agent1, agent2]
intervention2 = Intervention(agents=agents_list)  # создаем инстанс интервенции со списком агентов
```

#### `check_precondition(self)`

```python
def check_precondition(self):
    """
    Check if the precondition for the intervention is met.
    """
    ...
```

**Назначение**: Проверяет, выполнено ли условие для применения интервенции.

**Вызывает исключения**:
- `NotImplementedError`: Метод должен быть переопределен в подклассах.

**Как работает функция**:
- В текущей реализации метод вызывает исключение `NotImplementedError`, указывая на то, что он должен быть переопределен в подклассах для реализации конкретной логики проверки условий.

#### `apply(self)`

```python
def apply(self):
    """
    Apply the intervention.
    """
    ...
```

**Назначение**: Применяет интервенцию, вызывая функцию эффекта.

**Как работает функция**:
- Функция вызывает функцию `self.effect_func` с аргументами `self.agents` и `self.environments`, что приводит к применению эффекта интервенции к заданным агентам и/или окружениям.

#### `set_textual_precondition(self, text: str)`

```python
def set_textual_precondition(self, text):
    """
    Args:
        text (str): the text of the precondition
    """
    ...
```

**Назначение**: Устанавливает текстовое условие для применения интервенции.

**Параметры**:
- `text` (str): Текст условия.

**Как работает функция**:
- Функция устанавливает атрибут `self.text_precondition` равным переданному тексту, который представляет собой текстовое описание условия для применения интервенции.

#### `set_functional_precondition(self, func)`

```python
def set_functional_precondition(self, func):
    """
    Args:
        func (function): the function of the precondition. 
          Must have the arguments: agent, agents, environment, environments.
    """
    ...
```

**Назначение**: Устанавливает функциональное условие для применения интервенции.

**Параметры**:
- `func` (function): Функция условия. Функция должна принимать аргументы: `agent`, `agents`, `environment`, `environments`.

**Как работает функция**:
- Функция устанавливает атрибут `self.precondition_func` равным переданной функции, которая представляет собой функциональное условие для применения интервенции.

#### `set_effect(self, effect_func)`

```python
def set_effect(self, effect_func):
    """
    Args:
        effect (str): the effect function of the intervention
    """
    ...
```

**Назначение**: Устанавливает функцию эффекта для интервенции.

**Параметры**:
- `effect_func` (function): Функция эффекта.

**Как работает функция**:
- Функция устанавливает атрибут `self.effect_func` равным переданной функции, которая определяет эффект интервенции при ее применении.