# Модуль `tiny_social_network.py`

## Обзор

Модуль `tiny_social_network.py` содержит класс `TinySocialNetwork`, который расширяет функциональность класса `TinyWorld`, добавляя возможность моделирования социальных связей между агентами (экземплярами класса `TinyPerson`). Он позволяет устанавливать отношения между агентами и ограничивать взаимодействие между ними на основе этих отношений.

## Подробней

Этот модуль используется для создания симуляций, в которых агенты могут взаимодействовать только с теми, с кем у них установлены отношения. Это позволяет моделировать социальные сети и изучать поведение агентов в условиях ограниченной коммуникации.
В частности, модуль реализует возможность отправки сообщений только агентам, находящимся в тех же социальных связях, что и отправитель.

## Классы

### `TinySocialNetwork`

**Описание**: Класс `TinySocialNetwork` представляет собой социальную сеть, в которой агенты (`TinyPerson`) могут находиться в определенных отношениях друг с другом. Этот класс наследует функциональность класса `TinyWorld` и добавляет возможность управления социальными связями между агентами.

**Наследует**:

- `TinyWorld`: Класс `TinySocialNetwork` наследует от `TinyWorld`, расширяя его функциональность для моделирования социальных взаимодействий между агентами.

**Атрибуты**:

- `name` (str): Имя социальной сети.
- `broadcast_if_no_target` (bool): Флаг, определяющий, следует ли широковещательно рассылать действия агента, если цель действия не найдена.
- `relations` (dict): Словарь, содержащий отношения между агентами. Ключи словаря - имена отношений, значения - списки кортежей, где каждый кортеж содержит пару агентов, связанных данным отношением.

**Принцип работы**:

1.  При создании экземпляра `TinySocialNetwork` инициализируется базовая функциональность `TinyWorld`.
2.  Метод `add_relation` позволяет добавлять отношения между агентами.
3.  Метод `_update_agents_contexts` обновляет контексты агентов, определяя, какие агенты доступны для взаимодействия на основе установленных отношений.
4.  Метод `_handle_reach_out` ограничивает отправку сообщений только агентам, находящимся в тех же отношениях, что и отправитель.
5.  Метод `is_in_relation_with` проверяет, находятся ли два агента в определенных отношениях.

## Методы класса

### `__init__`

```python
def __init__(self, name, broadcast_if_no_target=True):
    """
    Create a new TinySocialNetwork environment.

    Args:
        name (str): The name of the environment.
        broadcast_if_no_target (bool): If True, broadcast actions through an agent\'s available relations
          if the target of an action is not found.
    """
```

**Назначение**: Инициализирует новый экземпляр класса `TinySocialNetwork`.

**Параметры**:

-   `name` (str): Имя окружения (социальной сети).
-   `broadcast_if_no_target` (bool): Если `True`, широковещательные действия агентов через доступные отношения, если цель действия не найдена. По умолчанию `True`.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `TinyWorld` для инициализации основных атрибутов окружения.
2.  Инициализирует атрибут `relations` как пустой словарь, который будет использоваться для хранения отношений между агентами.

**Примеры**:

```python
network = TinySocialNetwork(name="MyNetwork", broadcast_if_no_target=False)
print(network.name)
print(network.relations)
```

### `add_relation`

```python
@transactional
def add_relation(self, agent_1, agent_2, name="default"):
    """
    Adds a relation between two agents.
    
    Args:
        agent_1 (TinyPerson): The first agent.
        agent_2 (TinyPerson): The second agent.
        name (str): The name of the relation.
    """
```

**Назначение**: Добавляет отношение между двумя агентами.

**Параметры**:

-   `agent_1` (`TinyPerson`): Первый агент.
-   `agent_2` (`TinyPerson`): Второй агент.
-   `name` (str): Имя отношения. По умолчанию `"default"`.

**Как работает функция**:

1.  Логирует добавление отношения между агентами.
2.  Проверяет, находятся ли агенты уже в списке агентов социальной сети, и добавляет их, если это не так.
3.  Добавляет отношение в словарь `self.relations`. Если отношение с данным именем уже существует, добавляет новую пару агентов в список отношений. В противном случае создает новую запись в словаре с указанным именем отношения и добавляет туда пару агентов.
4.  Возвращает `self` для возможности цепочки вызовов.

**Примеры**:

```python
from tinytroupe.agent.agent import TinyPerson
network = TinySocialNetwork(name="MyNetwork")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
network.add_relation(agent1, agent2, name="friend")
print(network.relations)
```

### `_update_agents_contexts`

```python
@transactional
def _update_agents_contexts(self):
    """
    Updates the agents' observations based on the current state of the world.
    """
```

**Назначение**: Обновляет знания агентов об окружении на основе текущего состояния мира.

**Как работает функция**:

1.  Сначала делает всех агентов недоступными друг для друга, чтобы сбросить предыдущие состояния видимости.
2.  Затем, на основе установленных отношений, делает связанных агентов доступными друг для друга. Это означает, что каждый агент будет знать о существовании и состоянии тех агентов, с которыми он связан.
3.  Для каждого отношения в `self.relations` проходится по каждой паре агентов и делает их доступными друг для друга с помощью методов `make_agent_accessible`.

**Примеры**:

```python
from tinytroupe.agent.agent import TinyPerson
network = TinySocialNetwork(name="MyNetwork")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
network.add_relation(agent1, agent2, name="friend")
network._update_agents_contexts()
print(agent1.accessible_agents)  # агент 2 будет в списке доступных агенто для агента 1
```

### `_step`

```python
@transactional
def _step(self):
    self._update_agents_contexts()

    #call super
    super()._step()
```

**Назначение**: Выполняет один шаг симуляции в социальной сети.

**Как работает функция**:

1.  Обновляет контексты агентов, вызывая метод `_update_agents_contexts`.
2.  Вызывает метод `_step` родительского класса `TinyWorld` для выполнения основных действий шага симуляции.

**Примеры**:

```python
from tinytroupe.agent.agent import TinyPerson
network = TinySocialNetwork(name="MyNetwork")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
network.add_relation(agent1, agent2, name="friend")
network._step()
```

### `_handle_reach_out`

```python
@transactional
def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
    """
    Handles the REACH_OUT action. This social network implementation only allows
    REACH_OUT to succeed if the target agent is in the same relation as the source agent.

    Args:
        source_agent (TinyPerson): The agent that issued the REACH_OUT action.
        content (str): The content of the message.
        target (str): The target of the message.
    """
```

**Назначение**: Обрабатывает действие `REACH_OUT` (попытку связаться) одного агента с другим.

**Параметры**:

-   `source_agent` (`TinyPerson`): Агент, инициирующий действие `REACH_OUT`.
-   `content` (str): Содержание сообщения.
-   `target` (str): Имя целевого агента.

**Как работает функция**:

1.  Проверяет, находится ли целевой агент в тех же отношениях, что и агент-источник.
2.  Если целевой агент находится в тех же отношениях, вызывает метод `_handle_reach_out` родительского класса `TinyWorld` для обработки действия `REACH_OUT`.
3.  Если целевой агент не находится в тех же отношениях, агент-источник получает сообщение о том, что не может связаться с целевым агентом.

**Примеры**:

```python
from tinytroupe.agent.agent import TinyPerson
network = TinySocialNetwork(name="MyNetwork")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
agent3 = TinyPerson(name="Charlie")

network.add_relation(agent1, agent2, name="friend")

agent1.add_action("reach_out", {"target": "Bob", "content": "Hello, Bob!"})
network._handle_reach_out(agent1, "Hello, Bob!", "Bob")  # Alice может связаться с Bob
```

### `is_in_relation_with`

```python
def is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool:
    """
    Checks if two agents are in a relation. If the relation name is given, check that
    the agents are in that relation. If no relation name is given, check that the agents
    are in any relation. Relations are undirected, so the order of the agents does not matter.

    Args:
        agent_1 (TinyPerson): The first agent.
        agent_2 (TinyPerson): The second agent.
        relation_name (str): The name of the relation to check, or None to check any relation.

    Returns:
        bool: True if the two agents are in the given relation, False otherwise.
    """
```

**Назначение**: Проверяет, находятся ли два агента в каком-либо или конкретном отношении.

**Параметры**:

-   `agent_1` (`TinyPerson`): Первый агент.
-   `agent_2` (`TinyPerson`): Второй агент.
-   `relation_name` (str, optional): Имя отношения для проверки. Если `None`, проверяется наличие любого отношения между агентами. По умолчанию `None`.

**Возвращает**:

-   `bool`: `True`, если агенты находятся в указанном (или любом) отношении, `False` в противном случае.

**Как работает функция**:

1.  Если `relation_name` не указано, функция проходит по всем отношениям в `self.relations` и проверяет, есть ли пара агентов в каком-либо из отношений (порядок агентов не важен).
2.  Если `relation_name` указано, функция проверяет, существует ли такое отношение в `self.relations`, и если да, проверяет, есть ли пара агентов в этом отношении (порядок агентов не важен).
3.  Возвращает `True`, если агенты находятся в указанном (или любом) отношении, и `False` в противном случае.

**Примеры**:

```python
from tinytroupe.agent.agent import TinyPerson
network = TinySocialNetwork(name="MyNetwork")
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
network.add_relation(agent1, agent2, name="friend")
print(network.is_in_relation_with(agent1, agent2))
print(network.is_in_relation_with(agent1, agent2, relation_name="friend"))
print(network.is_in_relation_with(agent1, agent2, relation_name="family"))