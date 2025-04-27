**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the DeepInfra Class
=========================================================================================

Description
-------------------------
The `DeepInfra` class implements a provider for the `deepinfra.com` API. It allows users to interact with the DeepInfra text and image generation models through a consistent interface, simplifying interactions and reducing code repetition. 

Execution Steps
-------------------------
1. **Initialization**: The class initializes various attributes like the API base URL, default models, and login URL.
2. **Model Retrieval**: The `get_models` and `get_image_models` methods retrieve lists of available text and image models from the DeepInfra API.
3. **Async Generation**: The `create_async_generator` method handles asynchronous generation of text or images based on the selected model and provided prompt.
4. **Image Generation**: The `create_async_image` method handles image generation using the selected model and prompt, sending the request to the DeepInfra API.
5. **Response Handling**: The code parses the response from the API, extracts image URLs, and returns an `ImageResponse` object containing the generated images.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

# Instantiate the DeepInfra provider
deepinfra_provider = DeepInfra()

# Get a list of available models
models = deepinfra_provider.get_models()

# Generate an image
prompt = "A cat sitting on a sunny beach"
image_response = deepinfra_provider.create_async_image(prompt, model="stabilityai/sd3.5")

# Access the generated image URLs
image_urls = image_response.images
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".