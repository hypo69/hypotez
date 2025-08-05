# TypeGPT Provider

## Overview

This module defines the `TypeGPT` class, which acts as a provider for the `gpt4free` endpoint within the `hypotez` project. It provides functionality for interacting with the TypeGPT API and utilizes the `OpenaiTemplate` class for common API interactions.

## Details

The `TypeGPT` class inherits from the `OpenaiTemplate` class, leveraging its methods for sending requests, processing responses, and handling common API operations. It defines specific attributes and methods relevant to the TypeGPT API, such as:

- **`label`**: Identifies the provider as "TypeGpt".
- **`url`**: Sets the base URL for the TypeGPT website.
- **`api_base`**: Specifies the base URL for the TypeGPT API.
- **`working`**: Indicates whether the provider is currently functional (set to `True`).
- **`headers`**: Defines the default headers for API requests.
- **`default_model`**: Specifies the default GPT model used by the provider.
- **`default_vision_model`**: Defines the default model for image processing tasks.
- **`vision_models`**: Lists available models for image processing.
- **`fallback_models`**: Lists backup models to use if the primary model is unavailable.
- **`image_models`**: Lists models specifically designed for image generation.
- **`model_aliases`**: Maps model aliases to their actual model names.
- **`get_models`**: A class method that retrieves a list of available models from the TypeGPT API.

## Classes

### `TypeGPT`

**Description**: This class represents the TypeGPT provider, handling interactions with the TypeGPT API.

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `label` (str): Provider identifier, "TypeGpt".
- `url` (str): Base URL for the TypeGPT website.
- `api_base` (str): Base URL for the TypeGPT API.
- `working` (bool): Indicates the provider's functionality (True).
- `headers` (dict): Default headers for API requests.
- `default_model` (str): The default GPT model used by the provider.
- `default_vision_model` (str): The default model for image processing tasks.
- `vision_models` (list): List of available models for image processing.
- `fallback_models` (list): List of backup models for when the primary model is unavailable.
- `image_models` (list): List of models specialized for image generation.
- `model_aliases` (dict): Mapping of model aliases to actual model names.

**Methods**:

- `get_models`(): A class method that retrieves a list of available models from the TypeGPT API.

## Class Methods

### `get_models`

```python
    @classmethod
    def get_models(cls, **kwargs):
        if not cls.models:
            cls.models = requests.get(f"{cls.url}/api/config").json()["customModels"].split(",")
            cls.models = [model.split("@")[0][1:] for model in cls.models if model.startswith("+") and model not in cls.image_models]
        return cls.models
```

**Purpose**: This method retrieves a list of available GPT models from the TypeGPT API.

**Parameters**:

- `**kwargs`: This method accepts any additional keyword arguments, but they are not currently used.

**Returns**:

- `list`: A list of available GPT models.

**How the Function Works**:

1. **Check if `models` is empty**: If the `models` attribute is not yet populated, it proceeds to fetch the model list.
2. **Fetch API response**: Makes a GET request to the `api/config` endpoint of the TypeGPT website.
3. **Parse API response**: Extracts the `customModels` list from the JSON response.
4. **Filter and format model names**: Splits each model string at `"@"` and extracts the part after `"+"`. This ensures only valid models are included.
5. **Return model list**: Returns the filtered and formatted list of models.

**Examples**:

```python
>>> TypeGPT.get_models()
['gpt-4o-mini-2024-07-18', 'gpt-3.5-turbo', 'gpt-3.5-turbo-202201', ..., 'o3-mini']
```