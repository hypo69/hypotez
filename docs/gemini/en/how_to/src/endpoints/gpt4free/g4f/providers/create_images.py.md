**Instructions for Generating Code Documentation**

How to Use the `CreateImagesProvider` Class
=========================================================================================

Description
-------------------------
The `CreateImagesProvider` class extends the base provider functionality to enable the generation of images within conversational interactions. It intercepts image creation prompts embedded in messages and utilizes image generation functions to produce images.

Execution Steps
-------------------------
1. **Initialization:** The `CreateImagesProvider` is initialized with a base provider, synchronous and asynchronous image generation functions, a system message explaining image generation capabilities, and a flag to indicate whether to include image placeholders in the output.

2. **Message Processing:** The `create_completion` method processes incoming messages, looking for image creation prompts formatted as `<img data-prompt="prompt text">`. When found, it calls the synchronous image generation function to create the image and inserts the generated image data into the output.

3. **Asynchronous Image Generation:** The `create_async` method handles image generation asynchronously. It finds image prompts in messages, calls the asynchronous image generation function, and then replaces the image prompts with the generated image data in the final response.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.providers import CreateImagesProvider
from hypotez.src.endpoints.gpt4free.g4f.providers import OpenAI
from hypotez.src.endpoints.gpt4free.g4f.providers.response import ImageResponse
from hypotez.src.endpoints.gpt4free.g4f.providers.types import ProviderType

# Create a base provider (OpenAI in this example)
base_provider = OpenAI(api_key="YOUR_API_KEY")

# Define image creation functions (placeholder for actual implementation)
def create_images(prompt: str) -> str:
    """
    Example function to generate an image from a prompt.
    """
    return f"<img src='https://example.com/image.png' alt='Generated Image'> "

async def create_images_async(prompt: str) -> str:
    """
    Example asynchronous function to generate an image from a prompt.
    """
    # Asynchronously generate image data
    image_data = await ...
    return f"<img src='data:image/png;base64,{image_data}' alt='Generated Image'> "

# Create an instance of CreateImagesProvider
image_provider = CreateImagesProvider(
    provider=base_provider,
    create_images=create_images,
    create_async=create_images_async
)

# Generate a response with an image
response = image_provider.create_completion(
    model="text-davinci-003",
    messages=[
        {"role": "user", "content": "Generate an image of a cat sitting on a couch."}
    ],
)

# Process the response and retrieve the image
for chunk in response:
    if isinstance(chunk, ImageResponse):
        print(f"Image data: {chunk.content}")
    elif isinstance(chunk, str):
        print(f"Response chunk: {chunk}")
```