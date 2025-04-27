# ToolBox_requests Module

## Overview

This module implements the `ToolBox` class, which is responsible for handling requests from Telegram users interacting with the ToolBox bot. The bot utilizes various neural networks, including GPT-4o-mini and FLUX schnell, for processing text and image generation requests.

## Details

This file contains the core logic of the ToolBox bot, which provides users with several functionalities:

- **Text Generation:** Users can choose from different text types, like commercial, SMM, brainstorming, advertising, and more, to generate various text formats.
- **Image Generation:** Users can generate images based on their prompts, with the option to upscale and regenerate them.
- **Free Mode:** Allows users to have free-form conversations and interact with the bot using natural language.
- **Tariffs:** Provides information about the available subscription plans.

## Classes

### `class ToolBox`

**Description:** This class handles all interactions with the Telegram bot, including receiving user requests, processing them, and sending responses.

**Inherits:** 

- `keyboards`: Provides methods for generating Telegram keyboards.
- `neural_networks`: Contains methods for interacting with neural network models.

**Attributes:**

- `name` (`list[str]`): A list of names for the main bot actions (Text, Images, Free mode, Tariffs).
- `data` (`list[str]`): A list of data associated with each action, used for keyboard creation.
- `prompts_text` (`dict`): A dictionary containing prompts and texts used in the bot's responses.
- `bot` (`telebot.TeleBot`): An instance of the Telegram bot.
- `keyboard_blank` (`callable`): A function for generating a blank keyboard with two buttons.
- `reply_keyboard` (`callable`): A function for generating a reply keyboard.
- `__delay` (`callable`): A function for sending a message indicating a delay.
- `start_request` (`callable`): A function for sending the initial welcome message.
- `restart` (`callable`): A function for sending a message to restart the user interaction.
- `restart_markup` (`callable`): A function for editing a message with the restart keyboard.
- `OneTextArea` (`callable`): A function for editing a message with a single text input area.
- `SomeTextsArea` (`callable`): A function for editing a message with an area for multiple texts.
- `ImageSize` (`callable`): A function for editing a message with a keyboard for image size selection.
- `ImageArea` (`callable`): A function for editing a message with an input area for image generation requests.
- `ImageChange` (`callable`): A function for sending a message with a keyboard for image manipulation options.
- `BeforeUpscale` (`callable`): A function for sending a message with a keyboard for image regeneration or upscaling options.
- `FreeArea` (`callable`): A function for sending a message to start free-form conversations.
- `TariffArea` (`callable`): A function for editing a message with a keyboard for tariff selection.
- `TariffExit` (`callable`): A function for sending a message with the tariff keyboard (without the "Ref" button).
- `TarrifEnd` (`callable`): A function for sending a message when the user's paid requests are exhausted.
- `FreeTariffEnd` (`callable`): A function for sending a message when the user's free requests are exhausted.
- `SomeTexts` (`callable`): A function for editing a message with a keyboard for choosing between one or multiple texts.

**Methods:**

- `__gpt_4o_mini(self, prompt: list[dict], message)`: Processes text requests using the GPT-4o-mini model.
    - **Parameters:**
        - `prompt` (`list[dict]`): A list of prompt dictionaries containing the user's request.
        - `message` (`telebot.types.Message`): The Telegram message object.
    - **Returns:**
        - `tuple[dict[str, str], int, int]`: A tuple containing the model's response, incoming tokens, and outgoing tokens.
- `__FLUX_schnell(self, prompt: str, size: list[int], message, seed: int, num_inference_steps: int)`: Processes image generation requests using the FLUX schnell model.
    - **Parameters:**
        - `prompt` (`str`): The user's prompt for image generation.
        - `size` (`list[int]`): The desired image size.
        - `message` (`telebot.types.Message`): The Telegram message object.
        - `seed` (`int`): A random seed for image generation.
        - `num_inference_steps` (`int`): The number of inference steps for the model.
    - **Returns:**
        - `None`: Returns `None` if the process is successful, otherwise raises an exception.
- `Text_types(self, message)`: Presents a keyboard with different text types to the user.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
    - **Returns:**
        - `telebot.types.Message`: The edited message with the text type keyboard.
- `Basic_tariff(self, message)`: Sends an invoice for the BASIC tariff.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
    - **Returns:**
        - `None`: Returns `None` if the process is successful, otherwise raises an exception.
- `Pro_tariff(self, message)`: Sends an invoice for the PRO tariff.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
    - **Returns:**
        - `None`: Returns `None` if the process is successful, otherwise raises an exception.
- `TextCommands(self, message, ind: int)`: Processes text requests from the user based on the selected text type.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
        - `ind` (`int`): The index of the selected text type.
    - **Returns:**
        - `tuple[int, int, int]`: A tuple containing the incoming tokens, outgoing tokens, and the number of processed requests.
- `SomeTextsCommand(self, message, ind: int, tokens: dict[str, int])`: Processes multiple text requests based on the selected text type.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
        - `ind` (`int`): The index of the selected text type.
        - `tokens` (`dict[str, int]`): A dictionary containing the user's remaining tokens and requests.
    - **Returns:**
        - `tuple[int, int, int]`: A tuple containing the incoming tokens, outgoing tokens, and the number of processed requests.
- `ImageCommand(self, message, prompt: str, size: list[int])`: Processes image generation requests.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
        - `prompt` (`str`): The user's prompt for image generation.
        - `size` (`list[int]`): The desired image size.
    - **Returns:**
        - `int`: The random seed used for image generation.
- `Image_Regen_And_Upscale(self, message, prompt: str, size: list[int], seed, num_inference_steps=4)`: Processes image regeneration and upscaling requests.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
        - `prompt` (`str`): The user's prompt for image generation.
        - `size` (`list[int]`): The desired image size.
        - `seed` (`int`): The random seed used for image generation.
        - `num_inference_steps` (`int`): The number of inference steps for the model (default: 4).
    - **Returns:**
        - `None`: Returns `None` if the process is successful, otherwise raises an exception.
- `FreeCommand(self, message, prompts: list[str])`: Processes user requests in free mode.
    - **Parameters:**
        - `message` (`telebot.types.Message`): The Telegram message object.
        - `prompts` (`list[str]`): A list of previous prompts and responses in the conversation.
    - **Returns:**
        - `tuple[int, int, list[str]]`: A tuple containing the incoming tokens, outgoing tokens, and the updated list of prompts and responses.

## Functions

### `__gpt_4o_mini`

**Purpose:** This function handles text generation using the GPT-4o-mini model.

**Parameters:**

- `prompt` (`list[dict]`): A list of prompt dictionaries containing the user's request.
- `message` (`telebot.types.Message`): The Telegram message object.

**Returns:**

- `tuple[dict[str, str], int, int]`: A tuple containing the model's response, incoming tokens, and outgoing tokens.

**Raises Exceptions:**

- `Exception`: If an error occurs during model interaction.

**How the Function Works:**

1. Sends a message to the user indicating a delay.
2. Calls the `_free_gpt_4o_mini` method from the `neural_networks` class to process the prompt using the GPT-4o-mini model.
3. Edits the delay message with the generated response, using the `PromptsCompressor` class to format the text with HTML tags.
4. Returns the model's response, incoming tokens, and outgoing tokens.

### `__FLUX_schnell`

**Purpose:** This function handles image generation using the FLUX schnell model.

**Parameters:**

- `prompt` (`str`): The user's prompt for image generation.
- `size` (`list[int]`): The desired image size.
- `message` (`telebot.types.Message`): The Telegram message object.
- `seed` (`int`): A random seed for image generation.
- `num_inference_steps` (`int`): The number of inference steps for the model.

**Returns:**

- `None`: Returns `None` if the process is successful, otherwise raises an exception.

**How the Function Works:**

1. Sends a message to the user indicating a delay.
2. Attempts to generate an image using the `_FLUX_schnell` method from the `neural_networks` class.
3. If successful, sends the generated image to the user.
4. Deletes the delay message.
5. If an error occurs during image generation, edits the delay message with an error message.

### `Text_types`

**Purpose:** This function presents a keyboard with different text types to the user.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.

**Returns:**

- `telebot.types.Message`: The edited message with the text type keyboard.

**How the Function Works:**

1. Defines a list of text types and their corresponding data values.
2. Uses the `keyboard_blank` function to create a keyboard with the text type options.
3. Edits the message with the generated keyboard.

### `Basic_tariff`

**Purpose:** This function sends an invoice for the BASIC tariff.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.

**Returns:**

- `None`: Returns `None` if the process is successful, otherwise raises an exception.

**How the Function Works:**

1. Creates a Telegram inline keyboard with buttons for subscribing to the BASIC tariff and returning to the tariffs menu.
2. Defines the invoice details, including title, description, price, and currency.
3. Sends the invoice to the user using the `bot.send_invoice` method.

### `Pro_tariff`

**Purpose:** This function sends an invoice for the PRO tariff.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.

**Returns:**

- `None`: Returns `None` if the process is successful, otherwise raises an exception.

**How the Function Works:**

1. Creates a Telegram inline keyboard with buttons for subscribing to the PRO tariff and returning to the tariffs menu.
2. Defines the invoice details, including title, description, price, and currency.
3. Sends the invoice to the user using the `bot.send_invoice` method.

### `TextCommands`

**Purpose:** This function processes text requests from the user based on the selected text type.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.
- `ind` (`int`): The index of the selected text type.

**Returns:**

- `tuple[int, int, int]`: A tuple containing the incoming tokens, outgoing tokens, and the number of processed requests.

**How the Function Works:**

1. Checks if the selected text type requires additional parameters from the user.
2. If parameters are needed, sends a message prompting the user to enter them.
3. Uses the `pc.get_prompt` method to construct a prompt based on the user's input and the selected text type.
4. Calls the `__gpt_4o_mini` function to process the prompt using the GPT-4o-mini model.
5. Sends a message to the user with the generated response.
6. Returns the incoming tokens, outgoing tokens, and the number of processed requests.

### `SomeTextsCommand`

**Purpose:** This function processes multiple text requests based on the selected text type.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.
- `ind` (`int`): The index of the selected text type.
- `tokens` (`dict[str, int]`): A dictionary containing the user's remaining tokens and requests.

**Returns:**

- `tuple[int, int, int]`: A tuple containing the incoming tokens, outgoing tokens, and the number of processed requests.

**How the Function Works:**

1. Prompts the user to enter the number of texts they want to generate.
2. Collects input texts from the user.
3. Uses the `pc.get_prompt` method to construct prompts for each text based on the user's input.
4. Processes each prompt concurrently using a thread pool executor.
5. Updates the user's token count and sends responses for each generated text.
6. Returns the incoming tokens, outgoing tokens, and the number of processed requests.

### `ImageCommand`

**Purpose:** This function processes image generation requests.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.
- `prompt` (`str`): The user's prompt for image generation.
- `size` (`list[int]`): The desired image size.

**Returns:**

- `int`: The random seed used for image generation.

**How the Function Works:**

1. Generates a random seed for image generation.
2. Calls the `__FLUX_schnell` function to generate the image using the FLUX schnell model.
3. Sends the generated image to the user.
4. Presents a keyboard for image manipulation options.
5. Returns the random seed used for image generation.

### `Image_Regen_And_Upscale`

**Purpose:** This function processes image regeneration and upscaling requests.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.
- `prompt` (`str`): The user's prompt for image generation.
- `size` (`list[int]`): The desired image size.
- `seed` (`int`): The random seed used for image generation.
- `num_inference_steps` (`int`): The number of inference steps for the model (default: 4).

**Returns:**

- `None`: Returns `None` if the process is successful, otherwise raises an exception.

**How the Function Works:**

1. Calls the `__FLUX_schnell` function to regenerate or upscale the image based on the user's selection.
2. Sends the updated image to the user.

### `FreeCommand`

**Purpose:** This function processes user requests in free mode.

**Parameters:**

- `message` (`telebot.types.Message`): The Telegram message object.
- `prompts` (`list[str]`): A list of previous prompts and responses in the conversation.

**Returns:**

- `tuple[int, int, list[str]]`: A tuple containing the incoming tokens, outgoing tokens, and the updated list of prompts and responses.

**How the Function Works:**

1. Adds the user's message to the list of prompts.
2. Calls the `__gpt_4o_mini` function to process the conversation history using the GPT-4o-mini model.
3. Appends the model's response to the list of prompts.
4. Returns the incoming tokens, outgoing tokens, and the updated list of prompts and responses.

## Parameter Details

- `message` (`telebot.types.Message`): The Telegram message object containing information about the user's request, such as the chat ID, message ID, and text.
- `prompt` (`str` | `list[dict]`): The user's prompt for text or image generation. For image generation, it's a string. For text generation, it's a list of dictionaries containing the user's request and previous responses.
- `size` (`list[int]`): The desired image size, represented as a list of two integers (width, height).
- `seed` (`int`): A random seed used for image generation, providing a unique starting point for the model.
- `num_inference_steps` (`int`): The number of inference steps for the FLUX schnell model, controlling the image generation process's complexity.
- `ind` (`int`): The index representing the selected text type or other action from the user.
- `tokens` (`dict[str, int]`): A dictionary containing information about the user's remaining tokens and free requests.

## Examples

### Example 1: Text Generation

```python
# User sends a message with a text generation request
message = telebot.types.Message(chat.id=123456789, message_id=1, text="/text_type 1")
# Process the request
incoming_tokens, outgoing_tokens, num_requests = toolbox.TextCommands(message, ind=1)
# Send a response with the generated text
toolbox.bot.send_message(chat_id=message.chat.id, text="Generated text: ...")
```

### Example 2: Image Generation

```python
# User sends a message with an image generation request
message = telebot.types.Message(chat.id=123456789, message_id=1, text="/image_prompt A beautiful sunset over the ocean")
# Process the request
seed = toolbox.ImageCommand(message, prompt="A beautiful sunset over the ocean", size=[576, 1024])
# Send a response with the generated image
toolbox.bot.send_photo(chat_id=message.chat.id, photo=...)
```

### Example 3: Free Mode

```python
# User sends a message in free mode
message = telebot.types.Message(chat.id=123456789, message_id=1, text="Hello, how are you?")
# Process the request
incoming_tokens, outgoing_tokens, prompts = toolbox.FreeCommand(message, prompts=[])
# Send a response to the user
toolbox.bot.send_message(chat_id=message.chat.id, text=prompts[-1]["content"])
```

### Example 4: Tariff Selection

```python
# User sends a message to view tariffs
message = telebot.types.Message(chat.id=123456789, message_id=1, text="/tariffs")
# Edit the message with the tariffs keyboard
toolbox.TariffArea(message)
```

### Example 5: Paying for a Tariff

```python
# User sends a message to subscribe to the BASIC tariff
message = telebot.types.Message(chat.id=123456789, message_id=1, text="/basic_tariff")
# Send an invoice for the BASIC tariff
toolbox.Basic_tariff(message)
```