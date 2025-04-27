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
The code snippet defines a class `BlackForestLabs_Flux1Schnell` that implements an asynchronous image generation provider using the BlackForestLabs Flux-1-Schnell model hosted on Hugging Face Spaces. It leverages the `aiohttp` library for asynchronous HTTP requests and the `raise_for_status` function for handling potential errors. 

Execution Steps
-------------------------
1. **Initialization**: The class is initialized with the model name, URL, and API endpoint information.
2. **Asynchronous Generator Creation**: The `create_async_generator` class method handles the image generation process.
3. **Prompt Formatting**: The provided message and prompt are combined into a formatted string.
4. **API Request**: A POST request is sent to the API endpoint with the formatted prompt, seed, and other generation parameters.
5. **Event Monitoring**: The code continuously monitors the response, waiting for the "complete" event.
6. **Image URL Extraction**: Once the "complete" event is received, the image URL is extracted from the response data.
7. **Image Response Yielding**: An `ImageResponse` object is created and yielded, containing the image URL and the original prompt.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Schnell import BlackForestLabs_Flux1Schnell

async def generate_image():
    provider = BlackForestLabs_Flux1Schnell()
    messages = [
        {"role": "user", "content": "Generate a picture of a cat sitting on a table"}
    ]
    async for response in provider.create_async_generator(model="flux-schnell", messages=messages):
        print(f"Image URL: {response.images[0]}")

# Run the function asynchronously
import asyncio
asyncio.run(generate_image())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".