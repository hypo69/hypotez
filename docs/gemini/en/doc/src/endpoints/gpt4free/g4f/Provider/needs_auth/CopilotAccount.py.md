# CopilotAccount Provider

## Overview

This module defines the `CopilotAccount` class, which represents a provider for the Copilot model requiring authentication. It extends the base `AsyncAuthedProvider` class and implements the `Copilot` interface for accessing Copilot's functionality. This provider leverages HAR files for authentication and provides a mechanism to handle cases where authentication is required but no valid HAR file is available.

## Details

The `CopilotAccount` provider uses HAR files for authentication. If a valid HAR file is found, it extracts the access token and cookies for authentication. If no valid HAR file exists, it attempts to authenticate using a web driver, prompting the user for login credentials.

## Classes

### `CopilotAccount`

**Description**: This class represents a Copilot provider that requires authentication. It extends the base `AsyncAuthedProvider` class and implements the `Copilot` interface. It leverages HAR files for authentication and provides a mechanism to handle cases where authentication is required but no valid HAR file is available.

**Inherits**: `AsyncAuthedProvider`, `Copilot`

**Attributes**:

- `needs_auth`: Boolean value indicating whether authentication is required (always `True` for this provider).
- `use_nodriver`: Boolean value indicating whether to use a web driver for authentication (defaults to `True`).
- `parent`: String value representing the parent provider (always "Copilot").
- `default_model`: String value representing the default model (always "Copilot").
- `default_vision_model`: String value representing the default vision model (always "Copilot").

**Methods**:

#### `on_auth_async(proxy: str = None, **kwargs) -> AsyncIterator`

**Purpose**: This method handles the authentication process asynchronously. It tries to read the access token and cookies from a HAR file. If no valid HAR file exists, it either prompts the user for login credentials using a web driver (if `use_nodriver` is `True`) or raises an exception.

**Parameters**:

- `proxy`: Optional string value representing the proxy to use for network requests.

**Returns**:

- `AsyncIterator`: An asynchronous iterator that yields either a `RequestLogin` object (if a web driver is needed) or an `AuthResult` object (if authentication is successful).

**Raises**:

- `NoValidHarFileError`: If no valid HAR file is found and `use_nodriver` is `False`.

#### `create_authed(model: str, messages: Messages, auth_result: AuthResult, **kwargs) -> AsyncResult`

**Purpose**: This method creates an authenticated completion request to the Copilot API. It uses the access token and cookies provided in the `auth_result` object to make the request.

**Parameters**:

- `model`: String value representing the Copilot model to use.
- `messages`: A list of messages to send to the model.
- `auth_result`: An `AuthResult` object containing the access token and cookies.

**Returns**:

- `AsyncResult`: An asynchronous result object that yields the responses from the Copilot API.

**How the Function Works**:

- The method retrieves the access token and cookies from the `auth_result` object.
- It sets the `Copilot._access_token` and `Copilot._cookies` attributes for future requests.
- It calls the `Copilot.create_completion()` method to generate a completion request.
- It yields each chunk of the completion response.
- After the completion request is finished, it updates the cookies in the `auth_result` object.

**Examples**:

```python
# Assuming the 'auth_result' object contains valid access token and cookies
async def use_copilot(messages: Messages):
    provider = CopilotAccount()
    async for chunk in provider.create_authed(model="copilot", messages=messages, auth_result=auth_result):
        print(chunk)
```


## Inner Functions

### `cookies_to_dict()`

**Purpose**: This function converts a list of cookies (as obtained from the HAR file or web driver) into a dictionary where the keys are cookie names and the values are cookie values.

**Returns**:

- `dict`: A dictionary containing cookie names and values.

**How the Function Works**:

- It checks if `Copilot._cookies` is a dictionary. If it is, it returns the dictionary as is.
- Otherwise, it iterates through each cookie in `Copilot._cookies` and creates a dictionary where the key is the cookie name and the value is the cookie value.

**Examples**:

```python
cookies = [
    { "name": "sessionid", "value": "abcdef1234567890" },
    { "name": "user_id", "value": "12345" },
]
cookie_dict = cookies_to_dict()
print(cookie_dict) # Output: {'sessionid': 'abcdef1234567890', 'user_id': '12345'}
```

## Parameter Details

- `auth_result`: An `AuthResult` object containing the access token and cookies necessary for authentication.
- `proxy`: A string value representing the proxy to use for network requests.

## Examples

```python
# Example usage with a valid HAR file
async def use_copilot_with_har():
    provider = CopilotAccount()
    auth_result = await provider.authenticate()
    messages = [
        { "role": "user", "content": "Write a Python function to reverse a string" }
    ]
    async for chunk in provider.create_authed(model="copilot", messages=messages, auth_result=auth_result):
        print(chunk)

# Example usage with a web driver for authentication (if no valid HAR file exists)
async def use_copilot_with_webdriver():
    provider = CopilotAccount()
    async for auth_result in provider.authenticate():
        if isinstance(auth_result, RequestLogin):
            # Handle the login request using a web driver
            # ...
        else:
            # Use the authenticated provider
            messages = [
                { "role": "user", "content": "Write a Python function to reverse a string" }
            ]
            async for chunk in provider.create_authed(model="copilot", messages=messages, auth_result=auth_result):
                print(chunk)
```