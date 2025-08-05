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
This code block defines the `BotHandler` class, responsible for handling messages from Telegram users. It provides methods to process various types of messages, including text, URLs, voice messages, and documents. 

Execution Steps
-------------------------
1. The `__init__` method initializes the scenario, language model, and a list of fallback questions.
2. The `handle_message` method is called when a user sends a message to the bot. It analyzes the message content and routes it to the appropriate handler method.
3. `_send_user_flowchart` method sends a user flowchart diagram to the user.
4. `_handle_url` method processes URLs, extracting data from the OneTab service and starting the scenario execution.
5. `_handle_next_command` method handles the `--next` command, asking a random question and providing an answer from the language model.
6. `help_command` method displays the list of available commands.
7. `send_pdf` method handles the `/sendpdf` command, sending a PDF file to the user.
8. `handle_voice` method processes voice messages, transcribing them into text (currently a placeholder function).
9. `handle_document` method handles document messages, saving them to a temporary location.

Usage Example
-------------------------

```python
    # Initialize a BotHandler object
    handler = BotHandler()
    
    # Process a text message:
    message = telebot.types.Message(text='Hello, world!') 
    handler.handle_message(bot, message) 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".