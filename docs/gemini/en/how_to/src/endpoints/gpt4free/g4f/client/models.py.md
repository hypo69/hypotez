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
The `ClientModels` class provides methods for retrieving a list of models available for various tasks, including text generation, vision, and media processing. It utilizes the `ModelUtils` and `ProviderUtils` modules to determine the best provider for a given model or task. 

Execution Steps
-------------------------
1. **Initialization**: The `ClientModels` class is initialized with a `client` object, a `provider` (optional), and a `media_provider` (optional). These providers are used to retrieve model lists from different platforms.
2. **`get()` Method**: This method retrieves the best provider for a given model or task name. It checks both the `ModelUtils.convert` and `ProviderUtils.convert` dictionaries for the specified name and returns the corresponding provider. If the name is not found, it returns a default value.
3. **`get_all()` Method**: This method retrieves a list of all models available from the specified provider. It handles the API key and optional keyword arguments for filtering the model list.
4. **`get_vision()` Method**: This method retrieves a list of vision models available from the specified provider. It first checks the `ModelUtils.convert` dictionary for vision models and then retrieves a list of vision models from the provider.
5. **`get_media()` Method**: This method retrieves a list of media models available from the specified provider. It retrieves a list of models from the provider and optionally filters the list based on keyword arguments.
6. **`get_image()` Method**: This method retrieves a list of image models available from the specified provider. It first checks the `ModelUtils.convert` dictionary for image models and then retrieves a list of image models from the provider.
7. **`get_video()` Method**: This method retrieves a list of video models available from the specified provider. It retrieves a list of models from the provider and filters the list for video models.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.client import Client, ClientModels

# Initialize a Client object
client = Client(api_key="YOUR_API_KEY")

# Initialize a ClientModels object
models = ClientModels(client)

# Get the best provider for the "text-davinci-003" model
provider = models.get("text-davinci-003")

# Get a list of all models available from the provider
all_models = models.get_all(provider=provider)

# Get a list of vision models
vision_models = models.get_vision(provider=provider)

# Get a list of image models
image_models = models.get_image(provider=provider)

# Get a list of video models
video_models = models.get_video(provider=provider)

print(f"Best provider for text-davinci-003: {provider}")
print(f"All models: {all_models}")
print(f"Vision models: {vision_models}")
print(f"Image models: {image_models}")
print(f"Video models: {video_models}")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".