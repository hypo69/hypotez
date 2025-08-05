# Theb Provider Helper Module

## Overview

This module provides a helper function for interacting with the Theb chatbot API. It handles sending requests to the API and parsing the response to extract the chatbot's generated content. This module is part of the FreeGPT-Webui-Ru project and specifically designed to work with the Theb provider.

## Details

The module primarily utilizes the `curl_cffi` library to send HTTP requests to the Theb chatbot API. It constructs a JSON payload containing the user's prompt and sends it to the API endpoint `/api/chat-process`. The `format` function is used to process chunks of the response, extracting the relevant text content from the chatbot's generated response.

## Functions

### `format`

**Purpose**: This function processes chunks of the chatbot's response, extracting the relevant text content from the chatbot's generated response.

**Parameters**:
- `chunk` (bytes): A chunk of the response data received from the Theb API.

**Returns**:
- `None`: Returns `None` if an error occurs during processing.

**Raises Exceptions**:
- `Exception`: Raises an exception if an error occurs during processing, such as an invalid response format or an error while decoding the data.

**How the Function Works**:

1. The function uses a regular expression to extract the text content from the `chunk` using `findall`. 
2. It extracts the `content` value from the JSON object within the `chunk` using `json.loads`. 
3. If an exception occurs, it prints an error message to the console and returns `None`.

**Examples**:

```python
>>> chunk = b'{"content":"This is the chatbot's response.", "fin":true}'
>>> format(chunk)
This is the chatbot's response.
```

## Inner Functions

### `format`

**Purpose**: This function processes chunks of the chatbot's response, extracting the relevant text content from the chatbot's generated response.

**Parameters**:
- `chunk` (bytes): A chunk of the response data received from the Theb API.

**Returns**:
- `None`: Returns `None` if an error occurs during processing.

**Raises Exceptions**:
- `Exception`: Raises an exception if an error occurs during processing, such as an invalid response format or an error while decoding the data.

**How the Function Works**:

1. The function uses a regular expression to extract the text content from the `chunk` using `findall`. 
2. It extracts the `content` value from the JSON object within the `chunk` using `json.loads`. 
3. If an exception occurs, it prints an error message to the console and returns `None`.

**Examples**:

```python
>>> chunk = b'{"content":"This is the chatbot's response.", "fin":true}'
>>> format(chunk)
This is the chatbot's response.
```