# hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/tools.py

## Overview

This module provides tools for agents in the `hypotez` project.  Tools allow agents to perform specialized tasks, such as writing documents, managing calendars, and exporting artifacts.

## Details

This file defines the `TinyTool` base class and several concrete tool implementations, including:

- `TinyCalendar`: A basic calendar tool for managing events.
- `TinyWordProcessor`: A basic word processor tool for writing documents.

## Classes

### `TinyTool`

**Description**:  This is the base class for all tools. It provides a common interface for tools to interact with agents and process actions.

**Attributes**:

- `name` (str): The name of the tool.
- `description` (str): A brief description of the tool.
- `owner` (str): The agent that owns the tool. If `None`, the tool can be used by anyone.
- `real_world_side_effects` (bool): Whether the tool has real-world side effects. If `True`, it should be used with caution.
- `exporter` (ArtifactExporter): An exporter that can be used to export the results of the tool's actions. If `None`, the tool will not be able to export results.
- `enricher` (Enricher): An enricher that can be used to enrich the results of the tool's actions. If `None`, the tool will not be able to enrich results.

**Methods**:

- `_process_action(self, agent, action: dict) -> bool`: This method is called when an agent wants to use the tool. Subclasses must implement this method to define the specific actions the tool can perform. 
- `_protect_real_world(self)`: Logs a warning if the tool has real-world side effects.
- `_enforce_ownership(self, agent)`: Raises an error if the agent does not own the tool.
- `set_owner(self, owner)`: Sets the owner of the tool.
- `actions_definitions_prompt(self) -> str`: Returns a prompt that describes the actions the tool can perform. Subclasses must implement this method.
- `actions_constraints_prompt(self) -> str`: Returns a prompt that describes the constraints for using the tool. Subclasses must implement this method.
- `process_action(self, agent, action: dict) -> bool`: This method is called by the agent to use the tool. It enforces ownership and real-world side effects, then calls the `_process_action` method.

**Examples**:

```python
# Creating a new tool
tool = TinyTool(
    name="my_tool",
    description="A tool for doing something",
    owner="agent_name",
    real_world_side_effects=False,
    exporter=ArtifactExporter(),
    enricher=TinyEnricher()
)

# Using the tool
tool.process_action(agent, {"type": "some_action", "content": "some_data"})
```

### `TinyCalendar`

**Description**: A basic calendar tool that allows agents to keep track of meetings and appointments.

**Attributes**:

- `calendar` (dict): A dictionary that maps dates to lists of events. Each event is a dictionary with keys `title`, `description`, `owner`, `mandatory_attendees`, `optional_attendees`, `start_time`, and `end_time`.

**Methods**:

- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Adds a new event to the calendar.
- `find_events(self, year, month, day, hour=None, minute=None)`: Finds events that occur on the specified date and time.
- `_process_action(self, agent, action) -> bool`: Processes an action from an agent, such as creating a new event.
- `actions_definitions_prompt(self) -> str`: Returns a prompt that describes the actions the tool can perform.
- `actions_constraints_prompt(self) -> str`: Returns a prompt that describes the constraints for using the tool.

**Examples**:

```python
# Creating a new calendar tool
calendar_tool = TinyCalendar(owner="agent_name")

# Adding an event
calendar_tool.add_event(
    date="2024-03-15",
    title="Meeting",
    description="Discuss project plans.",
    owner="agent_name",
    mandatory_attendees=["agent_1", "agent_2"],
    start_time="10:00",
    end_time="11:00"
)

# Finding events
events = calendar_tool.find_events(year=2024, month=3, day=15)
```

### `TinyWordProcessor`

**Description**: A basic word processor tool that allows agents to write documents.

**Attributes**:

- `exporter` (ArtifactExporter): An exporter that can be used to export the results of the tool's actions.
- `enricher` (Enricher): An enricher that can be used to enrich the results of the tool's actions.

**Methods**:

- `write_document(self, title, content, author=None)`: Writes a new document with the given title, content, and author.
- `_process_action(self, agent, action) -> bool`: Processes an action from an agent, such as writing a new document.
- `actions_definitions_prompt(self) -> str`: Returns a prompt that describes the actions the tool can perform.
- `actions_constraints_prompt(self) -> str`: Returns a prompt that describes the constraints for using the tool.

**Examples**:

```python
# Creating a new word processor tool
word_processor = TinyWordProcessor(
    owner="agent_name",
    exporter=ArtifactExporter(),
    enricher=TinyEnricher()
)

# Writing a document
word_processor.write_document(
    title="My Document",
    content="This is the content of the document.",
    author="agent_name"
)
```

## Parameter Details

- `name` (str): The name of the tool.
- `description` (str): A brief description of the tool.
- `owner` (str): The agent that owns the tool. If `None`, the tool can be used by anyone.
- `real_world_side_effects` (bool): Whether the tool has real-world side effects. If `True`, it should be used with caution.
- `exporter` (ArtifactExporter): An exporter that can be used to export the results of the tool's actions. If `None`, the tool will not be able to export results.
- `enricher` (Enricher): An enricher that can be used to enrich the results of the tool's actions. If `None`, the tool will not be able to enrich results.

## Examples

```python
# Creating a new tool
tool = TinyTool(
    name="my_tool",
    description="A tool for doing something",
    owner="agent_name",
    real_world_side_effects=False,
    exporter=ArtifactExporter(),
    enricher=TinyEnricher()
)

# Using the tool
tool.process_action(agent, {"type": "some_action", "content": "some_data"})
```

```python
# Creating a new calendar tool
calendar_tool = TinyCalendar(owner="agent_name")

# Adding an event
calendar_tool.add_event(
    date="2024-03-15",
    title="Meeting",
    description="Discuss project plans.",
    owner="agent_name",
    mandatory_attendees=["agent_1", "agent_2"],
    start_time="10:00",
    end_time="11:00"
)

# Finding events
events = calendar_tool.find_events(year=2024, month=3, day=15)
```

```python
# Creating a new word processor tool
word_processor = TinyWordProcessor(
    owner="agent_name",
    exporter=ArtifactExporter(),
    enricher=TinyEnricher()
)

# Writing a document
word_processor.write_document(
    title="My Document",
    content="This is the content of the document.",
    author="agent_name"
)
```