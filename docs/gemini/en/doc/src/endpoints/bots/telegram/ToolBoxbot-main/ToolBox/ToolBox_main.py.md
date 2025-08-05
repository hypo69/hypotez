# Telegram Bot Main Script

## Overview

This script is the main file for the Telegram bot, handling user interactions and managing bot functionalities. It uses the `telebot` library for Telegram API interaction, `ToolBox_requests` for bot commands, and `ToolBox_DataBase` for user data storage. The script includes functions for handling bot commands, processing payment requests, managing user profiles, and interacting with the user via text messages and images.

## Details

The bot utilizes a user-centric approach, storing and updating user data in a SQLite database. It provides various functionalities, including text generation, image generation, and subscription management. The bot's behavior is primarily driven by user commands, callback queries, and text messages.  

**Key Components:**

- **User Data Management:** The script maintains a database (`db`) containing user information, including subscription status, usage details, and recent interactions. 
- **Command Handling:** The bot responds to commands like `/start`, `/profile`, and `/stat` with appropriate actions based on the user's data.
- **Payment Processing:** The script processes payment requests for basic and PRO subscriptions, updating user data accordingly.
- **Text Generation:** The bot allows users to generate different types of text, such as social media content, advertising copy, and SEO text.
- **Image Generation:** Users with a PRO subscription can generate images.
- **Free Mode:** The bot provides a limited free mode with daily text generation limits.
- **Subscription Management:** The script handles user subscription changes, activating PRO subscriptions and updating user data.
- **Promo Codes:** The script allows users to redeem promo codes for PRO subscriptions.

## Classes

### `ToolBox`

**Description**: This class is used for handling various functions related to the bot, including user interactions, command execution, and data storage.

**Attributes**:

- `bot`: The `telebot` object, representing the Telegram bot instance.
- `data`: A dictionary containing data for callback queries.

**Methods**:

- `start_request(message)`: Displays the initial menu to the user.
- `Text_types(message)`: Presents a selection of text types for generation.
- `ImageSize(message)`: Offers image size options for PRO users.
- `FreeArea(message)`: Provides the free mode area for users.
- `TariffArea(message)`: Displays options for subscriptions.
- `ImageArea(message)`: Handles image generation requests.
- `Image_Regen_And_Upscale(message, prompt, size, seed, upscale_ratio=None)`: Generates, regenerates, and upscales images.
- `Basic_tariff(message)`: Handles the BASIC subscription request.
- `Pro_tariff(message)`: Handles the PRO subscription request.
- `SomeTexts(message, i)`: Presents a list of texts for specific purposes.
- `OneTextArea(message, i)`: Provides a single text field for specific purposes.
- `SomeTextsArea(message, i)`: Handles text generation requests for multiple purposes.
- `FreeCommand(message, sessions_messages)`: Processes text generation in free mode.
- `TextCommands(message, i)`: Processes text generation requests for specific types.
- `SomeTextsCommand(message, i, tokens)`: Processes text generation requests for multiple purposes.
- `FreeTariffEnd(message)`: Informs the user about the end of the free mode.
- `TarrifEnd(message)`: Informs the user about the end of their paid subscription.
- `ImageCommand(message, prompt, size)`: Generates an image based on user input.
- `restart_markup(message)`: Clears the keyboard and returns the user to the main menu.
- `TariffExit(message)`: Exits the subscription selection area.
- `restart(message)`: Resets the bot's state and returns to the main menu.

## Functions

### `generate_promo_code(length)`

**Purpose**: Generates a random promo code with a specified length.

**Parameters**:

- `length`: The desired length of the promo code.

**Returns**:

- `str`: The generated promo code.

**How the Function Works**:

The function generates a random string of characters using the specified length. It includes lowercase letters, uppercase letters, and digits.

**Examples**:

```python
>>> generate_promo_code(10)
'g4bT3hV5k2'
```

### `DATA_PATTERN`

**Purpose**: Creates a dictionary representing user data.

**Parameters**:

- `text`: A list representing the user's text generation preferences.
- `sessions_messages`: A list containing the conversation history.
- `some`: A boolean indicating whether the user wants to generate text for multiple purposes.
- `images`: A string representing the user's image generation preferences.
- `free`: A boolean indicating whether the user is in free mode.
- `basic`: A boolean indicating whether the user has a BASIC subscription.
- `pro`: A boolean indicating whether the user has a PRO subscription.
- `incoming_tokens`: The number of incoming tokens available to the user.
- `outgoing_tokens`: The number of outgoing tokens available to the user.
- `free_requests`: The number of free text generation requests available to the user.
- `datetime_sub`: The date and time of the user's subscription expiration.
- `promocode`: A boolean indicating whether the user has redeemed a promo code.
- `ref`: The user's referral code.

**Returns**:

- `dict`: A dictionary containing the user's data.

### `TokensCancelletionPattern(user_id: str, func, message, i: int = None)`

**Purpose**: Handles token consumption and user data updates during text generation.

**Parameters**:

- `user_id`: The unique ID of the user.
- `func`: The function to be executed for text generation.
- `message`: The user's message containing the text generation request.
- `i`: The index of the text type being generated.

**Returns**:

- `None`

**How the Function Works**:

This function checks the user's token balance and free requests, deducting tokens or decreasing free requests as necessary based on the type of text generation. It then calls the `func` to execute the text generation process and updates the user's data accordingly.

### `end_check_tariff_time()`

**Purpose**: Periodically checks user subscription expiration and updates user data accordingly.

**Parameters**:

- None

**Returns**:

- `None`

**How the Function Works**:

This function runs asynchronously, checking the subscription expiration date of each user. If a user's subscription has expired, it updates their data to reflect free mode or disables their subscription privileges.

## Inner Functions

### `get_promo_code(message)`

**Purpose**: Processes user input for promo code redemption.

**Parameters**:

- `message`: The user's message containing the promo code.

**Returns**:

- `None`

**How the Function Works**:

This function validates the user's input, checking if the promo code is "free24" or matches the user's referral code. If valid, it activates the PRO subscription and updates user data.

## Parameter Details

- `user_id`: A string representing the unique ID of the user.
- `message`: A `telebot` message object containing the user's request or interaction.
- `i`: An integer index representing the specific type of text generation or task.
- `func`: A function that performs the actual text generation or task based on user requests.
- `sessions_messages`: A list containing the history of messages exchanged between the user and the bot during a specific conversation.
- `tokens`: A dictionary containing the user's token balance.

## Examples

**Example of `start_request(message)`**:

```python
>>> from ToolBox import ToolBox
>>> tb = ToolBox()
>>> message = # a telebot message object
>>> tb.start_request(message) # Displays the initial menu
```

**Example of `TextCommands(message, i)`**:

```python
>>> from ToolBox import ToolBox
>>> tb = ToolBox()
>>> message = # a telebot message object
>>> i = 1 # index of the text type
>>> tb.TextCommands(message, i) # Processes the text generation request
```

**Example of `generate_promo_code(length)`**:

```python
>>> generate_promo_code(10)
'g4bT3hV5k2'
```