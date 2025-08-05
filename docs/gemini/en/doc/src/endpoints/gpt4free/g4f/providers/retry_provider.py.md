# Retry Provider for GPT4Free

## Overview

This module provides a retry provider mechanism for GPT4Free, designed to enhance reliability and flexibility in utilizing various providers for generating completions. The `IterListProvider` and `RetryProvider` classes facilitate the use of multiple providers and implement retry strategies for handling provider failures.

## Details

This module plays a crucial role in the GPT4Free system by providing a layer of resilience against potential provider failures. The implementation utilizes a list of providers that are iterated through when generating completions. If one provider encounters an error, the system automatically tries the next provider in the list. This approach ensures that completions can still be generated even if a specific provider is unavailable or experiencing issues. 

The module also introduces the `RetryProvider` class, which implements a retry mechanism for a single provider. If a provider fails to generate a completion, the `RetryProvider` will retry the same provider up to a specified number of times before moving on to the next provider. This feature allows for more persistent attempts to obtain a completion from a specific provider, potentially increasing success rates.

## Classes

### `class IterListProvider`

**Description**: This class provides an abstraction for iterating over a list of providers and attempting to generate completions using each provider until a successful completion is achieved. This approach allows for flexible usage of different GPT4Free providers.

**Inherits**: `BaseRetryProvider`

**Attributes**:

- `providers` (List[Type[BaseProvider]]): A list of provider classes to be used for generating completions.

- `shuffle` (bool): A flag indicating whether to shuffle the order of providers in the list. Defaults to `True`.

- `working` (bool): A flag indicating whether the provider is currently operational.

- `last_provider` (Type[BaseProvider]): The last provider that was used for generating completions.

**Methods**:

#### `create_completion(model: str, messages: Messages, stream: bool = False, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> CreateResult`

**Purpose**: This method generates a completion using available providers, with an option to stream the response. 

**Parameters**:

- `model` (str): The model to be used for completion.

- `messages` (Messages): The messages to be used for generating completion.

- `stream` (bool, optional): Flag to indicate if the response should be streamed. Defaults to `False`.

- `ignore_stream` (bool, optional): Flag to indicate whether to ignore the stream flag if the provider does not support streaming. Defaults to `False`.

- `ignored` (list[str], optional): A list of provider names to be ignored. Defaults to `[]`.

- `kwargs`: Additional keyword arguments to be passed to the provider's completion function.

**Yields**:

- `CreateResult`: Tokens or results from the completion.

**Raises**:

- `Exception`: Any exception encountered during the completion process.

#### `create_async_generator(model: str, messages: Messages, stream: bool = True, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> AsyncResult`

**Purpose**: This method generates a completion asynchronously using available providers, with an option to stream the response. 

**Parameters**:

- `model` (str): The model to be used for completion.

- `messages` (Messages): The messages to be used for generating completion.

- `stream` (bool, optional): Flag to indicate if the response should be streamed. Defaults to `True`.

- `ignore_stream` (bool, optional): Flag to indicate whether to ignore the stream flag if the provider does not support streaming. Defaults to `False`.

- `ignored` (list[str], optional): A list of provider names to be ignored. Defaults to `[]`.

- `kwargs`: Additional keyword arguments to be passed to the provider's async completion function.

**Yields**:

- `AsyncResult`: Tokens or results from the asynchronous completion.

**Raises**:

- `Exception`: Any exception encountered during the asynchronous completion process.

#### `get_create_function(self) -> callable`

**Purpose**: This method returns the completion function for the provider.

**Returns**:

- `callable`: The completion function.

#### `get_async_create_function(self) -> callable`

**Purpose**: This method returns the asynchronous completion function for the provider.

**Returns**:

- `callable`: The asynchronous completion function.

#### `get_providers(self, stream: bool, ignored: list[str]) -> list[ProviderType]`

**Purpose**: This method retrieves a list of providers that meet specific criteria, such as supporting streaming or not being ignored.

**Parameters**:

- `stream` (bool): Flag to indicate if the provider should support streaming.

- `ignored` (list[str]): A list of provider names to be ignored.

**Returns**:

- `list[ProviderType]`: A list of providers that meet the specified criteria.

### `class RetryProvider`

**Description**: This class extends the `IterListProvider` functionality by implementing a retry mechanism for a single provider. It allows for multiple attempts to generate a completion using the same provider before switching to another provider.

**Inherits**: `IterListProvider`

**Attributes**:

- `single_provider_retry` (bool): A flag indicating whether to retry a single provider if it fails. Defaults to `False`.

- `max_retries` (int): The maximum number of retries for a single provider. Defaults to `3`.

**Methods**:

#### `create_completion(model: str, messages: Messages, stream: bool = False, **kwargs) -> CreateResult`

**Purpose**: This method generates a completion using available providers, with an option to stream the response. If `single_provider_retry` is set to `True`, the method will retry the first provider in the list up to `max_retries` times before moving on to other providers.

**Parameters**:

- `model` (str): The model to be used for completion.

- `messages` (Messages): The messages to be used for generating completion.

- `stream` (bool, optional): Flag to indicate if the response should be streamed. Defaults to `False`.

- `kwargs`: Additional keyword arguments to be passed to the provider's completion function.

**Yields**:

- `CreateResult`: Tokens or results from the completion.

**Raises**:

- `Exception`: Any exception encountered during the completion process.

#### `create_async_generator(model: str, messages: Messages, stream: bool = True, **kwargs) -> AsyncResult`

**Purpose**: This method generates a completion asynchronously using available providers, with an option to stream the response. If `single_provider_retry` is set to `True`, the method will retry the first provider in the list up to `max_retries` times before moving on to other providers.

**Parameters**:

- `model` (str): The model to be used for completion.

- `messages` (Messages): The messages to be used for generating completion.

- `stream` (bool, optional): Flag to indicate if the response should be streamed. Defaults to `True`.

- `kwargs`: Additional keyword arguments to be passed to the provider's async completion function.

**Yields**:

- `AsyncResult`: Tokens or results from the asynchronous completion.

**Raises**:

- `Exception`: Any exception encountered during the asynchronous completion process.

## Functions

### `raise_exceptions(exceptions: dict) -> None`

**Purpose**: This function raises a combined exception if any occurred during retries.

**Parameters**:

- `exceptions` (dict): A dictionary containing exceptions encountered by different providers during retries.

**Raises**:

- `RetryProviderError`: If any provider encountered an exception.

- `RetryNoProviderError`: If no provider is found.

## How the Retry Provider Works

The Retry Provider operates by maintaining a list of GPT4Free providers. When a completion request is received, it iterates through this list, attempting to generate a completion using each provider. If a provider fails, it records the exception and moves on to the next provider. If no provider is successful, the Retry Provider raises an exception.

The `RetryProvider` class extends this behavior by implementing a retry mechanism for a single provider. If a provider fails to generate a completion, the `RetryProvider` will retry the same provider up to a specified number of times before moving on to the next provider.

This approach allows for more robust and reliable access to GPT4Free capabilities, even if individual providers experience temporary issues. By handling provider failures gracefully, the Retry Provider ensures that the overall GPT4Free system remains resilient and continues to provide reliable service.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.retry_provider import RetryProvider
from hypotez.src.endpoints.gpt4free.g4f.providers import OpenAIProvider, GPT4AllProvider

providers = [OpenAIProvider, GPT4AllProvider]

# Create a RetryProvider instance with a maximum of 3 retries for a single provider
retry_provider = RetryProvider(providers, single_provider_retry=True, max_retries=3)

# Generate a completion using the RetryProvider
completion = retry_provider.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello, world!'}]))

# Print the generated completion
print(completion)
```

In this example, we create a `RetryProvider` instance with two providers: `OpenAIProvider` and `GPT4AllProvider`. The `single_provider_retry` flag is set to `True`, and the `max_retries` value is set to `3`. This means that if the first provider (in this case, `OpenAIProvider`) fails to generate a completion, the `RetryProvider` will retry it up to three times before moving on to the next provider.

The `create_completion` method is used to generate a completion, passing in the desired model (`gpt-3.5-turbo`) and the user message. If the first provider fails, the `RetryProvider` will retry it up to three times, and if it still fails, it will move on to the `GPT4AllProvider`. If both providers fail, the `RetryProvider` will raise an exception.

## Conclusion

The Retry Provider is a vital component of the GPT4Free system, ensuring that completions can be generated reliably even if individual providers encounter issues. It leverages a list of providers and implements a retry mechanism to handle failures gracefully, ultimately contributing to the robustness and resilience of the overall system.