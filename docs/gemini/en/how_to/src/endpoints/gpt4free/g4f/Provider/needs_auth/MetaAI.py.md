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
This code block defines a class `MetaAI` that provides access to the Meta AI API. The class implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces, enabling asynchronous communication and handling of provider models.

Execution Steps
-------------------------
1. The `MetaAI` class initializes a client session with the Meta AI API, managing cookies and access tokens.
2. The `create_async_generator` class method is used to create an asynchronous generator that handles communication with the Meta AI API, fetching responses and yielding them as chunks.
3. The `update_access_token` method updates the access token by sending a POST request to the Meta AI API with user-provided birthday information.
4. The `prompt` method sends a message to the Meta AI API, handling authentication, message formatting, and responses. It yields the response text and any generated images.
5. The `update_cookies` method updates the cookies by fetching the Meta AI homepage, extracting necessary cookie values, and storing them in the `cookies` attribute.
6. The `fetch_sources` method fetches sources related to the provided `fetch_id` from the Meta AI API and returns them as a list of dictionaries.
7. The `extract_value` static method is used to extract a specific value from a given text string based on provided parameters.
8. The `generate_offline_threading_id` static method generates a random offline threading ID for use with the Meta AI API.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAI import MetaAI

# Initialize the MetaAI provider
provider = MetaAI()

# Define a list of messages for the chat conversation
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Use the async generator to send messages to the MetaAI API
async for chunk in provider.prompt(format_prompt(messages)):
    # Handle the response chunks
    print(chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".