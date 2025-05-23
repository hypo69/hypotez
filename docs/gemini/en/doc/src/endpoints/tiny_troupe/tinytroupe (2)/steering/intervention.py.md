# Intervention -  Управление поведением в TinyTroupe 

## Обзор

Модуль Intervention предоставляет возможность управлять поведением агентов (TinyPerson) и миров (TinyWorld) в TinyTroupe, определяя условия для воздействия (предусловия) и непосредственно действия (эффекты).

## Детали

Intervention служит для создания  и управления правилами, которые влияют на поведение агентов и миров. Он позволяет задавать  условия, которые должны быть выполнены, чтобы  сработал эффект. 

## Классы

### `class Intervention`

**Описание**: Класс Intervention представляет  интервенцию, которая позволяет изменять поведение агентов или миров в TinyTroupe.

**Атрибуты**:
- `targets` (`Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]`): Цель интервенции (агент или мир, или список агентов/миров).
- `first_n` (`int`, optional): Количество первых взаимодействий, которые учитываются в контексте. По умолчанию `None`.
- `last_n` (`int`, optional): Количество последних взаимодействий (самых последних), которые учитываются в контексте. По умолчанию `5`.
- `name` (`str`, optional): Название интервенции. По умолчанию генерируется уникальное имя.
- `text_precondition` (`str`, optional): Текстовое описание предусловия, которое интерпретируется языковой моделью.
- `precondition_func` (`function`, optional): Функция, определяющая предусловие, которое проверяется кодом.
- `effect_func` (`function`, optional): Функция, реализующая эффект интервенции.
- `_last_text_precondition_proposition` (`Proposition`): Последнее предложение, которое использовалось для проверки предусловия, основанного на тексте.
- `_last_functional_precondition_check` (`bool`): Результат последней проверки функционального предусловия.

**Методы**:
- `__call__()`: Выполняет интервенцию.
- `execute()`: Выполняет интервенцию. Сначала проверяет предусловие, а затем, если оно выполнено, применяет эффект.
- `check_precondition()`: Проверяет, выполнено ли предусловие для интервенции.
- `apply_effect()`: Применяет эффект интервенции. 
- `set_textual_precondition(text)`: Задает предусловие как текст, который будет интерпретироваться языковой моделью.
- `set_functional_precondition(func)`: Задает предусловие как функцию, которая будет вычисляться кодом.
- `set_effect(effect_func)`: Задает эффект интервенции.
- `precondition_justification()`: Получает обоснование для предусловия.


## Функции

### `__call__()`

**Описание**: Выполняет интервенцию. 

**Параметры**:
- `self`: Текущий объект Intervention.

**Возвращаемое значение**:
- `bool`: Флаг, указывающий на то, был ли применен эффект интервенции.


### `execute()`

**Описание**: Выполняет интервенцию. Сначала проверяет предусловие, а затем, если оно выполнено, применяет эффект.

**Параметры**:
- `self`: Текущий объект Intervention.

**Возвращаемое значение**:
- `bool`: Флаг, указывающий на то, был ли применен эффект интервенции.


### `check_precondition()`

**Описание**: Проверяет, выполнено ли предусловие для интервенции.

**Параметры**:
- `self`: Текущий объект Intervention.

**Возвращаемое значение**:
- `bool`: Флаг, указывающий на то, выполнено ли предусловие.


### `apply_effect()`

**Описание**: Применяет эффект интервенции.

**Параметры**:
- `self`: Текущий объект Intervention.


### `set_textual_precondition(text)`

**Описание**: Задает предусловие как текст, который будет интерпретироваться языковой моделью.

**Параметры**:
- `self`: Текущий объект Intervention.
- `text` (`str`): Текст предусловия.

**Возвращаемое значение**:
- `self`: Текущий объект Intervention (для цепочки вызовов).


### `set_functional_precondition(func)`

**Описание**: Задает предусловие как функцию, которая будет вычисляться кодом.

**Параметры**:
- `self`: Текущий объект Intervention.
- `func` (`function`): Функция, определяющая предусловие. Должна принимать один аргумент `targets` (агент или мир, или список) и возвращать булево значение.

**Возвращаемое значение**:
- `self`: Текущий объект Intervention (для цепочки вызовов).


### `set_effect(effect_func)`

**Описание**: Задает эффект интервенции.

**Параметры**:
- `self`: Текущий объект Intervention.
- `effect_func` (`function`): Функция, реализующая эффект интервенции.

**Возвращаемое значение**:
- `self`: Текущий объект Intervention (для цепочки вызовов).


### `precondition_justification()`

**Описание**: Получает обоснование для предусловия.

**Параметры**:
- `self`: Текущий объект Intervention.

**Возвращаемое значение**:
- `str`: Обоснование для предусловия, которое включает в себя информацию о текстовом и функциональном предусловиях.

## Примеры

```python
# Создание интервенции для агента
agent = TinyPerson(name="Alice")
intervention = Intervention(targets=agent)

# Установка текстового предусловия
intervention.set_textual_precondition("Агент должен быть голоден.") 

# Установка функционального предусловия
def is_hungry(target):
    return target.hunger_level > 5
intervention.set_functional_precondition(is_hungry)

# Установка эффекта
def eat(target):
    target.hunger_level -= 2
intervention.set_effect(eat)

# Выполнение интервенции
intervention() # Вызовет eat() только если Alice голодна (hunger_level > 5)

# Получение обоснования для предусловия
print(intervention.precondition_justification()) 

# Создание интервенции для мира
world = TinyWorld(name="My World")
intervention = Intervention(targets=world)

# Установка текстового предусловия
intervention.set_textual_precondition("В мире должна быть хорошая погода.") 

# Установка эффекта
def change_weather(target):
    target.weather = "sunny"
intervention.set_effect(change_weather)

# Выполнение интервенции
intervention() # Вызовет change_weather() только если в мире хорошая погода 
```

## Примечания

- В коде используются функции `utils.fresh_id()` для генерации уникальных идентификаторов, а также модуль `logger` для вывода логов.
- Интервенции могут использоваться для создания сложных сценариев взаимодействия агентов и миров в TinyTroupe, позволяя задавать  правила  для  изменения  их  поведения.
- Функции `check_precondition()` и `apply_effect()`  могут  быть  переопределены  в  подклассах  `Intervention`  для  реализации  более  специализированных  условий  и  действий.