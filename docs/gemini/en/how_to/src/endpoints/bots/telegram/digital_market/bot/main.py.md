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
This code snippet initializes and runs a Telegram bot. It sets up default commands, handles webhooks, and registers middlewares and routers.

Execution Steps
-------------------------
1. **Import Libraries**: Imports necessary libraries like `aiogram`, `aiohttp`, `loguru`, and configurations from `bot.config`.
2. **Set Default Commands**: Defines a function `set_default_commands` that sets the default command `/start` for the bot.
3. **Startup and Shutdown Functions**: 
    - `on_startup`: Executes upon application startup. Sets default commands, sets the webhook, and sends a message to admins.
    - `on_shutdown`: Executes upon application shutdown. Sends a message to admins and closes the bot session.
4. **Register Middlewares**: Defines a function `register_middlewares` to register database middlewares for request processing.
5. **Register Routers**: Defines a function `register_routers` to include routers for different functionalities (catalog, user, admin).
6. **Create Application**: Defines a function `create_app` to create and configure an `aiohttp` application. It adds routes for different functionalities, sets up the application with the bot and dispatcher, and registers startup and shutdown functions.
7. **Main Function**: 
    - Registers middlewares and routers.
    - Creates an `aiohttp` application.
    - Runs the application on specified host and port.

Usage Example
-------------------------

```python
# Run the bot
if __name__ == "__main__":
    main()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".