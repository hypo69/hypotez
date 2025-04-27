# Backend API Module

## Overview

This module provides the backend functionality for the FreeGPT web UI, handling user conversations and interactions with AI models.

## Details

The `Backend_Api` class is responsible for managing the API endpoints, handling incoming requests, and processing them using various AI models. It utilizes libraries like `g4f`, `googletrans`, and `flask` for interacting with AI models, translating languages, and managing the Flask application.

The module implements conversation management, including building conversation histories with system messages, user prompts, and potential search results retrieved from DuckDuckGo. It also handles jailbreak instructions, providing specific prompts for different jailbreak scenarios.

## Classes

### `Backend_Api`

**Description**: This class handles API endpoints, processes user requests, and manages conversations with AI models.

**Inherits**: 

**Attributes**:

- `app` (`Flask`): The Flask application instance.
- `use_auto_proxy` (`bool`): Indicates whether to use automatic proxy selection.
- `routes` (`dict`): A dictionary mapping API endpoints to their corresponding functions and allowed HTTP methods.

**Methods**:

- `__init__(self, app, config: dict) -> None`: Initializes the Backend_Api instance, sets up routes, and starts a thread for updating working proxies if `use_auto_proxy` is enabled.
- `_conversation()`: Handles the `/backend-api/v2/conversation` endpoint, processes user requests, generates responses from AI models, and returns the result.

## Functions

### `build_messages(jailbreak)`

**Purpose**: This function builds the conversation history for an AI model, including system messages, user prompts, and potential search results.

**Parameters**:

- `jailbreak` (`str`): The requested jailbreak mode (e.g., "Default", "Ask anything").

**Returns**:

- `list`: A list of conversation messages.

**How the Function Works**:

1. Retrieves conversation history, internet access status, and the user prompt from the request data.
2. Constructs a system message with information like the date, response language, and model description.
3. Adds the existing conversation history to the message list.
4. Fetches search results from DuckDuckGo if internet access is enabled.
5. Adds jailbreak instructions to the conversation based on the `jailbreak` parameter.
6. Appends the user prompt to the conversation history.
7. Reduces the conversation size to avoid API token limits.
8. Returns the finalized conversation history.

**Examples**:

```python
>>> request.json = {
...     'meta': {
...         'content': {
...             'conversation': [{'role': 'user', 'content': 'Hello'}],
...             'internet_access': True,
...             'parts': [{'content': 'What is the meaning of life?'}]
...         }
...     },
...     'jailbreak': 'Default'
... }
>>> build_messages('Default')
[
    {'role': 'system', 'content': 'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. Strictly follow the users instructions. Current date: 2023-12-22. You will respond in the language: en. '},
    {'role': 'user', 'content': 'Hello'},
    {'role': 'system', 'content': '[1] "The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one definitive answer, as it is a deeply personal and subjective question. Some people find meaning in their relationships, their work, or their faith. Others find meaning in their pursuit of knowledge or creativity. Ultimately, the meaning of life is up to each individual to define for themselves." URL:https://www.google.com/search?q=meaning+of+life.'},
    {'role': 'user', 'content': 'What is the meaning of life?'}
]
```

### `fetch_search_results(query)`

**Purpose**: This function retrieves search results from DuckDuckGo based on a given query.

**Parameters**:

- `query` (`str`): The search query.

**Returns**:

- `list`: A list of search results.

**How the Function Works**:

1. Sends a request to the DuckDuckGo API using the `requests.get` function.
2. Parses the JSON response and extracts relevant information (snippet and link).
3. Constructs a system message with the formatted search results and appends it to a list.
4. Returns the list of search results.

**Examples**:

```python
>>> fetch_search_results('What is the meaning of life?')
[{'role': 'system', 'content': '[1] "The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one definitive answer, as it is a deeply personal and subjective question. Some people find meaning in their relationships, their work, or their faith. Others find meaning in their pursuit of knowledge or creativity. Ultimately, the meaning of life is up to each individual to define for themselves." URL:https://www.google.com/search?q=meaning+of+life.'}]
```

### `generate_stream(response, jailbreak)`

**Purpose**: This function generates a stream of responses from the AI model, handling jailbreak instructions.

**Parameters**:

- `response` (`list`): The response from the AI model.
- `jailbreak` (`str`): The requested jailbreak mode.

**Returns**:

- `generator`: A generator that yields individual response messages.

**How the Function Works**:

1. Checks if jailbreak instructions are enabled.
2. If jailbreak instructions are enabled, iterates through the response messages and checks for jailbroken response patterns (e.g., "ACT:", "GPT:").
3. If a jailbroken response pattern is detected, it checks for success or failure based on the response content.
4. Yields the response messages, either individually or as a combined string for jailbroken responses.
5. If jailbreak instructions are not enabled, yields the response messages directly.

**Examples**:

```python
>>> response = ['GPT: This is a jailbroken response.', 'ACT: Do as I say!']
>>> generate_stream(response, 'Ask anything')
'GPT: This is a jailbroken response.ACT: Do as I say!'
>>> response = ['This is a normal response.']
>>> generate_stream(response, 'Default')
'This is a normal response.'
```

### `response_jailbroken_success(response: str) -> bool`

**Purpose**: This function checks if a jailbroken response is successful.

**Parameters**:

- `response` (`str`): The response text from the AI model.

**Returns**:

- `bool`: `True` if the response indicates success, `False` otherwise.

**How the Function Works**:

1. Uses regular expressions to search for the pattern "ACT:" in the response.
2. Returns `True` if the pattern is found, indicating a successful jailbreak.

**Examples**:

```python
>>> response_jailbroken_success('ACT: I am now jailbroken.')
True
>>> response_jailbroken_success('This is not a jailbroken response.')
False
```

### `response_jailbroken_failed(response)`

**Purpose**: This function checks if a jailbroken response is failed.

**Parameters**:

- `response` (`str`): The response text from the AI model.

**Returns**:

- `bool`: `True` if the response indicates failure, `False` otherwise.

**How the Function Works**:

1. Checks if the response length is less than 4 characters.
2. If the response length is greater than or equal to 4 characters, it checks if the response starts with "GPT:" or "ACT:".
3. Returns `True` if the response length is less than 4 characters or if it doesn't start with "GPT:" or "ACT:", indicating a failed jailbreak.

**Examples**:

```python
>>> response_jailbroken_failed('ACT: Failed.')
False
>>> response_jailbroken_failed('This is not a jailbroken response.')
True
```

### `set_response_language(prompt)`

**Purpose**: This function detects the language of the user prompt and returns a message indicating the response language.

**Parameters**:

- `prompt` (`dict`): The user prompt.

**Returns**:

- `str`: A message indicating the response language.

**How the Function Works**:

1. Uses the `googletrans` library to detect the language of the prompt content.
2. Returns a string indicating the detected language.

**Examples**:

```python
>>> prompt = {'content': 'Bonjour'}
>>> set_response_language(prompt)
'You will respond in the language: fr. '
```

### `isJailbreak(jailbreak)`

**Purpose**: This function checks if a jailbreak mode is specified and returns the corresponding instructions.

**Parameters**:

- `jailbreak` (`str`): The requested jailbreak mode.

**Returns**:

- `list` | `None`: A list of jailbreak instructions if the mode is valid, `None` otherwise.

**How the Function Works**:

1. Checks if the `jailbreak` parameter is not "Default".
2. If the `jailbreak` mode is not "Default", retrieves the corresponding instructions from the `special_instructions` dictionary.
3. Returns the instructions if found, otherwise returns `None`.

**Examples**:

```python
>>> isJailbreak('Ask anything')
[{'role': 'system', 'content': 'I am a large language model, trained by Google. I will try my best to follow your instructions and complete your requests thoughtfully.'}]
>>> isJailbreak('Default')
None
```