# OIVSCode Provider

## Overview

This module defines the `OIVSCode` class, which acts as a provider for the GPT4Free endpoint. It provides access to the OpenAI VSCode Server, a powerful tool for code generation and analysis.

## Details

The `OIVSCode` class inherits from the `OpenaiTemplate` class, inheriting its core functionality for interacting with OpenAI APIs. It specifically focuses on the OpenAI VSCode Server, a service hosted on Render.

## Classes

### `OIVSCode`

**Description**: This class represents the `OIVSCode` provider for the GPT4Free endpoint. It extends the `OpenaiTemplate` class and provides access to the OpenAI VSCode Server.

**Inherits**: `OpenaiTemplate`

**Attributes**:
- `label` (str): A descriptive label for the provider.
- `url` (str): The base URL for the OpenAI VSCode Server.
- `api_base` (str): The base URL for the API endpoint.
- `working` (bool): Indicates whether the provider is currently active.
- `needs_auth` (bool): Indicates whether authentication is required for the provider.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `default_model` (str): The default model to use.
- `default_vision_model` (str): The default model for vision tasks.
- `vision_models` (list): A list of vision models supported by the provider.
- `models` (list): A combined list of all models, including vision and code-related models.
- `model_aliases` (dict): A dictionary mapping model aliases to their full model IDs.

**Methods**:
- `__init__(self, **kwargs)`: Initializes the `OIVSCode` provider object with provided parameters.
- `__str__(self)`: Returns a string representation of the provider.
- `_preprocess_request(self, request: dict) -> dict`: Prepares the request data for the OpenAI API call.
- `_validate_response(self, response: dict) -> dict`: Validates the response from the OpenAI API.
- `_handle_error(self, message: str) -> dict`: Handles errors encountered during the API call.
- `_check_if_model_available(self, model: str) -> bool`: Checks if the specified model is available for the provider.
- `_process_response(self, response: dict) -> dict`: Processes the response from the OpenAI API.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.OIVSCode import OIVSCode

# Create an OIVSCode provider instance
provider = OIVSCode()

# Check if the provider is working
print(provider.working)  # Output: True

# Get the default model
print(provider.default_model)  # Output: gpt-4o-mini-2024-07-18

# Check if a specific model is available
print(provider.check_if_model_available("gpt-4o-mini-2024-07-18"))  # Output: True

# Prepare a request
request = {"prompt": "Generate a Python code snippet to calculate the factorial of a number."}

# Preprocess the request
preprocessed_request = provider._preprocess_request(request)

# Send the request to the OpenAI API and get the response
response = provider._send_request(preprocessed_request)

# Process the response
processed_response = provider._process_response(response)

# Print the generated code snippet
print(processed_response["content"]) 
```