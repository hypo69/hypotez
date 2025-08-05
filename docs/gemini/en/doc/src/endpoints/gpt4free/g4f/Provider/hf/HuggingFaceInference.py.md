# HuggingFaceInference Module

## Overview

This module provides the `HuggingFaceInference` class, which allows for interaction with the Hugging Face inference API. It uses the `AsyncGeneratorProvider` and `ProviderModelMixin` classes from the `hypotez` project, enabling asynchronous generation of text or images based on user prompts. The module leverages the `StreamSession` class for handling asynchronous requests and provides methods for fetching model data from the Hugging Face API and processing user input.

## Classes

### `HuggingFaceInference`

**Description**: This class implements the interaction with the Hugging Face inference API, allowing for asynchronous generation of text or images based on user prompts.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:
- `url` (str): Base URL for Hugging Face.
- `parent` (str): Parent provider name.
- `working` (bool): Indicates whether the provider is active.
- `default_model` (str): Default model name.
- `default_image_model` (str): Default image model name.
- `model_aliases` (dict): Model aliases mapping.
- `image_models` (list): List of supported image models.
- `model_data` (dict): Cache for model data fetched from the Hugging Face API.

**Methods**:
- `get_models()`: Fetches the list of supported models from the Hugging Face API and caches them for future use.
- `get_model_data(session: StreamSession, model: str)`: Retrieves model information from the Hugging Face API, caching it for subsequent use.
- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, timeout: int = 600, api_base: str = "https://api-inference.huggingface.co", api_key: str = None, max_tokens: int = 1024, temperature: float = None, prompt: str = None, action: str = None, extra_data: dict = {}, seed: int = None, aspect_ratio: str = None, width: int = None, height: int = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for processing user prompts and generating responses using the selected Hugging Face model.

## Functions

### `format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str`:

**Purpose**: Formats the user prompt for Mistral models.

**Parameters**:
- `messages` (Messages): List of messages in the conversation.
- `do_continue` (bool): Flag indicating whether to continue the conversation.

**Returns**:
- `str`: Formatted prompt for the Mistral model.

**How the Function Works**:
- Extracts the user's last message and the system messages from the conversation.
- Constructs a prompt string for the Mistral model, combining the user's last message with the system messages.

**Examples**:
```python
>>> messages = [
...     {'role': 'user', 'content': 'What is the capital of France?'},
...     {'role': 'assistant', 'content': 'The capital of France is Paris.'},
... ]
>>> format_prompt_mistral(messages)
'<s>[INST]What is the capital of France? [/INST] The capital of France is Paris.</s>'
```

### `format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str`:

**Purpose**: Formats the user prompt for Qwen models.

**Parameters**:
- `messages` (Messages): List of messages in the conversation.
- `do_continue` (bool): Flag indicating whether to continue the conversation.

**Returns**:
- `str`: Formatted prompt for the Qwen model.

**How the Function Works**:
- Constructs a prompt string for the Qwen model, incorporating the user's messages and special delimiters.

**Examples**:
```python
>>> messages = [
...     {'role': 'user', 'content': 'What is the meaning of life?'},
...     {'role': 'assistant', 'content': 'The meaning of life is 42.'},
... ]
>>> format_prompt_qwen(messages)
'<|im_start|>user\nWhat is the meaning of life?\n<|im_end|>\n<|im_start|>assistant\nThe meaning of life is 42.\n<|im_end|>\n<|im_start|>assistant\n'
```

### `format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str`:

**Purpose**: Formats the user prompt for Qwen-2 models.

**Parameters**:
- `messages` (Messages): List of messages in the conversation.
- `do_continue` (bool): Flag indicating whether to continue the conversation.

**Returns**:
- `str`: Formatted prompt for the Qwen-2 model.

**How the Function Works**:
- Constructs a prompt string for the Qwen-2 model, incorporating the user's messages and special delimiters.

**Examples**:
```python
>>> messages = [
...     {'role': 'user', 'content': 'What is the capital of France?'},
...     {'role': 'assistant', 'content': 'The capital of France is Paris.'},
... ]
>>> format_prompt_qwen2(messages)
'<｜User｜>What is the capital of France?<｜end of sentence｜><｜Assistant｜>The capital of France is Paris.<｜end of sentence｜><｜Assistant｜>'
```

### `format_prompt_llama(messages: Messages, do_continue: bool = False) -> str`:

**Purpose**: Formats the user prompt for Llama models.

**Parameters**:
- `messages` (Messages): List of messages in the conversation.
- `do_continue` (bool): Flag indicating whether to continue the conversation.

**Returns**:
- `str`: Formatted prompt for the Llama model.

**How the Function Works**:
- Constructs a prompt string for the Llama model, incorporating the user's messages and special delimiters.

**Examples**:
```python
>>> messages = [
...     {'role': 'user', 'content': 'What is the weather like today?'},
...     {'role': 'assistant', 'content': 'The weather is sunny and warm.'},
... ]
>>> format_prompt_llama(messages)
'<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWhat is the weather like today?\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n\nThe weather is sunny and warm.\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n\n'
```

### `format_prompt_custom(messages: Messages, end_token: str = "</s>", do_continue: bool = False) -> str`:

**Purpose**: Formats the user prompt for models with a custom end-of-text token.

**Parameters**:
- `messages` (Messages): List of messages in the conversation.
- `end_token` (str): Custom end-of-text token.
- `do_continue` (bool): Flag indicating whether to continue the conversation.

**Returns**:
- `str`: Formatted prompt for the model.

**How the Function Works**:
- Constructs a prompt string using the specified end-of-text token for the model.

**Examples**:
```python
>>> messages = [
...     {'role': 'user', 'content': 'What is the capital of Italy?'},
...     {'role': 'assistant', 'content': 'The capital of Italy is Rome.'},
... ]
>>> format_prompt_custom(messages, end_token="</s>")
'<|user|>\nWhat is the capital of Italy?</s>\n<|assistant|>\nThe capital of Italy is Rome.</s>\n<|assistant|>\n'
```

### `get_inputs(messages: Messages, model_data: dict, model_type: str, do_continue: bool = False) -> str`:

**Purpose**: Generates the input prompt based on the model type and conversation messages.

**Parameters**:
- `messages` (Messages): List of messages in the conversation.
- `model_data` (dict): Model data dictionary.
- `model_type` (str): Model type, e.g., "gpt2", "mistral", "llama".
- `do_continue` (bool): Flag indicating whether to continue the conversation.

**Returns**:
- `str`: Input prompt for the model.

**How the Function Works**:
- Determines the appropriate prompt formatting based on the model type.
- Uses specific prompt formatting functions for Mistral, Qwen, Qwen-2, Llama, and other models.

**Examples**:
```python
>>> messages = [
...     {'role': 'user', 'content': 'What is the population of London?'},
...     {'role': 'assistant', 'content': 'The population of London is approximately 9 million.'},
... ]
>>> model_data = {'config': {'tokenizer_config': {'eos_token': '</s>'}}}
>>> get_inputs(messages, model_data, model_type='gpt2')
'<|user|>\nWhat is the population of London?</s>\n<|assistant|>\nThe population of London is approximately 9 million.</s>\n'
```

## Parameter Details

- `messages` (Messages): List of messages in the conversation, each message containing a role (e.g., "user", "assistant") and the corresponding content.
- `model` (str): Name of the Hugging Face model to use for generation, e.g., "gpt2", "mistral", "llama".
- `stream` (bool): Flag indicating whether to stream the response or generate it all at once. Default is `True`.
- `proxy` (str): URL of the proxy server to use.
- `timeout` (int): Request timeout in seconds.
- `api_base` (str): Base URL for the Hugging Face inference API.
- `api_key` (str): Hugging Face API key for authentication.
- `max_tokens` (int): Maximum number of tokens to generate in the response.
- `temperature` (float): Sampling temperature to control the randomness of the generated response.
- `prompt` (str): Optional custom prompt to use for generation.
- `action` (str): Optional action to perform, e.g., "continue" for continuing the conversation.
- `extra_data` (dict): Additional data to pass to the model.
- `seed` (int): Optional seed for random number generation.
- `aspect_ratio` (str): Aspect ratio for image generation, e.g., "16:9".
- `width` (int): Width of the generated image.
- `height` (int): Height of the generated image.
- `**kwargs`: Additional keyword arguments.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceInference import HuggingFaceInference
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Create an instance of the HuggingFaceInference class
provider = HuggingFaceInference()

# Define conversation messages
messages: Messages = [
    {'role': 'user', 'content': 'What is the meaning of life?'},
    {'role': 'assistant', 'content': 'The meaning of life is 42.'},
]

# Generate a response using the 'gpt2' model
async for chunk in provider.create_async_generator(model='gpt2', messages=messages):
    print(chunk)

# Generate an image using the 'stable-diffusion-xl' model
async for chunk in provider.create_async_generator(model='stabilityai/stable-diffusion-xl', messages=messages, stream=False):
    print(chunk)
```
```markdown