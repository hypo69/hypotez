# Модуль Intervention

## Обзор

Модуль содержит класс `Intervention` для работы с вмешательствами в TinyWorld. 

Вмешательство - это действие, которое может быть выполнено в TinyWorld для изменения его состояния.  Intervention может быть основан как на текстовом условии (precondition), так и на функциональном условии.

## Подробней

Intervention представляет собой механизм для создания и управления действиями, которые могут быть выполнены в виртуальной среде TinyWorld. 

Intervention состоит из:

* **Цели (Targets):**  Объект, на который направлено действие (TinyPerson или TinyWorld).
* **Условие (Precondition):**  Текст или функция, которая проверяется перед выполнением эффекта.
* **Эффект (Effect):**  Функция, которая выполняется, если выполнено условие.

### Принцип работы:

1. **Инициализация:**
   - Создается объект Intervention, передавая в качестве аргумента цель, количество взаимодействий, которые необходимо учитывать в контексте, а также название вмешательства.
   - Инициализируется текстовое условие (text_precondition) и функциональное условие (precondition_func).
   - Инициализируется функция эффекта (effect_func).
   - Устанавливаются значения first_n и last_n, определяющие количество взаимодействий, которые нужно учитывать для проверки условия.
   - Устанавливается имя вмешательства (name).
2. **Выполнение:**
   - Вызывается метод `execute()` или используете `__call__`, который:
     - Проверяет условие (precondition) с использованием `check_precondition()`.
     - Если условие выполнено, применяется эффект (effect) с использованием `apply_effect()`.
3. **Проверка условия (Precondition):**
   - Метод `check_precondition()` проверяет как текстовое условие, так и функциональное условие. 
   - Текстовое условие проверяется с использованием объекта `Proposition`, который анализирует текст на основе контекста и возвращает результат проверки.
   - Функциональное условие выполняется, если задана функция `precondition_func`.
   - Возвращает `True`, если оба условия выполнены, иначе `False`.
4. **Применение эффекта (Effect):**
   - Метод `apply_effect()` выполняет эффект (effect_func),  если условие выполнено.
5. **Установка условий (Precondition) и эффекта (Effect):**
   - Используются методы `set_textual_precondition()`, `set_functional_precondition()` и `set_effect()`,  для задания  текстового условия, функционального условия и эффекта вмешательства соответственно.
6. **Проверка выполнения условий:**
    - Метод `precondition_justification()`  возвращает строку с обоснованием того, почему вмешательство было выполнено или не выполнено.

## Классы

### `Intervention`

**Описание**: Класс для управления вмешательствами в TinyWorld.

**Атрибуты**:

- `targets` (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): Цель вмешательства (TinyPerson, TinyWorld или их список).
- `first_n` (int): Количество первых взаимодействий, которые нужно учитывать при проверке условия. 
- `last_n` (int): Количество последних взаимодействий (самых последних), которые нужно учитывать при проверке условия.
- `name` (str): Имя вмешательства.
- `text_precondition` (str): Текстовое условие.
- `precondition_func` (function): Функциональное условие.
- `effect_func` (function):  Функция эффекта.
- `_last_text_precondition_proposition` (Proposition):  Последняя проверка текстового условия.
- `_last_functional_precondition_check` (bool):  Последняя проверка функционального условия.

**Методы**:

- `__call__()`: Выполняет вмешательство.
- `execute()`:  Выполняет вмешательство, проверяя условие и применяя эффект, если оно выполнено.
- `check_precondition()`: Проверяет условие (text_precondition и precondition_func). 
- `apply_effect()`:  Применяет эффект, если условие выполнено.
- `set_textual_precondition(text)`:  Устанавливает текстовое условие.
- `set_functional_precondition(func)`:  Устанавливает функциональное условие.
- `set_effect(effect_func)`:  Устанавливает функцию эффекта.
- `precondition_justification()`:  Возвращает строку с обоснованием,  почему вмешательство было выполнено или не выполнено.


## Функции
### `__call__`

**Назначение**: Выполняет вмешательство.

**Параметры**:

-  None

**Возвращает**:

- `bool`: True, если вмешательство было выполнено, False - если нет.

**Как работает функция**:

- Вызывает метод `execute()`.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Выполняем вмешательство
result = intervention() #  result - булево значение, показывающие, выполнено вмешательство или нет
```

### `execute`

**Назначение**:  Выполняет вмешательство, проверяя условие и применяя эффект, если оно выполнено.

**Параметры**:

- None

**Возвращает**:

- `bool`: True, если эффект был применен, False - если нет.

**Как работает функция**:

- Проверяет условие с помощью `check_precondition()`.
- Если условие выполнено, применяется эффект с помощью `apply_effect()`.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Выполняем вмешательство
result = intervention.execute() #  result - булево значение, показывающие, выполнено вмешательство или нет
```

### `check_precondition`

**Назначение**:  Проверяет условие вмешательства.

**Параметры**:

- None

**Возвращает**:

- `bool`: True, если условие выполнено, False - если нет.

**Как работает функция**:

-  Проверяет текстовое условие с помощью `Proposition`.
-  Проверяет функциональное условие, если оно установлено (`precondition_func`).
- Возвращает `True`, если оба условия выполнены, иначе `False`.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Устанавливаем текстовое условие
intervention.set_textual_precondition("The person is happy")
# Проверяем условие
result = intervention.check_precondition() #  result - булево значение, показывающие, выполнено вмешательство или нет
```


### `apply_effect`

**Назначение**:  Применяет эффект вмешательства.

**Параметры**:

- None

**Возвращает**:

- None

**Как работает функция**:

- Выполняет эффект (effect_func), если он был задан.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Устанавливаем эффект
intervention.set_effect(lambda targets: print("Effect applied!"))
# Применяем эффект
intervention.apply_effect() 
```

### `set_textual_precondition`

**Назначение**:  Устанавливает текстовое условие вмешательства.

**Параметры**:

- `text` (str): Текстовое условие.

**Возвращает**:

- `Intervention`: Текущий объект Intervention.

**Как работает функция**:

-  Записывает текст условия в `self.text_precondition`.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Устанавливаем текстовое условие
intervention.set_textual_precondition("The person is happy") 
```

### `set_functional_precondition`

**Назначение**:  Устанавливает функциональное условие вмешательства.

**Параметры**:

- `func` (function): Функция, которая проверяет функциональное условие.

**Возвращает**:

- `Intervention`: Текущий объект Intervention.

**Как работает функция**:

- Записывает функцию условия в `self.precondition_func`.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Устанавливаем функциональное условие
intervention.set_functional_precondition(lambda targets: targets.is_happy())
```

### `set_effect`

**Назначение**:  Устанавливает функцию эффекта вмешательства.

**Параметры**:

- `effect_func` (function):  Функция, которая будет выполнена, если условие вмешательства выполнено.

**Возвращает**:

- `Intervention`: Текущий объект Intervention.

**Как работает функция**:

- Записывает функцию эффекта в `self.effect_func`.

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Устанавливаем эффект
intervention.set_effect(lambda targets: print("Effect applied!"))
```


### `precondition_justification`

**Назначение**:  Возвращает строку с обоснованием того, почему вмешательство было выполнено или не выполнено.

**Параметры**:

- None

**Возвращает**:

- `str`: Строка с обоснованием.

**Как работает функция**:

-  Если было выполнено текстовое условие, то возвращает текст  `Proposition.justification`.
-  Если было выполнено функциональное условие, то возвращает строку "Functional precondition was met."
-  Если ни одно из условий не было выполнено, то возвращает строку "Preconditions do not appear to be met."

**Примеры**:

```python
intervention = Intervention(targets=tiny_world)
# Выполняем вмешательство
intervention.execute()
# Получаем обоснование выполнения вмешательства
justification = intervention.precondition_justification()
print(justification) 
```

## Параметры класса
- `targets` (Union[TinyPerson, TinyWorld, List[TinyPerson], List[TinyWorld]]): Цель вмешательства (TinyPerson, TinyWorld или их список). 
- `first_n` (int): Количество первых взаимодействий, которые нужно учитывать при проверке условия. 
- `last_n` (int): Количество последних взаимодействий (самых последних), которые нужно учитывать при проверке условия.
- `name` (str): Имя вмешательства.
- `text_precondition` (str): Текстовое условие.
- `precondition_func` (function): Функциональное условие.
- `effect_func` (function):  Функция эффекта.
- `_last_text_precondition_proposition` (Proposition):  Последняя проверка текстового условия.
- `_last_functional_precondition_check` (bool):  Последняя проверка функционального условия.

## Примеры

```python
from tinytroupe.extraction import logger
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.steering.intervention import Intervention


# Создаем TinyWorld 
tiny_world = TinyWorld()

# Создаем TinyPerson
person = TinyPerson(tiny_world, name='John')


# Создаем Intervention
intervention = Intervention(targets=person, name="Make John happy")

# Устанавливаем текстовое условие
intervention.set_textual_precondition("John is sad")

# Устанавливаем эффект
intervention.set_effect(lambda targets: targets.set_happy())

# Выполняем Intervention
result = intervention.execute()

# Выводим результат
print(f"Intervention result: {result}")
print(intervention.precondition_justification())
```

```python
from tinytroupe.extraction import logger
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.steering.intervention import Intervention


# Создаем TinyWorld 
tiny_world = TinyWorld()

# Создаем TinyPerson
person = TinyPerson(tiny_world, name='John')


# Создаем Intervention
intervention = Intervention(targets=person, name="Make John happy")

# Устанавливаем функциональное условие
intervention.set_functional_precondition(lambda targets: not targets.is_happy())

# Устанавливаем эффект
intervention.set_effect(lambda targets: targets.set_happy())

# Выполняем Intervention
result = intervention.execute()

# Выводим результат
print(f"Intervention result: {result}")
print(intervention.precondition_justification())
```
```python
from tinytroupe.extraction import logger
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.steering.intervention import Intervention


# Создаем TinyWorld 
tiny_world = TinyWorld()

# Создаем TinyPerson
person = TinyPerson(tiny_world, name='John')


# Создаем Intervention
intervention = Intervention(targets=person, name="Make John happy")

# Устанавливаем текстовое условие
intervention.set_textual_precondition("John is sad")

# Устанавливаем эффект
intervention.set_effect(lambda targets: targets.set_happy())

# Выполняем Intervention
result = intervention.execute()

# Выводим результат
print(f"Intervention result: {result}")
print(intervention.precondition_justification())