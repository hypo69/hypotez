# MiniMax.py

## Overview

This module defines the `MiniMax` class, a provider for the `hypotez` project, which implements the OpenAI template for interacting with the MiniMax API.

## Details

The `MiniMax` class inherits from the `OpenaiTemplate` class, providing a standardized interface for interacting with the MiniMax API. It defines specific parameters and configurations related to MiniMax API interactions, including:

- **URL**: The base URL for the MiniMax API.
- **Login URL**: The URL for accessing the MiniMax login interface.
- **API Base**: The base URL for the MiniMax API endpoints.
- **Working**: Flag indicating whether the provider is currently active and functional.
- **Needs Auth**: Flag indicating whether the provider requires authentication for API requests.
- **Default Model**: The default language model used for text-based interactions.
- **Default Vision Model**: The default language model used for image-based interactions.
- **Models**: A list of supported language models.
- **Model Aliases**: A dictionary mapping common model names to their corresponding model IDs.

## Classes

### `MiniMax`

**Description**: This class represents the provider for the MiniMax API, implementing the `OpenaiTemplate` interface for interacting with the API. 

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `label` (str): Provider label - "MiniMax API".
- `url` (str): Base URL for the MiniMax API.
- `login_url` (str): URL for accessing the MiniMax login interface.
- `api_base` (str): Base URL for the MiniMax API endpoints.
- `working` (bool): Flag indicating whether the provider is currently active and functional.
- `needs_auth` (bool): Flag indicating whether the provider requires authentication for API requests.
- `default_model` (str): The default language model used for text-based interactions.
- `default_vision_model` (str): The default language model used for image-based interactions.
- `models` (list): A list of supported language models.
- `model_aliases` (dict): A dictionary mapping common model names to their corresponding model IDs. 

**Methods**:

- **`__init__`**: Initializes the `MiniMax` object with specific API configurations.

## Inner Functions

- **`__init__`**: This is the constructor for the `MiniMax` class. It initializes the class attributes with specific values for the MiniMax API provider, including base URL, login URL, API endpoints, and model information. 

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.MiniMax import MiniMax

# Creating a MiniMax provider instance
mini_max = MiniMax()

# Accessing attributes
print(mini_max.label) # Output: "MiniMax API"
print(mini_max.url) # Output: "https://www.hailuo.ai/chat"
print(mini_max.default_model) # Output: "MiniMax-Text-01"
```