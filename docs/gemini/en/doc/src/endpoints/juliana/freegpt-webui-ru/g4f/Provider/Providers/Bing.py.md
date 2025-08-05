# Bing Provider

## Overview

This module implements the `Bing` provider for the `g4f` project, providing access to the Bing AI service for text generation. It leverages the Bing Chat API and WebSockets to stream responses from the Bing AI model.

## Details

The module utilizes the `aiohttp` library for asynchronous HTTP requests and WebSockets communication. It establishes a connection to the Bing ChatHub server, sends prompts, and receives streamed responses from the AI model. The `_create_completion` function acts as an interface for the `g4f` framework, accepting a list of messages and generating streamed responses.

## Classes

### `optionsSets`

**Description**:  Defines optional parameter sets for the Bing AI request.

**Attributes**:

- `optionSet (dict)`: A dictionary representing an optional parameter set. It contains the following keys:
    - `tone (str)`:  A string specifying the tone of the response.
    - `optionsSets (list)`: A list of strings representing additional optional parameters for the Bing AI request.
- `jailbreak (dict)`: A pre-defined set of optional parameters to potentially "jailbreak" the AI model, allowing it to provide more creative or unrestricted responses.

### `Defaults`

**Description**: Defines default values for various parameters used in the Bing provider.

**Attributes**:

- `delimiter (str)`:  A delimiter used to separate messages in the streamed responses.
- `ip_address (str)`: A randomly generated IP address for spoofing location information.
- `allowedMessageTypes (list)`: A list of allowed message types supported by the Bing AI service.
- `sliceIds (list)`: A list of slice IDs used to filter specific types of content.
- `location (dict)`: A dictionary containing location information used in the Bing AI request.

## Functions

### `_format(msg: dict) -> str`

**Purpose**: Formats a dictionary as a JSON string with the delimiter appended.

**Parameters**:

- `msg (dict)`: The dictionary to be formatted.

**Returns**:

- `str`: The formatted JSON string with the delimiter appended.

### `create_conversation()`

**Purpose**: Creates a new Bing AI conversation by sending a request to the `/conversation/create` endpoint.

**Returns**:

- `tuple`: A tuple containing the conversation ID, client ID, and conversation signature.

### `stream_generate(prompt: str, mode: optionsSets.optionSet = optionsSets.jailbreak, context: bool or str = False)`

**Purpose**:  Generates a streamed response from the Bing AI model based on the given prompt.

**Parameters**:

- `prompt (str)`: The input prompt to be sent to the Bing AI model.
- `mode (optionsSets.optionSet)`: An optional parameter set to be used for the AI request.
- `context (bool or str)`:  A boolean indicating whether to include context in the request or a string representing the context to be included.

**Returns**:

- `Generator[str, None, None]`: A generator that yields streamed response chunks from the Bing AI model.

**How the Function Works**:

1. **Establish WebSocket Connection**: The function connects to the Bing ChatHub server via WebSockets.
2. **Send Initial Message**: It sends a message to establish the WebSocket protocol.
3. **Send Request**: It constructs a request object with the prompt, mode, and context information and sends it to the AI model.
4. **Receive Streamed Responses**: The function receives streamed responses from the AI model.
5. **Process Responses**: It processes each response chunk, extracting the generated text and yielding it to the caller.

**Examples**:

```python
# Generate a response to a simple prompt without context
async for token in stream_generate("What is the meaning of life?"):
    print(token, end="")

# Generate a response with context
async for token in stream_generate("What is the capital of France?", context="France is a country in Western Europe."):
    print(token, end="")
```

### `run(generator)`

**Purpose**: Runs an asynchronous generator, yielding its results.

**Parameters**:

- `generator`: The asynchronous generator to be run.

**Returns**:

- `Generator[Any, None, None]`: A generator that yields values produced by the asynchronous generator.

### `convert(messages)`

**Purpose**: Converts a list of messages into a formatted string suitable for use as context.

**Parameters**:

- `messages (list)`: A list of message dictionaries. Each dictionary should contain the `role` and `content` of the message.

**Returns**:

- `str`: A formatted string representing the message context.

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`

**Purpose**: Generates a completion (text response) from the Bing AI model based on a list of messages.

**Parameters**:

- `model (str)`: The name of the model to be used (currently only "gpt-4" is supported).
- `messages (list)`: A list of message dictionaries representing the conversation history.
- `stream (bool)`: A boolean indicating whether to stream the response.
- `**kwargs`:  Additional keyword arguments for the Bing AI request.

**Returns**:

- `Generator[str, None, None]`: A generator that yields streamed response chunks or a complete response string if `stream` is `False`.

**How the Function Works**:

1. **Extract Prompt and Context**: It extracts the last message from the `messages` list as the current prompt and constructs context from all previous messages.
2. **Call Stream Generate**: It calls the `stream_generate` function to generate a streamed response from the Bing AI model.
3. **Yield Responses**: If `stream` is `True`, it yields each streamed response chunk. Otherwise, it accumulates all chunks into a single string and yields the complete response.

## Parameter Details

- `model (str)`: The name of the AI model to be used (currently only "gpt-4" is supported).
- `messages (list)`: A list of message dictionaries representing the conversation history. Each message dictionary should contain the `role` (e.g., "user", "assistant") and `content` (the message text).
- `stream (bool)`: A boolean indicating whether the response should be streamed or returned as a single string.

## Examples

```python
# Generate a response to a single prompt
for token in _create_completion(model="gpt-4", messages=[{'role': 'user', 'content': 'Hello, world!'}]):
    print(token, end="")

# Generate a response to a conversation
for token in _create_completion(model="gpt-4", messages=[
    {'role': 'user', 'content': 'What is the capital of France?'},
    {'role': 'assistant', 'content': 'Paris.'},
    {'role': 'user', 'content': 'What is the population of Paris?'}
]):
    print(token, end="")
```

## Inner Functions

This module does not have any inner functions.