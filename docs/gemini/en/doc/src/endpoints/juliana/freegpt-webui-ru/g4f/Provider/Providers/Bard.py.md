# Provider: Bard

## Overview

This module provides a provider for the `g4f` framework that utilizes Google Bard for text generation. 

## Details

This module defines the `Bard` provider class, which uses Google Bard's API to generate text. The provider requires authorization and utilizes Google's `Palm2` model.

## Classes

### `class Bard`

**Description**: This class implements a provider for the `g4f` framework using Google Bard for text generation.

**Inherits**: `Provider`

**Attributes**:
  - `url`: The URL of the Google Bard website.
  - `model`: The model used by Google Bard (currently `Palm2`).
  - `supports_stream`: Indicates whether streaming responses are supported.
  - `needs_auth`: Indicates whether authorization is required.

**Methods**:
  - `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: This method handles the interaction with Google Bard's API, sending a request with a formatted prompt and retrieving the generated text.


## Functions

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`

**Purpose**: This function sends a request to Google Bard's API to generate text based on the provided prompt and model.

**Parameters**:
  - `model`: The model name to use for generation (e.g., `Palm2`).
  - `messages`: A list of messages containing the prompt and previous conversation history.
  - `stream`: Indicates whether to receive the response as a stream.
  - `**kwargs`: Optional keyword arguments, including `proxy`.

**Returns**:
  - A generator yielding the generated text from Google Bard.

**Raises Exceptions**:
  - `ConnectionError`: If a connection error occurs during the API request.
  - `ValueError`: If an invalid parameter is provided.

**How the Function Works**:
  - The function first formats the prompt by combining messages with their roles.
  - It then retrieves a Google Bard session cookie (PSID) from the browser's cookies.
  - If a proxy is specified, the function configures the request with proxy settings.
  - The function then performs a POST request to Google Bard's API with the formatted prompt and necessary parameters.
  - It parses the response and yields the generated text as a stream.

**Examples**:
  ```python
  >>> model = 'Palm2'
  >>> messages = [
  ...     {'role': 'user', 'content': 'Tell me a joke.'}
  ... ]
  >>> stream = False
  >>> proxy = 'http://127.0.0.1:8080'
  >>> completion = _create_completion(model, messages, stream, proxy=proxy)
  >>> for text in completion:
  ...     print(text)
  Why don't scientists trust atoms? Because they make up everything!
  ``` 

## Parameter Details
  - `model` (str): The name of the language model to be used for text generation.
  - `messages` (list): A list of dictionaries containing the prompt and any previous conversation history. Each dictionary should have the following keys:
    - `role`: The role of the message sender (e.g., 'user', 'assistant').
    - `content`: The text content of the message.
  - `stream` (bool): Indicates whether the response should be streamed.
  - `**kwargs`: Additional keyword arguments that can be passed to the function. For example, a proxy server address can be specified using `proxy`.

## Examples

```python
>>> from hypotez.src.endpoints.juliana.freegpt_webui_ru.g4f.Provider.Providers import Bard
>>> bard = Bard()
>>> messages = [
...     {'role': 'user', 'content': 'Tell me a joke.'}
... ]
>>> completion = bard._create_completion(model='Palm2', messages=messages, stream=False)
>>> for text in completion:
...     print(text)
Why don't scientists trust atoms? Because they make up everything!
```