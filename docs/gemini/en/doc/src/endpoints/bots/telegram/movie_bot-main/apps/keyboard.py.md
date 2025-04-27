# Keyboard Module

## Overview

This module defines keyboard layouts used in the Telegram movie bot. The keyboards are built using `InlineKeyboardMarkup` from the `aiogram` library, which allows for interactive buttons within messages.

## Details

This module is a part of the Telegram movie bot's functionality. It provides two main keyboard layouts:

- `find_movie`: This keyboard has a single button labeled "Найти" (Find), which triggers the search functionality in the bot.
- `choice`: This keyboard offers two buttons: "Сериал" (Series) and "Фильм" (Movie), allowing users to choose the type of content they're looking for. 

These keyboards are used to guide the user through the bot's interface, providing interactive options for navigation and data selection.


## Classes

### `InlineKeyboardButton` 

**Description**: Represents a single button within an inline keyboard.

**Inherits**: Inherits from `InlineKeyboardButton` class provided by `aiogram`.

**Attributes**:

- `text`: The text displayed on the button.
- `callback_data`: The data sent back to the bot when the button is pressed.

**Methods**: 

- `__init__(self, text: str, callback_data: str)`:  Initializes a new `InlineKeyboardButton` object with the given text and callback data.

### `InlineKeyboardMarkup`

**Description**: Represents a collection of buttons organized into a keyboard layout.

**Inherits**: Inherits from `InlineKeyboardMarkup` class provided by `aiogram`.

**Attributes**:

- `inline_keyboard`: A list of rows, where each row is a list of `InlineKeyboardButton` objects.

**Methods**: 

- `__init__(self, inline_keyboard: list)`: Initializes a new `InlineKeyboardMarkup` object with the provided layout.

## Functions 

### `find_movie`

**Purpose**: Creates an inline keyboard with a single "Найти" (Find) button, which triggers the search functionality.

**Parameters**: None

**Returns**: `InlineKeyboardMarkup`: The keyboard layout.

**Example**:

```python
from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.keyboard import find_movie

keyboard = find_movie()
# ... Use the keyboard to send a message to the user
```

### `choice` 

**Purpose**: Creates an inline keyboard with two buttons: "Сериал" (Series) and "Фильм" (Movie), allowing users to choose the type of content they're looking for.

**Parameters**: None

**Returns**: `InlineKeyboardMarkup`: The keyboard layout.

**Example**:

```python
from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.keyboard import choice

keyboard = choice()
# ... Use the keyboard to send a message to the user
```

## Parameter Details

- `text` (str): The text displayed on the button.
- `callback_data` (str): The data sent back to the bot when the button is pressed.
- `inline_keyboard`: A list of rows, where each row is a list of `InlineKeyboardButton` objects.


## Examples

**Example 1: Using `find_movie` keyboard**

```python
from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.keyboard import find_movie
from aiogram import Bot, Dispatcher, types

bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Найти фильм или сериал?', reply_markup=find_movie())

if __name__ == '__main__':
    dp.run_polling()
```

**Example 2: Using `choice` keyboard**

```python
from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.keyboard import choice
from aiogram import Bot, Dispatcher, types

bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Выберите тип контента:', reply_markup=choice())

if __name__ == '__main__':
    dp.run_polling()
```