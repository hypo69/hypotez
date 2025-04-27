# TinyCalendar: A Basic Calendar Tool for Agents

## Overview

This module provides a basic calendar tool (`TinyCalendar`) for agents to keep track of meetings and appointments. It allows agents to create events, find events based on date, and process actions related to event management.

## Details

The `TinyCalendar` class is a subclass of the `TinyTool` class, which is used for implementing tools within the TinyTroupe project. The calendar tool is primarily intended to assist agents in managing their schedules and coordinating appointments.

## Classes

### `TinyCalendar`

**Description:** A basic calendar tool for agents to keep track of meetings and appointments.

**Inherits:** `TinyTool`

**Attributes:**

- `calendar (dict)`: A dictionary that maps dates to a list of events. Each event is a dictionary with keys:
    - `title (str)`: The title of the event.
    - `description (str)`: A brief description of the event.
    - `owner (str)`: The name of the agent who created the event.
    - `mandatory_attendees (list)`: A list of agent names who must attend the event.
    - `optional_attendees (list)`: A list of agent names who are invited to the event but are not required to attend.
    - `start_time (str)`: The start time of the event.
    - `end_time (str)`: The end time of the event.

**Methods:**

- `__init__(self, owner=None)`: Initializes the calendar tool with a given owner.

- `add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Adds a new event to the calendar.

- `find_events(self, year, month, day, hour=None, minute=None)`: Finds events that occur on a specified date.

- `_process_action(self, agent, action) -> bool`: Processes actions related to the calendar, such as creating new events.

- `actions_definitions_prompt(self) -> str`: Returns a prompt that defines the actions available for the calendar tool.

- `actions_constraints_prompt(self) -> str`: Returns a prompt that defines the constraints for the actions.

## Methods

### `__init__`

```python
def __init__(self, owner=None):
    """
    Инициализирует экземпляр класса TinyCalendar.

    Args:
        owner (str, optional): Имя владельца календаря. По умолчанию None.

    Returns:
        None

    Raises:
        None
    """
    super().__init__("calendar", "A basic calendar tool that allows agents to keep track meetings and appointments.", owner=owner, real_world_side_effects=False)
    
    # maps date to list of events. Each event itself is a dictionary with keys "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time"
    self.calendar = {} 
```

**Purpose**: Initializes the `TinyCalendar` instance, setting up the basic attributes and functionalities.

**Parameters**:

- `owner (str, optional)`: The name of the agent who owns the calendar. Defaults to `None`.

**Returns**:

- `None`

**Raises Exceptions**:

- None


### `add_event`

```python
def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
    """
    Добавляет новое событие в календарь.

    Args:
        date (str): Дата события.
        title (str): Заголовок события.
        description (str, optional): Описание события. По умолчанию None.
        owner (str, optional): Имя владельца события. По умолчанию None.
        mandatory_attendees (list, optional): Список имен агентов, которые должны присутствовать на событии. По умолчанию None.
        optional_attendees (list, optional): Список имен агентов, которые приглашены на событие, но не обязаны присутствовать. По умолчанию None.
        start_time (str, optional): Время начала события. По умолчанию None.
        end_time (str, optional): Время окончания события. По умолчанию None.

    Returns:
        None

    Raises:
        None
    """
    if date not in self.calendar:
        self.calendar[date] = []
    self.calendar[date].append({"title": title, "description": description, "owner": owner, "mandatory_attendees": mandatory_attendees, "optional_attendees": optional_attendees, "start_time": start_time, "end_time": end_time})
```

**Purpose**: Adds a new event to the calendar based on the provided date and event details.

**Parameters**:

- `date (str)`: The date of the event.
- `title (str)`: The title of the event.
- `description (str, optional)`: A description of the event. Defaults to `None`.
- `owner (str, optional)`: The name of the agent who created the event. Defaults to `None`.
- `mandatory_attendees (list, optional)`: A list of agent names who must attend the event. Defaults to `None`.
- `optional_attendees (list, optional)`: A list of agent names who are invited to the event but are not required to attend. Defaults to `None`.
- `start_time (str, optional)`: The start time of the event. Defaults to `None`.
- `end_time (str, optional)`: The end time of the event. Defaults to `None`.

**Returns**:

- `None`

**Raises Exceptions**:

- None


### `find_events`

```python
def find_events(self, year, month, day, hour=None, minute=None):
    # TODO
    pass
```

**Purpose**: Finds events that occur on a specific date or date and time.

**Parameters**:

- `year (int)`: The year of the event.
- `month (int)`: The month of the event.
- `day (int)`: The day of the event.
- `hour (int, optional)`: The hour of the event. Defaults to `None`.
- `minute (int, optional)`: The minute of the event. Defaults to `None`.

**Returns**:

- `list`: A list of events that match the specified date or date and time.

**Raises Exceptions**:

- None


### `_process_action`

```python
def _process_action(self, agent, action) -> bool:
    """
    Обрабатывает действия, связанные с календарем.

    Args:
        agent (Agent): Экземпляр агента, который выполняет действие.
        action (dict): Словарь, описывающий действие.

    Returns:
        bool: True, если действие обработано успешно, False - в противном случае.

    Raises:
        None
    """
    if action['type'] == "CREATE_EVENT" and action['content'] is not None:
        # parse content json
        event_content = json.loads(action['content'])
        
        # checks whether there are any kwargs that are not valid
        valid_keys = ["title", "description", "mandatory_attendees", "optional_attendees", "start_time", "end_time"]
        utils.check_valid_fields(event_content, valid_keys)

        # uses the kwargs to create a new event
        self.add_event(event_content)

        return True

    else:
        return False
```

**Purpose**: Processes actions related to the calendar, such as creating new events.

**Parameters**:

- `agent (Agent)`: The agent who is performing the action.
- `action (dict)`: A dictionary describing the action.

**Returns**:

- `bool`: `True` if the action was processed successfully, `False` otherwise.

**Raises Exceptions**:

- None


### `actions_definitions_prompt`

```python
def actions_definitions_prompt(self) -> str:
    """
    Возвращает подсказку, определяющую действия, доступные для календаря.

    Args:
        None

    Returns:
        str: Подсказка, определяющая действия.

    Raises:
        None
    """
    prompt = \\\
        """
          - CREATE_EVENT: You can create a new event in your calendar. The content of the event has many fields, and you should use a JSON format to specify them. Here are the possible fields:
            * title: The title of the event. Mandatory.
            * description: A brief description of the event. Optional.
            * mandatory_attendees: A list of agent names who must attend the event. Optional.
            * optional_attendees: A list of agent names who are invited to the event, but are not required to attend. Optional.
            * start_time: The start time of the event. Optional.
            * end_time: The end time of the event. Optional.
        """
    # TODO how the atendee list will be handled? How will they be notified of the invitation? I guess they must also have a calendar themselves. <-------------------------------------\
\
    return utils.dedent(prompt)
```

**Purpose**: Returns a prompt that defines the actions available for the calendar tool.

**Parameters**:

- `None`

**Returns**:

- `str`: A prompt defining the actions.

**Raises Exceptions**:

- None


### `actions_constraints_prompt`

```python
def actions_constraints_prompt(self) -> str:
    """
    Возвращает подсказку, определяющую ограничения для действий.

    Args:
        None

    Returns:
        str: Подсказка, определяющая ограничения.

    Raises:
        None
    """
    prompt = \\\
        """
          
        """
        # TODO
\
    return textwrap.dedent(prompt)
```

**Purpose**: Returns a prompt that defines the constraints for the actions.

**Parameters**:

- `None`

**Returns**:

- `str`: A prompt defining the constraints.

**Raises Exceptions**:

- None

## Parameter Details

- `date (str)`: The date of the event in a string format, such as "YYYY-MM-DD".
- `title (str)`: The title of the event, which should be descriptive and concise.
- `description (str, optional)`: A more detailed explanation of the event, providing context and additional information. Defaults to `None`.
- `owner (str, optional)`: The name of the agent who created the event. Defaults to `None`.
- `mandatory_attendees (list, optional)`: A list of agent names who are required to attend the event. Defaults to `None`.
- `optional_attendees (list, optional)`: A list of agent names who are invited to the event but not required to attend. Defaults to `None`.
- `start_time (str, optional)`: The start time of the event in a string format, such as "HH:MM". Defaults to `None`.
- `end_time (str, optional)`: The end time of the event in a string format, such as "HH:MM". Defaults to `None`.
- `year (int)`: The year of the event.
- `month (int)`: The month of the event.
- `day (int)`: The day of the event.
- `hour (int, optional)`: The hour of the event. Defaults to `None`.
- `minute (int, optional)`: The minute of the event. Defaults to `None`.
- `agent (Agent)`: The agent who is performing the action.
- `action (dict)`: A dictionary describing the action, containing keys like `type` and `content`.

## Examples

**Example 1: Creating a new event:**

```python
# Create a calendar instance
calendar = TinyCalendar()

# Add a new event
calendar.add_event(date="2024-02-15", title="Meeting with John", description="Discuss the project proposal", owner="Alice", mandatory_attendees=["John"], start_time="10:00", end_time="11:00")

# Print the calendar
print(calendar.calendar)

# Output: 
# {'2024-02-15': [{'title': 'Meeting with John', 'description': 'Discuss the project proposal', 'owner': 'Alice', 'mandatory_attendees': ['John'], 'optional_attendees': None, 'start_time': '10:00', 'end_time': '11:00'}]}
```

**Example 2: Finding events on a specific date:**

```python
# Find events on February 15th, 2024
events = calendar.find_events(year=2024, month=2, day=15)

# Print the events
print(events)

# Output: 
# [{'title': 'Meeting with John', 'description': 'Discuss the project proposal', 'owner': 'Alice', 'mandatory_attendees': ['John'], 'optional_attendees': None, 'start_time': '10:00', 'end_time': '11:00'}]
```

**Example 3: Processing an action to create a new event:**

```python
# Create an action to create a new event
action = {
    "type": "CREATE_EVENT",
    "content": json.dumps({"title": "Team Brainstorming", "description": "Brainstorming session for the new product", "owner": "Bob", "optional_attendees": ["Alice", "Charlie"], "start_time": "14:00", "end_time": "16:00"})
}

# Process the action
success = calendar._process_action(agent="Bob", action=action)

# Print the result
print(success)

# Output: 
# True
```

**Example 4: Using the actions_definitions_prompt():**

```python
# Get the actions definitions prompt
prompt = calendar.actions_definitions_prompt()

# Print the prompt
print(prompt)

# Output: 
# """
#   - CREATE_EVENT: You can create a new event in your calendar. The content of the event has many fields, and you should use a JSON format to specify them. Here are the possible fields:
#     * title: The title of the event. Mandatory.
#     * description: A brief description of the event. Optional.
#     * mandatory_attendees: A list of agent names who must attend the event. Optional.
#     * optional_attendees: A list of agent names who are invited to the event, but are not required to attend. Optional.
#     * start_time: The start time of the event. Optional.
#     * end_time: The end time of the event. Optional.
# """
```

**Example 5: Using the actions_constraints_prompt():**

```python
# Get the actions constraints prompt
prompt = calendar.actions_constraints_prompt()

# Print the prompt
print(prompt)

# Output: 
# """
# 
# """
```