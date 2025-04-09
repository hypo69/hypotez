# Модуль TinySocialNetwork

## Обзор

Модуль `TinySocialNetwork` предоставляет класс `TinySocialNetwork`, который является подклассом `TinyWorld` и предназначен для моделирования социальной сети агентов (`TinyPerson`). Он позволяет устанавливать отношения между агентами, обновлять контексты агентов на основе этих отношений и обрабатывать действия взаимодействия между агентами.

## Подробней

Модуль расширяет возможности `TinyWorld`, добавляя функциональность для управления социальными связями между агентами. Это включает в себя добавление отношений между агентами, обновление контекстов агентов на основе этих отношений и обработку действий взаимодействия, таких как `REACH_OUT`, с учетом социальных связей.

## Классы

### `TinySocialNetwork`

**Описание**: Класс `TinySocialNetwork` представляет собой социальную сеть, состоящую из агентов (`TinyPerson`) и отношений между ними.

**Наследует**:
- `TinyWorld`: Наследует функциональность базового мира, такую как управление агентами и выполнение шагов симуляции.

**Атрибуты**:
- `relations (dict)`: Словарь, хранящий отношения между агентами. Ключом является имя отношения, а значением - список кортежей, содержащих пары агентов, связанных этим отношением.

**Методы**:
- `__init__(self, name, broadcast_if_no_target=True)`: Конструктор класса, инициализирует социальную сеть с заданным именем и параметром широковещания.
- `add_relation(self, agent_1, agent_2, name="default")`: Добавляет отношение между двумя агентами.
- `_update_agents_contexts(self)`: Обновляет контексты агентов на основе текущего состояния мира, устанавливая доступность агентов друг для друга в зависимости от установленных отношений.
- `_step(self)`: Выполняет один шаг симуляции, обновляя контексты агентов и вызывая метод `_step` родительского класса.
- `_handle_reach_out(self, source_agent: TinyPerson, content: str, target: str)`: Обрабатывает действие `REACH_OUT`, позволяя агенту обратиться к другому агенту только в том случае, если они находятся в одном отношении.
- `is_in_relation_with(self, agent_1: TinyPerson, agent_2: TinyPerson, relation_name=None) -> bool`: Проверяет, находятся ли два агента в каком-либо отношении или в конкретном отношении.

**Принцип работы**:
1.  При создании экземпляра `TinySocialNetwork` вызывается конструктор `__init__`, который инициализирует имя социальной сети и устанавливает параметр `broadcast_if_no_target`. Также инициализируется пустой словарь `relations` для хранения отношений между агентами.
2.  Метод `add_relation` добавляет отношение между двумя агентами, указанными как `agent_1` и `agent_2`. Если агенты еще не находятся в социальной сети, они добавляются в список `agents`. Отношение сохраняется в словаре `relations`, где ключом является имя отношения, а значением - список кортежей, содержащих пары агентов, связанных этим отношением.
3.  Метод `_update_agents_contexts` обновляет наблюдения агентов на основе текущего состояния мира. Сначала он очищает все предыдущие настройки доступности агентов. Затем, на основе установленных отношений, он делает агентов доступными друг для друга.
4.  Метод `_step` выполняет один шаг симуляции. Он вызывает метод `_update_agents_contexts` для обновления контекстов агентов, а затем вызывает метод `_step` родительского класса `TinyWorld` для выполнения других действий, связанных с шагом симуляции.
5.  Метод `_handle_reach_out` обрабатывает действие `REACH_OUT`, когда один агент пытается обратиться к другому. Он проверяет, находятся ли агенты в одном отношении. Если это так, то вызывается метод `_handle_reach_out` родительского класса для обработки действия. Если агенты не находятся в одном отношении, то исходному агенту сообщается, что он не может обратиться к целевому агенту.
6.  Метод `is_in_relation_with` проверяет, находятся ли два агента в каком-либо отношении или в конкретном отношении. Если указано имя отношения, то проверяется, находятся ли агенты в этом отношении. Если имя отношения не указано, то проверяется, находятся ли агенты в каком-либо отношении.

## Функции

### `add_relation`

```python
    @transactional
    def add_relation(self, agent_1, agent_2, name="default") -> TinySocialNetwork:
        """
        Adds a relation between two agents.
        
        Args:
            agent_1 (TinyPerson): The first agent.
            agent_2 (TinyPerson): The second agent.
            name (str): The name of the relation.
        Returns:
            TinySocialNetwork:  Возвращает экземпляр `TinySocialNetwork` для цепочки вызовов.
        """
```

**Назначение**: Добавляет отношение между двумя агентами в социальной сети.

**Параметры**:
- `agent_1 (TinyPerson)`: Первый агент, участвующий в отношении.
- `agent_2 (TinyPerson)`: Второй агент, участвующий в отношении.
- `name (str, optional)`: Название отношения. По умолчанию "default".

**Возвращает**:
- `TinySocialNetwork`: Возвращает экземпляр `TinySocialNetwork` для цепочки вызовов.

**Как работает функция**:
1.  Логирует добавление отношения с указанным именем между двумя агентами.
2.  Проверяет, находятся ли агенты уже в списке агентов социальной сети. Если нет, добавляет их.
3.  Проверяет, существует ли уже отношение с указанным именем. Если да, добавляет пару агентов в список этого отношения. Если нет, создает новое отношение с указанным именем и добавляет пару агентов в этот список.
4.  Возвращает экземпляр `TinySocialNetwork` для возможности цепочки вызовов методов.

**Примеры**:

```python
from tinytroupe.environment.tiny_social_network import TinySocialNetwork
from tinytroupe.agent import TinyPerson
import logging
from src.logger import logger

# Инициализация агентов
agent1 = TinyPerson(name="Alice")
agent2 = TinyPerson(name="Bob")
agent3 = TinyPerson(name="Charlie")

# Инициализация социальной сети
social_network = TinySocialNetwork(name="MyNetwork")

# Добавление отношения между агентами
social_network.add_relation(agent1, agent2, name="friends")
social_network.add_relation(agent2, agent3, name="colleagues")

logger.info(f"Relations: {social_network.relations}")
# Relations: {'friends': [(<tinytroupe.agent.TinyPerson object at 0x...>, <tinytroupe.agent.TinyPerson object at 0x...>)], 'colleagues': [(<tinytroupe.agent.TinyPerson object at 0x...>, <tinytroupe.agent.TinyPerson object at 0x...>)]}
```

### `_update_agents_contexts`

```python
    @transactional
    def _update_agents_contexts(self):
        """
        Updates the agents' observations based on the current state of the world.
        """
```

**Назначение**: Обновляет контексты агентов на основе текущего состояния мира, устанавливая доступность агентов друг для друга в зависимости от установленных отношений.

**Как работает функция**:
1.  Перебирает всех агентов в социальной сети и делает всех агентов недоступными друг для друга, вызывая метод `make_all_agents_inaccessible` для каждого агента.
2.  Перебирает все отношения в словаре `relations`.
3.  Для каждого отношения перебирает пары агентов, связанных этим отношением.
4.  Для каждой пары агентов делает агентов доступными друг для друга, вызывая метод `make_agent_accessible` для каждого агента.

### `_step`

```python
    @transactional
    def _step(self):
        """
        Выполняет один шаг симуляции, обновляя контексты агентов и вызывая метод `_step` родительского класса.
        """
```

**Назначение**: Выполняет один шаг симуляции в социальной сети.

**Как работает функция**:
1.  Вызывает метод `_update_agents_contexts` для обновления контекстов агентов на основе текущего состояния мира.
2.  Вызывает метод `_step` родительского класса `TinyWorld` для выполнения других действий, связанных с шагом симуляции.

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

**Назначение**: Обрабатывает действие `REACH_OUT`, позволяя агенту обратиться к другому агенту только в том случае, если они находятся в одном отношении.

**Параметры**:
- `source_agent (TinyPerson)`: Агент, инициировавший действие `REACH_OUT`.
- `content (str)`: Содержимое сообщения.
- `target (str)`: Имя целевого агента.

**Как работает функция**:
1.  Проверяет, находится ли целевой агент в том же отношении, что и исходный агент, с помощью метода `is_in_relation_with`.
2.  Если целевой агент находится в том же отношении, вызывается метод `_handle_reach_out` родительского класса `TinyWorld` для обработки действия `REACH_OUT`.
3.  Если целевой агент не находится в том же отношении, исходному агенту сообщается, что он не может обратиться к целевому агенту, вызывая метод `socialize`.

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

**Назначение**: Проверяет, находятся ли два агента в каком-либо отношении или в конкретном отношении.

**Параметры**:
- `agent_1 (TinyPerson)`: Первый агент.
- `agent_2 (TinyPerson)`: Второй агент.
- `relation_name (str, optional)`: Название отношения для проверки. Если `None`, проверяется наличие любого отношения.

**Возвращает**:
- `bool`: `True`, если агенты находятся в указанном отношении (или в любом отношении, если `relation_name` is `None`), `False` иначе.

**Как работает функция**:
1.  Если `relation_name` равно `None`, функция перебирает все отношения в словаре `self.relations`.
2.  Для каждого отношения проверяет, содержится ли пара агентов `(agent_1, agent_2)` или `(agent_2, agent_1)` в списке агентов, связанных этим отношением. Если да, возвращает `True`.
3.  Если ни одно отношение не содержит пару агентов, возвращает `False`.
4.  Если `relation_name` не равно `None`, функция проверяет, существует ли отношение с указанным именем в словаре `self.relations`.
5.  Если отношение существует, функция проверяет, содержится ли пара агентов `(agent_1, agent_2)` или `(agent_2, agent_1)` в списке агентов, связанных этим отношением. Возвращает результат проверки.
6.  Если отношение не существует, возвращает `False`.