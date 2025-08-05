# Configuration for FreeGPT-Webui-RU Server

## Overview

This module defines configuration settings for the FreeGPT-Webui-RU server, including available models, special instructions, and prompt generators.

## Details

This module provides a dictionary called `models` that specifies the list of available language models supported by the server. It also contains a dictionary called `special_instructions` which includes various instructions for specific modes, such as `DAN Mode`, `EvilBOT Mode`, `Developer Mode`, and more. These instructions are used for controlling the behavior and response style of the language models. Additionally, the module defines prompts for generative AI models like Midjourney and Stable Diffusion, assisting users in generating images based on textual descriptions.

## Classes

### `Config`

**Description**: This class acts as a container for configuration settings.
**Inherits**: None
**Attributes**: None

**Methods**: None


## Functions

### `get_model_by_name`

**Purpose**: This function retrieves a model based on its name.

**Parameters**:
- `model_name` (str): The name of the model to retrieve.

**Returns**:
- `str`: The model name if found, otherwise `None`.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function checks if the provided `model_name` exists in the `models` dictionary. 
- If found, it returns the model name; otherwise, it returns `None`.

**Examples**:
- `get_model_by_name('gpt-3.5-turbo')` returns `'gpt-3.5-turbo'`
- `get_model_by_name('unknown_model')` returns `None`

### `get_special_instructions`

**Purpose**: This function retrieves special instructions for a specific model.

**Parameters**:
- `model_name` (str): The name of the model for which to retrieve instructions.

**Returns**:
- `list`: A list of special instructions for the specified model.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function checks if the `model_name` is present in the `special_instructions` dictionary.
- If found, it returns the list of instructions associated with that model.
- Otherwise, it returns an empty list.

**Examples**:
- `get_special_instructions('gpt-dan-11.0')` returns a list of instructions for DAN Mode.
- `get_special_instructions('unknown_model')` returns an empty list.

### `get_prompt_generator`

**Purpose**: This function retrieves the appropriate prompt generator based on the specified mode.

**Parameters**:
- `mode` (str): The mode for which to retrieve a prompt generator.

**Returns**:
- `dict`: A dictionary containing special instructions and prompt generation logic for the specified mode.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function retrieves special instructions from the `special_instructions` dictionary based on the provided `mode`.
- It returns a dictionary containing the instructions and prompt generation logic specific to the mode.

**Examples**:
- `get_prompt_generator('midjourney-promt')` returns a dictionary containing instructions for Midjourney prompt generation.
- `get_prompt_generator('sd-promt')` returns a dictionary containing instructions for Stable Diffusion prompt generation.

### `get_default_special_instructions`

**Purpose**: This function retrieves default special instructions, which are applicable to all models.

**Parameters**:
- None

**Returns**:
- `list`: A list of default special instructions.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function simply returns the list of instructions associated with the `'default'` key in the `special_instructions` dictionary.

**Examples**:
- `get_default_special_instructions()` returns a list of default instructions.

## Parameter Details

- `models` (dict): A dictionary containing a list of available language models supported by the FreeGPT-Webui-RU server.
- `special_instructions` (dict): A dictionary containing special instructions for various modes, such as `DAN Mode`, `EvilBOT Mode`, and more. 
- `mode` (str): The specific mode, such as `'midjourney-promt'`, `'sd-promt'`, or `'gpt-dan-11.0'`, for which to retrieve instructions or prompt generation logic.

## Examples

```python
# Get a list of all available models
models = config.models

# Get special instructions for DAN Mode
dan_instructions = config.get_special_instructions('gpt-dan-11.0')

# Get prompt generator for Midjourney
midjourney_generator = config.get_prompt_generator('midjourney-promt')

# Get default special instructions
default_instructions = config.get_default_special_instructions()
```