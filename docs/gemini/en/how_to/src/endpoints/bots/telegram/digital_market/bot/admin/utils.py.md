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
This function is used to delete the last message sent by the user and the current message.

Execution Steps
-------------------------
1. The function retrieves data from the state context, specifically looking for the 'last_msg_id' key.
2. If the 'last_msg_id' is found, the function attempts to delete the corresponding message using the bot object.
3. If the 'last_msg_id' is not found, a warning message is logged.
4. The current message is then deleted using `message.delete()`.
5. The function handles potential errors during the deletion process by logging them with the `logger.error()` method.

Usage Example
-------------------------

```python
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message
    from loguru import logger

    from bot.config import bot

    # Assuming the state context contains the 'last_msg_id'
    async def handle_message(message: Message, state: FSMContext):
        await process_dell_text_msg(message, state)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".