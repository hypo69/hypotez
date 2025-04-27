**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `TelegramBot` Class
=========================================================================================

Description
-------------------------
The `TelegramBot` class represents a Telegram bot interface that interacts with a FastAPI server through RPC. It manages the bot's initialization, webhook setup, handling incoming messages, and graceful shutdown. 

Execution Steps
-------------------------
1. **Initialization**: The `__init__` method initializes the bot with a Telegram token and a webhook route. It also loads the bot's configuration from a JSON file.
2. **RPC Setup**: The `run` method establishes an RPC connection to a server. The server is started using the `start_server` method, and the bot's webhook route is registered via RPC.
3. **Webhook Setup**: The `initialize_bot_webhook` method sets up a webhook for the Telegram bot. It uses a publicly accessible URL for the webhook, which may be provided by a service like ngrok.
4. **Message Handling**:  Default handlers are registered to handle various types of messages, including command messages, voice messages, documents, and text messages.
5. **Graceful Shutdown**: The `stop` method closes the bot's web application, deletes the webhook, and terminates the RPC connection.

Usage Example
-------------------------

```python
from dotenv import load_dotenv
from hypotez.src.endpoints.bots.telegram.bot_aiogram import TelegramBot

load_dotenv()
bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
bot.run() 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".