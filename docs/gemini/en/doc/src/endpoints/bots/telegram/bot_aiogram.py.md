# Telegram Bot via FastAPI Server Using RPC

## Overview

This module implements a Telegram bot that utilizes a FastAPI server for handling webhook requests. The bot communicates with the FastAPI server via RPC (Remote Procedure Call) for efficient and scalable communication. The module relies on the `aiogram` library for Telegram bot interaction.

## Details

The module's main functionality resides in the `TelegramBot` class, which acts as an interface for interacting with the Telegram bot. The bot is initialized with a Telegram bot token and a webhook route for the FastAPI server. 

This module also sets up an RPC (Remote Procedure Call) connection for communication with the FastAPI server. This connection allows the bot to register routes and start the server remotely.

## Classes

### `TelegramBot`

**Description**: The `TelegramBot` class represents the interface for interacting with the Telegram bot. It handles initialization, webhook setup, and running the bot.

**Inherits**: None

**Attributes**:

- `token`:  The Telegram bot token (str).
- `port`: The port used for the FastAPI server (int).
- `route`: The webhook route for the FastAPI server (str).
- `config`: Configuration settings loaded from a JSON file (SimpleNamespace).
- `bot`: The `aiogram` bot instance (Bot).
- `dp`: The `aiogram` dispatcher instance (Dispatcher).
- `bot_handler`: An instance of `BotHandler` responsible for handling different bot commands and messages (BotHandler).
- `app`: The FastAPI application instance (web.Application).
- `rpc_client`: An instance of `ServerProxy` for RPC communication (ServerProxy).

**Methods**:

- `run()`: Runs the bot, establishes the RPC connection, and sets up the webhook.
- `_register_default_handlers()`: Registers default handlers for bot commands, messages, and media types.
- `_handle_message(message: types.Message)`: Handles text messages sent to the bot.
- `initialize_bot_webhook(route: str)`: Initializes the bot webhook and sets up a secure connection if needed.
- `_register_route_via_rpc(rpc_client: ServerProxy)`: Registers the Telegram webhook route via RPC.
- `stop()`: Stops the bot and deletes the webhook.

**Principle of Operation**:

1. **Initialization**: The `TelegramBot` class is initialized with a bot token and a webhook route. The configuration is loaded from a JSON file and the `aiogram` bot and dispatcher instances are created.
2. **RPC Connection**: An RPC connection is established with the FastAPI server. This connection allows the bot to start the server remotely and register routes.
3. **Webhook Setup**: The bot's webhook is initialized. If the FastAPI server is running on a local machine, a secure connection is established using `ngrok`.
4. **Route Registration**: The Telegram webhook route is registered via RPC on the FastAPI server.
5. **Bot Running**: The bot is run using either polling or webhook-based message handling depending on the server's setup.
6. **Message Handling**: The `BotHandler` instance handles incoming messages and commands, performing actions based on the user's input.
7. **Stopping the Bot**: The `stop()` method shuts down the FastAPI application, disables the bot's webhook, and stops the bot.


## Functions

### `_register_default_handlers()`

**Purpose**: Registers the default handlers for the bot, including commands for start, help, sending PDFs, and handling various message types.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**Inner Functions**: None

**How the Function Works**: 

This function registers various handlers for the Telegram bot using the `aiogram` dispatcher. These handlers cover common bot commands like `/start`, `/help`, `/sendpdf`, and respond to various message types like text, voice notes, documents, and logs. The `bot_handler` instance handles the logic for these handlers.

**Examples**:

```python
# Example usage in the TelegramBot class:
self.dp.message.register(self.bot_handler.start, Command('start'))  # Registers handler for `/start` command
self.dp.message.register(self.bot_handler.help_command, Command('help'))  # Registers handler for `/help` command
```

### `_handle_message(message: types.Message)`

**Purpose**: Handles text messages sent to the bot.

**Parameters**:

- `message`: The Telegram message object (types.Message).

**Returns**: None

**Raises Exceptions**: None

**Inner Functions**: None

**How the Function Works**:

This function is called whenever a text message is received by the bot. It uses the `bot_handler` instance to process the message and send a response to the user.

**Examples**:

```python
# Example usage in the TelegramBot class:
self.dp.message.register(self._handle_message)  # Registers handler for text messages
```

### `initialize_bot_webhook(route: str)`

**Purpose**: Initializes the bot webhook and sets up a secure connection if the FastAPI server is running locally.

**Parameters**:

- `route`: The webhook route for the FastAPI server (str).

**Returns**:

- `str | bool`: The webhook URL if successful, otherwise `False`.

**Raises Exceptions**: None

**Inner Functions**: None

**How the Function Works**:

1. **Route Validation**: Ensures that the route starts with a forward slash ('/') and constructs a full webhook URL.
2. **Local Server Detection**: Checks if the FastAPI server is running on a local machine (`127.0.0.1` or `localhost`).
3. **Secure Connection Setup**: If the server is local, it uses `ngrok` to create a secure tunnel and obtain a public URL for the webhook.
4. **Webhook Setting**: Attempts to set the bot's webhook using the generated or provided URL.
5. **Success/Error Handling**: Logs success or error messages depending on the outcome of the webhook setup process.

**Examples**:

```python
# Example usage in the TelegramBot class:
webhook_url = self.initialize_bot_webhook(self.route)  # Initializes the webhook and sets up a secure connection if needed
```

### `_register_route_via_rpc(rpc_client: ServerProxy)`

**Purpose**: Registers the Telegram webhook route via RPC on the FastAPI server.

**Parameters**:

- `rpc_client`: The RPC client instance (ServerProxy).

**Returns**: None

**Raises Exceptions**: None

**Inner Functions**: None

**How the Function Works**:

This function uses the RPC client to register the Telegram webhook route on the FastAPI server. It ensures that the route is properly formatted and passes the route information to the server for registration.

**Examples**:

```python
# Example usage in the TelegramBot class:
self._register_route_via_rpc(self.rpc_client)  # Registers the webhook route via RPC
```

### `stop()`

**Purpose**: Stops the bot and deletes the webhook.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**Inner Functions**: None

**How the Function Works**:

1. **Application Shutdown**: If the FastAPI application is running, it is shut down and cleaned up.
2. **Webhook Deletion**: Attempts to delete the bot's webhook using the `aiogram` library.
3. **Success/Error Handling**: Logs success or error messages depending on the outcome of the shutdown and webhook deletion processes.

**Examples**:

```python
# Example usage in the TelegramBot class:
bot.stop()  # Stops the bot and deletes the webhook
```


## Parameter Details

- `token`: The Telegram bot token (str).
- `route`: The webhook route for the FastAPI server (str).
- `port`: The port used for the FastAPI server (int).
- `message`: The Telegram message object (types.Message).
- `rpc_client`: The RPC client instance (ServerProxy).

## Examples

**Example 1: Creating a TelegramBot instance and running it**

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot

bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.run() 
```

**Example 2: Handling a text message**

```python
# Inside the `TelegramBot` class
async def _handle_message(self, message: types.Message):
    """Handles text messages sent to the bot."""
    await self.bot_handler.handle_message(message)
```

**Example 3: Registering a default handler**

```python
# Inside the `TelegramBot` class
self.dp.message.register(self.bot_handler.start, Command('start'))  # Registers handler for `/start` command
```

**Example 4: Initializing the bot webhook**

```python
# Inside the `TelegramBot` class
webhook_url = self.initialize_bot_webhook(self.route)  # Initializes the webhook and sets up a secure connection if needed
```

**Example 5: Registering a route via RPC**

```python
# Inside the `TelegramBot` class
self._register_route_via_rpc(self.rpc_client)  # Registers the webhook route via RPC
```

**Example 6: Stopping the bot**

```python
# Inside the `TelegramBot` class
bot.stop()  # Stops the bot and deletes the webhook
```