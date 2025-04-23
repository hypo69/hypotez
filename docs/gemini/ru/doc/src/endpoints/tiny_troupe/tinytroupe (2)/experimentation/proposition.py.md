# Модуль proposition.py

## Обзор

Модуль `proposition.py` определяет класс `Proposition`, предназначенный для представления и проверки утверждений (proposition) о целях (targets), которыми могут быть экземпляры классов `TinyWorld`, `TinyPerson` или их списки. Также, модуль предоставляет функцию `check_proposition` для удобной проверки утверждений без создания объекта `Proposition`.

## Подробнее

Модуль позволяет формализовать утверждения об агентах и их окружении в симуляции, а также оценивать истинность этих утверждений с использованием языковых моделей (LLM). Он предоставляет механизм для передачи контекста симуляции в LLM, получения оценки утверждения, а также обоснования и уверенности в этой оценке.

## Классы

### `Proposition`

**Описание**: Класс `Proposition` представляет собой утверждение о цели (или целях), которое может быть проверено на основе контекста симуляции.

**Атрибуты**:
- `targets` (list): Список целей (экземпляры `TinyWorld` или `TinyPerson`), к которым относится утверждение.
- `claim` (str): Текстовое утверждение, которое необходимо проверить.
- `first_n` (int, optional): Количество первых взаимодействий, которые следует учитывать в контексте.
- `last_n` (int, optional): Количество последних взаимодействий (самых последних), которые следует учитывать в контексте.
- `value` (bool, optional): Значение утверждения (True или False) после проверки. Изначально `None`.
- `justification` (str, optional): Обоснование значения утверждения, полученное от LLM. Изначально `None`.
- `confidence` (float, optional): Уверенность LLM в значении утверждения. Изначально `None`.
- `raw_llm_response` (str, optional): Необработанный ответ от LLM. Изначально `None`.

**Методы**:
- `__init__(target, claim: str, first_n: int = None, last_n: int = None)`: Конструктор класса.
- `__call__(additional_context=None)`: Позволяет вызывать экземпляр класса как функцию, что эквивалентно вызову метода `check`.
- `check(additional_context="No additional context available.")`: Проверяет истинность утверждения на основе контекста симуляции и дополнительного контекста, используя LLM.

#### `__init__(target, claim: str, first_n: int = None, last_n: int = None)`

```python
def __init__(self, target, claim: str, first_n: int = None, last_n: int = None):
    """
    Инициализирует объект Proposition.

    Args:
        target (TinyWorld, TinyPerson, list): Цель или цели утверждения.
        claim (str): Утверждение.
        first_n (int, optional): Количество первых взаимодействий для учета. По умолчанию `None`.
        last_n (int, optional): Количество последних взаимодействий для учета. По умолчанию `None`.

    Raises:
        ValueError: Если цель не является `TinyWorld`, `TinyPerson` или списком `TinyWorld` или `TinyPerson`.
    """
```
Функция инициализирует класс `Proposition` и устанавливает значения атрибутов, такие как цели (`target`), утверждение (`claim`), а также количество первых (`first_n`) и последних (`last_n`) взаимодействий, которые будут учитываться. Проверяет, что `target` является допустимым типом (TinyWorld, TinyPerson или список этих типов) и вызывает исключение `ValueError`, если это не так.

#### `__call__(additional_context=None)`

```python
def __call__(self, additional_context=None):
    """
    Позволяет вызывать экземпляр класса как функцию.

    Args:
        additional_context (str, optional): Дополнительный контекст для проверки. По умолчанию `None`.

    Returns:
        bool: Результат проверки утверждения.
    """
```
Функция позволяет экземпляру класса `Proposition` вызываться как функция. При вызове вызывается метод `check` с переданным дополнительным контекстом (`additional_context`). Возвращает результат проверки утверждения.

#### `check(additional_context="No additional context available.")`

```python
def check(self, additional_context="No additional context available."):
    """
    Проверяет, выполняется ли утверждение для заданных целей, используя LLM.

    Args:
        additional_context (str, optional): Дополнительный контекст для предоставления LLM. По умолчанию "No additional context available.".

    Returns:
        bool: Значение утверждения (True или False).
    """
```

**Как работает функция**:
- Функция `check` оценивает, является ли утверждение (`self.claim`) истинным или ложным, основываясь на контексте симуляции и дополнительном контексте.
- Она перебирает все цели (`targets`) и извлекает их траектории взаимодействий с использованием метода `pretty_current_interactions`.
- Затем формирует контекст, добавляя траектории каждой цели.
- Создает объект `LLMRequest` с системным запросом, который инструктирует LLM оценивать утверждение на основе предоставленного контекста.
- Запрос содержит утверждение, контекст и дополнительный контекст.
- Вызывает `llm_request` для получения оценки утверждения от LLM.
- Извлекает обоснование, уверенность и необработанный ответ от LLM.
- Сохраняет полученные значения в атрибуты экземпляра класса.
- Возвращает значение утверждения.

Внутри `check` есть следующие преобразования и вызовы:
 1. Цикл `for target in self.targets`:
    - Итерация по списку целей утверждения.
    - Для каждой цели извлекается траектория взаимодействий с помощью `target.pretty_current_interactions`.
 2. Формирование контекста:
    - Контекст формируется как строка, включающая траектории всех целей и дополнительный контекст.
 3. Создание и вызов `LLMRequest`:
    - Создается объект `LLMRequest`, который отправляет запрос к LLM для оценки утверждения.
    - `llm_request()` вызывает LLM, и возвращает результат.
 4. Извлечение результатов от LLM:
    - Извлекаются значение, обоснование и уверенность из ответа LLM.
    - Сохраняются в атрибуты `self.value`, `self.justification` и `self.confidence`.
 5. Возврат значения утверждения:
    - Функция возвращает результат оценки утверждения, полученный от LLM (`self.value`).

## Функции

### `check_proposition(target, claim: str, additional_context="No additional context available.", first_n: int = None, last_n: int = None)`

```python
def check_proposition(target, claim: str, additional_context="No additional context available.",
                      first_n: int = None, last_n: int = None):
    """
    Проверяет, выполняется ли пропозициональное утверждение для заданных целей.

    Args:
        target (TinyWorld, TinyPerson, list): Цель или цели утверждения.
        claim (str): Утверждение.
        additional_context (str, optional): Дополнительный контекст для предоставления LLM. По умолчанию "No additional context available.".
        first_n (int, optional): Количество первых взаимодействий для учета. По умолчанию `None`.
        last_n (int, optional): Количество последних взаимодействий для учета. По умолчанию `None`.

    Returns:
        bool: Значение утверждения (True или False).
    """
```

**Назначение**:
Функция `check_proposition` проверяет, истинно ли заданное утверждение (`claim`) для указанной цели (`target`), используя языковую модель (LLM). Она предназначена для удобной проверки утверждений без необходимости создания экземпляра класса `Proposition`.

**Параметры**:
- `target` (TinyWorld, TinyPerson, list): Цель или список целей, для которых проверяется утверждение. Это может быть экземпляр класса `TinyWorld` или `TinyPerson`, либо список таких экземпляров.
- `claim` (str): Утверждение, которое необходимо проверить. Это текстовое описание утверждения о цели.
- `additional_context` (str, optional): Дополнительный контекст, который передается в LLM для оценки утверждения. По умолчанию "No additional context available.".
- `first_n` (int, optional): Количество первых взаимодействий цели, которые следует учитывать при оценке утверждения. Если не указано, учитываются все взаимодействия.
- `last_n` (int, optional): Количество последних взаимодействий цели, которые следует учитывать при оценке утверждения. Если не указано, учитываются все взаимодействия.

**Возвращает**:
- `bool`: Значение утверждения (True или False), полученное от LLM.

**Как работает функция**:
- Функция создает экземпляр класса `Proposition` с переданными параметрами.
- Затем вызывает метод `check` этого экземпляра, передавая дополнительный контекст.
- Возвращает результат проверки утверждения, полученный от метода `check`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.experimentation.proposition import check_proposition

# Пример с TinyPerson
person = TinyPerson(name="Alice", persona="friendly")
claim = "Alice is friendly"
result = check_proposition(person, claim)
print(f"Is the claim '{claim}' true for {person.name}? {result}")

# Пример с TinyWorld
world = TinyWorld(name="Wonderland")
claim = "Wonderland is a happy place"
result = check_proposition(world, claim)
print(f"Is the claim '{claim}' true for {world.name}? {result}")

# Пример со списком целей
person1 = TinyPerson(name="Bob", persona="helpful")
person2 = TinyPerson(name="Charlie", persona="kind")
targets = [person1, person2]
claim = "Both Bob and Charlie are helpful"
result = check_proposition(targets, claim)
print(f"Is the claim '{claim}' true for {', '.join([t.name for t in targets])}? {result}")
```