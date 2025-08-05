**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
The `TinyCalendar` class provides a basic calendar tool for agents to manage meetings and appointments. It uses a dictionary to store events by date, with each event represented as a dictionary containing details like title, description, attendees, and time.

Execution Steps
-------------------------
1. **Initialization:** The `__init__` method initializes the calendar tool, setting up an empty dictionary to store events and defining its purpose.
2. **Adding Events:** The `add_event` method allows agents to add new events to the calendar. It checks if the date already exists in the dictionary and appends the event details to the corresponding date.
3. **Finding Events:** The `find_events` method is intended to retrieve events based on specific criteria like date, time, and possibly attendees. It is currently not fully implemented.
4. **Processing Actions:** The `_process_action` method handles user actions related to the calendar. Currently, it only supports the `CREATE_EVENT` action, which parses event content from a JSON string and adds the event to the calendar.
5. **Action Definitions Prompt:** The `actions_definitions_prompt` method generates a text prompt that describes available actions for the calendar, including `CREATE_EVENT` and its required fields. 
6. **Action Constraints Prompt:** The `actions_constraints_prompt` method is intended to generate a prompt outlining constraints or rules for calendar actions but is not yet fully implemented.

Usage Example
-------------------------

```python
    # Create a TinyCalendar instance
    calendar = TinyCalendar()

    # Add an event
    event_data = {
        "title": "Meeting with Team",
        "description": "Discuss project updates",
        "mandatory_attendees": ["Agent A", "Agent B"],
        "start_time": "10:00 AM",
        "end_time": "11:00 AM"
    }
    calendar.add_event("2024-03-15", **event_data)

    # Process a CREATE_EVENT action
    action = {
        "type": "CREATE_EVENT",
        "content": json.dumps(event_data) 
    }
    calendar._process_action(agent, action) 

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".