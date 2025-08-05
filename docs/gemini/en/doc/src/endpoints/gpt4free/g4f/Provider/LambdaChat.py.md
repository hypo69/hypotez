# LambdaChat Provider for gpt4free

## Overview

This module defines the `LambdaChat` class, a provider class for the `gpt4free` project that allows interaction with the Lambda Chat platform. It inherits from the `HuggingChat` class and provides specific configuration and model details for Lambda Chat.

## Details

The `LambdaChat` class is responsible for interfacing with the Lambda Chat platform and managing model selection and execution. It extends the functionality of the `HuggingChat` class with specific parameters and models related to Lambda Chat.

## Classes

### `class LambdaChat`

**Description**: A provider class for the `gpt4free` project that allows interaction with the Lambda Chat platform. It inherits from the `HuggingChat` class and provides specific configuration and model details for Lambda Chat.

**Inherits**: `HuggingChat`

**Attributes**:

- `label (str)`: The name of the provider ("Lambda Chat").
- `domain (str)`: The domain name of the Lambda Chat platform ("lambda.chat").
- `origin (str)`: The base URL for the Lambda Chat platform (constructed using the `domain`).
- `url (str)`: The URL of the Lambda Chat platform.
- `working (bool)`: Indicates whether the provider is currently working.
- `use_nodriver (bool)`: Determines whether the provider uses a web driver.
- `needs_auth (bool)`: Indicates whether the provider requires authentication.
- `default_model (str)`: The default model used by the provider ("deepseek-llama3.3-70b").
- `reasoning_model (str)`: The model used for reasoning tasks ("deepseek-r1").
- `image_models (list)`: A list of models supporting image processing (empty in this case).
- `fallback_models (list)`: A list of fallback models that can be used if the preferred model is unavailable.
- `models (list)`: A copy of the `fallback_models` list.
- `model_aliases (dict)`: A dictionary mapping aliases to actual model names.

**Methods**: 

- `__init__(self, **kwargs)`: Initializes the `LambdaChat` object with the specified attributes.
- `get_available_models(self, model: str | None = None) -> List[str]`: Returns a list of available models based on the specified `model` or using the provider's default models.
- `get_model_by_alias(self, model_alias: str) -> str`: Returns the actual model name based on the provided alias.
- `get_preferred_model(self, model: str | None = None) -> str`: Returns the preferred model for the current task, either the specified `model` or the default model.

**Example**:

```python
# Creating a LambdaChat instance
lambda_chat = LambdaChat()

# Accessing the default model
default_model = lambda_chat.default_model

# Getting a list of available models
available_models = lambda_chat.get_available_models()

# Getting the model based on an alias
model_name = lambda_chat.get_model_by_alias("deepseek-v3")
```

**How the Class Works**: 

The `LambdaChat` class serves as a wrapper for interacting with the Lambda Chat platform. It provides a convenient way to access and utilize models available on Lambda Chat. The `default_model`, `reasoning_model`, `image_models`, and `fallback_models` attributes define the models that the provider can use. The `model_aliases` attribute allows users to refer to models using more user-friendly aliases.