# Module `bot_long_polling.py`

## Overview

The `bot_long_polling.py` module implements a Telegram bot using long polling to listen for updates. It includes functionalities to handle commands, text messages, voice messages, and documents. The bot uses a separate `BotHandler` class to manage command and message processing logic.

## More details

This module sets up the Telegram bot, registers command handlers, and message handlers for various types of incoming data. It initializes the `BotHandler` and integrates it with the bot to manage different commands and message types. The module also includes functionalities for speech recognition, text-to-speech conversion, and file processing.
It can be used to replace the current message handler with a new one. This is useful for dynamically changing the bot's behavior based on context or user input.

## Classes

### `TelegramBot`

**Description**: Represents the Telegram bot interface.

**Attributes**:
- `application` (Application): The Telegram bot application instance.
- `handler` (BotHandler): An instance of the `BotHandler` class for handling commands and messages.
- `_original_message_handler` (MessageHandler): ссылка на исходный обработчик сообщений для последующей замены.

**Working principle**:
The `TelegramBot` class is initialized with a bot token, sets up the bot application, registers command and message handlers, and manages the bot's interaction with the Telegram API. It also provides method for replacing message handlers.

**Methods**:
- `__init__`: Initializes the Telegram bot.
- `register_handlers`: Registers bot commands and message handlers.
- `start`: Handles the `/start` command.
- `replace_message_handler`: Replaces the current text message handler with a new one.

## Class Methods

### `__init__`

```python
def __init__(self, token: str):
    """Инициализирует Telegram-бота.

    Args:
        token (str): Telegram bot token, e.g., `gs.credentials.telegram.bot.kazarinov`.
    """
    ...
```

**Purpose**: Initializes the `TelegramBot` instance with a bot token.

**Parameters**:
- `token` (str): The Telegram bot token.

**How the function works**:
The function initializes the Telegram bot application with the provided token, creates an instance of `BotHandler`, and registers the command and message handlers.

### `register_handlers`

```python
def register_handlers(self) -> None:
    """Регистрирует команды бота и обработчики сообщений."""
    ...
```

**Purpose**: Registers the command and message handlers for the Telegram bot.

**How the function works**:
The function registers command handlers for `/start`, `/help`, and `/sendpdf` commands. It also registers message handlers for text messages (excluding commands), voice messages, and documents.

### `replace_message_handler`

```python
def replace_message_handler(self, new_handler: Callable) -> None:
    """
    Заменяет текущий обработчик текстовых сообщений на новый.

    Args:
        new_handler (Callable): Новая функция для обработки сообщений.
    """
    ...
```

**Purpose**: Replaces the current text message handler with a new handler.

**Parameters**:
- `new_handler` (Callable): The new message handler function.

**How the function works**:
The function removes the old message handler, creates a new message handler with the provided function, and registers the new handler.

### `start`

```python
async def start(self, update: Update, context: CallbackContext) -> None:
    """Обрабатывает команду /start."""
    ...
```

**Purpose**: Handles the `/start` command.

**Parameters**:
- `update` (Update): The update object from Telegram.
- `context` (CallbackContext): The context object for the handler.

**How the function works**:
The function logs the start event and sends a welcome message to the user.

## Examples

**Creating and initializing a Telegram bot**:

```python
from src.endpoints.bots.telegram.bot_long_polling import TelegramBot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = TelegramBot(token='YOUR_BOT_TOKEN')