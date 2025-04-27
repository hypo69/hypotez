# Vercel Provider for GPT-4Free

## Overview

This module provides the `Vercel` class, which implements the `AbstractProvider` interface and enables interaction with the Vercel AI platform for generating text completions using various AI models. This provider leverages Vercel's `sdk.vercel.ai` API and supports different models, including `gpt-3.5-turbo`, `llama70b-v2-chat`, and `bloom`.

## Details

The `Vercel` provider offers a way to access and utilize Vercel's AI capabilities for text completion tasks. It supports a range of AI models, providing flexibility for users to choose the most suitable option for their needs. This module allows developers to integrate Vercel's AI services into their applications, facilitating text generation, conversation simulation, and other AI-powered tasks.

## Classes

### `class Vercel`

**Description**: This class represents a provider for generating text completions using the Vercel AI platform. It implements the `AbstractProvider` interface and provides methods for creating completions with various supported AI models.

**Inherits**: `AbstractProvider`

**Attributes**:

- `url (str)`: Base URL for the Vercel AI API.
- `working (bool)`: Indicates whether the provider is currently operational.
- `supports_message_history (bool)`: Flag indicating whether the provider supports message history.
- `supports_gpt_35_turbo (bool)`: Flag indicating whether the provider supports the `gpt-3.5-turbo` model.
- `supports_stream (bool)`: Flag indicating whether the provider supports streaming responses.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> CreateResult`: This method is responsible for generating text completions using the specified AI model. It takes a model name, a list of messages, a flag indicating whether to stream the response, an optional proxy server address, and keyword arguments.

### `class ModelInfo`

**Description**: This class represents the information associated with an AI model supported by the Vercel provider.

**Attributes**:

- `id (str)`: The unique identifier for the model within the Vercel platform.
- `default_params (dict[str, Any])`: Default parameters for the model.

## Functions

### `get_anti_bot_token() -> str`

**Purpose**: This function retrieves an anti-bot token from the Vercel platform, ensuring that requests from the provider are not blocked by the API.

**How the Function Works**:

1. The function sends a GET request to the `https://sdk.vercel.ai/openai.jpeg` endpoint with appropriate headers.
2. It decodes the base64-encoded response and extracts relevant data.
3. Using `execjs`, the function executes a JavaScript script to generate the anti-bot token.
4. The token is then encoded in base64 format and returned.

### `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> CreateResult`

**Purpose**: This method is responsible for generating text completions using the specified AI model. It takes a model name, a list of messages, a flag indicating whether to stream the response, an optional proxy server address, and keyword arguments.

**Parameters**:

- `model (str)`: The name of the AI model to use for generating the completion.
- `messages (Messages)`: A list of messages representing the conversation history.
- `stream (bool)`: Flag indicating whether to stream the response.
- `proxy (str, optional)`: The address of a proxy server to use for making API requests. Defaults to `None`.
- `**kwargs`: Additional keyword arguments to be passed to the AI model.

**Returns**:

- `CreateResult`: A dictionary containing the generated response.

**Raises Exceptions**:

- `MissingRequirementsError`: If the `PyExecJS` package is not installed.
- `ValueError`: If the specified model is not supported by the Vercel provider.

**How the Function Works**:

1. It checks if the necessary requirements (`PyExecJS`) are installed.
2. It verifies that the specified model is supported.
3. It prepares the request headers, including an anti-bot token.
4. It constructs the JSON data for the API request, including the model ID, messages, playground ID, chat index, and other model-specific parameters.
5. It performs multiple retries (up to 20) to handle potential network issues.
6. It sends a POST request to the `https://chat.vercel.ai/api/chat` endpoint with the prepared data.
7. It iterates through the streamed response and yields each token as a decoded string.

## Parameter Details

- `model (str)`: The name of the AI model to use for generating the completion. Supported models include:
    - `gpt-3.5-turbo`
    - `replicate/llama70b-v2-chat`
    - `a16z-infra/llama7b-v2-chat`
    - `a16z-infra/llama13b-v2-chat`
    - `replicate/llama-2-70b-chat`
    - `bigscience/bloom`
    - `google/flan-t5-xxl`
    - `EleutherAI/gpt-neox-20b`
    - `OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5`
    - `OpenAssistant/oasst-sft-1-pythia-12b`
    - `bigcode/santacoder`
    - `command-light-nightly`
    - `command-nightly`
    - `code-davinci-002`
    - `text-ada-001`
    - `text-babbage-001`
    - `text-curie-001`
    - `text-davinci-002`
    - `text-davinci-003`

- `messages (Messages)`: A list of messages representing the conversation history. Each message should be a dictionary with the following keys:
    - `role (str)`: The role of the speaker (e.g., 'user', 'assistant').
    - `content (str)`: The text content of the message.

- `stream (bool)`: Flag indicating whether to stream the response. If set to `True`, the method will yield each token of the response as it becomes available.

- `proxy (str, optional)`: The address of a proxy server to use for making API requests. Defaults to `None`.

- `**kwargs`: Additional keyword arguments to be passed to the AI model. These arguments may include:
    - `temperature (float)`: Controls the randomness of the generated text.
    - `maximumLength (int)`: The maximum length of the generated response.
    - `topP (float)`: The probability threshold for sampling from the model's vocabulary.
    - `topK (int)`: The number of top-k candidates to consider for sampling.
    - `presencePenalty (float)`: A penalty for generating tokens that have already appeared in the context.
    - `frequencyPenalty (float)`: A penalty for generating tokens that have appeared frequently in the context.
    - `stopSequences (list[str])`: A list of sequences that signal the end of the response.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vercel import Vercel
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vercel import model_info
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vercel import get_anti_bot_token

# Create an instance of the Vercel provider
provider = Vercel()

# Example of generating text completions using the "gpt-3.5-turbo" model
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
]

# Generate a text completion using the "gpt-3.5-turbo" model
for token in provider.create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

# Example of generating text completions using the "replicate/llama70b-v2-chat" model
messages = [
    {'role': 'user', 'content': 'What is the meaning of life?'},
]

# Generate a text completion using the "replicate/llama70b-v2-chat" model
for token in provider.create_completion(model='replicate/llama70b-v2-chat', messages=messages, stream=True):
    print(token, end='')
```

## Conclusion

The `Vercel` provider provides a robust and versatile mechanism for leveraging Vercel's AI capabilities for text generation and other AI-driven tasks. Its support for various models, streaming responses, and integration with the `AbstractProvider` interface makes it a valuable component for developers working with AI-powered applications.