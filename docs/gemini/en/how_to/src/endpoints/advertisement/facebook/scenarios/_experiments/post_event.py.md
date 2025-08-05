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
This code block is responsible for posting Facebook events to specific groups. It reads event data from JSON files stored in a specified directory structure, processes the data, and sends the corresponding messages to the designated Facebook groups.

Execution Steps
-------------------------
1. The `post_events()` function retrieves a list of event directories from the `events` folder within the 'aliexpress' directory on Google Drive.
2. It iterates through each event directory and reads the corresponding JSON file using `j_loads_ns`.
3. The code initializes a `FacebookPromoter` object, which handles the interaction with Facebook groups.
4. For each event, the `process_groups` method of the `FacebookPromoter` object is called to send the event to the specified groups.
5. The `post_to_my_group()` function is a separate function that can be used to send an event to a specific group defined in the `my_managed_groups.json` file.

Usage Example
-------------------------

```python
    # Get an event from a JSON file
    event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events'  / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')

    # Send the event to all managed groups
    post_events()

    # Send the event to a specific group
    post_to_my_group(event) 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".