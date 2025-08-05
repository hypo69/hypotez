# TinySocialNetwork Environment

## Overview

This module defines the `TinySocialNetwork` class, which represents a social network environment in the `tinytroupe` project. This environment extends the base `TinyWorld` class and adds functionality related to social interactions between agents, including:

- **Relationships:**  Agents can be connected through relationships with specific names.
- **Accessibility:** Agents can become aware of other agents through relationships.
- **Limited communication:** `REACH_OUT` actions are only successful if the target agent is in the same relation as the source agent.

## Details

The `TinySocialNetwork` environment provides a basic framework for simulating social interactions within a limited network. Agents within this environment can establish relationships, and communication is constrained based on those relationships. The `_update_agents_contexts` method ensures agents are aware of other agents based on existing relationships.

## Classes

### `TinySocialNetwork`

**Description**:  Represents a social network environment where agents can have relationships and interact with each other.

**Inherits**: `TinyWorld`

**Attributes**:
- `relations` (dict):  A dictionary that stores relationships between agents. Keys represent relation names, and values are lists of tuples containing pairs of agents in that relation.

**Methods**:
- `add_relation(agent_1, agent_2, name="default")`: Adds a relationship between two agents.
- `_update_agents_contexts()`: Updates agent observations based on existing relationships, ensuring that agents are aware of others they are connected to.
- `_step()`:  Performs a step in the environment, including updating agent contexts.
- `_handle_reach_out(source_agent, content, target)`: Handles the `REACH_OUT` action. Only successful if the target agent is in the same relationship as the source agent.
- `is_in_relation_with(agent_1, agent_2, relation_name=None)`: Checks if two agents are in a given relationship.

## Class Methods

### `add_relation(agent_1, agent_2, name="default")`

```python
    @transactional
    def add_relation(self, agent_1, agent_2, name="default"):
        """
        Добавляет связь между двумя агентами.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент.
            name (str): Название связи.
        """

        logger.debug(f"Добавление связи {name} между {agent_1.name} и {agent_2.name}.")

        # агенты должны уже быть в среде, если нет, они сначала добавляются
        if agent_1 not in self.agents:
            self.agents.append(agent_1)
        if agent_2 not in self.agents:
            self.agents.append(agent_2)

        if name in self.relations:
            self.relations[name].append((agent_1, agent_2))
        else:
            self.relations[name] = [(agent_1, agent_2)]

        return self # for chaining
```

**Purpose**: Adds a relationship between two agents within the social network.

**Parameters**:
- `agent_1` (TinyPerson): The first agent in the relationship.
- `agent_2` (TinyPerson): The second agent in the relationship.
- `name` (str, optional): The name of the relationship. Defaults to "default".

**Returns**:
- `TinySocialNetwork`: Returns the environment object for method chaining.

**How the Method Works**:
1. Checks if the agents are already in the environment's agent list. If not, they are added.
2. Adds the pair of agents to the `relations` dictionary under the specified relation name. If the relation name doesn't exist, a new entry is created in the dictionary.

**Example**:

```python
>>> alice = TinyPerson(name="Alice")
>>> bob = TinyPerson(name="Bob")
>>> social_network = TinySocialNetwork("MyNetwork")
>>> social_network.add_relation(alice, bob, name="friends")
>>> social_network.relations
{'friends': [(alice, bob)]}
```

### `_update_agents_contexts()`

```python
    @transactional
    def _update_agents_contexts(self):
        """
        Обновляет наблюдения агентов на основе текущего состояния мира.
        """

        # очистить всю доступность в первую очередь
        for agent in self.agents:
            agent.make_all_agents_inaccessible()

        # теперь обновить доступность на основе отношений
        for relation_name, relation in self.relations.items():
            logger.debug(f"Обновление наблюдений агентов для связи {relation_name}.")
            for agent_1, agent_2 in relation:
                agent_1.make_agent_accessible(agent_2)
                agent_2.make_agent_accessible(agent_1)
```

**Purpose**: Updates the `accessible_agents` set of each agent within the social network based on their relationships.

**How the Method Works**:
1. Iterates through all agents and initializes their `accessible_agents` set to an empty set, making all agents initially inaccessible.
2. Iterates through all relationships:
   - For each pair of agents in the relationship, it makes each agent accessible to the other.

**Example**:

```python
>>> alice = TinyPerson(name="Alice")
>>> bob = TinyPerson(name="Bob")
>>> charlie = TinyPerson(name="Charlie")
>>> social_network = TinySocialNetwork("MyNetwork")
>>> social_network.add_relation(alice, bob, name="friends")
>>> social_network.add_relation(bob, charlie, name="colleagues")
>>> social_network._update_agents_contexts()
>>> alice.accessible_agents
{bob}
>>> bob.accessible_agents
{alice, charlie}
>>> charlie.accessible_agents
{bob}
```

### `_step()`

```python
    @transactional
    def _step(self):
        self._update_agents_contexts()

        #call super
        super()._step()
```

**Purpose**: Executes a single step in the social network environment. This includes updating agent contexts based on relationships and calling the parent class's `_step` method for general environment updates.

**How the Method Works**:
1. Calls `_update_agents_contexts` to ensure agents are aware of other agents they are connected to.
2. Calls the parent class's `_step` method, which typically handles general environment updates, such as processing agent actions.

### `_handle_reach_out(source_agent, content, target)`

```python
    @transactional
    def _handle_reach_out(self, source_agent: TinyPerson, content: str, target: str):
        """
        Обрабатывает действие REACH_OUT. Эта реализация социальной сети позволяет только REACH_OUT
        удаться, если целевой агент находится в том же отношении, что и источник.

        Args:
            source_agent (TinyPerson): Агент, который выдал действие REACH_OUT.
            content (str): Содержание сообщения.
            target (str): Цель сообщения.
        """
            
        # проверка, находится ли цель в том же отношении, что и источник
        if self.is_in_relation_with(source_agent, self.get_agent_by_name(target)):
            super()._handle_reach_out(source_agent, content, target)
            
        # если мы дошли сюда, значит цель не находится в том же отношении, что и источник
        source_agent.socialize(f"{target} is not in the same relation as you, so you cannot reach out to them.", source=self)
```

**Purpose**: Handles the `REACH_OUT` action for communication between agents.

**Parameters**:
- `source_agent` (TinyPerson): The agent sending the message.
- `content` (str): The message content.
- `target` (str): The name of the target agent to receive the message.

**How the Method Works**:
1. Checks if the target agent is in the same relationship as the source agent using the `is_in_relation_with` method.
2. If the target is in the same relationship, it calls the parent class's `_handle_reach_out` method to handle the communication.
3. If the target is not in the same relationship, it uses the `socialize` method to inform the source agent that the action failed.

**Example**:

```python
>>> alice = TinyPerson(name="Alice")
>>> bob = TinyPerson(name="Bob")
>>> charlie = TinyPerson(name="Charlie")
>>> social_network = TinySocialNetwork("MyNetwork")
>>> social_network.add_relation(alice, bob, name="friends")
>>> alice.reach_out("Hi Bob!", target="Bob") # Successful REACH_OUT
>>> alice.reach_out("Hi Charlie!", target="Charlie") # Unsuccessful REACH_OUT
```

### `is_in_relation_with(agent_1, agent_2, relation_name=None)`

```python
    def is_in_relation_with(self, agent_1:TinyPerson, agent_2:TinyPerson, relation_name=None) -> bool:
        """
        Проверяет, находятся ли два агента в связи. Если имя связи дано, проверьте,
        что агенты находятся в этой связи. Если имя связи не дано, проверьте,
        что агенты находятся в любой связи. Связи ненаправленные, поэтому порядок агентов не имеет значения.

        Args:
            agent_1 (TinyPerson): Первый агент.
            agent_2 (TinyPerson): Второй агент.
            relation_name (str): Название связи, которую нужно проверить, или None, чтобы проверить любую связь.

        Returns:
            bool: True, если два агента находятся в заданной связи, False в противном случае.
        """
        if relation_name is None:
            for relation_name, relation in self.relations.items():
                if (agent_1, agent_2) in relation or (agent_2, agent_1) in relation:
                    return True
            return False
        
        else:
            if relation_name in self.relations:
                return (agent_1, agent_2) in self.relations[relation_name] or (agent_2, agent_1) in self.relations[relation_name]
            else:
                return False
```

**Purpose**: Checks if two agents are in a given relationship.

**Parameters**:
- `agent_1` (TinyPerson): The first agent.
- `agent_2` (TinyPerson): The second agent.
- `relation_name` (str, optional): The name of the relationship to check. If `None`, checks any relationship.

**Returns**:
- `bool`: True if the agents are in the specified relationship, False otherwise.

**How the Method Works**:
1. If `relation_name` is `None`, iterates through all relations and checks if the agent pair is present in any of them.
2. If `relation_name` is provided, checks if the agent pair is present in the specified relationship.

**Example**:

```python
>>> alice = TinyPerson(name="Alice")
>>> bob = TinyPerson(name="Bob")
>>> charlie = TinyPerson(name="Charlie")
>>> social_network = TinySocialNetwork("MyNetwork")
>>> social_network.add_relation(alice, bob, name="friends")
>>> social_network.add_relation(bob, charlie, name="colleagues")
>>> social_network.is_in_relation_with(alice, bob) # True
>>> social_network.is_in_relation_with(alice, charlie) # False
>>> social_network.is_in_relation_with(bob, charlie, relation_name="colleagues") # True
```