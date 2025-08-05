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
This code block defines a `Cromicle` class, which is a subclass of `AsyncGeneratorProvider`, designed to interact with a GPT-like API provided by Cromicle.

Execution Steps
-------------------------
1. The `Cromicle` class initializes its `url` attribute with the Cromicle API endpoint URL.
2. The `create_async_generator` class method is used to generate asynchronous responses from the Cromicle API. 
   - It takes the desired `model`, `messages` (a list of chat messages), and optional `proxy` settings.
   - It establishes an asynchronous HTTP session with custom headers using `aiohttp`.
   - It sends a POST request to the Cromicle API endpoint with formatted prompt data.
   - It handles the response asynchronously, iterating through the streaming content and yielding decoded chunks of the response.
3. The `_create_header` function generates the necessary headers for the API request, including `accept` and `content-type`.
4. The `_create_payload` function constructs the JSON payload for the API request, including the formatted `message`, a fixed `token`, and a SHA256 hash generated from the token and message.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Cromicle import Cromicle

# Define the model and messages
model = "gpt-3.5-turbo"
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking. How can I assist you today?"},
]

# Create an async generator for the Cromicle API
async_generator = Cromicle.create_async_generator(model=model, messages=messages)

# Iterate through the asynchronous responses and process the results
async for stream in async_generator:
    print(stream)  # Process the stream, for example, display the response
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".