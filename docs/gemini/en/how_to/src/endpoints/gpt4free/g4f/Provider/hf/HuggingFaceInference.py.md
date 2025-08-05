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
This code block implements the `HuggingFaceInference` class, which provides a way to interact with Hugging Face models for text generation and image generation. The class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, enabling asynchronous processing and model management.

Execution Steps
-------------------------
1. The code defines the `HuggingFaceInference` class and its attributes:
    - `url`: The base URL for Hugging Face.
    - `parent`: The parent provider, which is "HuggingFace" in this case.
    - `working`: Indicates whether the provider is currently functional.
    - `default_model`: The default text model to use.
    - `default_image_model`: The default image model to use.
    - `model_aliases`: A dictionary mapping model aliases to their actual names.
    - `image_models`: A list of supported image models.
    - `model_data`: A dictionary to store model information retrieved from Hugging Face API.

2. The `get_models` class method retrieves a list of supported models from Hugging Face API. It checks for text generation models and image generation models, adding them to the `models` list.

3. The `get_model_data` class method fetches model data from Hugging Face API, storing it in the `model_data` dictionary for later use.

4. The `create_async_generator` class method is the core method for generating text or images from the model. It receives parameters like model name, messages, and API key. It checks if the model is supported, formats the input prompt, and then sends a request to the Hugging Face API.

5. Depending on the model type and settings, the method handles different types of responses:
    - If the model is a Together model, it directly yields image URLs from the response.
    - If the model is a text generation model, it iterates over the stream response and yields text chunks.
    - If the model is an image generation model, it saves the image response to a file and yields the image path.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceInference import HuggingFaceInference

async def generate_text(model: str, messages: list[dict]) -> list[str]:
    """Generates text using Hugging Face model."""
    provider = HuggingFaceInference(model)
    async for chunk in provider.create_async_generator(model, messages):
        yield chunk
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".