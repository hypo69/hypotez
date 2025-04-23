# Module `types.py`

## Overview

This module defines abstract base classes for providers used in the `gpt4free` package. It includes base classes for standard providers and providers with retry logic. The module also defines a type alias for provider types.

## More details

This module defines the basic structure for creating different providers, including those with retry functionality. It ensures that all providers have a consistent interface. This facilitates easy switching and management of different providers within the system.

## Classes

### `BaseProvider`

**Description**: Abstract base class for a provider. Serves as the base for all specific provider implementations.

**Attributes**:
- `url` (str): URL of the provider.
- `working` (bool): Indicates whether the provider is currently working.
- `needs_auth` (bool): Indicates whether the provider requires authentication.
- `supports_stream` (bool): Indicates whether the provider supports streaming.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `params` (str): List of parameters for the provider.

**Working principle**:
This class establishes a common interface for all providers. It defines attributes related to the provider's capabilities and status, and abstract methods that must be implemented by subclasses.

**Methods**:
- `get_create_function()`: Abstract method to get the create function for the provider.
- `get_async_create_function()`: Abstract method to get the async create function for the provider.
- `get_dict()`: Method to get a dictionary representation of the provider.

### `BaseProvider.get_create_function()`

```python
def get_create_function() -> callable:
    """
    Get the create function for the provider.

    Returns:
        callable: The create function.
    """
```

**Purpose**: Abstract method for retrieving the synchronous create function of the provider.

**Parameters**:
- None

**Returns**:
- `callable`: The synchronous create function.

**Raises**:
- `NotImplementedError`: Always raised because this is an abstract method.

**How the function works**:
This function is intended to be overridden in subclasses. It should return a callable that represents the synchronous implementation for creating something (e.g., generating text).

### `BaseProvider.get_async_create_function()`

```python
def get_async_create_function() -> callable:
    """
    Get the async create function for the provider.

    Returns:
        callable: The create function.
    """
```

**Purpose**: Abstract method for retrieving the asynchronous create function of the provider.

**Parameters**:
- None

**Returns**:
- `callable`: The asynchronous create function.

**Raises**:
- `NotImplementedError`: Always raised because this is an abstract method.

**How the function works**:
This function is intended to be overridden in subclasses. It should return a callable that represents the asynchronous implementation for creating something (e.g., generating text).

### `BaseProvider.get_dict()`

```python
def get_dict(cls) -> Dict[str, str]:
    """
    Get a dictionary representation of the provider.

    Returns:
        Dict[str, str]: A dictionary with provider's details.
    """
```

**Purpose**: Returns a dictionary representation of the provider, containing its name, URL, and label.

**Parameters**:
- `cls`: The class itself (`BaseProvider`).

**Returns**:
- `Dict[str, str]`: A dictionary with the provider's details.

**How the function works**:
This class method creates and returns a dictionary that contains the name, URL, and label of the provider. The `getattr` function is used to safely access the `label` attribute, returning `None` if it does not exist.

**Examples**:
```python
provider_dict = BaseProvider.get_dict()
print(provider_dict)
```

### `BaseRetryProvider`

**Description**: Base class for a provider that implements retry logic.

**Inherits**:
- `BaseProvider`: Inherits attributes and methods from `BaseProvider`.

**Attributes**:
- `providers` (List[Type[BaseProvider]]): List of providers to use for retries.
- `shuffle` (bool): Whether to shuffle the providers list.  <next, if any>.
- `exceptions` (Dict[str, Exception]): Dictionary of exceptions encountered.
- `last_provider` (Type[BaseProvider]): The last provider used.

**Working principle**:
This class extends `BaseProvider` and provides a mechanism for retrying requests using a list of different providers. It manages the list of providers, tracks exceptions, and stores the last used provider.

### `Streaming`

**Description**: Class for handling streaming data.

**Attributes**:
- `data` (str): The streaming data.

**Methods**:
- `__str__()`: Returns the streaming data as a string.

**Working principle**:
This class is a simple wrapper around a string, representing streaming data. The `__str__` method allows the object to be easily converted to a string.

### `Streaming.__init__()`

```python
def __init__(self, data: str) -> None:
    """
    Initializes a new instance of the Streaming class.

    Args:
        data (str): The streaming data.
    """
```

**Purpose**: Initializes a new instance of the `Streaming` class.

**Parameters**:
- `data` (str): The streaming data.

**How the function works**:
This is the constructor for the `Streaming` class. It takes a string `data` as input and assigns it to the `self.data` attribute.

### `Streaming.__str__()`

```python
def __str__(self) -> str:
    """
    Returns the streaming data as a string.

    Returns:
        str: The streaming data.
    """
```

**Purpose**: Returns the streaming data as a string.

**Parameters**:
- None

**Returns**:
- `str`: The streaming data.

**How the function works**:
This method returns the streaming data stored in the `self.data` attribute as a string.

## Type Aliases

- `ProviderType` (Union[Type[BaseProvider], BaseRetryProvider]): Represents either a standard provider or a retry provider.