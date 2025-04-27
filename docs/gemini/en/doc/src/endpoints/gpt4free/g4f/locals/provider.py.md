# LocalProvider Module

## Overview

This module provides functionality for interacting with GPT4All models for generating text. It includes a `LocalProvider` class that encapsulates methods for creating text completions using locally stored GPT4All models.

## Details

This module is designed to be used within a larger project that requires access to GPT4All models. It handles tasks like:

- Loading model configurations from a `MODEL_LIST` dictionary.
- Finding the directory containing the specified GPT4All model file.
- Downloading the model file if it's not found locally.
- Using the `GPT4All` library to generate text completions based on a given prompt and conversation history.

## Classes

### `LocalProvider`

**Description**: This class is used for interacting with GPT4All models and generating text completions.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool = False, **kwargs)`: This method generates a text completion based on the specified model, messages (conversation history), and streaming options.

## Functions

### `find_model_dir(model_file: str) -> str`

**Purpose**: This function finds the directory containing the specified GPT4All model file (`model_file`). It searches in various locations, including the project's `models` directory and the local directory, and returns the path to the directory.

**Parameters**:

- `model_file` (str): The name of the GPT4All model file.

**Returns**:

- `str`: The path to the directory containing the model file.

**How the Function Works**:

- The function first tries to find the model file in the project's `models` directory.
- If not found there, it checks the local directory.
- If still not found, it walks through the current working directory to find the model file.
- If the file is not found in any of these locations, the function returns the path to the project's `models` directory.

**Examples**:

- If the model file `gpt4all-lora-quantized.bin` exists in the project's `models` directory, the function will return the path to that directory.
- If the model file `gpt4all-lora-quantized.bin` exists in the local directory, the function will return the path to that directory.
- If the model file `gpt4all-lora-quantized.bin` exists in a subdirectory named `models` within the working directory, the function will return the path to that subdirectory.

### `create_completion(model: str, messages: Messages, stream: bool = False, **kwargs)`

**Purpose**: This method generates a text completion based on the specified model, messages (conversation history), and streaming options.

**Parameters**:

- `model` (str): The name of the GPT4All model to use.
- `messages` (Messages): A list of messages representing the conversation history.
- `stream` (bool): If `True`, the completion will be generated in a streaming fashion, returning tokens one by one. Defaults to `False`.

**Returns**:

- `Generator[str, None, None] | str`: A generator of tokens if `stream` is `True`, otherwise a string containing the complete generated text.

**How the Function Works**:

- The function first checks if the specified model exists in the `MODEL_LIST` dictionary.
- If not found, it raises a `ValueError`.
- It then retrieves the model file path and directory from the `MODEL_LIST`.
- If the model file is not found, it prompts the user to download it.
- It then initializes a `GPT4All` instance using the model file path and directory.
- It extracts the system message from the `messages` list.
- It constructs a prompt template and a conversation string based on the messages.
- It uses the `GPT4All` model to generate a completion, either streaming or non-streaming, based on the `stream` parameter.
- Finally, it returns the generated text or a generator of tokens.

**Examples**:

- `create_completion(model="gpt4all-lora-quantized", messages=[{"role": "user", "content": "Hello, world!"}], stream=False)`: This call will generate a text completion using the "gpt4all-lora-quantized" model, based on the prompt "Hello, world!" and will return the complete text.
- `create_completion(model="gpt4all-lora-quantized", messages=[{"role": "user", "content": "Hello, world!"}], stream=True)`: This call will generate a text completion using the "gpt4all-lora-quantized" model, based on the prompt "Hello, world!" and will return a generator of tokens, allowing for streaming output.

## Parameter Details

- `model_file` (str): The name of the GPT4All model file to be used.
- `messages` (Messages): A list of messages representing the conversation history. Each message is a dictionary with the following structure:
    - `role` (str): The role of the message sender (e.g., "user", "system", "assistant").
    - `content` (str): The content of the message.
- `stream` (bool): If `True`, the completion will be generated in a streaming fashion, returning tokens one by one. Defaults to `False`.

## Examples

### Example 1: Generating Text Completion

```python
from hypotez.src.endpoints.gpt4free.g4f.locals.provider import LocalProvider
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

provider = LocalProvider()

messages: Messages = [
    {"role": "user", "content": "What is the meaning of life?"},
]

completion = provider.create_completion(model="gpt4all-lora-quantized", messages=messages, stream=False)
print(completion)
```

### Example 2: Streaming Text Completion

```python
from hypotez.src.endpoints.gpt4free.g4f.locals.provider import LocalProvider
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

provider = LocalProvider()

messages: Messages = [
    {"role": "user", "content": "What is the capital of France?"},
]

for token in provider.create_completion(model="gpt4all-lora-quantized", messages=messages, stream=True):
    print(token, end="")
```