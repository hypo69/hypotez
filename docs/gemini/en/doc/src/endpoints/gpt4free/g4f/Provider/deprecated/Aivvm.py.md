# Aivvm Provider

## Overview

This module provides the `Aivvm` class, which implements the `AbstractProvider` interface to interact with the Aivvm API for generating text and code.

## Details

The `Aivvm` provider utilizes the Aivvm API (https://chat.aivvm.com) to provide access to various language models, including GPT-3.5 and GPT-4. It enables communication with these models by sending messages and receiving responses.

## Classes

### `Aivvm`

**Description**: This class provides access to the Aivvm API for interacting with language models like GPT-3.5 and GPT-4.

**Inherits**: `AbstractProvider`

**Attributes**:

- `url (str)`: The base URL of the Aivvm API.
- `supports_stream (bool)`: Indicates whether the provider supports streaming responses.
- `working (bool)`: Indicates the current working status of the provider.
- `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports the GPT-3.5-turbo model.
- `supports_gpt_4 (bool)`: Indicates whether the provider supports the GPT-4 model.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`

### `create_completion`

**Purpose**: Sends a request to the Aivvm API to generate a response based on the provided model, messages, and stream setting.

**Parameters**:

- `model (str)`: The name of the language model to use.
- `messages (Messages)`: A list of messages representing the conversation history.
- `stream (bool)`: Indicates whether to stream the response.
- `**kwargs`: Additional keyword arguments that can be passed to the API, such as "system_message", "temperature".

**Returns**:

- `CreateResult`: A result object containing the generated response and other information.

**Raises Exceptions**:

- `ValueError`: If the specified model is not supported by the provider.

**How the Function Works**:

1. **Model Selection**: The function first checks if a model is specified. If not, it defaults to "gpt-3.5-turbo". It then verifies that the model is supported.
2. **Request Preparation**: The function prepares a JSON payload containing the model, messages, API key, prompt, and temperature.
3. **API Call**: The function sends a POST request to the Aivvm API using the prepared data and headers.
4. **Response Handling**: The function iterates through the streamed response chunks and decodes them using UTF-8 or Unicode escape to handle potential encoding issues.

**Examples**:

```python
# Example 1: Generating a response using GPT-3.5-turbo with default settings
response = provider.create_completion(model="gpt-3.5-turbo", messages=[], stream=True)

# Example 2: Generating a response using GPT-4 with custom system message and temperature
response = provider.create_completion(
    model="gpt-4", messages=[], stream=True, system_message="You are a helpful assistant.", temperature=0.5
)
```

## Inner Functions

There are no inner functions in this file.

## Parameter Details

- `model (str)`: The name of the language model to use. This parameter specifies the AI model that will be used to generate the response.
- `messages (Messages)`: A list of messages representing the conversation history. This parameter provides context for the current request by including past interactions with the model.
- `stream (bool)`: Indicates whether to stream the response. When set to `True`, the response is returned incrementally as it is generated.
- `**kwargs`: Additional keyword arguments that can be passed to the API, such as "system_message", "temperature". These parameters offer control over the model's behavior and response generation.

## Examples

```python
# Example 1: Generating a response using GPT-3.5-turbo with default settings
response = provider.create_completion(model="gpt-3.5-turbo", messages=[], stream=True)

# Example 2: Generating a response using GPT-4 with custom system message and temperature
response = provider.create_completion(
    model="gpt-4", messages=[], stream=True, system_message="You are a helpful assistant.", temperature=0.5
)
```

## Conclusion

The `Aivvm` provider provides a simple and efficient way to access the Aivvm API and leverage its various language models for text generation and other tasks. It supports streaming responses for a more interactive user experience.