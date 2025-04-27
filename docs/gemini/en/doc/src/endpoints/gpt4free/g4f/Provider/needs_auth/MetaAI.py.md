# Meta AI Provider 

## Overview

This module provides the `MetaAI` class, a subclass of `AsyncGeneratorProvider` and `ProviderModelMixin`, which is used to interact with the Meta AI API. It handles authentication, sending prompts, and retrieving responses from the Meta AI model.

## Details

The `MetaAI` class is designed to function as an asynchronous generator provider for the Meta AI model. It leverages the Meta AI API for generating responses based on given prompts. The class handles authentication using cookies, access tokens, and  `lsd` and `dtsg` values obtained from the Meta AI website. 

## Classes

### `MetaAI`

**Description:** Class for interacting with the Meta AI API.
**Inherits:**
- `AsyncGeneratorProvider`: Provides asynchronous generation capabilities for the Meta AI model.
- `ProviderModelMixin`: Provides common functionality for model providers.

**Attributes:**
- `label`: Identifies the provider as "Meta AI".
- `url`: Specifies the base URL of the Meta AI website.
- `working`: Indicates the provider's status, currently set to `True`.
- `default_model`: The default model name, set to 'meta-ai'.
- `session`: A `ClientSession` object for making HTTP requests.
- `cookies`: A dictionary storing cookies used for authentication.
- `access_token`: An access token for the Meta AI API.

**Methods:**

- `create_async_generator`: Creates an asynchronous generator for the Meta AI model.
- `update_access_token`: Updates the access token for the Meta AI API.
- `prompt`: Sends a prompt to the Meta AI API and returns an asynchronous generator for responses.
- `update_cookies`: Updates cookies used for authentication.
- `fetch_sources`: Retrieves sources related to a specific fetch ID.
- `extract_value`: Extracts a specific value from a string.
- `generate_offline_threading_id`: Generates a unique offline threading ID.

## Class Methods

### `create_async_generator`
**Purpose:** Creates an asynchronous generator to interact with the Meta AI model.
**Parameters:**
- `model` (str): The name of the Meta AI model.
- `messages` (Messages): A list of messages representing the conversation history.
- `proxy` (str): Optional proxy server address.
- `**kwargs`: Other keyword arguments.

**Returns:**
- `AsyncResult`: An asynchronous generator that yields response chunks.

**How the Function Works:**
- Initializes a `MetaAI` instance using the provided model, messages, and proxy.
- Calls the `prompt` method to send the formatted messages as a prompt to the Meta AI API.
- Iterates over the response chunks from the `prompt` method and yields each chunk asynchronously.

### `update_access_token`

**Purpose:** Updates the access token for the Meta AI API.
**Parameters:**
- `birthday` (str, optional): Date of birth in the format "YYYY-MM-DD". Defaults to "1999-01-01".

**Returns:**
- `None`

**How the Function Works:**
- Sends a POST request to the Meta AI API's GraphQL endpoint to accept terms of service and obtain a temporary access token.
- Sets the `access_token` attribute with the obtained token.

### `prompt`

**Purpose:** Sends a prompt to the Meta AI API and returns an asynchronous generator for responses.
**Parameters:**
- `message` (str): The prompt to be sent to the Meta AI model.
- `cookies` (Cookies, optional): Optional cookies for authentication. Defaults to `None`.

**Returns:**
- `AsyncResult`: An asynchronous generator that yields response chunks.

**How the Function Works:**
- Checks if cookies are provided. If not, updates cookies by calling `update_cookies`.
- If no access token is available and no cookies are provided, updates the access token by calling `update_access_token`.
- Sends a POST request to the Meta AI API's GraphQL endpoint with the provided message and necessary headers.
- Parses the response stream for text and image data.
- Yields each chunk of text and image data asynchronously.

### `update_cookies`

**Purpose:** Updates cookies used for authentication.
**Parameters:**
- `cookies` (Cookies, optional): Optional cookies for authentication. Defaults to `None`.

**Returns:**
- `None`

**How the Function Works:**
- Sends a GET request to the Meta AI website to retrieve cookies.
- Extracts `_js_datr`, `abra_csrf`, and `datr` cookies from the response text.
- Updates the `cookies` attribute with the retrieved cookies.
- Extracts `lsd` and `dtsg` values from the response text.
- Sets the `lsd` and `dtsg` attributes with the extracted values.


### `fetch_sources`

**Purpose:** Retrieves sources related to a specific fetch ID.
**Parameters:**
- `fetch_id` (str): The fetch ID for which sources are to be retrieved.

**Returns:**
- `Sources`: An object containing a list of sources.

**How the Function Works:**
- Sends a POST request to the Meta AI API's GraphQL endpoint with the provided fetch ID.
- Parses the response text for sources.
- Returns a `Sources` object containing the retrieved sources.

### `extract_value`

**Purpose:** Extracts a specific value from a string.
**Parameters:**
- `text` (str): The string from which to extract the value.
- `key` (str, optional): The key associated with the value to be extracted. Defaults to `None`.
- `start_str` (str, optional): The starting string delimiter. Defaults to `None`.
- `end_str` (str, optional): The ending string delimiter. Defaults to `\'`,\'.

**Returns:**
- `str`: The extracted value.

**How the Function Works:**
- Finds the starting and ending positions of the desired value within the text using the provided delimiters.
- Returns the substring between the start and end positions.

### `generate_offline_threading_id`

**Purpose:** Generates a unique offline threading ID.
**Parameters:**
- `None`

**Returns:**
- `str`: The generated offline threading ID.

**How the Function Works:**
- Generates a random 64-bit integer.
- Gets the current timestamp in milliseconds.
- Combines the timestamp and random value to create a unique identifier.
- Returns the identifier as a string.