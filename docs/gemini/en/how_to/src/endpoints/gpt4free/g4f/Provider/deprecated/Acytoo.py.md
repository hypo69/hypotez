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
This code snippet defines a class named `Acytoo` that implements an asynchronous generator-based provider for accessing a GPT-like chatbot service. The provider leverages the `aiohttp` library for asynchronous HTTP requests and supports sending messages to the chatbot and receiving responses in a streaming fashion. The code also includes helper functions for constructing the request headers and payload.

Execution Steps
-------------------------
1. **Initialize the Provider**: Instantiate an `Acytoo` object, which will be used to interact with the chatbot service.
2. **Create Asynchronous Generator**: Call the `create_async_generator` class method on the `Acytoo` object, passing the desired model, messages, and optional parameters like `proxy`.
3. **Send Messages and Receive Responses**: The `create_async_generator` method uses an asynchronous session to send a POST request to the chatbot API endpoint, passing the configured messages and parameters. The response is then streamed, yielding individual message chunks as they become available.
4. **Handle Response Stream**: Use the `yield` keyword to iterate through the response stream and process each message chunk individually.
5. **Close the Session**: The asynchronous session is automatically closed after the response stream has been processed.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Acytoo import Acytoo

# Example usage:
async def main():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    provider = Acytoo()
    async for message in provider.create_async_generator(
        model="gpt-3.5-turbo",
        messages=messages
    ):
        print(f"Chatbot response: {message}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".