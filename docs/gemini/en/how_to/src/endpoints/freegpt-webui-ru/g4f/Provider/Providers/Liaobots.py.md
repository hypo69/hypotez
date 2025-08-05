**Instructions for Generating Code Documentation**

How to Use the Liaobots Provider for FreeGPT
========================================================================================

Description
-------------------------
This code defines a provider class for FreeGPT using the Liaobots API. It allows users to interact with the GPT-3.5-turbo and GPT-4 models provided by Liaobots.

Execution Steps
-------------------------
1. **Import Necessary Modules**: Imports required modules like `os`, `uuid`, `requests`, and type definitions from the `typing` module.
2. **Define Provider Configuration**: Sets up the provider's basic information like URL, supported models, streaming capabilities, and authentication requirements.
3. **Define Model Configurations**: Creates a dictionary mapping model names to their respective configurations (e.g., ID, name, maximum length, token limit).
4. **Implement `_create_completion` Function**: This function handles sending requests to the Liaobots API for text generation.
    - **Construct Headers**: Builds headers for the API request, including authentication information.
    - **Prepare JSON Data**: Creates a JSON object containing the conversation ID, model ID, messages, and prompt.
    - **Send Request**: Sends a POST request to the Liaobots API with the prepared JSON data.
    - **Stream Responses**: Iterates through the streamed response and yields decoded tokens for text generation.
5. **Print Function Parameters**: Logs the parameters passed to the `_create_completion` function.

Usage Example
-------------------------

```python
from g4f.Provider.Providers.Liaobots import _create_completion

# Example usage:
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking!"},
]

response = _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth="your_api_key")

for token in response:
    print(token, end="")
```