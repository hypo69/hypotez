# Bot for Telegram using Pyrogram

## Overview

This module provides a basic Telegram bot implementation using the Pyrogram library. The bot is designed to handle simple commands and echo text messages.

## Details

The code defines a Telegram bot that responds to the `/start` command with a greeting message and echoes back any text message it receives, excluding commands. 

The bot is configured using environment variables for Telegram API credentials, including `API_ID`, `API_HASH`, and `BOT_TOKEN`.

The code is primarily used for demonstrating the basic functionality of creating a Telegram bot with Pyrogram.

## Classes

### `Client` 

**Description**:
Represents a Telegram client instance for interacting with the Telegram API.

**Inherits**:
 - `pyrogram.Client`: This class inherits from the `pyrogram.Client` class, which provides the core functionality for interacting with the Telegram API.

**Attributes**:
 - `api_id`: (int): The API ID provided by Telegram.
 - `api_hash`: (str): The API hash provided by Telegram.
 - `bot_token`: (str): The bot token provided by Telegram.

**Methods**:
 - `on_message`: (function): A decorator that defines message handlers for specific types of messages.
 - `run`: (function): Starts the bot and listens for incoming messages.

## Functions

### `start_command`

**Purpose**:
 Handles the `/start` command and sends a greeting message to the user.

**Parameters**:
 - `client`: (pyrogram.Client): The Pyrogram client instance.
 - `message`: (pyrogram.types.Message): The received message object.

**Returns**:
 - `None`: The function does not return any value.

**Raises Exceptions**:
 - `None`: The function does not raise any exceptions.

**How the Function Works**:
 - This function is decorated with `@app.on_message` to handle incoming messages that match the `/start` command.
 - When the `/start` command is received, the function replies to the message with a greeting message using `message.reply_text`.

**Examples**:
```python
>>> from pyrogram import Client, filters
>>> app = Client("my_simple_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

>>> @app.on_message(filters.command("start"))
... def start_command(client, message):
...     message.reply_text("Привет! Я простой бот на Pyrogram.")
```


### `echo_message`

**Purpose**:
 Handles all text messages, excluding commands, and echoes them back to the user.

**Parameters**:
 - `client`: (pyrogram.Client): The Pyrogram client instance.
 - `message`: (pyrogram.types.Message): The received message object.

**Returns**:
 - `None`: The function does not return any value.

**Raises Exceptions**:
 - `None`: The function does not raise any exceptions.

**How the Function Works**:
 - This function is decorated with `@app.on_message` to handle incoming messages that match the `filters.text & ~filters.command` condition.
 - This condition ensures that the function only handles text messages that are not commands.
 - When a text message is received, the function replies to the message with the same text using `message.reply_text`.

**Examples**:
```python
>>> from pyrogram import Client, filters
>>> app = Client("my_simple_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

>>> @app.on_message(filters.text & ~filters.command)
... def echo_message(client, message):
...     message.reply_text(message.text)
```

## Parameter Details

- `client`: (pyrogram.Client): The Pyrogram client instance.
- `message`: (pyrogram.types.Message): The received message object.

## Examples

```python
# Example of a simple Telegram bot using Pyrogram

from pyrogram import Client, filters
import os

# Replace with your own values
API_ID = int(os.environ.get("TELEGRAM_API_ID", ''))
API_HASH = os.environ.get("TELEGRAM_API_HASH", '')
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN", '')

# Create a Pyrogram client instance
app = Client(
    "my_simple_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start command handler
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Привет! Я простой бот на Pyrogram.")

# Text message handler (excluding commands)
@app.on_message(filters.text & ~filters.command)
def echo_message(client, message):
    message.reply_text(message.text)

# Start the bot
if __name__ == "__main__":
    print("Бот запущен...")
    app.run()
```