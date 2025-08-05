# Module for Auxiliary Classes in Telegram Bot
## Overview

This module contains auxiliary classes used within the `ToolBoxbot-main` Telegram bot. The primary classes include:

- `keyboards`: This class provides functions for creating and managing keyboards for the bot.
- `PromptsCompressor`: This class handles the compression and retrieval of prompts for the bot's responses.

## Details

This module aims to improve the bot's functionality by providing organized and efficient methods for handling keyboards, compressing prompts, and inserting HTML tags into bot responses. It promotes code reusability and enhances the bot's user experience.

## Classes

### `keyboards`

**Description**: This class defines functions for creating and managing keyboards for the bot. It provides methods for generating inline keyboards and reply keyboards, allowing the bot to present interactive menus to users.

**Methods**:

- `_keyboard_two_blank(data: list[str], name: list[str]) -> types.InlineKeyboardMarkup`: Generates an inline keyboard with two columns, where each button has a corresponding `callback_data` value.
- `_reply_keyboard(name: list[str]) -> types.ReplyKeyboardMarkup`: Generates a reply keyboard with buttons specified in the `name` list.

### `PromptsCompressor`

**Description**: This class is responsible for compressing and retrieving prompts used in the bot's responses. It handles prompt formatting and simplifies the process of creating dynamic prompts based on user input.

**Attributes**:

- `commands_size (list[list[str]])`: Stores the structure of prompt commands, defining the expected order of parameters for each command type.

**Methods**:

- `__init__(self)`: Initializes the `PromptsCompressor` instance by defining the `commands_size` attribute.
- `get_prompt(self, info: list[str], ind: int) -> str`: Retrieves a prompt from the `prompts.json` file, replacing placeholders with the provided information.
- `html_tags_insert(response: str) -> str`: Inserts HTML tags into the response text, formatting it for display within the Telegram bot.

## Parameter Details

- `data (list[str])`: A list of data values used to generate `callback_data` for inline keyboard buttons.
- `name (list[str])`: A list of button names for the inline keyboard or reply keyboard.
- `info (list[str])`: A list of information values used to replace placeholders in the prompt.
- `ind (int)`: The index of the prompt command in the `commands_size` list.
- `response (str)`: The text response to be formatted with HTML tags.

## Examples

### Creating Inline Keyboards:

```python
from hypotez.src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.BaseSettings.AuxiliaryClasses import keyboards
keyboard_instance = keyboards()
data = ["data1", "data2", "data3"]
name = ["Name 1", "Name 2", "Name 3"]
inline_keyboard = keyboard_instance._keyboard_two_blank(data, name)
```

### Creating Reply Keyboards:

```python
from hypotez.src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.BaseSettings.AuxiliaryClasses import keyboards
keyboard_instance = keyboards()
button_names = ["Button 1", "Button 2", "Button 3"]
reply_keyboard = keyboard_instance._reply_keyboard(button_names)
```

### Retrieving Prompts:

```python
from hypotez.src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.BaseSettings.AuxiliaryClasses import PromptsCompressor
prompts_compressor = PromptsCompressor()
info = ["topic", "text", "tone", "structure", "length", "extra"]
prompt = prompts_compressor.get_prompt(info, 0)
```

### Inserting HTML Tags:

```python
from hypotez.src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.BaseSettings.AuxiliaryClasses import PromptsCompressor
response = "#### This is a heading\n### This is a subheading\n**Bold text**\n*Italic text*\n```python\nprint('Hello, World!')\n```\n`Code snippet`"
formatted_response = PromptsCompressor.html_tags_insert(response)
```