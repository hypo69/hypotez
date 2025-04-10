# Модуль `intervention.py`

## Обзор

Модуль определяет класс `Intervention`, предназначенный для моделирования и выполнения вмешательств в симуляциях с использованием `TinyPerson` и `TinyWorld`. Вмешательства позволяют изменять поведение агентов и окружающей среды на основе предварительных условий.

## Подробней

Основная цель данного модуля - предоставить механизм для активного управления симуляцией путем применения различных эффектов к агентам или миру при выполнении определенных условий. Это позволяет проводить эксперименты, в которых реакция системы на различные вмешательства может быть изучена и проанализирована.

## Классы

### `Intervention`

**Описание**: Класс `Intervention` предназначен для определения и выполнения вмешательств в симуляции. Он позволяет задавать условия, при которых должно быть выполнено вмешательство, а также эффекты, которые должны быть применены.

**Атрибуты**:
- `targets` (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): Цель вмешательства (агент, мир или их список).
- `first_n` (int, optional): Количество первых взаимодействий, учитываемых в контексте. По умолчанию `None`.
- `last_n` (int, optional): Количество последних взаимодействий (самых новых), учитываемых в контексте. По умолчанию 5.
- `name` (str, optional): Имя вмешательства. Если не указано, генерируется автоматически.
- `text_precondition` (str, optional): Текстовое описание предварительного условия для вмешательства.
- `precondition_func` (function, optional): Функция, определяющая предварительное условие.
- `effect_func` (function, optional): Функция, определяющая эффект вмешательства.
- `_last_text_precondition_proposition` (Proposition, optional): Последнее текстовое предложение предварительного условия, использованное для проверки предварительного условия.
- `_last_functional_precondition_check` (bool, optional): Результат последней проверки функционального предварительного условия.

**Методы**:
- `__init__`: Инициализирует объект вмешательства.
- `__call__`: Выполняет вмешательство.
- `execute`: Выполняет вмешательство, проверяя предварительные условия и применяя эффект.
- `check_precondition`: Проверяет, выполнено ли предварительное условие для вмешательства.
- `apply_effect`: Применяет эффект вмешательства.
- `set_textual_precondition`: Устанавливает текстовое предварительное условие.
- `set_functional_precondition`: Устанавливает функциональное предварительное условие.
- `set_effect`: Устанавливает эффект вмешательства.
- `precondition_justification`: Возвращает обоснование для предварительного условия.

#### `__init__`

```python
def __init__(self, targets: Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]], 
                 first_n:int=None, last_n:int=5,
                 name: str = None):
```

**Назначение**: Инициализирует объект `Intervention`.

**Параметры**:
- `targets` (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): Цель вмешательства (агент, мир или их список).
- `first_n` (int, optional): Количество первых взаимодействий, учитываемых в контексте. По умолчанию `None`.
- `last_n` (int, optional): Количество последних взаимодействий (самых новых), учитываемых в контексте. По умолчанию 5.
- `name` (str, optional): Имя вмешательства. Если не указано, генерируется автоматически.

**Как работает функция**:
- Инициализирует атрибуты объекта `Intervention`, такие как цели (`targets`), параметры контекста (`first_n`, `last_n`) и имя (`name`).
- Устанавливает `text_precondition`, `precondition_func` и `effect_func` в `None`.
- Инициализирует `_last_text_precondition_proposition` и `_last_functional_precondition_check` в `None`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Пример создания вмешательства для TinyPerson
person = TinyPerson()
intervention_person = Intervention(targets=person, name="PersonIntervention")

# Пример создания вмешательства для TinyWorld
world = TinyWorld()
intervention_world = Intervention(targets=world, name="WorldIntervention")

# Пример создания вмешательства для списка TinyPerson
person_list = [TinyPerson(), TinyPerson()]
intervention_person_list = Intervention(targets=person_list, name="PersonListIntervention")
```

#### `__call__`

```python
def __call__(self):
```

**Назначение**: Позволяет вызывать объект `Intervention` как функцию, что эквивалентно вызову метода `execute`.

**Возвращает**:
- `bool`: Возвращает `True`, если эффект вмешательства был применен, и `False` в противном случае.

**Как работает функция**:
- Вызывает метод `execute`, который выполняет проверку предварительных условий и применяет эффект вмешательства, если условия выполнены.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример использования __call__ для выполнения вмешательства
person = TinyPerson()
intervention = Intervention(targets=person)
result = intervention()  # Эквивалентно intervention.execute()
print(result)
```

#### `execute`

```python
def execute(self):
```

**Назначение**: Выполняет вмешательство, проверяя предварительные условия и применяя эффект, если они выполнены.

**Возвращает**:
- `bool`: Возвращает `True`, если эффект вмешательства был применен, и `False` в противном случае.

**Как работает функция**:
1. Логирует начало выполнения вмешательства.
2. Проверяет предварительное условие с помощью метода `check_precondition`.
3. Если предварительное условие выполнено, применяет эффект с помощью метода `apply_effect` и логирует это.
4. Возвращает `True`, если эффект был применен, и `False` в противном случае.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from src.logger import logger  # Import logger

# Пример выполнения вмешательства с предварительным условием и эффектом
person = TinyPerson()
intervention = Intervention(targets=person)

def precondition_func(target):
    #Предварительное условие: проверить, что у агента energy < 50
    return target.energy < 50  

def effect_func(target):
    #Эффект: увеличить energy агента до 100
    target.energy = 100  

intervention.set_functional_precondition(precondition_func)
intervention.set_effect(effect_func)

# Перед выполнением intervention.execute() agent.energy = 20
result = intervention.execute()

#После выполнением intervention.execute() agent.energy = 100
print(result)
```

#### `check_precondition`

```python
def check_precondition(self):
```

**Назначение**: Проверяет, выполнено ли предварительное условие для вмешательства.

**Возвращает**:
- `bool`: Возвращает `True`, если предварительное условие выполнено, и `False` в противном случае.

**Как работает функция**:
1. Создает объект `Proposition` для проверки текстового предварительного условия.
2. Проверяет функциональное предварительное условие, если оно задано.
3. Проверяет, выполнены ли оба предварительных условия (текстовое и функциональное).
4. Сохраняет результаты проверок в атрибутах `_last_text_precondition_proposition` и `_last_functional_precondition_check`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.experimentation import Proposition

# Пример проверки предварительного условия
person = TinyPerson()
intervention = Intervention(targets=person)

# Задаем текстовое предварительное условие
intervention.set_textual_precondition("The agent is tired")

# Выполняем проверку предварительного условия
result = intervention.check_precondition()
print(result)
```

#### `apply_effect`

```python
def apply_effect(self):
```

**Назначение**: Применяет эффект вмешательства.

**Как работает функция**:
- Вызывает функцию эффекта `effect_func` с целью вмешательства (`targets`) в качестве аргумента. Не проверяет предварительные условия, поэтому рекомендуется вызывать после `check_precondition`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример применения эффекта вмешательства
person = TinyPerson()
intervention = Intervention(targets=person)

def effect_func(target):
    # Эффект: увеличить уровень энергии агента
    target.energy += 10

intervention.set_effect(effect_func)

# Выполняем применение эффекта
intervention.apply_effect()
print(person.energy)
```

#### `set_textual_precondition`

```python
def set_textual_precondition(self, text):
```

**Назначение**: Устанавливает текстовое предварительное условие для вмешательства.

**Параметры**:
- `text` (str): Текст предварительного условия, который будет интерпретироваться языковой моделью.

**Возвращает**:
- `Intervention`: Возвращает объект `Intervention` для возможности chaining (цепочки вызовов).

**Как работает функция**:
- Устанавливает атрибут `text_precondition` равным переданному тексту.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример установки текстового предварительного условия
person = TinyPerson()
intervention = Intervention(targets=person)

intervention.set_textual_precondition("The agent is happy")
```

#### `set_functional_precondition`

```python
def set_functional_precondition(self, func):
```

**Назначение**: Устанавливает функциональное предварительное условие для вмешательства.

**Параметры**:
- `func` (function): Функция предварительного условия. Функция должна принимать один аргумент `targets` (TinyWorld или TinyPerson, или их список) и возвращать булево значение.

**Возвращает**:
- `Intervention`: Возвращает объект `Intervention` для возможности chaining.

**Как работает функция**:
- Устанавливает атрибут `precondition_func` равным переданной функции.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример установки функционального предварительного условия
person = TinyPerson()
intervention = Intervention(targets=person)

def precondition_func(target):
    # Предварительное условие: проверить, что уровень энергии агента меньше 50
    return target.energy < 50

intervention.set_functional_precondition(precondition_func)
```

#### `set_effect`

```python
def set_effect(self, effect_func):
```

**Назначение**: Устанавливает эффект вмешательства.

**Параметры**:
- `effect_func` (function): Функция эффекта вмешательства.

**Возвращает**:
- `Intervention`: Возвращает объект `Intervention` для возможности chaining.

**Как работает функция**:
- Устанавливает атрибут `effect_func` равным переданной функции.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример установки эффекта вмешательства
person = TinyPerson()
intervention = Intervention(targets=person)

def effect_func(target):
    # Эффект: увеличить уровень энергии агента на 10 единиц
    target.energy += 10

intervention.set_effect(effect_func)
```

#### `precondition_justification`

```python
def precondition_justification(self):
```

**Назначение**: Возвращает обоснование для предварительного условия.

**Возвращает**:
- `str`: Строка с обоснованием для предварительного условия.

**Как работает функция**:
1. Проверяет, было ли задано текстовое предварительное условие. Если да, добавляет обоснование из объекта `Proposition` в строку.
2. Если текстовое предварительное условие не задано, проверяет, было ли выполнено функциональное предварительное условие. Если да, добавляет соответствующее сообщение в строку.
3. Если ни одно из предварительных условий не выполнено, добавляет сообщение о том, что предварительные условия не выполнены.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример получения обоснования для предварительного условия
person = TinyPerson()
intervention = Intervention(targets=person)

# Задаем текстовое предварительное условие
intervention.set_textual_precondition("The agent is happy")

# Выполняем проверку предварительного условия
intervention.check_precondition()

# Получаем обоснование для предварительного условия
justification = intervention.precondition_justification()
print(justification)
```