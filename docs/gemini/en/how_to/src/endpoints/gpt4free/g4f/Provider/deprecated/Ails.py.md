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
This code block implements the `Ails` class, which is a provider for accessing the AI.ls API. The class extends `AsyncGeneratorProvider` and defines methods for sending messages to the API and receiving responses.

Execution Steps
-------------------------
1. **Initialization**: The `Ails` class initializes key variables such as the API URL, working status, and support for message history and GPT models.
2. **Asynchronous Generator**: The `create_async_generator` method creates an asynchronous generator to handle the communication with the AI.ls API.
3. **Headers Setup**: The method sets up headers for the API request, including authorization, client ID, content type, and user agent.
4. **API Request**: The method sends a POST request to the AI.ls API endpoint `https://api.caipacity.com/v1/chat/completions` with the request body containing the model, temperature, stream flag, messages, and timestamps.
5. **Response Handling**: The method handles the API response, iterating through the response content and extracting tokens from the received JSON data. 
6. **Token Filtering**: The method filters the received tokens to exclude specific strings related to AI.ls or AI.ci, preventing potential errors.
7. **Yield Token**: The method yields the extracted tokens to the asynchronous generator.
8. **Hash Calculation**: The `_hash` function calculates a SHA256 hash based on the timestamp, message content, and a predefined string.
9. **Timestamp Formatting**: The `_format_timestamp` function modifies the provided timestamp to ensure a consistent format.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Ails import Ails

# Initialize the provider
provider = Ails()

# Define the messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you!"},
]

# Create an asynchronous generator
async_generator = await provider.create_async_generator(
    model="gpt-3.5-turbo", messages=messages, stream=True
)

# Iterate through the generator and print the received tokens
async for token in async_generator:
    print(token)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".