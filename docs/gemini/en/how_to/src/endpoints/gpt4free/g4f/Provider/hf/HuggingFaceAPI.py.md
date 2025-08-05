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
This code snippet defines the `HuggingFaceAPI` class, which implements a provider for using Hugging Face models within the `hypotez` project. It handles model selection, fetching model mapping information, and creating an asynchronous generator for interacting with the Hugging Face API.

Execution Steps
-------------------------
1. The `HuggingFaceAPI` class inherits from the `OpenaiTemplate` class, providing a base structure and common methods for interacting with APIs.
2. It defines class attributes like `label`, `parent`, `url`, `api_base`, `working`, and `needs_auth` to identify the provider and its characteristics.
3. It establishes default models, model aliases, and fallback models for different types of tasks, including text generation and vision.
4. The `provider_mapping` attribute stores a dictionary mapping model names to their corresponding Hugging Face API endpoints and tasks.
5. The `get_model` method handles model name conversions and aliases.
6. The `get_models` method dynamically fetches a list of available models from Hugging Face.
7. The `get_mapping` method retrieves the mapping information for a specified model from the Hugging Face API.
8. The `create_async_generator` method constructs an asynchronous generator to interact with the Hugging Face API for model requests. It iterates over different providers within the model mapping, selects the appropriate API endpoint and task, and yields a `ProviderInfo` object for each provider.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceAPI import HuggingFaceAPI

# Initialize the Hugging Face API provider
api = HuggingFaceAPI()

# Get a list of available models
models = api.get_models()

# Get the mapping information for a specific model
model_mapping = api.get_mapping("google/gemma-3-27b-it")

# Create an asynchronous generator to interact with the API
async def generate_text(messages: Messages):
    async for chunk in api.create_async_generator(model="google/gemma-3-27b-it", messages=messages):
        print(chunk)

# Usage in a function
async def my_function(messages):
    # Create an asynchronous generator
    async for chunk in generate_text(messages):
        print(chunk)

# Example usage with a list of messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you. How can I help you?"},
]
my_function(messages)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".