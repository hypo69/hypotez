# Telegram Bot: Long Polling

## Overview

This module provides a class for interacting with a Telegram bot using long polling. 

The `TelegramBot` class facilitates communication between the bot and users, handling commands, messages, voice messages, and document files. It utilizes long polling to continuously check for updates from the Telegram server.

## Details

The `TelegramBot` class implements the following features:

- **Initialization:**  It takes the Telegram bot token as input during initialization and constructs a `telegram.ext.Application` object for handling updates.
- **Handler Registration:** It registers command handlers for `start`, `help`, and `sendpdf`.  It also registers a message handler for text messages and another handler for voice and document files.
- **Message Handling:** It provides methods for handling various types of messages (text, voice, documents) and executing appropriate actions based on the received message. 
- **Long Polling:** The `TelegramBot` class leverages long polling to continuously check for updates from Telegram, ensuring the bot is always responsive to user interactions.

## Classes

### `TelegramBot`

**Description**: This class represents the Telegram bot interface. It handles communication with the bot and processes incoming updates.

**Attributes**:

- `application`:  An instance of `telegram.ext.Application` for managing bot interactions.
- `handler`:  An instance of `BotHandler` for handling incoming messages and executing commands.
- `_original_message_handler`:  A reference to the original message handler for text messages.

**Methods**:

- `__init__(self, token: str)`: Initializes the Telegram bot with the provided token.
- `register_handlers(self) -> None`: Registers handlers for bot commands and messages.
- `replace_message_handler(self, new_handler: Callable) -> None`:  Replaces the default text message handler with a custom one.
- `start(self, update: Update, context: CallbackContext) -> None`: Handles the `/start` command.

## Class Methods

### `register_handlers`

**Purpose**: This method registers handlers for bot commands and messages, including `start`, `help`, `sendpdf`, and handlers for text messages, voice messages, and documents.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- None

**How the Function Works**:

1. Registers the `/start` command handler using `CommandHandler('start', self.handler.start)`, which calls the `start` method of the `BotHandler` class.
2. Registers the `/help` command handler using `CommandHandler('help', self.handler.help_command)`, which calls the `help_command` method of the `BotHandler` class.
3. Registers the `/sendpdf` command handler using `CommandHandler('sendpdf', self.handler.send_pdf)`, which calls the `send_pdf` method of the `BotHandler` class.
4. Registers a message handler for text messages that are not commands using `MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler.handle_message)`, which calls the `handle_message` method of the `BotHandler` class.
5. Registers a message handler for voice messages using `MessageHandler(filters.VOICE, self.handler.handle_voice)`, which calls the `handle_voice` method of the `BotHandler` class.
6. Registers a message handler for document files using `MessageHandler(filters.Document.ALL, self.handler.handle_document)`, which calls the `handle_document` method of the `BotHandler` class.

**Examples**:

```python
# Registering handlers for the Telegram bot
bot = TelegramBot(token='your_bot_token')
bot.register_handlers()
```

### `replace_message_handler`

**Purpose**: This method allows for replacing the default text message handler with a custom one. This can be used to modify the bot's behavior for handling text messages.

**Parameters**:

- `new_handler (Callable)`: The new handler function for processing messages.

**Returns**:

- None

**Raises Exceptions**:

- None

**How the Function Works**:

1. Removes the existing message handler from the application's handlers.
2. Creates a new message handler using the provided `new_handler` function.
3. Registers the new message handler with the application.

**Examples**:

```python
# Define a custom message handler
def custom_message_handler(update: Update, context: CallbackContext) -> None:
    # Custom logic for handling text messages
    ...

# Replace the default message handler
bot = TelegramBot(token='your_bot_token')
bot.replace_message_handler(custom_message_handler)
```


### `start`

**Purpose**: This method handles the `/start` command, which is typically used to initiate a conversation with the bot.

**Parameters**:

- `update (Update)`:  An instance of `telegram.Update` representing the received update.
- `context (CallbackContext)`:  An instance of `telegram.ext.CallbackContext` for accessing context information related to the update.

**Returns**:

- None

**Raises Exceptions**:

- None

**How the Function Works**:

1. Logs a message indicating that the bot has been started by the user.
2. Sends a welcome message to the user.

**Examples**:

```python
# Handling the /start command
bot = TelegramBot(token='your_bot_token')
bot.application.add_handler(CommandHandler('start', bot.start))
```

## Parameter Details

- `token` (str): The Telegram bot token. This is a unique identifier for your bot obtained from the BotFather on Telegram.
- `update` (Update): An instance of `telegram.Update`, which represents the received update from Telegram. This object contains information about the user, message, and other relevant details.
- `context` (CallbackContext): An instance of `telegram.ext.CallbackContext`, which provides access to context information related to the update. This includes data passed between handlers and other useful information.
- `new_handler (Callable)`: This is a function or callable object that will handle incoming text messages. 

## Examples

**Example 1: Initializing a bot with a token**

```python
# Initializing a Telegram bot with a token
token = 'your_bot_token'
bot = TelegramBot(token)
```

**Example 2: Starting the bot and handling messages**

```python
# Starting the bot
async def main():
    bot = TelegramBot(token='your_bot_token')
    await bot.application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
```

**Example 3: Replacing the default message handler**

```python
# Defining a custom message handler
def custom_message_handler(update: Update, context: CallbackContext) -> None:
    # Custom logic for handling text messages
    message = update.message.text
    await update.message.reply_text(f"You said: {message}")

# Replacing the default handler
bot = TelegramBot(token='your_bot_token')
bot.replace_message_handler(custom_message_handler)

# Starting the bot
async def main():
    await bot.application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
```