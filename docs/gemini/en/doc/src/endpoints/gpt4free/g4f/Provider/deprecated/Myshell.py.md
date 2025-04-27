# Myshell Provider

## Overview

This module provides a `Myshell` class that implements an asynchronous generator provider for interacting with the Myshell.ai API. It enables sending messages and receiving responses from the Myshell chatbot through a WebSocket connection.

## Details

The `Myshell` class inherits from `AsyncGeneratorProvider` and provides functionality for establishing a WebSocket connection to the Myshell.ai API, sending messages, and receiving responses. It supports different models, including `samantha`, `gpt-3.5-turbo`, and `gpt-4`, and provides a mechanism for generating a visitor ID and a signature for each message.

## Classes

### `Myshell`

**Description**: This class implements an asynchronous generator provider for interacting with the Myshell.ai API. It establishes a WebSocket connection, sends chat messages, and receives responses from the chatbot.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url (str)`: The base URL for the Myshell.ai API.
- `working (bool)`: Indicates whether the provider is currently working.
- `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports the `gpt-3.5-turbo` model.
- `supports_gpt_4 (bool)`: Indicates whether the provider supports the `gpt-4` model.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 90, **kwargs) -> AsyncResult`: This method establishes a WebSocket connection to the Myshell.ai API, sends the given `messages` to the chatbot, and returns an asynchronous generator that yields responses from the chatbot.

## Functions

### `generate_timestamp() -> str`

**Purpose**: This function generates a timestamp in milliseconds as a string.

**Parameters**: None

**Returns**: `str`: The timestamp in milliseconds as a string.

**How the Function Works**:

1.  Obtains the current time in seconds using `time.time()`.
2.  Multiplies the time by 1000 to convert it to milliseconds.
3.  Converts the milliseconds to a string.
4.  Calculates a checksum based on the last digit of the timestamp.
5.  Concatenates the timestamp with the checksum and returns the result as a string.

**Examples**:

```python
>>> generate_timestamp()
'1688638229982'
```

### `generate_signature(text: str)`

**Purpose**: This function generates a signature for a given text message.

**Parameters**:

- `text (str)`: The text message for which to generate a signature.

**Returns**: `dict`: A dictionary containing the signature, timestamp, and version.

**How the Function Works**:

1.  Generates a timestamp using the `generate_timestamp()` function.
2.  Creates a data string by concatenating the version, text message, timestamp, and a secret key.
3.  Calculates the MD5 hash of the data string.
4.  Reverses the hash and stores it as the signature.
5.  Returns a dictionary containing the signature, timestamp, and version.

**Examples**:

```python
>>> generate_signature("Hello, world!")
{'signature': 'a53704d78478e8248d69046a12208898', 'timestamp': '1688638230033', 'version': 'v1.0.0'}
```

### `xor_hash(B: str)`

**Purpose**: This function calculates a XOR hash of a given string.

**Parameters**:

- `B (str)`: The string for which to calculate the XOR hash.

**Returns**: `str`: The XOR hash in hexadecimal format.

**How the Function Works**:

1.  Initializes an empty list `r` and a variable `i` to 0.
2.  Iterates through each character in the string `B`.
3.  Converts each character to its ASCII code and inserts it into the beginning of the list `r`.
4.  If the length of `r` is greater than or equal to 4, it calculates a value `i` by performing a XOR operation on `i` and the first 4 elements of `r`. Then clears the list `r`.
5.  If `r` is not empty after iterating through all characters, it calculates a value `i` by performing a XOR operation on `i` and the remaining elements of `r`.
6.  Converts the final value of `i` to hexadecimal format and returns it as a string.

**Examples**:

```python
>>> xor_hash("Hello, world!")
'9043d586'
```

### `performance() -> str`

**Purpose**: This function calculates a performance value based on the current time.

**Parameters**: None

**Returns**: `str`: The performance value in hexadecimal format.

**How the Function Works**:

1.  Obtains the current time in milliseconds using `time.time() * 1000`.
2.  Starts a loop that continues as long as the current time remains the same.
3.  Increments a counter `e` within the loop.
4.  Returns the hexadecimal representations of the initial time and the counter `e` concatenated together.

**Examples**:

```python
>>> performance()
'16886382301770000'
```

### `generate_visitor_id(user_agent: str) -> str`

**Purpose**: This function generates a unique visitor ID based on the user agent string.

**Parameters**:

- `user_agent (str)`: The user agent string to use for generating the visitor ID.

**Returns**: `str`: The unique visitor ID as a string.

**How the Function Works**:

1.  Calculates a performance value using the `performance()` function.
2.  Generates a random 16-character hexadecimal string.
3.  Calculates a XOR hash of the user agent string using the `xor_hash()` function.
4.  Calculates the hexadecimal representation of the screen resolution (1080 x 1920).
5.  Concatenates the performance value, random string, XOR hash, screen resolution, and performance value again, separated by hyphens.
6.  Returns the concatenated string as the visitor ID.

**Examples**:

```python
>>> generate_visitor_id("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
'16886382301770000-a42635-9043d586-43200-16886382301770000'
```

## Parameter Details

- `model (str)`: The name of the language model to use for the chat session. Currently supported models are `samantha`, `gpt-3.5-turbo`, and `gpt-4`.
- `messages (Messages)`: A list of chat messages to send to the chatbot.
- `proxy (str, optional)`: A proxy server URL to use for connecting to the Myshell.ai API. Defaults to `None`.
- `timeout (int, optional)`: The timeout in seconds for connecting to the WebSocket server. Defaults to `90`.

## Examples

```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

```python
# Example of using Myshell to send a message and receive a response
async def main():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    async for response in Myshell.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

This example demonstrates how to use the `Myshell` class to establish a WebSocket connection, send a message, and receive a response. The `create_async_generator()` method returns an asynchronous generator that yields responses from the chatbot. The example code iterates over the generator and prints each response received.

## Conclusion

The `Myshell` class provides a convenient way to interact with the Myshell.ai API through a WebSocket connection. It supports various language models and provides a mechanism for generating a visitor ID and signature for each message. The class is designed to be used asynchronously, allowing for efficient communication with the chatbot.