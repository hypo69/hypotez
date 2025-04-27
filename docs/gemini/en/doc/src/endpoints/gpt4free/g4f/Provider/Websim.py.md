# Websim.py

## Overview

This module provides the `Websim` class, which is a provider for the GPT-4 Free API. It allows for the creation of a `Websim` object that can be used to generate responses from the GPT-4 Free AI model. The class implements methods for both chat and image generation requests.

## Details

The `Websim` class extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes, enabling it to handle asynchronous requests and model selection. The class utilizes the `aiohttp` library for making asynchronous requests to the GPT-4 Free API. It supports features such as system messages, message history, and stream responses.

## Classes

### `Websim`

**Description**: The `Websim` class is a provider for the GPT-4 Free API, enabling communication with the GPT-4 Free AI model for both chat and image generation.

**Inherits**:
  - `AsyncGeneratorProvider`: For asynchronous request handling.
  - `ProviderModelMixin`: For model selection and management.

**Attributes**:

  - `url` (str): The base URL for the GPT-4 Free API.
  - `login_url` (str): The login URL for the GPT-4 Free API.
  - `chat_api_endpoint` (str): The API endpoint for chat requests.
  - `image_api_endpoint` (str): The API endpoint for image generation requests.
  - `working` (bool): Indicates whether the provider is operational.
  - `needs_auth` (bool): Indicates whether the provider requires authentication.
  - `use_nodriver` (bool): Indicates whether the provider uses a headless browser.
  - `supports_stream` (bool): Indicates whether the provider supports stream responses.
  - `supports_system_message` (bool): Indicates whether the provider supports system messages.
  - `supports_message_history` (bool): Indicates whether the provider supports message history.
  - `default_model` (str): The default model for chat requests.
  - `default_image_model` (str): The default model for image generation requests.
  - `image_models` (list): A list of available models for image generation requests.
  - `models` (list): A list of available models for both chat and image generation requests.

**Methods**:

  - `generate_project_id(for_image=False)`: Generates a unique project ID for requests.
  - `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", project_id: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator to process chat or image requests.
  - `_handle_image_request(project_id: str, messages: Messages, prompt: str, aspect_ratio: str, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Handles image generation requests.
  - `_handle_chat_request(project_id: str, messages: Messages, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Handles chat requests.

## Functions

### `generate_project_id(for_image=False)`

**Purpose**: Generates a unique project ID for chat and image generation requests.

**Parameters**:

  - `for_image` (bool, optional): Indicates whether the project ID is for an image generation request. Defaults to `False`.

**Returns**:

  - `str`: A unique project ID in the appropriate format for chat or image generation.

**How the Function Works**:

  - The function generates a random string of characters using `string.ascii_lowercase` and `string.digits`.
  - For chat requests, the project ID is formatted like `ke3_xh5gai3gjkmruomu`.
  - For image generation requests, the project ID is formatted like `kx0m131_rzz66qb2xoy7`.

**Examples**:

  ```python
  >>> Websim.generate_project_id()
  'ke3_xh5gai3gjkmruomu'

  >>> Websim.generate_project_id(for_image=True)
  'kx0m131_rzz66qb2xoy7'
  ```

### `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", project_id: str = None, **kwargs) -> AsyncResult`

**Purpose**: Creates an asynchronous generator to process chat or image generation requests based on the provided model, messages, and other parameters.

**Parameters**:

  - `model` (str): The model to use for the request.
  - `messages` (Messages): A list of messages for the conversation.
  - `prompt` (str, optional): The prompt for the request. Defaults to `None`.
  - `proxy` (str, optional): A proxy to use for the request. Defaults to `None`.
  - `aspect_ratio` (str, optional): The aspect ratio for image generation requests. Defaults to "1:1".
  - `project_id` (str, optional): A project ID for the request. Defaults to `None`.
  - `**kwargs`: Additional keyword arguments to pass to the API request.

**Returns**:

  - `AsyncResult`: An asynchronous generator that yields the responses from the GPT-4 Free API.

**How the Function Works**:

  - The function first determines if the request is for image generation based on the specified model.
  - If a project ID is not provided, it generates a unique project ID using the `generate_project_id` function.
  - It sets the appropriate headers for the request, including a `referer` header based on the type of request.
  - The function then handles the request based on its type:
    - For image generation requests, it calls the `_handle_image_request` method.
    - For chat requests, it calls the `_handle_chat_request` method.

**Examples**:

  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "Hello, how are you?"},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='gemini-1.5-pro', messages=messages):
  ...         print(response)

  >>> asyncio.run(main())
  I'm doing well, thank you for asking! How can I help you today?
  ```

### `_handle_image_request(project_id: str, messages: Messages, prompt: str, aspect_ratio: str, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: Handles image generation requests using the `image_api_endpoint`.

**Parameters**:

  - `project_id` (str): The project ID for the request.
  - `messages` (Messages): A list of messages for the conversation.
  - `prompt` (str): The prompt for the image generation request.
  - `aspect_ratio` (str): The aspect ratio for the generated image.
  - `headers` (dict): The headers for the API request.
  - `proxy` (str, optional): A proxy to use for the request. Defaults to `None`.
  - `**kwargs`: Additional keyword arguments to pass to the API request.

**Returns**:

  - `AsyncResult`: An asynchronous generator that yields an `ImageResponse` object containing the generated image URL.

**How the Function Works**:

  - The function uses the `aiohttp` library to send a POST request to the `image_api_endpoint` with the provided parameters.
  - The request body includes the project ID, the prompt, and the aspect ratio.
  - The response is checked for errors using the `raise_for_status` function.
  - If the request is successful, the generated image URL is extracted from the response and yielded as an `ImageResponse` object.

**Examples**:

  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "Generate an image of a cat."},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='flux', messages=messages):
  ...         print(response)

  >>> asyncio.run(main())
  <ImageResponse object at ...>
  ```

### `_handle_chat_request(project_id: str, messages: Messages, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: Handles chat requests using the `chat_api_endpoint`.

**Parameters**:

  - `project_id` (str): The project ID for the request.
  - `messages` (Messages): A list of messages for the conversation.
  - `headers` (dict): The headers for the API request.
  - `proxy` (str, optional): A proxy to use for the request. Defaults to `None`.
  - `**kwargs`: Additional keyword arguments to pass to the API request.

**Returns**:

  - `AsyncResult`: An asynchronous generator that yields the generated text response.

**How the Function Works**:

  - The function uses the `aiohttp` library to send a POST request to the `chat_api_endpoint` with the provided parameters.
  - The request body includes the project ID and the messages.
  - The response is checked for errors using the `raise_for_status` function.
  - If the request is successful, the generated text response is extracted from the response and yielded as a string.
  - The function includes retry logic to handle rate limiting issues, retrying up to three times with exponential backoff.

**Examples**:

  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "What is the meaning of life?"},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='gemini-1.5-pro', messages=messages):
  ...         print(response)

  >>> asyncio.run(main())
  The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one definitive answer, as the meaning of life is subjective and personal. Some people find meaning in their relationships, their work, their hobbies, or their spiritual beliefs. Others find meaning in helping others, making a difference in the world, or simply experiencing the beauty of life. Ultimately, the meaning of life is up to each individual to decide.
  ```

## Parameter Details

- `model` (str): The model to use for the request. It should be one of the supported models, like `gemini-1.5-pro` or `flux`.
- `messages` (Messages): A list of messages for the conversation. Each message is a dictionary with keys `role` (user or assistant) and `content` (the message text).
- `prompt` (str, optional): The prompt for the request. It is used for both chat and image generation requests. 
- `proxy` (str, optional): A proxy to use for the request. This is useful if you are behind a firewall or need to route requests through a specific proxy server.
- `aspect_ratio` (str, optional): The aspect ratio for image generation requests. It determines the proportions of the generated image.
- `project_id` (str, optional): A project ID for the request. It is generated automatically if not provided. 

## Examples

- **Chat Request**:
  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "What is the capital of France?"},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='gemini-1.5-pro', messages=messages):
  ...         print(response)

  >>> asyncio.run(main())
  The capital of France is Paris.
  ```

- **Image Generation Request**:
  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "Generate an image of a cat sitting on a couch."},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='flux', messages=messages):
  ...         print(response)

  >>> asyncio.run(main())
  <ImageResponse object at ...>
  ```

- **Using Proxy**:
  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "What is the weather like in London?"},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='gemini-1.5-pro', messages=messages, proxy='http://your-proxy-server:port'):
  ...         print(response)

  >>> asyncio.run(main())
  # ... the response from the GPT-4 Free model
  ```

- **Specifying Aspect Ratio for Image Generation**:
  ```python
  >>> async def main():
  ...     messages = [
  ...         {"role": "user", "content": "Generate an image of a landscape."},
  ...     ]
  ...     async for response in Websim.create_async_generator(model='flux', messages=messages, aspect_ratio='16:9'):
  ...         print(response)

  >>> asyncio.run(main())
  <ImageResponse object at ...>
  ```