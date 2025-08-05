# Telegram Bot via FastAPI and RPC

## Overview

This module implements a Telegram bot that leverages the FastAPI framework and RPC communication for seamless interaction. It encapsulates the bot's functionality into the `TelegramBot` class, enabling a robust and efficient solution.

## Details

The module utilizes the `fastapi` and `telegram.ext` libraries to create a Telegram bot server hosted on FastAPI. Communication with the bot happens through webhook URLs registered using an RPC server. The RPC server is managed by another part of the project.

**Key components of the module:**

1. **`TelegramBot` Class**: The core class responsible for initializing and running the Telegram bot. It handles tasks like:
    - Setting up the Telegram bot application (`self.application`).
    - Defining default handlers for specific commands (`self.handler`).
    - Establishing an RPC connection to the server (`rpc_client`).
    - Registering webhook routes via RPC.
    - Running the bot either in polling mode or webhook mode.

2. **`BotHandler` Class**: This class houses the logic for handling various Telegram events and commands:
    - `start`: Initiates the bot interaction.
    - `help_command`: Provides help information.
    - `sendpdf`: Handles the sending of PDF files.
    - `handle_message`: Processes text messages.
    - `handle_voice`: Handles voice messages.
    - `handle_document`: Handles document uploads.
    - `handle_log`: Handles log messages.

3. **RPC Communication**: The bot interacts with the server through RPC calls. This allows for dynamic route registration, server management, and overall flexibility.

**Module Architecture:**

- The module defines a `TelegramBot` class that encapsulates the core bot functionality.
- It uses a separate `BotHandler` class to handle various events and commands.
- RPC calls are made to a separate server for managing the bot's server and webhook routes.

## Classes

### `TelegramBot`

**Description**:  The main class responsible for initializing and running the Telegram bot.
**Inherits**:  N/A
**Attributes**:
- `token` (str): The Telegram bot token.
- `port` (int): The port for the FastAPI server. Defaults to 443.
- `route` (str): The webhook route for FastAPI. Defaults to `/telegram_webhook`.
- `config` (SimpleNamespace):  Configuration settings loaded from `telegram.json`.
- `application` (Application): The Telegram bot application instance.
- `handler` (BotHandler): The `BotHandler` instance for handling bot events.

**Methods**:

- `run()`: Starts the bot and initializes the RPC and webhook.
- `_register_default_handlers()`: Registers default bot handlers using the `BotHandler` instance.
- `_handle_message(update: Update, context: CallbackContext)`:  Asynchronously handles text messages.
- `initialize_bot_webhook(route: str)`: Sets up the webhook for the bot.
- `_register_route_via_rpc(rpc_client: ServerProxy)`: Registers the Telegram webhook route via RPC.
- `stop()`: Stops the bot and deletes the webhook.

## Functions

### `_register_default_handlers`

**Purpose**: Registers default handlers for specific commands using the `BotHandler` instance.

**Parameters**:

- None

**Returns**:

- None

**How the Function Works**:
-  Adds handlers for the `start`, `help`, `sendpdf`, `handle_message`, `handle_voice`, `handle_document`, and `handle_log` commands.
-  These handlers are defined within the `BotHandler` class, and they are responsible for reacting to various user interactions.

### `_handle_message`

**Purpose**: Asynchronously handles text messages received from the Telegram bot.

**Parameters**:

- `update` (Update): Contains information about the incoming message.
- `context` (CallbackContext): Provides access to the bot's context.

**Returns**:

- None

**How the Function Works**:
-  Uses the `bot_handler` (an instance of `BotHandler`) to handle the incoming text message.
-  Delegates the message processing to the `handle_message` method of the `BotHandler` class.

### `initialize_bot_webhook`

**Purpose**: Initializes the bot webhook, setting up the endpoint where Telegram sends updates.

**Parameters**:

- `route` (str): The URL route for the webhook.

**Returns**:

- str: The full URL of the webhook, or `False` if an error occurs.

**How the Function Works**:
-  Constructs the webhook URL based on the provided `route` and the host address (`gs.host`).
-  If the host is `127.0.0.1` or `localhost`, it uses `pyngrok` to create a public URL for the webhook.
-  Sets the webhook using the `set_webhook` method of the Telegram bot.
-  Logs the success of the operation or any errors that occur during the process.

### `_register_route_via_rpc`

**Purpose**: Registers the Telegram webhook route with the RPC server.

**Parameters**:

- `rpc_client` (ServerProxy): The RPC client connected to the server.

**Returns**:

- None

**How the Function Works**:
-  Uses the RPC client to register the `route` with the server.
-  Logs the success of the operation or any errors that occur during registration.

### `stop`

**Purpose**: Stops the Telegram bot and deletes the webhook.

**Parameters**:

- None

**Returns**:

- None

**How the Function Works**:
-  Stops the bot application using the `stop` method.
-  Deletes the webhook using the `delete_webhook` method.
-  Logs the success of the operation or any errors that occur during the process.

## Example

```python
from src.endpoints.bots.telegram.bot_webhoks import TelegramBot

# Initialize a TelegramBot instance with your bot token and route
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN', route='/telegram_webhook')

# Start the bot
bot.run()

# Stop the bot
bot.stop()
```