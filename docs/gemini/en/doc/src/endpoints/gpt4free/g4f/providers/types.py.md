# hypotez/src/endpoints/gpt4free/g4f/providers/types.py

## Overview

This module defines the types and base classes for providers used in the `gpt4free` endpoint.

## Details

This module provides the fundamental building blocks for integrating different GPT providers, like OpenAI and Gemini, into the `hypotez` project. It defines base classes and interfaces that govern how providers interact with the system, ensuring consistent behavior and allowing for easy extension with new providers.

## Classes

### `BaseProvider`

**Description**: An abstract base class representing a GPT provider. It defines the common functionality and attributes shared by all providers.

**Attributes**:

- `url` (str): The URL of the provider's API endpoint.
- `working` (bool): Indicates whether the provider is currently functional and accessible.
- `needs_auth` (bool): Whether the provider requires authentication to access its API.
- `supports_stream` (bool): Whether the provider supports streaming responses, allowing for incremental output delivery.
- `supports_message_history` (bool): Whether the provider supports preserving and utilizing previous conversation history.
- `supports_system_message` (bool): Whether the provider allows for setting a system message to provide context for the conversation.
- `params` (str): List of parameters specific to the provider, used for configuration and customization.

**Methods**:

- `get_create_function() -> callable`: Returns the function responsible for creating a new instance of the provider.
- `get_async_create_function() -> callable`: Returns the asynchronous function for creating a new provider instance.
- `get_dict() -> Dict[str, str]`: Returns a dictionary representation of the provider, containing its name, URL, and label.

### `BaseRetryProvider`

**Description**: Base class for providers that implement retry logic. It inherits from `BaseProvider` and adds functionality for handling failures and attempting to connect with alternative providers in a sequence.

**Attributes**:

- `providers` (List[Type[BaseProvider]]): A list of providers to attempt in case of failures.
- `shuffle` (bool): Whether to randomize the order of providers in the retry sequence.
- `exceptions` (Dict[str, Exception]): A dictionary to store exceptions encountered during retries.
- `last_provider` (Type[BaseProvider]): The last provider that was used in the retry sequence.

### `Streaming`

**Description**: This class defines the structure for streaming data, allowing for the incremental delivery of responses from GPT providers.

**Attributes**:

- `data` (str): The content of the stream response, which is continuously updated as new data is received.

**Methods**:

- `__str__() -> str`: Returns the current content of the stream response as a string.

## Parameter Details

- `url` (str): The URL of the provider's API endpoint. This is used to communicate with the provider and send requests.
- `working` (bool): Indicates whether the provider is currently functional and accessible. If `False`, the provider may be unavailable or experiencing technical issues.
- `needs_auth` (bool): Indicates whether the provider requires authentication to access its API. If `True`, users may need to provide credentials before interacting with the provider.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses. This allows for the incremental delivery of output, improving performance and user experience.
- `supports_message_history` (bool): Indicates whether the provider supports preserving and utilizing previous conversation history. If `True`, the provider can maintain context and provide more coherent responses based on past interactions.
- `supports_system_message` (bool): Indicates whether the provider allows for setting a system message to provide context for the conversation. This enables users to define initial instructions and constraints for the AI model.
- `params` (str): List of parameters specific to the provider. This allows for customizing the behavior of the provider, such as setting API keys, configuring output format, or specifying model preferences.

## How the Code Works

This module provides the foundation for integrating GPT providers into the `hypotez` project. By defining base classes like `BaseProvider` and `BaseRetryProvider`, it ensures that all providers follow a consistent structure and behavior. 

The `BaseProvider` class defines the core functionalities that are expected from all providers, such as retrieving the create function, handling authentication, and supporting streaming responses. This standardization makes it easier to manage and extend the project with new providers without major code rewrites. 

The `BaseRetryProvider` further enhances the robustness by implementing retry logic. This means that if one provider fails to provide a response, the system can attempt to use another provider in the sequence, improving the likelihood of success. 

Finally, the `Streaming` class provides a way to manage the incremental delivery of responses from GPT providers. This improves the user experience by allowing users to see partial responses as they are generated, rather than waiting for the entire response to be completed.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import BaseProvider

class MyProvider(BaseProvider):
    """
    Example provider implementation.
    """
    url: str = "https://example.com/api"
    working: bool = True
    needs_auth: bool = False
    supports_stream: bool = False
    supports_message_history: bool = False
    supports_system_message: bool = False
    params: str = ""

    def get_create_function(self) -> callable:
        """
        Returns a function to create a new instance of the provider.
        """
        def create_provider():
            return MyProvider()
        return create_provider

    def get_async_create_function(self) -> callable:
        """
        Returns an asynchronous function to create a new instance of the provider.
        """
        async def create_provider():
            return MyProvider()
        return create_provider
```

This example shows how to implement a custom provider class that inherits from `BaseProvider`. The class must define the necessary attributes and methods, including the `get_create_function` and `get_async_create_function` methods.

## Conclusion

This module plays a critical role in the `gpt4free` endpoint by defining the core types and interfaces for interacting with GPT providers. It promotes consistency and extensibility, allowing for easy integration of new providers and enhancing the overall reliability of the endpoint.