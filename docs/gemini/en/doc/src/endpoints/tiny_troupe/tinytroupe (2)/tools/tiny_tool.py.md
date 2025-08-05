# TinyTool Module Documentation

## Overview

This module defines the `TinyTool` class, a base class for tools that can be used by agents in a simulation environment. 

## Details

The `TinyTool` class represents a tool that an agent can use to perform actions. Tools are designed to interact with the world outside the simulation and can have real-world side effects. 

The `TinyTool` class is implemented as a `JsonSerializableRegistry` subclass, allowing it to be serialized and deserialized from JSON. This enables the creation of reusable tool definitions and the loading of tools from external sources. 

## Classes

### `TinyTool`

**Description**: Base class for tools in a simulation environment. 
**Inherits**: `JsonSerializableRegistry` 

**Attributes**:

- `name` (str): The name of the tool.
- `description` (str): A brief description of the tool.
- `owner` (str): The agent that owns the tool. If `None`, the tool can be used by anyone.
- `real_world_side_effects` (bool): Whether the tool has real-world side effects. 
- `exporter` (`ArtifactExporter`): An exporter for exporting results of tool actions.
- `enricher` (`Enricher`): An enricher for enriching results of tool actions.

**Methods**:

- `__init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None)`: Initializes a new tool instance.
- `_process_action(self, agent, action: dict) -> bool`:  Processes an action. This method must be implemented by subclasses.
- `_protect_real_world(self)`: Raises a warning if the tool has real-world side effects.
- `_enforce_ownership(self, agent)`: Enforces ownership of the tool. Raises a `ValueError` if the agent does not own the tool. 
- `set_owner(self, owner)`: Sets the owner of the tool. 
- `actions_definitions_prompt(self) -> str`: Returns a prompt for defining tool actions. This method must be implemented by subclasses.
- `actions_constraints_prompt(self) -> str`: Returns a prompt for defining tool action constraints. This method must be implemented by subclasses.
- `process_action(self, agent, action: dict) -> bool`: Processes an action, including protection against real-world side effects and ownership enforcement. 

## Class Methods

### `_process_action`

```python
    def _process_action(self, agent, action: dict) -> bool:
        """
        Processes an action. This method must be implemented by subclasses.

        Args:
            agent (Agent): The agent that is performing the action.
            action (dict): The action to be processed.

        Returns:
            bool: Whether the action was successful.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.

        Example:
            >>> tool = TinyTool('MyTool', 'A tool for doing things')
            >>> tool._process_action(agent, {'action_type': 'do_something'})
            Traceback (most recent call last):
              ...
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method.")
```

### `_protect_real_world`

```python
    def _protect_real_world(self):
        """
        Raises a warning if the tool has real-world side effects.

        Example:
            >>> tool = TinyTool('MyTool', 'A tool for doing things', real_world_side_effects=True)
            >>> tool._protect_real_world()
            WARNING: !!!!!!!!!! Tool MyTool has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!
        """
        if self.real_world_side_effects:
            logger.warning(f" !!!!!!!!!! Tool {self.name} has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!")
```

### `_enforce_ownership`

```python
    def _enforce_ownership(self, agent):
        """
        Enforces ownership of the tool. Raises a ValueError if the agent does not own the tool.

        Args:
            agent (Agent): The agent that is trying to use the tool.

        Raises:
            ValueError: If the agent does not own the tool.

        Example:
            >>> tool = TinyTool('MyTool', 'A tool for doing things', owner='Alice')
            >>> tool._enforce_ownership(agent='Bob')
            Traceback (most recent call last):
              ...
            ValueError: Agent Bob does not own tool MyTool, which is owned by Alice.
        """
        if self.owner is not None and agent.name != self.owner.name:
            raise ValueError(f"Agent {agent.name} does not own tool {self.name}, which is owned by {self.owner.name}.")
```

### `actions_definitions_prompt`

```python
    def actions_definitions_prompt(self) -> str:
        """
        Returns a prompt for defining tool actions. This method must be implemented by subclasses.

        Returns:
            str: The prompt for defining tool actions.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.

        Example:
            >>> tool = TinyTool('MyTool', 'A tool for doing things')
            >>> tool.actions_definitions_prompt()
            Traceback (most recent call last):
              ...
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method.")
```

### `actions_constraints_prompt`

```python
    def actions_constraints_prompt(self) -> str:
        """
        Returns a prompt for defining tool action constraints. This method must be implemented by subclasses.

        Returns:
            str: The prompt for defining tool action constraints.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.

        Example:
            >>> tool = TinyTool('MyTool', 'A tool for doing things')
            >>> tool.actions_constraints_prompt()
            Traceback (most recent call last):
              ...
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method.")
```

### `process_action`

```python
    def process_action(self, agent, action: dict) -> bool:
        """
        Processes an action, including protection against real-world side effects and ownership enforcement.

        Args:
            agent (Agent): The agent that is performing the action.
            action (dict): The action to be processed.

        Returns:
            bool: Whether the action was successful.

        Example:
            >>> tool = TinyTool('MyTool', 'A tool for doing things', real_world_side_effects=True)
            >>> tool.process_action(agent, {'action_type': 'do_something'})
            WARNING: !!!!!!!!!! Tool MyTool has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!
            ...  # Further processing of the action
        """
        self._protect_real_world()
        self._enforce_ownership(agent)
        self._process_action(agent, action)
```

## Parameter Details

- `name` (str): The name of the tool. This should be a concise and descriptive name that helps identify the tool's purpose.
- `description` (str): A brief description of the tool. This should provide a clear understanding of what the tool does and how it works.
- `owner` (str): The agent that owns the tool. This should be a string identifying the agent that is authorized to use the tool. If set to `None`, the tool can be used by any agent. 
- `real_world_side_effects` (bool): This boolean flag indicates whether the tool has the potential to modify the state of the world outside the simulation. 
- `exporter` (`ArtifactExporter`): An instance of the `ArtifactExporter` class, which is used to export the results of the tool's actions. If `None`, the tool cannot export results.
- `enricher` (`Enricher`): An instance of the `Enricher` class, which is used to enrich the results of the tool's actions. If `None`, the tool cannot enrich results.

## Examples

```python
from tinytroupe.tools import TinyTool
from tinytroupe.utils import JsonSerializableRegistry

class MyTool(TinyTool):

    def __init__(self, name, description, owner=None, real_world_side_effects=False, exporter=None, enricher=None):
        super().__init__(name, description, owner, real_world_side_effects, exporter, enricher)

    def _process_action(self, agent, action: dict) -> bool:
        # Implement the actual processing of the action here
        return True

    def actions_definitions_prompt(self) -> str:
        return "What action do you want to perform?"

    def actions_constraints_prompt(self) -> str:
        return "What are the constraints for this action?"

# Creating an instance of the MyTool class
tool = MyTool(name='MyTool', description='A tool for doing things', owner='Alice')

# Defining an action
action = {'action_type': 'do_something'}

# Processing the action
tool.process_action(agent='Alice', action=action)

# Output: 
# WARNING: !!!!!!!!!! Tool MyTool has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!
# ...  # Further processing of the action
```

This example demonstrates how to create a new tool, define an action, and process the action using the `process_action` method.