# Mental Faculties Module

## Overview

This module defines various mental faculties for the agent, which represent its cognitive abilities. These faculties are responsible for actions like recalling information, accessing local files and web pages, and using tools. They provide a structured framework for the agent to interact with its environment and perform tasks effectively.

## Details

The mental faculties are implemented as subclasses of the `TinyMentalFaculty` class. Each subclass defines specific actions and constraints related to its functionality.  The `CustomMentalFaculty` subclass allows for user-defined faculties with customizable actions and constraints. The `RecallFaculty`, `FilesAndWebGroundingFaculty`, and `TinyToolUse` classes implement specific mental abilities.

## Classes

### `TinyMentalFaculty`

**Description**: Represents a mental faculty of an agent. Mental faculties are the cognitive abilities that an agent has.

**Inherits**: `JsonSerializableRegistry`

**Attributes**:

- `name` (str): The name of the mental faculty.
- `requires_faculties` (list): A list of mental faculties that this faculty requires to function properly.

**Methods**:

- `__init__(self, name: str, requires_faculties: list=None) -> None`: Initializes the mental faculty.
- `__str__(self) -> str`: Returns a string representation of the mental faculty.
- `__eq__(self, other)`: Checks if two mental faculties are equal based on their names.
- `process_action(self, agent, action: dict) -> bool`: Processes an action related to this faculty.
- `actions_definitions_prompt(self) -> str`: Returns the prompt for defining actions related to this faculty.
- `actions_constraints_prompt(self) -> str`: Returns the prompt for defining constraints on actions related to this faculty.

### `CustomMentalFaculty`

**Description**: Represents a custom mental faculty of an agent. Custom mental faculties are the cognitive abilities that an agent has and that are defined by the user just by specifying the actions that the faculty can perform or the constraints that the faculty introduces. Constraints might be related to the actions that the faculty can perform or be independent, more general constraints that the agent must follow.

**Inherits**: `TinyMentalFaculty`

**Attributes**:

- `actions_configs` (dict): A dictionary with the configuration of actions that this faculty can perform. Format is {<action_name>: {"description": <description>, "function": <function>}}.
- `constraints` (dict): A list with the constraints introduced by this faculty. Format is [<constraint1>, <constraint2>, ...].

**Methods**:

- `__init__(self, name: str, requires_faculties: list = None, actions_configs: dict = None, constraints: dict = None)`: Initializes the custom mental faculty.
- `add_action(self, action_name: str, description: str, function: Callable=None)`: Adds a new action to the faculty's action configurations.
- `add_actions(self, actions: dict)`: Adds multiple actions to the faculty's action configurations.
- `add_action_constraint(self, constraint: str)`: Adds a constraint to the faculty.
- `add_actions_constraints(self, constraints: list)`: Adds multiple constraints to the faculty.
- `process_action(self, agent, action: dict) -> bool`: Processes an action related to this faculty.
- `actions_definitions_prompt(self) -> str`: Returns the prompt for defining actions related to this faculty.
- `actions_constraints_prompt(self) -> str`: Returns the prompt for defining constraints on actions related to this faculty.

### `RecallFaculty`

**Description**:  Allows the agent to recall information from its memory.

**Inherits**: `TinyMentalFaculty`

**Methods**:

- `__init__(self)`: Initializes the RecallFaculty.
- `process_action(self, agent, action: dict) -> bool`: Processes an action related to this faculty.
- `actions_definitions_prompt(self) -> str`: Returns the prompt for defining actions related to this faculty.
- `actions_constraints_prompt(self) -> str`: Returns the prompt for defining constraints on actions related to this faculty.

### `FilesAndWebGroundingFaculty`

**Description**: Allows the agent to access local files and web pages to ground its knowledge.

**Inherits**: `TinyMentalFaculty`

**Attributes**:

- `local_files_grounding_connector` (`LocalFilesGroundingConnector`): Connector for accessing local files.
- `web_grounding_connector` (`WebPagesGroundingConnector`): Connector for accessing web pages.

**Methods**:

- `__init__(self, folders_paths: list=None, web_urls: list=None)`: Initializes the FilesAndWebGroundingFaculty.
- `process_action(self, agent, action: dict) -> bool`: Processes an action related to this faculty.
- `actions_definitions_prompt(self) -> str`: Returns the prompt for defining actions related to this faculty.
- `actions_constraints_prompt(self) -> str`: Returns the prompt for defining constraints on actions related to this faculty.

### `TinyToolUse`

**Description**: Allows the agent to use tools to accomplish tasks. 

**Inherits**: `TinyMentalFaculty`

**Attributes**:

- `tools` (list): A list of tools that the agent can use.

**Methods**:

- `__init__(self, tools:list) -> None`: Initializes the TinyToolUse faculty.
- `process_action(self, agent, action: dict) -> bool`: Processes an action related to this faculty.
- `actions_definitions_prompt(self) -> str`: Returns the prompt for defining actions related to this faculty.
- `actions_constraints_prompt(self) -> str`: Returns the prompt for defining constraints on actions related to this faculty.

## Conclusion

This module provides a foundational set of mental faculties that empower the agent with crucial cognitive abilities, enabling it to access information, recall memories, and utilize tools for effective task completion. The flexible design of custom faculties allows for further customization and expansion of the agent's cognitive capabilities.