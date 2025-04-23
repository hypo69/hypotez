# Module for interaction with the Raycast service.

## Overview

The module contains the `Raycast` class, which is used to interact with the Raycast service to obtain text completions based on specified models and messages.

## More details

This module allows you to use the Raycast service for generating text completions. It supports specifying a model, sending messages, and streaming the results. To use this module, you need an authentication token from Raycast, which should be passed in the `auth` parameter.

## Classes

### `Raycast`

**Description**: The class for interacting with the Raycast service to get text completions.

**Inherits**:
- `AbstractProvider`: Inherits from the abstract provider class.

**Attributes**:
- `url` (str): The base URL for the Raycast service.
- `supports_stream` (bool): A flag indicating whether the provider supports streaming responses.
- `needs_auth` (bool): A flag indicating whether the provider requires authentication.
- `working` (bool): A flag indicating whether the provider is currently working.
- `models` (list): A list of supported models.

**Working principle**:
The `Raycast` class defines the settings and methods for interacting with the Raycast service. It uses the `requests` library to send POST requests to the Raycast API endpoint. The class requires an authentication token to work. It also supports streaming responses, which allows receiving text completions in real-time.

## Class Methods

### `create_completion`

```python
def create_completion(
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    **kwargs,
) -> CreateResult:
    """Function generates text completions based on the specified model and messages using the Raycast service.

    Args:
        model (str): The name of the model to use for generating the completion.
        messages (Messages): A list of messages to send to the model.
        stream (bool): A flag indicating whether to stream the response.
        proxy (str, optional): The proxy server to use for the request. Defaults to `None`.
        **kwargs: Additional keyword arguments, including the authentication token (`auth`).

    Returns:
        CreateResult: A generator that yields text tokens as they are received from the Raycast service.

    Raises:
        ValueError: If the authentication token is not provided.

    Example:
        >>> auth_token = "YOUR_AUTH_TOKEN"
        >>> messages = [{"role": "user", "content": "Hello, Raycast!"}]
        >>> for token in Raycast.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth=auth_token):
        ...     print(token, end="")
        Hello! How can I assist you today?
    """
```

## Class Parameters

- `model` (str): The model to use for the completion.
- `messages` (Messages): The messages to be sent to the model.
- `stream` (bool): Whether to stream the response.
- `proxy` (str, optional): Proxy server URL. Defaults to `None`.
- `kwargs` (dict): Additional keyword arguments. The `auth` parameter must be passed in `kwargs`.

**Examples**:
```python
auth_token = "YOUR_AUTH_TOKEN"
messages = [{"role": "user", "content": "Hello, Raycast!"}]

# Example of calling the function with the necessary parameters
for token in Raycast.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth=auth_token):
    print(token, end="")