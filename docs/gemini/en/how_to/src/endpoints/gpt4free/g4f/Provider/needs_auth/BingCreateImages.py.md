**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block implements the `BingCreateImages` class, a provider for generating images using the Microsoft Designer service in Bing. It handles authentication, image generation, and response formatting.

Execution Steps
-------------------------
1. **Initialization**:
   - The `BingCreateImages` class is initialized with optional cookies, proxy, and API key.
   - If an API key is provided, it's added to the cookies dictionary.
   - The `cookies` and `proxy` are stored for later use.
2. **Asynchronous Generator**:
   - The `create_async_generator` class method creates an asynchronous generator to handle image generation requests.
   - It initializes a `BingCreateImages` instance with the provided parameters.
   - It formats the prompt using the `format_image_prompt` helper function and then yields the result of the `generate` method.
3. **Image Generation**:
   - The `generate` method fetches cookies from the browser or uses provided cookies.
   - It raises a `MissingAuthError` if the `_U` cookie (API key) is missing.
   - It creates a session using the `create_session` helper function, passing the cookies and proxy.
   - It uses the `create_images` function to generate images based on the prompt.
   - It returns an `ImageResponse` object, containing the generated images, prompt, and preview URLs (if multiple images are generated).

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.BingCreateImages import BingCreateImages

# Example using API key
async def generate_images(api_key: str, prompt: str):
    provider = BingCreateImages(api_key=api_key)
    response = await provider.generate(prompt)
    images = response.images
    # ... process the images

# Example using cookies
async def generate_images_with_cookies(cookies: dict, prompt: str):
    provider = BingCreateImages(cookies=cookies)
    response = await provider.generate(prompt)
    images = response.images
    # ... process the images
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".