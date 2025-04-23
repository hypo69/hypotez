# Module Name

## Overview

This module defines the `Glider` class, which inherits from `OpenaiTemplate`. It configures specific settings for the Glider provider, such as the API endpoint, supported models, and model aliases. This provider is designed to work with the Glider platform and its associated AI models.

## More details

The `Glider` class extends the `OpenaiTemplate` to provide a specific configuration for interacting with the Glider platform. It defines the API endpoint (`https://glider.so/api/chat`), a list of supported models, and aliases for those models. This setup allows the `hypotez` project to seamlessly utilize Glider's services with predefined settings.

## Classes

### `Glider`

**Description**: Defines the configuration for the Glider provider, inheriting from `OpenaiTemplate`.

**Inherits**:
- `OpenaiTemplate`: Provides a base template for interacting with OpenAI-like APIs.

**Attributes**:
- `label` (str): A string representing the label for this provider, set to `"Glider"`.
- `url` (str): A string representing the URL for this provider, set to `"https://glider.so"`.
- `api_endpoint` (str): A string representing the API endpoint for this provider, set to `"https://glider.so/api/chat"`.
- `working` (bool): A boolean indicating whether this provider is currently working, set to `True`.
- `default_model` (str): A string representing the default model for this provider, set to `'chat-llama-3-1-70b'`.
- `models` (list): A list of strings representing the supported models for this provider.
- `model_aliases` (dict): A dictionary mapping aliases to the corresponding model names.

**Working principle**:
The `Glider` class inherits from `OpenaiTemplate` and sets several class attributes to configure the Glider provider. These attributes include the provider's label, URL, API endpoint, working status, default model, supported models, and model aliases. The `model_aliases` dictionary allows the use of shorter, more user-friendly names for the models.

**Methods**:
- None explicitly defined in the class definition.

## Class Parameters

- `label` (str): The label for the provider.
- `url` (str): The URL for the provider.
- `api_endpoint` (str): The API endpoint for the provider.
- `working` (bool): Indicates whether the provider is working.
- `default_model` (str): The default model to use for the provider.
- `models` (list): A list of supported models.
- `model_aliases` (dict): A dictionary mapping model aliases to model names.

**Examples**

```python
from src.endpoints.gpt4free.g4f.Provider import Glider

# Creating an instance of the Glider provider is typically done by other parts of the system.
# Here's how you might access some of the class attributes:

print(Glider.label)
print(Glider.url)
print(Glider.api_endpoint)
print(Glider.working)
print(Glider.default_model)
print(Glider.models)
print(Glider.model_aliases)
```