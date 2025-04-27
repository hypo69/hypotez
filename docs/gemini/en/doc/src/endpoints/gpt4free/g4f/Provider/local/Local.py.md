# Local Provider for GPT4Free

## Overview

This module defines the `Local` class, which acts as a provider for the GPT4Free endpoint using local models. It leverages the `gpt4all` library for local model interactions. 

## Details

The `Local` class inherits from `AbstractProvider` and `ProviderModelMixin`, inheriting base functionality and model management capabilities. It provides a simple interface for interacting with local GPT-4-like models via the `gpt4all` library.

## Classes

### `class Local`

**Description**: This class represents a local GPT-4Free provider, enabling interactions with local models using the `gpt4all` library.

**Inherits**: `AbstractProvider`, `ProviderModelMixin`

**Attributes**:

- `label` (str): The name of the provider, set to "GPT4All".
- `working` (bool): Indicates whether the provider is active. Set to `True` for this provider.
- `supports_message_history` (bool): Indicates whether the provider supports message history. Set to `True` for this provider.
- `supports_system_message` (bool): Indicates whether the provider supports system messages. Set to `True` for this provider.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses. Set to `True` for this provider.

**Methods**:

- `get_models()`: Returns a list of available local models for this provider.
- `create_completion()`: Generates a completion based on the provided messages and model.

## Class Methods

### `get_models()`

```python
    @classmethod
    def get_models(cls):
        if not cls.models:
            cls.models = list(get_models())
            cls.default_model = cls.models[0]
        return cls.models
```

**Purpose**: Retrieves the list of available local models.

**Parameters**: None

**Returns**: 
- `list`: A list of available local model names.

**How the Function Works**:

- Checks if the `models` attribute is already populated.
- If not, it calls the `get_models()` function from the `locals.models` module to retrieve a list of models.
- It sets the first model in the list as the default model.
- It returns the list of available models.


### `create_completion()`

```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:
        if not has_requirements:
            raise MissingRequirementsError('Install "gpt4all" package | pip install -U g4f[local]')
        return LocalProvider.create_completion(
            cls.get_model(model),
            messages,
            stream,
            **kwargs
        )
```

**Purpose**: Generates a completion using a local GPT-4-like model.

**Parameters**:

- `model` (str): The name of the local model to use for completion.
- `messages` (Messages): A list of messages to provide as context for the completion.
- `stream` (bool): Indicates whether to stream the response or wait for the full response.
- `**kwargs`: Additional keyword arguments to pass to the `gpt4all` completion function.

**Returns**: 
- `CreateResult`: An object containing the generated completion and other information.

**Raises Exceptions**:

- `MissingRequirementsError`: If the `gpt4all` package is not installed.

**How the Function Works**:

- Checks if the `gpt4all` package is installed. If not, raises a `MissingRequirementsError`.
- Retrieves the model object using `cls.get_model(model)`.
- Calls the `create_completion()` method of the `LocalProvider` class to generate the completion.
- Passes the selected model, messages, stream flag, and additional keyword arguments to the `LocalProvider` method.
- Returns the result of the completion process as a `CreateResult` object.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Local import Local

# Get the list of available local models
models = Local.get_models()
print(models)  # Output: ['gpt4all-j-6b-v2', 'gpt4all-lora-13b', ...]

# Create a completion using the 'gpt4all-j-6b-v2' model
completion = Local.create_completion(model='gpt4all-j-6b-v2', messages=[{'role': 'user', 'content': 'Hello world!'}], stream=False)
print(completion) # Output:  <CreateResult object>
```