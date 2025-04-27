# `readme_table.py` Module Documentation

## Overview

This module provides functionality to generate a Markdown table summarizing the available GPT-4Free providers and models, along with their status, website links, and model types. This table is intended for documentation purposes and to provide users with a clear overview of the supported options within the `gpt4free` project.

## Details

The `readme_table.py` file dynamically generates the Markdown table content for the `providers.md` file. It does this by iterating through the available providers in the `g4f` library and gathering information about their status, supported features, and models.

## Functions

### `test_async(provider: ProviderType)`

**Purpose**: This function tests whether a given provider is currently active and working. It attempts to send a basic message to the provider using the `g4f` library's async functionalities.

**Parameters**:

- `provider` (ProviderType): The `g4f` provider to be tested.

**Returns**:

- `bool`: `True` if the provider is active and working, `False` otherwise.

**Raises Exceptions**:

- `Exception`: If any errors occur during the communication with the provider, an `Exception` is raised and logged.

**How the Function Works**:

- The function checks if the provider is marked as `working`.
- If the provider is marked as working, the function creates an asynchronous task to send a basic message to the provider using the `g4f` library.
- The function waits for a response for up to 30 seconds.
- If a successful response is received, the function returns `True`.
- If an exception occurs or the provider is not working, the function logs the error (if debugging is enabled) and returns `False`.


### `test_async_list(providers: list[ProviderType])`

**Purpose**: This function runs the `test_async` function for a list of providers concurrently using asyncio and returns a list of responses.

**Parameters**:

- `providers` (list[ProviderType]): A list of `g4f` providers to be tested.

**Returns**:

- `list`: A list of boolean values representing the results of the tests for each provider.

**How the Function Works**:

- The function uses `asyncio.run` to execute `test_async` for each provider in the input list concurrently.
- The results of each `test_async` execution are stored in a list and returned.


### `print_providers()`

**Purpose**: This function generates a list of Markdown lines representing a table of available providers categorized by "Free" and "Auth" types.

**Parameters**:

- None

**Returns**:

- `list`: A list of Markdown lines representing the provider table.

**How the Function Works**:

- The function iterates through all available providers in the `__providers__` list.
- For each provider, it checks if it's marked as `working` and whether it requires authentication.
- The function adds a row to the table with information about the provider, its status, website link, and supported features (such as message history, streaming, and system messages).
- If the provider supports models, it lists the models in the table as well.
- The table is categorized by "Free" and "Auth" types, grouping providers based on whether they require authentication.


### `print_models()`

**Purpose**: This function generates a list of Markdown lines representing a table of available models along with their corresponding base providers, website links, and best providers.

**Parameters**:

- None

**Returns**:

- `list`: A list of Markdown lines representing the model table.

**How the Function Works**:

- The function iterates through the available models in the `models.ModelUtils.convert` dictionary.
- For each model, it retrieves the model's name, base provider, website link, and best provider.
- The function filters out models that are not of type "gpt-3.5" or "gpt-4" (excluding variants).
- The function creates a table row for each model, displaying its details.


### `print_image_models()`

**Purpose**: This function generates a list of Markdown lines representing a table of image models and their corresponding providers, website links, and image generation capabilities.

**Parameters**:

- None

**Returns**:

- `list`: A list of Markdown lines representing the image models table.

**How the Function Works**:

- The function iterates through available providers that have image models or support vision models.
- For each provider, it collects information about its label, provider name, website link, supported image models, and whether it supports vision models.
- The function creates a table row for each provider, displaying its details.


## Parameter Details

- `provider` (ProviderType): Represents a specific provider for accessing GPT-4Free APIs, such as `g4f.Provider.OpenAI`.
- `providers` (list[ProviderType]): A list of `g4f` providers to be tested.
- `message_history` (bool): Indicates whether the provider supports message history.
- `stream` (bool): Indicates whether the provider supports streaming responses.
- `system_message` (bool): Indicates whether the provider supports system messages.
- `auth` (bool): Indicates whether the provider requires authentication.
- `website` (str): The URL of the provider's website.
- `models` (list): A list of model names supported by the provider.
- `image_models` (list): A list of image models supported by the provider.
- `vision_models` (bool): Indicates whether the provider supports vision models (image upload).


## Examples

**1. Example of calling `print_providers()`:**

```python
# Example usage to generate Markdown table content for providers
provider_table_lines = print_providers()

# The `provider_table_lines` variable will contain a list of Markdown lines 
# representing the provider table.
```

**2. Example of calling `print_models()`:**

```python
# Example usage to generate Markdown table content for models
model_table_lines = print_models()

# The `model_table_lines` variable will contain a list of Markdown lines 
# representing the model table.
```

**3. Example of calling `print_image_models()`:**

```python
# Example usage to generate Markdown table content for image models
image_model_table_lines = print_image_models()

# The `image_model_table_lines` variable will contain a list of Markdown lines 
# representing the image models table.
```