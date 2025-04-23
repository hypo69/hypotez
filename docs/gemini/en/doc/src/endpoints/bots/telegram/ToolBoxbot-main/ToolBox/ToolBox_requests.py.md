# Module ToolBox_requests.py

## Overview

This module defines the `ToolBox` class, which encapsulates the main functions for interacting with a Telegram bot. It includes methods for processing text and image generation requests, managing tariffs, and handling user interactions through the bot. The class inherits from `keyboards` and `neural_networks` classes, providing additional functionality for creating keyboards and working with neural networks.

## More details

The `ToolBox` class integrates various functionalities required for a Telegram bot that provides text and image generation services. It handles user requests, interacts with neural networks for content generation, manages user tariffs, and provides a user-friendly interface through Telegram bot commands and keyboards. The class leverages helper functions for tasks such as delaying responses, constructing prompts, and interacting with external services. It also includes error handling to manage potential issues during content generation.

## Classes

### `ToolBox`

**Description**: This class encapsulates the main functions for interacting with a Telegram bot.
**Inherits**:
- `keyboards`: Provides methods for creating and managing keyboards for user interaction.
- `neural_networks`: Provides methods for interacting with neural networks for content generation.

**Attributes**:
- `name` (list): List of start button names.
- `data` (list): List of start button data.
- `prompts_text` (dict): Dictionary containing prompts for different actions.
- `bot` (telebot.TeleBot): Telegram bot instance.
- `keyboard_blank` (function): Lambda function for creating inline keyboards.
- `reply_keyboard` (function): Lambda function for creating reply keyboards.
- `__delay` (function): Lambda function for sending a "please wait" message.
- `start_request` (function): Lambda function for handling the start command.
- `restart` (function): Lambda function for restarting the bot.
- `restart_markup` (function): Lambda function for restarting the bot with markup.
- `OneTextArea` (function): Lambda function for handling single text requests.
- `SomeTextsArea` (function): Lambda function for handling multiple text requests.
- `ImageSize` (function): Lambda function for selecting image size.
- `ImageArea` (function): Lambda function for handling image requests.
- `ImageChange` (function): Lambda function for handling image change options.
- `BeforeUpscale` (function): Lambda function for displaying options before upscaling.
- `FreeArea` (function): Lambda function for handling free mode requests.
- `TariffArea` (function): Lambda function for handling tariff requests.
- `TariffExit` (function): Lambda function for exiting the tariff area.
- `TarrifEnd` (function): Lambda function for handling tariff end messages.
- `FreeTariffEnd` (function): Lambda function for handling free tariff end messages.
- `SomeTexts` (function): Lambda function for selecting one or multiple texts.

**Working principle**:
The `ToolBox` class initializes with predefined names, data, and prompts. It sets up the Telegram bot with a token from environment variables and defines various lambda functions for handling different user interactions. These lambda functions send messages, edit messages, and display keyboards to guide users through the bot's functionalities. The class also includes methods for interacting with neural networks, processing text and image generation requests, and managing user tariffs.

**Methods**:
- `__gpt_4o_mini`: Processes text generation using the GPT-4o mini model.
- `__FLUX_schnell`: Processes image generation using the FLUX schnell model.
- `Text_types`: Displays text types for selection.
- `Basic_tariff`: Handles the purchase of the basic tariff.
- `Pro_tariff`: Handles the purchase of the pro tariff.
- `TextCommands`: Processes text commands based on user input.
- `SomeTextsCommand`: Processes multiple text commands based on user input.
- `ImageCommand`: Processes image generation commands.
- `Image_Regen_And_Upscale`: Processes image regeneration and upscaling.
- `FreeCommand`: Processes free mode commands.

## Class Methods

### `__gpt_4o_mini`

```python
def __gpt_4o_mini(self, prompt: list[dict], message) -> tuple[dict[str, str], int, int]:
    """ Processes text generation using the GPT-4o mini model.
    Args:
        prompt (list[dict]): List of dictionaries containing the prompt for the model.
        message: Telegram message object.

    Returns:
        tuple[dict[str, str], int, int]: A tuple containing the response from the model, incoming tokens, and outgoing tokens.
    """
    ...
```

**Parameters**:
- `prompt` (list[dict]): Список словарей, содержащий промпт для модели.
- `message`: Объект сообщения Telegram.

**Returns**:
- `tuple[dict[str, str], int, int]`: Кортеж, содержащий ответ от модели, количество входящих токенов и количество исходящих токенов.

**How the function works**:
1. Sends a "please wait" message to the user.
2. Calls the `_free_gpt_4o_mini` method from the parent class (`neural_networks`) to get the response, incoming tokens, and outgoing tokens from the GPT-4o mini model.
3. Edits the "please wait" message with the content of the response.
4. Inserts HTML tags into the response content using the `PromptsCompressor.html_tags_insert` method.
5. Returns the response, incoming tokens, and outgoing tokens.

**Examples**:
```python
# Пример вызова функции
prompt = [{"role": "user", "content": "Напиши короткий рассказ о космосе."}]
message = ... # Объект сообщения Telegram
response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=prompt, message=message)
```

### `__FLUX_schnell`

```python
def __FLUX_schnell(self, prompt: str, size: list[int], message, seed: int, num_inference_steps: int)-> None:
    """ Processes image generation using the FLUX schnell model.
    Args:
        prompt (str): Prompt for image generation.
        size (list[int]): List containing the size of the image.
        message: Telegram message object.
        seed (int): Seed for random number generation.
        num_inference_steps (int): Number of inference steps.
    Returns:
        None
    """
    ...
```

**Parameters**:
- `prompt` (str): Промпт для генерации изображения.
- `size` (list[int]): Список, содержащий размер изображения.
- `message`: Объект сообщения Telegram.
- `seed` (int): Зерно для генерации случайных чисел.
- `num_inference_steps` (int): Количество шагов инференса.

**Returns**:
- `None`

**How the function works**:
1. Sends a "please wait" message to the user.
2. Calls the `_FLUX_schnell` method from the parent class (`neural_networks`) to generate the image.
3. Sends the generated image to the user as a photo.
4. Deletes the "please wait" message.
5. If an error occurs during image generation, it retries until successful.
6. If the image generation fails, it edits the "please wait" message with an error message.

**Examples**:
```python
# Пример вызова функции
prompt = "космический пейзаж"
size = [1024, 1024]
message = ... # Объект сообщения Telegram
seed = 12345
num_inference_steps = 4
self.__FLUX_schnell(prompt=prompt, size=size, message=message, seed=seed, num_inference_steps=num_inference_steps)
```

### `Text_types`

```python
def Text_types(self, message):
    """ Displays text types for selection.
    Args:
        message: Telegram message object.

    Returns:
        The result of editing the message with the available text types.
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.

**Returns**:
- The result of editing the message with the available text types.

**How the function works**:
1. Defines lists of text type names and their corresponding data.
2. Edits the message with the available text types using the `keyboard_blank` method to display an inline keyboard.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
self.Text_types(message)
```

### `Basic_tariff`

```python
def Basic_tariff(self, message):
    """ Handles the purchase of the basic tariff.
    Args:
        message: Telegram message object.

    Returns:
        None
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.

**Returns**:
- `None`

**How the function works**:
1. Creates an inline keyboard with options to purchase the BASIC tariff or return to the tariff selection.
2. Defines the price for the BASIC tariff.
3. Deletes the original message.
4. Sends an invoice to the user with the details of the BASIC tariff.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
self.Basic_tariff(message)
```

### `Pro_tariff`

```python
def Pro_tariff(self, message):
    """ Handles the purchase of the pro tariff.
    Args:
        message: Telegram message object.

    Returns:
        None
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.

**Returns**:
- `None`

**How the function works**:
1. Creates an inline keyboard with options to purchase the PRO tariff or return to the tariff selection.
2. Defines the price for the PRO tariff.
3. Deletes the original message.
4. Sends an invoice to the user with the details of the PRO tariff.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
self.Pro_tariff(message)
```

### `TextCommands`

```python
def TextCommands(self, message, ind: int):
    """ Processes text commands based on user input.
    Args:
        message: Telegram message object.
        ind (int): Index of the command.

    Returns:
        tuple[int, int, int]: Incoming tokens, outgoing tokens, and 1.
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.
- `ind` (int): Индекс команды.

**Returns**:
- `tuple[int, int, int]`: Кортеж, содержащий количество входящих токенов, количество исходящих токенов и 1.

**How the function works**:
1. Checks if the command requires additional text input from the user.
2. If additional text input is required, prompts the user for the input and registers a next step handler.
3. Constructs a prompt using the user's input and the command index.
4. Calls the `__gpt_4o_mini` method to process the prompt and generate a response.
5. Restarts the bot and returns the incoming tokens, outgoing tokens, and 1.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
ind = 0
incoming_tokens, outgoing_tokens, _ = self.TextCommands(message, ind)
```

### `SomeTextsCommand`

```python
def SomeTextsCommand(self, message, ind: int, tokens: dict[str, int]):
    """ Processes multiple text commands based on user input.
    Args:
        message: Telegram message object.
        ind (int): Index of the command.
        tokens (dict[str, int]): Dictionary containing token information.

    Returns:
        tuple[int, int, int]: Incoming tokens, outgoing tokens, and the number of texts.
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.
- `ind` (int): Индекс команды.
- `tokens` (dict[str, int]): Словарь, содержащий информацию о токенах.

**Returns**:
- `tuple[int, int, int]`: Кортеж, содержащий количество входящих токенов, количество исходящих токенов и количество текстов.

**How the function works**:
1. Prompts the user for the number of texts to generate.
2. Prompts the user for the source text for each text to be generated.
3. Prompts the user for additional parameters for each text to be generated.
4. Constructs prompts for each text using the user's input and the command index.
5. Calls the `__gpt_4o_mini` method to process the prompts and generate responses.
6. Restarts the bot and returns the incoming tokens, outgoing tokens, and the number of texts.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
ind = 0
tokens = {"incoming_tokens": 1000, "outgoing_tokens": 1000, "free_requests": 10}
incoming_tokens, outgoing_tokens, num_texts = self.SomeTextsCommand(message, ind, tokens)
```

### `ImageCommand`

```python
def ImageCommand(self, message, prompt: str, size: list[int]):
    """ Processes image generation commands.
    Args:
        message: Telegram message object.
        prompt (str): Prompt for image generation.
        size (list[int]): List containing the size of the image.

    Returns:
        int: Seed used for image generation.
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.
- `prompt` (str): Промпт для генерации изображения.
- `size` (list[int]): Список, содержащий размер изображения.

**Returns**:
- `int`: Зерно, использованное для генерации изображения.

**How the function works**:
1. Generates a random seed for image generation.
2. Calls the `__FLUX_schnell` method to generate the image.
3. Calls the `ImageChange` method to display options for image modification.
4. Returns the seed used for image generation.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
prompt = "космический пейзаж"
size = [1024, 1024]
seed = self.ImageCommand(message, prompt, size)
```

### `Image_Regen_And_Upscale`

```python
def Image_Regen_And_Upscale(self, message, prompt: str, size: list[int], seed, num_inference_steps=4):
    """ Processes image regeneration and upscaling.
    Args:
        message: Telegram message object.
        prompt (str): Prompt for image generation.
        size (list[int]): List containing the size of the image.
        seed: Seed used for image generation.
        num_inference_steps (int): Number of inference steps.

    Returns:
        The result of calling the `__FLUX_schnell` method.
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.
- `prompt` (str): Промпт для генерации изображения.
- `size` (list[int]): Список, содержащий размер изображения.
- `seed`: Зерно, использованное для генерации изображения.
- `num_inference_steps` (int): Количество шагов инференса.

**Returns**:
- The result of calling the `__FLUX_schnell` method.

**How the function works**:
1. Calls the `__FLUX_schnell` method to regenerate or upscale the image.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
prompt = "космический пейзаж"
size = [1024, 1024]
seed = 12345
self.Image_Regen_And_Upscale(message, prompt, size, seed)
```

### `FreeCommand`

```python
def FreeCommand(self, message, prompts: list[str]):
    """ Processes free mode commands.
    Args:
        message: Telegram message object.
        prompts (list[str]): List of prompts.

    Returns:
        tuple[int, int, list[str]]: Incoming tokens, outgoing tokens, and the list of prompts.
    """
    ...
```

**Parameters**:
- `message`: Объект сообщения Telegram.
- `prompts` (list[str]): Список промптов.

**Returns**:
- `tuple[int, int, list[str]]`: Кортеж, содержащий количество входящих токенов, количество исходящих токенов и список промптов.

**How the function works**:
1. Appends the user's message to the list of prompts.
2. Calls the `__gpt_4o_mini` method to process the prompts and generate a response.
3. Appends the response to the list of prompts.
4. Returns the incoming tokens, outgoing tokens, and the list of prompts.

**Examples**:
```python
# Пример вызова функции
message = ... # Объект сообщения Telegram
prompts = []
incoming_tokens, outgoing_tokens, prompts = self.FreeCommand(message, prompts)
```

## Class Parameters

- `name` (list): List of start button names.
- `data` (list): List of start button data.
- `prompts_text` (dict): Dictionary containing prompts for different actions.
- `bot` (telebot.TeleBot): Telegram bot instance.
- `keyboard_blank` (function): Lambda function for creating inline keyboards.
- `reply_keyboard` (function): Lambda function for creating reply keyboards.
- `__delay` (function): Lambda function for sending a "please wait" message.
- `start_request` (function): Lambda function for handling the start command.
- `restart` (function): Lambda function for restarting the bot.
- `restart_markup` (function): Lambda function for restarting the bot with markup.
- `OneTextArea` (function): Lambda function for handling single text requests.
- `SomeTextsArea` (function): Lambda function for handling multiple text requests.
- `ImageSize` (function): Lambda function for selecting image size.
- `ImageArea` (function): Lambda function for handling image requests.
- `ImageChange` (function): Lambda function for handling image change options.
- `BeforeUpscale` (function): Lambda function for displaying options before upscaling.
- `FreeArea` (function): Lambda function for handling free mode requests.
- `TariffArea` (function): Lambda function for handling tariff requests.
- `TariffExit` (function): Lambda function for exiting the tariff area.
- `TarrifEnd` (function): Lambda function for handling tariff end messages.
- `FreeTariffEnd` (function): Lambda function for handling free tariff end messages.
- `SomeTexts` (function): Lambda function for selecting one or multiple texts.