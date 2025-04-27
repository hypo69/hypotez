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
The `TelegramBot` class provides a structure for managing a Telegram bot using FastAPI and RPC. It handles the initialization, webhook setup, default command handlers, and message processing.

Execution Steps
-------------------------
1. **Initialize the bot:** The `__init__` method sets up essential parameters like the token, port, route, configuration, Telegram bot application, and handler.
2. **Register default handlers:** The `_register_default_handlers` method adds standard command handlers for 'start', 'help', 'sendpdf', text messages, voice messages, documents, and logs.
3. **Start the bot:** The `run` method sets up the RPC client and server, initializes the bot webhook, and starts the application.
4. **Handle incoming messages:** The `_handle_message` method processes any incoming text messages using the `bot_handler`.
5. **Initialize the bot webhook:** The `initialize_bot_webhook` method configures the webhook URL using the `gs.host` and specified route, then sets it on the bot.
6. **Register the webhook route via RPC:** The `_register_route_via_rpc` method adds a new route to the RPC server for the Telegram webhook.
7. **Stop the bot:** The `stop` method stops the bot application and deletes the webhook.

Usage Example
-------------------------

```python
from src.endpoints.bots.telegram.telegram_webhooks import TelegramBot

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create a TelegramBot instance
bot = TelegramBot(token=os.getenv('TELEGRAM_TOKEN'))

# Run the bot
bot.run()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".