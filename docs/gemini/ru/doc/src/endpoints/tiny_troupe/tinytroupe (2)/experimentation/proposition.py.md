# Модуль для определения и проверки пропозиций в контексте TinyTroupe
## Обзор

Модуль `proposition.py` предназначен для работы с пропозициями (утверждениями) о целях, которыми могут быть `TinyWorld`, `TinyPerson` или их комбинации. Модуль предоставляет класс `Proposition` для определения пропозиций и функцию `check_proposition` для их проверки с использованием языковой модели (LLM).

## Подробнее

Модуль позволяет формулировать утверждения о поведении агентов или состоянии среды в многоагентном моделировании. Он использует `LLMRequest` для оценки истинности или ложности этих утверждений на основе предоставленного контекста, который может включать траекторию симуляции агентов и состояние среды.

## Классы

### `Proposition`

**Описание**: Класс для определения пропозиции как текстового утверждения о цели (целях), в качестве которых может выступать `TinyWorld`, `TinyPerson` или несколько экземпляров любого из них.

**Атрибуты**:
- `targets` (list): Список целей пропозиции (`TinyWorld` или `TinyPerson`).
- `claim` (str): Текст утверждения пропозиции.
- `first_n` (int): Количество первых взаимодействий для рассмотрения в контексте.
- `last_n` (int): Количество последних взаимодействий (самых последних) для рассмотрения в контексте.
- `value` (bool): Значение пропозиции (True или False) после проверки.
- `justification` (str): Обоснование значения пропозиции, предоставленное LLM.
- `confidence` (float): Уверенность LLM в значении пропозиции.
- `raw_llm_response` (str): Необработанный ответ от LLM.

**Методы**:
- `__init__(self, target, claim: str, first_n: int = None, last_n: int = None)`: Инициализирует объект `Proposition`.
- `__call__(self, additional_context=None)`: Вызывает метод `check` для проверки пропозиции.
- `check(self, additional_context="No additional context available.")`: Проверяет пропозицию, используя LLM, и возвращает её значение.

#### `__init__(self, target, claim: str, first_n: int = None, last_n: int = None)`

```python
def __init__(self, target, claim:str, first_n:int=None, last_n:int=None):
    """
    Args:
        target (TinyWorld, TinyPerson, list): the target or targets of the proposition
        claim (str): the claim of the proposition
        first_n (int): the number of first interactions to consider in the context
        last_n (int): the number of last interactions (most recent) to consider in the context

    """
```

**Описание**: Инициализирует объект `Proposition`, определяя цель (цели), утверждение и контекст.

**Параметры**:
- `target` (TinyWorld, TinyPerson, list): Цель или цели пропозиции. Может быть экземпляром `TinyWorld`, `TinyPerson` или списком экземпляров этих классов.
- `claim` (str): Утверждение, которое необходимо проверить.
- `first_n` (int, optional): Количество первых взаимодействий, которые следует учитывать в контексте. По умолчанию `None`.
- `last_n` (int, optional): Количество последних взаимодействий (самых недавних), которые следует учитывать в контексте. По умолчанию `None`.

**Как работает**:

1.  Проверяет тип цели (`target`). Если цель является экземпляром `TinyWorld` или `TinyPerson`, она преобразуется в список, содержащий только эту цель. Если цель является списком, проверяется, что все элементы списка являются экземплярами `TinyWorld` или `TinyPerson`. Если цель имеет недопустимый тип, вызывается исключение `ValueError`.
2.  Сохраняет утверждение (`claim`) в атрибуте `self.claim`.
3.  Сохраняет значения `first_n` и `last_n` в соответствующих атрибутах объекта.
4.  Инициализирует атрибуты `value`, `justification` и `confidence` значением `None`.

#### `__call__(self, additional_context=None)`

```python
def __call__(self, additional_context=None):
    """ """
```

**Описание**: Позволяет вызывать объект `Proposition` как функцию, что приводит к вызову метода `check`.

**Параметры**:
- `additional_context` (str, optional): Дополнительный контекст для передачи в метод `check`. По умолчанию `None`.

**Возвращает**:
- Результат вызова метода `check`.

#### `check(self, additional_context="No additional context available.")`

```python
def check(self, additional_context="No additional context available."):
    """ """
```

**Описание**: Проверяет истинность пропозиции с использованием языковой модели (LLM).

**Параметры**:
- `additional_context` (str, optional): Дополнительный контекст, который будет предоставлен LLM. По умолчанию "No additional context available.".

**Как работает**:

1.  Инициализирует переменную `context` пустой строкой.
2.  Для каждой цели (`target`) в списке `self.targets` выполняет следующие действия:
    *   Получает траекторию взаимодействий цели с помощью метода `pretty_current_interactions`.
    *   Формирует строку контекста, добавляя информацию о типе цели (агент или среда) и её имени.
    *   Добавляет траекторию взаимодействий цели в строку `context`.
3.  Создает объект `LLMRequest` с системным запросом, определяющим роль LLM как системы оценки истинности или ложности пропозиций в контексте многоагентного моделирования.
4.  Формирует пользовательский запрос (`user_prompt`), включающий текст пропозиции, контекст и дополнительный контекст.
5.  Вызывает LLM с помощью объекта `llm_request`, чтобы получить значение пропозиции.
6.  Сохраняет значение пропозиции, обоснование и уверенность, полученные от LLM, в соответствующих атрибутах объекта.
7.  Сохраняет необработанный ответ от LLM в атрибуте `raw_llm_response`.
8.  Возвращает значение пропозиции.

**Внутренние функции**:
- В данном методе нет внутренних функций.

**Пример**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Создание экземпляров TinyWorld и TinyPerson
world = TinyWorld(name='MyWorld')
person = TinyPerson(name='Alice')

# Создание пропозиции об агенте Alice
proposition = Proposition(target=person, claim="Alice is happy.")

# Проверка пропозиции
result = proposition.check()
print(f"Proposition value: {result}")

# Создание пропозиции об окружении MyWorld
proposition_world = Proposition(target=world, claim="The environment is clean.")

# Проверка пропозиции
result_world = proposition_world.check()
print(f"Proposition value: {result_world}")

# Создание пропозиции с дополнительным контекстом
proposition_with_context = Proposition(target=person, claim="Alice likes the weather.")
result_with_context = proposition_with_context.check(additional_context="The weather is sunny.")
print(f"Proposition value with additional context: {result_with_context}")
```

## Функции

### `check_proposition(target, claim: str, additional_context="No additional context available.", first_n: int = None, last_n: int = None)`

```python
def check_proposition(target, claim:str, additional_context="No additional context available.",
                      first_n:int=None, last_n:int=None):
    """
    Args:
        target (TinyWorld, TinyPerson, list): the target or targets of the proposition
        claim (str): the claim of the proposition
        additional_context (str): additional context to provide to the LLM
        first_n (int): the number of first interactions to consider in the context
        last_n (int): the number of last interactions (most recent) to consider in the context

    Returns:
        bool: whether the proposition holds for the given target(s)
    """
```

**Назначение**: Проверяет, выполняется ли пропозициональное утверждение для заданной цели (целей).

**Параметры**:
- `target` (TinyWorld, TinyPerson, list): Цель или цели пропозиции. Может быть экземпляром `TinyWorld`, `TinyPerson` или списком экземпляров этих классов.
- `claim` (str): Утверждение, которое необходимо проверить.
- `additional_context` (str, optional): Дополнительный контекст для предоставления LLM. По умолчанию "No additional context available.".
- `first_n` (int, optional): Количество первых взаимодействий, которые следует учитывать в контексте. По умолчанию `None`.
- `last_n` (int, optional): Количество последних взаимодействий (самых недавних), которые следует учитывать в контексте. По умолчанию `None`.

**Возвращает**:
- `bool`: Значение `True`, если пропозиция выполняется для заданных целей, и `False` в противном случае.

**Как работает функция**:

1.  Создает экземпляр класса `Proposition` с переданными аргументами: целью (`target`), утверждением (`claim`), `first_n` и `last_n`.
2.  Вызывает метод `check` созданного экземпляра `Proposition`, передавая дополнительный контекст (`additional_context`).
3.  Возвращает результат, полученный от метода `check`.

```
A: Создание экземпляра Proposition
↓
B: Вызов метода check экземпляра Proposition
↓
C: Возврат результата метода check
```

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Создание экземпляров TinyWorld и TinyPerson
world = TinyWorld(name='MyWorld')
person = TinyPerson(name='Alice')

# Проверка пропозиции об агенте Alice
result = check_proposition(target=person, claim="Alice is happy.")
print(f"Proposition value: {result}")

# Проверка пропозиции об окружении MyWorld
result_world = check_proposition(target=world, claim="The environment is clean.")
print(f"Proposition value: {result_world}")

# Проверка пропозиции с дополнительным контекстом
result_with_context = check_proposition(target=person, claim="Alice likes the weather.", additional_context="The weather is sunny.")
print(f"Proposition value with additional context: {result_with_context}")