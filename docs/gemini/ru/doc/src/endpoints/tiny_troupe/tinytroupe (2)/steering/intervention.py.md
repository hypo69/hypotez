# Модуль intervention.py

## Обзор

Модуль `intervention.py` предназначен для реализации логики вмешательств (interventions) в процессы, происходящие в рамках проекта `tinytroupe`. Он содержит класс `Intervention`, который позволяет определять условия и эффекты, применяемые к определенным целям (targets), таким как `TinyPerson` или `TinyWorld`.

## Подробней

Модуль предоставляет возможность задавать текстовые и функциональные предусловия для вмешательств, а также определять функцию эффекта, которая будет выполняться при выполнении предусловий. Это позволяет гибко настраивать логику вмешательств в зависимости от текущего состояния системы и целей вмешательства.

## Классы

### `Intervention`

**Описание**: Класс `Intervention` представляет собой основную структуру для определения и выполнения вмешательств.

**Атрибуты**:

-   `targets` (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): Цель (или цели), на которую направлено вмешательство.
-   `first_n` (int, optional): Количество первых взаимодействий, учитываемых в контексте.
-   `last_n` (int, optional): Количество последних взаимодействий (самых недавних), учитываемых в контексте. По умолчанию 5.
-   `name` (str, optional): Имя вмешательства. Если не указано, генерируется автоматически.
-   `text_precondition` (str, optional): Текстовое предусловие, которое должно быть выполнено для применения вмешательства.
-   `precondition_func` (function, optional): Функциональное предусловие, которое должно быть выполнено для применения вмешательства.
-   `effect_func` (function, optional): Функция, определяющая эффект вмешательства.
-   `_last_text_precondition_proposition` (Proposition, optional): Последнее предложение, использованное для проверки текстового предусловия.
-   `_last_functional_precondition_check` (bool, optional): Результат последней проверки функционального предусловия.

**Методы**:

-   `__init__`: Инициализирует объект вмешательства.
-   `__call__`: Вызывает метод `execute` для выполнения вмешательства.
-   `execute`: Выполняет вмешательство, проверяя предусловие и применяя эффект при его выполнении.
-   `check_precondition`: Проверяет, выполнено ли предусловие для вмешательства.
-   `apply_effect`: Применяет эффект вмешательства.
-   `set_textual_precondition`: Устанавливает текстовое предусловие для вмешательства.
-   `set_functional_precondition`: Устанавливает функциональное предусловие для вмешательства.
-   `set_effect`: Устанавливает эффект вмешательства.
-   `precondition_justification`: Возвращает обоснование для предусловия.

## Методы класса

### `__init__`

```python
def __init__(self, targets: Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]], 
                 first_n:int=None, last_n:int=5,
                 name: str = None):
    """
    Initialize the intervention.

    Args:
        target (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): the target to intervene on
        first_n (int): the number of first interactions to consider in the context
        last_n (int): the number of last interactions (most recent) to consider in the context
        name (str): the name of the intervention
    """
```

**Назначение**: Инициализирует объект класса `Intervention`.

**Параметры**:

-   `targets` (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): Цель (или цели) для вмешательства. Может быть экземпляром `TinyPerson`, `TinyWorld`, списком `TinyPerson` или списком `TinyWorld`.
-   `first_n` (int, optional): Количество первых взаимодействий, учитываемых в контексте. По умолчанию `None`.
-   `last_n` (int, optional): Количество последних взаимодействий (самых недавних), учитываемых в контексте. По умолчанию `5`.
-   `name` (str, optional): Имя вмешательства. Если не указано, генерируется автоматически. По умолчанию `None`.

**Как работает функция**:

-   Функция инициализирует атрибуты `targets`, `first_n`, `last_n` и `name` объекта `Intervention` на основе переданных аргументов.
-   Инициализирует атрибуты `text_precondition`, `precondition_func` и `effect_func` как `None`.
-   Генерирует уникальное имя для вмешательства, если `name` не указано.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person, name="MyIntervention")
```

### `__call__`

```python
def __call__(self):
    """
    Execute the intervention.

    Returns:
        bool: whether the intervention effect was applied.
    """
```

**Назначение**: Позволяет вызывать объект `Intervention` как функцию.

**Возвращает**:

-   `bool`: Возвращает `True`, если эффект вмешательства был применен, и `False` в противном случае.

**Как работает функция**:

-   Вызывает метод `execute` для выполнения вмешательства.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
result = intervention()  # Вызов intervention.__call__()
```

### `execute`

```python
def execute(self):
    """
    Execute the intervention. It first checks the precondition, and if it is met, applies the effect.
    This is the simplest method to run the intervention.

    Returns:
        bool: whether the intervention effect was applied.
    """
```

**Назначение**: Выполняет вмешательство, проверяя предусловие и применяя эффект при его выполнении.

**Возвращает**:

-   `bool`: Возвращает `True`, если эффект вмешательства был применен, и `False` в противном случае.

**Как работает функция**:

1.  Выводит отладочное сообщение о начале выполнения вмешательства с использованием `logger.debug`.
2.  Вызывает метод `check_precondition` для проверки предусловия.
3.  Если предусловие выполнено, вызывает метод `apply_effect` для применения эффекта вмешательства.
4.  Выводит отладочное сообщение об успешном применении эффекта, если предусловие было выполнено.
5.  Возвращает `True`, если эффект был применен, и `False` в противном случае.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
result = intervention.execute()
```

### `check_precondition`

```python
def check_precondition(self):
    """
    Check if the precondition for the intervention is met.
    """
```

**Назначение**: Проверяет, выполнено ли предусловие для вмешательства.

**Возвращает**:

-   `bool`: Возвращает `True`, если предусловие выполнено, и `False` в противном случае.

**Как работает функция**:

1.  Создает объект `Proposition` на основе `targets`, `text_precondition`, `first_n` и `last_n`.
2.  Если задана функциональное предусловие (`precondition_func`), вызывает его с `targets` в качестве аргумента.
3.  Если функциональное предусловие не задано, устанавливает `_last_functional_precondition_check` в `True`.
4.  Вызывает метод `check` объекта `Proposition` для проверки текстового предусловия.
5.  Возвращает `True`, если и текстовое, и функциональное предусловия выполнены, и `False` в противном случае.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
intervention.set_textual_precondition("Условие выполнено")
result = intervention.check_precondition()
```

### `apply_effect`

```python
def apply_effect(self):
    """
    Apply the intervention's effects. This won't check the precondition, 
    so it should be called after check_precondition.
    """
```

**Назначение**: Применяет эффект вмешательства.

**Как работает функция**:

-   Вызывает функцию эффекта (`effect_func`) с `targets` в качестве аргумента.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
def effect(target):
    print("Эффект применен к цели:", target)
intervention.set_effect(effect)
intervention.apply_effect()
```

### `set_textual_precondition`

```python
def set_textual_precondition(self, text):
    """
    Set a precondition as text, to be interpreted by a language model.

    Args:
        text (str): the text of the precondition
    """
```

**Назначение**: Устанавливает текстовое предусловие для вмешательства.

**Параметры**:

-   `text` (str): Текст предусловия.

**Возвращает**:

-   `self`: Возвращает объект `Intervention` для возможности chaining.

**Как работает функция**:

-   Устанавливает атрибут `text_precondition` объекта `Intervention` в переданный текст.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
intervention.set_textual_precondition("Условие: цель должна быть активна")
```

### `set_functional_precondition`

```python
def set_functional_precondition(self, func):
    """
    Set a precondition as a function, to be evaluated by the code.

    Args:
        func (function): the function of the precondition. 
          Must have the a single argument, targets (either a TinyWorld or TinyPerson, or a list). Must return a boolean.
    """
```

**Назначение**: Устанавливает функциональное предусловие для вмешательства.

**Параметры**:

-   `func` (function): Функция предусловия. Должна принимать один аргумент `targets` (либо `TinyWorld`, либо `TinyPerson`, либо список) и возвращать `bool`.

**Возвращает**:

-   `self`: Возвращает объект `Intervention` для возможности chaining.

**Как работает функция**:

-   Устанавливает атрибут `precondition_func` объекта `Intervention` в переданную функцию.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
def precondition(target):
    return True  # Пример предусловия, которое всегда выполняется
intervention.set_functional_precondition(precondition)
```

### `set_effect`

```python
def set_effect(self, effect_func):
    """
    Set the effect of the intervention.

    Args:
        effect (str): the effect function of the intervention
    """
```

**Назначение**: Устанавливает эффект вмешательства.

**Параметры**:

-   `effect_func` (function): Функция, определяющая эффект вмешательства.

**Возвращает**:

-   `self`: Возвращает объект `Intervention` для возможности chaining.

**Как работает функция**:

-   Устанавливает атрибут `effect_func` объекта `Intervention` в переданную функцию.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
def effect(target):
    print("Эффект применен к цели:", target)
intervention.set_effect(effect)
```

### `precondition_justification`

```python
def precondition_justification(self):
    """
    Get the justification for the precondition.
    """
```

**Назначение**: Получает обоснование для предусловия.

**Возвращает**:

-   `str`: Возвращает строку с обоснованием для предусловия.

**Как работает функция**:

1.  Инициализирует переменную `justification` пустой строкой.
2.  Если `_last_text_precondition_proposition` не `None`, добавляет обоснование из `_last_text_precondition_proposition.justification` и уверенность (confidence) в строку `justification`.
3.  Иначе, если `_last_functional_precondition_check` равно `True`, добавляет сообщение "Functional precondition was met." в строку `justification`.
4.  Иначе добавляет сообщение "Preconditions do not appear to be met." в строку `justification`.
5.  Возвращает строку `justification`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
person = TinyPerson()
intervention = Intervention(targets=person)
intervention.set_textual_precondition("Условие: цель должна быть активна")
intervention.check_precondition()
justification = intervention.precondition_justification()
print(justification)