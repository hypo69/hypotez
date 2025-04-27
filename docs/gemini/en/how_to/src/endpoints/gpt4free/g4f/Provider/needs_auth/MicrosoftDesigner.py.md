**Instructions for Generating Code Documentation**

How to Use the Microsoft Designer Provider
=========================================================================================

Description
-------------------------
The `MicrosoftDesigner` provider implements an asynchronous generator for generating images using the Microsoft Designer service. It utilizes a HAR file or, if not available, retrieves an access token and user agent dynamically from the browser. It then makes API requests to the Microsoft Designer service to generate images based on the provided prompt. The provider offers various image sizes and incorporates features like image quality control and error handling.

Execution Steps
-------------------------
1. **Initialization**: An instance of `MicrosoftDesigner` is created.
2. **Image Generation**: The `create_async_generator` method is called with a model, messages, and optional parameters like prompt and proxy.
3. **Model Selection**: The desired image model (e.g., `dall-e-3`, `1024x1024`) is chosen.
4. **Prompt Formatting**: The provided messages and optional prompt are formatted for the API request.
5. **Access Token and User Agent**: The provider checks if a HAR file with a valid access token exists; if not, it retrieves an access token and user agent from the browser.
6. **API Request**: The `create_images` function makes a POST request to the Microsoft Designer API with the formatted prompt, access token, user agent, and image size.
7. **Response Handling**: The function handles the API response, potentially polls for updates until image URLs are available, and returns an `ImageResponse` object containing the generated image URLs.
8. **Image Retrieval**: The `ImageResponse` object provides methods for accessing and handling the generated image URLs.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth import MicrosoftDesigner
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example messages for the prompt
messages: Messages = [
    {"role": "user", "content": "Generate an image of a cat playing piano."}
]

# Initialize the provider
provider = MicrosoftDesigner()

# Generate an image using the default model
async for image_response in provider.create_async_generator(
    model="dall-e-3",
    messages=messages
):
    # Access the generated image URLs
    image_urls = image_response.images

    # Do something with the image URLs (e.g., download, display)
    for url in image_urls:
        print(f"Image URL: {url}")
```

```python