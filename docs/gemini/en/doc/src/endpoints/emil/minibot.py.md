# Emil Mini-Bot Documentation

## Overview

This module implements a simple Telegram bot designed to handle requests for emil-design.com. The bot utilizes a  Google Gemini AI model to process user input and respond appropriately.

## Details

The `minibot` module implements a Telegram bot that interacts with users and provides responses based on user input and predefined scenarios. 

The bot's functionality includes:

- **User Flowchart Display**: The bot can send a user flowchart image to guide users through the process. 
- **OneTab URL Parsing**: When a user sends a valid OneTab URL, the bot fetches data from the URL, including the product price and name, and extracts a list of component URLs.
- **Scenario Execution**: The bot then runs a predefined scenario, using the extracted information to guide the user through a series of interactions, potentially including generating product descriptions, performing product searches, etc.
- **Chat-Based Responses**: For general text input, the bot utilizes a Google Gemini AI model to generate relevant responses.
- **Help Command**: The bot provides a `/help` command to display available commands and their functionalities.
- **File Handling**: The bot can handle voice messages and documents, transcribing voice messages and saving documents to a temporary directory.

The bot is configured using environment variables.  It interacts with the Telegram API using the `telebot` library, and uses Google Gemini for natural language processing tasks.

## Classes

### `BotHandler`

**Description**: 
    Handles the processing of Telegram bot commands and messages. 

**Attributes**: 
    - `base_dir (Path)`: The base directory for the bot's assets. 
    - `scenario (Scenario)`: An instance of the `Scenario` class, representing a predefined scenario.
    - `model (GoogleGenerativeAi)`: An instance of the `GoogleGenerativeAi` class, representing the Google Gemini AI model.
    - `questions_list (list)`: A list of questions that the bot can ask users.

**Methods**: 
    - `handle_message(bot, message)`: Handles incoming text messages from the Telegram bot.
    - `_send_user_flowchart(bot, chat_id)`: Sends the user flowchart image to the specified chat ID.
    - `_handle_url(bot, message)`: Processes URL messages, extracting data from OneTab URLs.
    - `_handle_next_command(bot, message)`: Handles commands to advance the scenario (e.g., '--next', '-next', etc.).
    - `help_command(bot, message)`: Provides information about available commands.
    - `send_pdf(bot, message, pdf_file)`: Sends a PDF file to the user.
    - `handle_voice(bot, message)`: Processes voice messages.
    - `_transcribe_voice(file_path)`: Transcribes a voice message (placeholder function).
    - `handle_document(bot, message)`: Processes documents.


### `Config`

**Description**: 
    Configuration class for the Telegram bot. Defines essential bot settings such as the bot token, channel ID, and default messages. 

**Attributes**: 
    - `BOT_TOKEN (str)`: The Telegram bot token.
    - `CHANNEL_ID (str)`: The Telegram channel ID for the bot.
    - `PHOTO_DIR (Path)`: The directory containing bot photos.
    - `COMMAND_INFO (str)`: A message describing the bot's capabilities.
    - `UNKNOWN_COMMAND_MESSAGE (str)`: A message to send for unknown commands.
    - `START_MESSAGE (str)`: A welcome message sent when the bot is started.
    - `HELP_MESSAGE (str)`: A message displaying the bot's help information.

## Functions

### `command_start(message)`

**Purpose**:
    Handles the `/start` command, sending a welcome message to the user.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the `/start` command.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the command_start function
    message = telebot.types.Message(text='/start', chat={'id': 123456789})
    command_start(message)
    ```

### `command_help(message)`

**Purpose**:
    Handles the `/help` command, sending the bot's help information to the user.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the `/help` command.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the command_help function
    message = telebot.types.Message(text='/help', chat={'id': 123456789})
    command_help(message)
    ```

### `command_info(message)`

**Purpose**:
    Handles the `/info` command, sending a message describing the bot's capabilities to the user.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the `/info` command.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the command_info function
    message = telebot.types.Message(text='/info', chat={'id': 123456789})
    command_info(message)
    ```

### `command_time(message)`

**Purpose**:
    Handles the `/time` command, sending the current time to the user.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the `/time` command.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the command_time function
    message = telebot.types.Message(text='/time', chat={'id': 123456789})
    command_time(message)
    ```

### `command_photo(message)`

**Purpose**:
    Handles the `/photo` command, sending a random photo from the bot's photo directory to the user.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the `/photo` command.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the command_photo function
    message = telebot.types.Message(text='/photo', chat={'id': 123456789})
    command_photo(message)
    ```

### `handle_voice_message(message)`

**Purpose**:
    Handles voice messages received from the user, transcribing the voice message and sending the transcribed text back.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the voice message.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the handle_voice_message function
    message = telebot.types.Message(voice={'file_id': 'voice_file_id'}, chat={'id': 123456789})
    handle_voice_message(message)
    ```

### `handle_document_message(message)`

**Purpose**:
    Handles document messages received from the user, saving the document to a temporary directory and sending a confirmation message.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the document message.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the handle_document_message function
    message = telebot.types.Message(document={'file_id': 'document_file_id'}, chat={'id': 123456789})
    handle_document_message(message)
    ```

### `handle_text_message(message)`

**Purpose**:
    Handles text messages received from the user, forwarding the message to the `handle_message` function in the `BotHandler` class for further processing.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the text message.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the handle_text_message function
    message = telebot.types.Message(text='Hello world', chat={'id': 123456789})
    handle_text_message(message)
    ```

### `handle_unknown_command(message)`

**Purpose**:
    Handles unknown commands received from the user, sending a message indicating the command was not recognized.

**Parameters**: 
    - `message (message)`: The Telegram message object containing the unknown command.

**Returns**:
    None

**Raises Exceptions**:
    None

**Example**:
    ```python
    # Example of calling the handle_unknown_command function
    message = telebot.types.Message(text='/unknown_command', chat={'id': 123456789})
    handle_unknown_command(message)
    ```

## Inner Functions

### `BotHandler._send_user_flowchart(bot, chat_id)`

**Purpose**: 
    Sends the user flowchart image to the specified chat ID. 

**Parameters**: 
    - `bot (telebot)`: The Telegram bot instance.
    - `chat_id (int)`: The chat ID to send the image to. 

**Returns**: 
    None

**Raises Exceptions**: 
    - `FileNotFoundError`: If the user flowchart image file is not found.

### `BotHandler._handle_url(bot, message)`

**Purpose**: 
    Parses URL messages, extracting data from OneTab URLs. 

**Parameters**: 
    - `bot (telebot)`: The Telegram bot instance.
    - `message (message)`: The Telegram message object containing the URL.

**Returns**: 
    None

**Raises Exceptions**: 
    - `Exception`: If an error occurs while fetching data from OneTab.

### `BotHandler._handle_next_command(bot, message)`

**Purpose**: 
    Handles commands to advance the scenario (e.g., '--next', '-next', etc.). 

**Parameters**: 
    - `bot (telebot)`: The Telegram bot instance.
    - `message (message)`: The Telegram message object containing the command.

**Returns**: 
    None

**Raises Exceptions**: 
    - `Exception`: If an error occurs while processing the command.

### `BotHandler._transcribe_voice(file_path)`

**Purpose**: 
    Transcribes a voice message (placeholder function).

**Parameters**: 
    - `file_path (str)`: The path to the voice message file.

**Returns**: 
    - `str`:  The transcribed text.

**Raises Exceptions**: 
    None 

## Parameter Details

- `bot (telebot)`: An instance of the `telebot` library, used for interacting with the Telegram API.
- `message (message)`: A Telegram message object, containing information about the user's input (text, voice, document, etc.).
- `chat_id (int)`: The unique identifier of the chat session with the user.
- `url (str)`: A URL string, typically provided by the user.
- `pdf_file (str)`: The path to a PDF file to be sent to the user.
- `file_path (str)`: The path to a file (e.g., a voice message or document).
- `text (str)`: A string containing the user's text message.


## Examples

**Example 1:  Sending a photo to a user using the `/photo` command.**

```python
# Example of calling the command_photo function
message = telebot.types.Message(text='/photo', chat={'id': 123456789})
command_photo(message)
```

**Example 2:  Handling a voice message from a user.**

```python
# Example of calling the handle_voice_message function
message = telebot.types.Message(voice={'file_id': 'voice_file_id'}, chat={'id': 123456789})
handle_voice_message(message)
```

**Example 3:  Handling a text message from a user.**

```python
# Example of calling the handle_text_message function
message = telebot.types.Message(text='Hello world', chat={'id': 123456789})
handle_text_message(message)
```

**Example 4:  Handling an unknown command from a user.**

```python
# Example of calling the handle_unknown_command function
message = telebot.types.Message(text='/unknown_command', chat={'id': 123456789})
handle_unknown_command(message)
```

**Example 5:  Sending a user flowchart to a user.**

```python
# Example of calling the _send_user_flowchart function
bot = telebot.TeleBot('YOUR_BOT_TOKEN') # Replace with your actual token
chat_id = 123456789
handler = BotHandler()
handler._send_user_flowchart(bot, chat_id)
```

**Example 6:  Parsing a OneTab URL and running a scenario.**

```python
# Example of calling the _handle_url function
bot = telebot.TeleBot('YOUR_BOT_TOKEN') # Replace with your actual token
message = telebot.types.Message(text='https://one-tab.com/123456789', chat={'id': 123456789})
handler = BotHandler()
handler._handle_url(bot, message)
```

**Example 7:  Handling a command to advance the scenario.**

```python
# Example of calling the _handle_next_command function
bot = telebot.TeleBot('YOUR_BOT_TOKEN') # Replace with your actual token
message = telebot.types.Message(text='--next', chat={'id': 123456789})
handler = BotHandler()
handler._handle_next_command(bot, message)
```