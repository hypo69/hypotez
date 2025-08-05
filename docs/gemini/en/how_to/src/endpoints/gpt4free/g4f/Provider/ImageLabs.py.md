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
The `ImageLabs` class implements an asynchronous image generation provider using the ImageLabs API. It allows users to generate images based on text prompts and offers various customization options.

Execution Steps
-------------------------
1. **Initialization**: The class defines essential attributes such as the API endpoint, supported features, and default models.
2. **Asynchronous Generator Creation**: The `create_async_generator` class method generates images asynchronously.
    - It takes parameters like `prompt`, `negative_prompt`, `width`, and `height` to customize image generation.
    - It sends a request to the ImageLabs API to start the image generation process.
    - It polls the API for progress updates until the image is generated or an error occurs.
    - It yields an `ImageResponse` object containing the generated image URL.
3. **Model Handling**: The `get_model` class method provides the default model used by the provider.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import ImageLabs

async def generate_image(prompt: str):
    """
    Generates an image using the ImageLabs provider.

    Args:
        prompt (str): The text prompt for the image.

    Returns:
        ImageResponse: The image response containing the generated image URL.
    """

    provider = ImageLabs()
    async for image_response in provider.create_async_generator(prompt=prompt):
        return image_response

# Example usage:
async def main():
    prompt = "A cute cat wearing a hat."
    image_response = await generate_image(prompt)
    print(f"Generated image URL: {image_response.images[0]}")

if __name__ == "__main__":
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".