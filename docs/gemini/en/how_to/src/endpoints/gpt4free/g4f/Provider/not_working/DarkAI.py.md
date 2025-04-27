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
This code block defines a class called `DarkAI` that represents a provider for the DarkAI chatbot. 

It implements the following:
  - **`AsyncGeneratorProvider`**: Provides a way to asynchronously generate responses from the DarkAI API.
  - **`ProviderModelMixin`**:  Provides a way to interact with different models (e.g., `gpt-4o`, `gpt-3.5-turbo`, `llama-3-70b`). 

Execution Steps
-------------------------
1. **Initialize a `DarkAI` instance**:
    - The code creates an instance of the `DarkAI` class, representing an interaction with the DarkAI chatbot service.
2. **Specify the desired model**:
    - The `model` parameter selects which model to use (e.g., `gpt-4o`, `gpt-3.5-turbo`, `llama-3-70b`).
3. **Provide the messages for the conversation**:
    - The `messages` parameter contains the history of the conversation as a list of dictionaries, each dictionary representing a message (user or assistant).
4. **Configure Optional Parameters**:
    - `proxy`: Specifies a proxy to use for making the API request (optional).
5. **Async Request**:
    - The `create_async_generator` method initiates a request to the DarkAI API, sending the conversation history and model choice.
6. **Stream Response**:
    - The API response is processed in a streaming manner, yielding text chunks as they are received.
7. **Process the Response**:
    - The code handles the response, parsing the received data to extract text chunks and stream them as an asynchronous generator.
8. **Error Handling**:
    - The code includes error handling mechanisms to gracefully manage unexpected situations.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.DarkAI import DarkAI
from hypotez.src.endpoints.gpt4free.g4f.Provider.helper import format_prompt

# Define the conversation history (messages)
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you! How can I help you today?"},
]

# Create a DarkAI instance and set the model
provider = DarkAI(model='gpt-4o')

# Generate the response
async def main():
    async for chunk in provider.create_async_generator(messages=messages):
        print(chunk)

# Run the asynchronous function
asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".