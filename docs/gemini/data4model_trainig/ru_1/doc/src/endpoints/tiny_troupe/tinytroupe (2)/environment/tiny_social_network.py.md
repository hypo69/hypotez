# Модуль `tiny_social_network.py`

## Обзор

Модуль определяет класс `TinySocialNetwork`, который расширяет функциональность `TinyWorld`, добавляя поддержку социальных отношений между агентами (`TinyPerson`). Он позволяет устанавливать связи между агентами и управлять видимостью агентов друг для друга на основе этих связей.

## Подробней

Этот модуль предоставляет основу для моделирования социальных взаимодействий в виртуальной среде. Он включает в себя возможность добавления отношений между агентами, обновления контекстов агентов на основе этих отношений и обработки действий `REACH_OUT` с учетом социальных связей.

## Классы

### `TinySocialNetwork`

**Описание**: Класс `TinySocialNetwork` представляет собой социальную сеть, в которой агенты (`TinyPerson`) могут устанавливать отношения друг с другом.

**Наследует**: `TinyWorld`

**Атрибуты**:
- `relations` (dict): Словарь, хранящий отношения между агентами. Ключи словаря - названия отношений, значения - списки кортежей, представляющих пары агентов, находящихся в этих отношениях.

**Методы**:
- `__init__(name, broadcast_if_no_target=True)`: Конструктор класса.
- `add_relation(agent_1, agent_2, name="default")`: Добавляет отношение между двумя агентами.
- `_update_agents_contexts()`: Обновляет контексты агентов на основе текущего состояния мира и отношений между агентами.
- `_step()`: Выполняет один шаг симуляции, обновляя контексты агентов и вызывая метод `_step()` родительского класса.
- `_handle_reach_out(source_agent, content, target)`: Обрабатывает действие `REACH_OUT`, проверяя, находится ли целевой агент в тех же отношениях, что и отправитель.
- `is_in_relation_with(agent_1, agent_2, relation_name=None)`: Проверяет, находятся ли два агента в каких-либо отношениях или в конкретном отношении.

#### `__init__`

```python
def __init__(self, name, broadcast_if_no_target=True):
    """
    Создает новую среду TinySocialNetwork.

    Args:
        name (str): Имя среды.
        broadcast_if_no_target (bool): Если True, транслирует действия через доступные отношения агента,
          если цель действия не найдена.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `TinySocialNetwork`.

**Параметры**:
- `name` (str): Имя социальной сети.
- `broadcast_if_no_target` (bool): Если `True`, действия транслируются через доступные отношения агента, если цель действия не найдена. По умолчанию `True`.

**Как работает функция**:
- Вызывает конструктор родительского класса `TinyWorld` с переданными аргументами.
- Инициализирует атрибут `relations` как пустой словарь.

#### `add_relation`

```python
@transactional
def add_relation(self, agent_1, agent_2, name="default"):
    """
    Добавляет отношение между двумя агентами.

    Args:
        agent_1 (TinyPerson): Первый агент.
        agent_2 (TinyPerson): Второй агент.
        name (str): Имя отношения.
    """
    ...
```

**Назначение**: Добавляет отношение между двумя агентами в социальной сети.

**Параметры**:
- `agent_1` (TinyPerson): Первый агент.
- `agent_2` (TinyPerson): Второй агент.
- `name` (str): Имя отношения. По умолчанию `default`.

**Как работает функция**:
- Использует декоратор `@transactional` для обеспечения атомарности операции.
- Логирует добавление отношения с использованием `logger.debug`.
- Проверяет, находятся ли агенты уже в списке агентов социальной сети, и добавляет их, если это не так.
- Добавляет пару агентов в словарь `self.relations` под указанным именем отношения. Если отношение с таким именем уже существует, добавляет пару в список отношений; в противном случае создает новый список с этой парой.
- Возвращает `self` для возможности chaining вызовов.

**Примеры**:
```python
# Пример добавления отношения между двумя агентами
network = TinySocialNetwork("MyNetwork")
agent1 = TinyPerson("Alice")
agent2 = TinyPerson("Bob")
network.add_relation(agent1, agent2, "friends")
```

#### `_update_agents_contexts`

```python
@transactional
def _update_agents_contexts(self):
    """
    Обновляет наблюдения агентов на основе текущего состояния мира.
    """
    ...
```

**Назначение**: Обновляет контексты агентов в социальной сети на основе установленных отношений.

**Как работает функция**:
- Использует декоратор `@transactional` для обеспечения атомарности операции.
- Сначала делает всех агентов недоступными друг для друга, вызывая метод `make_all_agents_inaccessible` для каждого агента.
- Затем, на основе существующих отношений, делает связанных агентов доступными друг для друга, вызывая метод `make_agent_accessible` для каждой пары агентов в каждом отношении.
- Логирует процесс обновления контекстов агентов для каждого отношения с использованием `logger.debug`.

**Примеры**:
```python
# Пример обновления контекстов агентов
network = TinySocialNetwork("MyNetwork")
agent1 = TinyPerson("Alice")
agent2 = TinyPerson("Bob")
network.add_relation(agent1, agent2, "friends")
network._update_agents_contexts()
```

#### `_step`

```python
@transactional
def _step(self):
    """
    Выполняет шаг в социальной сети, обновляя контексты агентов.
    """
    ...
```

**Назначение**: Выполняет один шаг симуляции в социальной сети.

**Как работает функция**:
- Использует декоратор `@transactional` для обеспечения атомарности операции.
- Обновляет контексты агентов, вызывая метод `_update_agents_contexts`.
- Вызывает метод `_step` родительского класса `TinyWorld` для выполнения остальных действий, связанных с шагом симуляции.

**Примеры**:
```python
# Пример выполнения шага в социальной сети
network = TinySocialNetwork("MyNetwork")
network._step()
```

#### `_handle_reach_out`

```python
@transactional
def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
    """
    Обрабатывает действие REACH_OUT. Эта реализация социальной сети позволяет
    REACH_OUT успешно выполняться, только если целевой агент находится в тех же отношениях, что и исходный агент.

    Args:
        source_agent (TinyPerson): Агент, который выдал действие REACH_OUT.
        content (str): Содержание сообщения.
        target (str): Цель сообщения.
    """
    ...
```

**Назначение**: Обрабатывает действие `REACH_OUT` (попытка связаться с другим агентом) в социальной сети.

**Параметры**:
- `source_agent` (TinyPerson): Агент, инициировавший действие `REACH_OUT`.
- `content` (str): Содержание сообщения, которое агент пытается передать.
- `target` (str): Имя целевого агента, которому отправляется сообщение.

**Как работает функция**:
- Использует декоратор `@transactional` для обеспечения атомарности операции.
- Проверяет, находится ли целевой агент в тех же отношениях, что и отправитель, с использованием метода `is_in_relation_with`.
- Если целевой агент находится в тех же отношениях, вызывает метод `_handle_reach_out` родительского класса `TinyWorld` для обработки действия.
- Если целевой агент не находится в тех же отношениях, вызывает метод `socialize` у исходного агента, чтобы сообщить ему, что связь невозможна.

**Примеры**:
```python
# Пример обработки действия REACH_OUT
network = TinySocialNetwork("MyNetwork")
agent1 = TinyPerson("Alice")
agent2 = TinyPerson("Bob")
network.add_relation(agent1, agent2, "friends")
network._handle_reach_out(agent1, "Hello, Bob!", "Bob")
```

#### `is_in_relation_with`

```python
def is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool:
    """
    Проверяет, находятся ли два агента в отношении. Если указано имя отношения, проверяет, что
    агенты находятся в этом отношении. Если имя отношения не указано, проверяет, что агенты
    находятся в каком-либо отношении. Отношения ненаправленные, поэтому порядок агентов не имеет значения.

    Args:
        agent_1 (TinyPerson): Первый агент.
        agent_2 (TinyPerson): Второй агент.
        relation_name (str): Имя отношения для проверки, или None для проверки любого отношения.

    Returns:
        bool: True, если два агента находятся в заданном отношении, False в противном случае.
    """
    ...
```

**Назначение**: Проверяет, находятся ли два агента в определенном отношении или в каком-либо отношении вообще.

**Параметры**:
- `agent_1` (TinyPerson): Первый агент.
- `agent_2` (TinyPerson): Второй агент.
- `relation_name` (str, optional): Имя отношения для проверки. Если `None`, проверяется наличие любого отношения между агентами. По умолчанию `None`.

**Возвращает**:
- `bool`: `True`, если агенты находятся в указанном отношении (или в каком-либо отношении, если `relation_name` is `None`), `False` в противном случае.

**Как работает функция**:
- Если `relation_name` не указано, функция перебирает все отношения в `self.relations` и проверяет, содержится ли пара агентов (в любом порядке) в каком-либо из отношений. Если найдено отношение, содержащее пару агентов, возвращает `True`. Если ни одно отношение не содержит пару агентов, возвращает `False`.
- Если `relation_name` указано, функция проверяет, существует ли отношение с таким именем в `self.relations`. Если отношение существует, функция проверяет, содержится ли пара агентов (в любом порядке) в этом отношении. Возвращает `True`, если отношение содержит пару агентов, и `False` в противном случае. Если отношение с указанным именем не существует, функция возвращает `False`.

**Примеры**:
```python
# Пример проверки, находятся ли два агента в отношении
network = TinySocialNetwork("MyNetwork")
agent1 = TinyPerson("Alice")
agent2 = TinyPerson("Bob")
network.add_relation(agent1, agent2, "friends")
print(network.is_in_relation_with(agent1, agent2, "friends"))  # Вывод: True
print(network.is_in_relation_with(agent1, agent2))  # Вывод: True
print(network.is_in_relation_with(agent1, TinyPerson("Charlie")))  # Вывод: False
```