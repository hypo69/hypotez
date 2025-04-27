# MicrosoftDesigner Provider

## Overview

The `MicrosoftDesigner` class is a provider for generating images using the Microsoft Designer API. This class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, which provide asynchronous generation capabilities and model management features respectively.

## Details

The `MicrosoftDesigner` provider leverages Microsoft Designer's API to generate images from text prompts. It utilizes the "Dall-E 3" model by default, but allows the user to select different image sizes like "1024x1024", "1024x1792", and "1792x1024". 

The provider uses a `HAR` file containing authentication tokens and user-agent information for the Microsoft Designer API. If no valid `HAR` file is found, it attempts to retrieve the tokens and user-agent asynchronously from the browser.

## Classes

### `class MicrosoftDesigner`

**Description:** A provider for generating images using the Microsoft Designer API.

**Inherits:**
    - `AsyncGeneratorProvider`: Provides asynchronous generation capabilities.
    - `ProviderModelMixin`: Provides model management features.

**Attributes:**
    - `label` (str): "Microsoft Designer"
    - `url` (str): "https://designer.microsoft.com"
    - `working` (bool): `True`
    - `use_nodriver` (bool): `True`
    - `needs_auth` (bool): `True`
    - `default_image_model` (str): "dall-e-3"
    - `image_models` (list): ["dall-e-3", "1024x1024", "1024x1792", "1792x1024"]
    - `models` (list): same as `image_models`

**Methods:**

    - `create_async_generator()`: Creates an asynchronous generator for generating images.
    - `generate()`: Generates images using the Microsoft Designer API.

#### `create_async_generator()`

**Purpose:** Creates an asynchronous generator for generating images.

**Parameters:**
    - `model` (str): The model to use for generation (e.g., "dall-e-3", "1024x1024", "1024x1792", "1792x1024").
    - `messages` (Messages): A list of messages representing the conversation history.
    - `prompt` (str, optional): The text prompt for image generation. Defaults to `None`.
    - `proxy` (str, optional): The proxy server to use for network requests. Defaults to `None`.
    - `kwargs`: Additional keyword arguments.

**Returns:**
    - `AsyncResult`: An asynchronous result containing the generated image.

**How the Function Works:**

1. Extracts the image size from the `model` argument.
2. Yields the result of calling the `generate()` method with the formatted prompt, image size, and proxy.

#### `generate()`

**Purpose:** Generates images using the Microsoft Designer API.

**Parameters:**
    - `prompt` (str): The text prompt for image generation.
    - `image_size` (str): The desired image size (e.g., "1024x1024", "1024x1792", "1792x1024").
    - `proxy` (str, optional): The proxy server to use for network requests. Defaults to `None`.

**Returns:**
    - `ImageResponse`: An object containing the generated image and the prompt.

**Raises Exceptions:**
    - `NoValidHarFileError`: If no valid `HAR` file is found containing authentication tokens.

**How the Function Works:**

1. Attempts to read authentication tokens and the user-agent from a `HAR` file.
2. If the `HAR` file is not found or invalid, attempts to retrieve the tokens and user-agent asynchronously from the browser.
3. Calls the `create_images()` method to generate images using the retrieved credentials.
4. Returns an `ImageResponse` object containing the generated images and the prompt.

## Functions

### `create_images()`

**Purpose:** Generates images using the Microsoft Designer API with the provided credentials.

**Parameters:**
    - `prompt` (str): The text prompt for image generation.
    - `access_token` (str): The access token for the Microsoft Designer API.
    - `user_agent` (str): The user-agent string for the request.
    - `image_size` (str): The desired image size (e.g., "1024x1024", "1024x1792", "1792x1024").
    - `proxy` (str, optional): The proxy server to use for network requests. Defaults to `None`.
    - `seed` (int, optional): A random seed for image generation. Defaults to `None`.

**Returns:**
    - list: A list of generated image URLs.

**How the Function Works:**

1. Generates a random seed if none is provided.
2. Constructs a request with the provided parameters and data.
3. Sends the request to the Microsoft Designer API.
4. Polls the API for generated images until they are available.
5. Returns a list of generated image URLs.

### `readHAR()`

**Purpose:** Reads authentication tokens and the user-agent from a `HAR` file.

**Parameters:**
    - `url` (str): The URL of the website from which to retrieve the tokens.

**Returns:**
    - tuple: A tuple containing the access token and the user-agent.

**Raises Exceptions:**
    - `NoValidHarFileError`: If no valid `HAR` file is found containing authentication tokens.

**How the Function Works:**

1. Iterates through a list of `HAR` files.
2. Parses the JSON content of each file.
3. Extracts the access token and user-agent from the `HAR` file entry corresponding to the provided URL.
4. Returns the retrieved token and user-agent.

### `get_access_token_and_user_agent()`

**Purpose:** Retrieves the access token and user-agent asynchronously from the browser.

**Parameters:**
    - `url` (str): The URL of the website from which to retrieve the tokens.
    - `proxy` (str, optional): The proxy server to use for network requests. Defaults to `None`.

**Returns:**
    - tuple: A tuple containing the access token and the user-agent.

**How the Function Works:**

1. Launches a headless browser using `get_nodriver` function and navigates to the specified URL.
2. Extracts the user-agent from the browser.
3. Searches for the access token in the browser's local storage.
4. Returns the retrieved access token and user-agent.

## Parameter Details

**General Parameters:**

- `prompt` (str): The text prompt used to generate the image. It should be a clear and concise description of the desired image.
- `model` (str): The model to use for image generation. The default model is "dall-e-3," but the following image sizes are also available: "1024x1024," "1024x1792," "1792x1024."
- `image_size` (str): The desired image size. It should be a string representing the width and height of the image, separated by an "x," like "1024x1024."
- `proxy` (str, optional): A proxy server that can be used for network requests. This parameter is optional. 
- `seed` (int, optional): A random seed for image generation. This parameter is optional.

**Specific Parameters:**

- `access_token` (str): The access token for the Microsoft Designer API. This token is required to access the API and generate images.
- `user_agent` (str): The user-agent string for the request. This string identifies the browser used to make the request.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth import MicrosoftDesigner

# Example 1: Generate an image using the default Dall-E 3 model with a custom prompt
prompt = "A beautiful sunset over a tropical beach"
images = await MicrosoftDesigner.generate(prompt=prompt, image_size="1024x1024")

# Example 2: Generate an image with a specific image size
prompt = "A futuristic city skyline"
images = await MicrosoftDesigner.generate(prompt=prompt, image_size="1792x1024")

# Example 3: Use a proxy server for network requests
prompt = "A portrait of a dog wearing a hat"
images = await MicrosoftDesigner.generate(prompt=prompt, image_size="1024x1024", proxy="http://myproxy.com:8080")
```