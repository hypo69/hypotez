**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
========================================================================================

Description
-------------------------
The `Airforce` class provides functionality for interacting with the Airforce API for text and image generation. It implements various methods for generating responses from different AI models, including text completion, image generation, and handling streaming responses.

Execution Steps
-------------------------
1. **Initialization**: The class initializes with predefined API endpoints, model defaults, and a set of supported models.
2. **Model Retrieval**: The `get_models` method fetches a list of available models from the API and updates the class attributes with the available models.
3. **Model Mapping**: The `get_model` method maps a model name to its actual identifier used in the API requests.
4. **Response Filtering**: The `_filter_content` and `_filter_response` methods filter out unwanted content from the API responses.
5. **Image Generation**: The `generate_image` method generates images based on the provided prompt, model, size, and seed.
6. **Text Generation**: The `generate_text` method handles text generation, splits long messages into chunks, and filters the generated response.
7. **Async Generator Creation**: The `create_async_generator` method creates an asynchronous generator to stream responses from the API based on the provided parameters.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

# Initialize the Airforce provider
provider = Airforce()

# Get a list of available models
models = provider.get_models()

# Generate a text response using the "llama-3.1-70b-chat" model
messages = [
    {"role": "user", "content": "What is the capital of France?"},
]
response = provider.create_async_generator(model="llama-3.1-70b-chat", messages=messages)

# Process the streamed response
for chunk in response:
    print(chunk)

# Generate an image using the "flux" model
image_response = provider.create_async_generator(model="flux", prompt="A cute cat", size="1024x1024", seed=42)

# Process the image response
for image_chunk in image_response:
    print(image_chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".