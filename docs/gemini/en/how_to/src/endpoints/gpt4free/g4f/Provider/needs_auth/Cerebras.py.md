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
This code defines a class `Cerebras` which extends the `OpenaiAPI` class. It provides methods to interact with the Cerebras Inference API, including authentication and model interaction. 

Execution Steps
-------------------------
1. The `Cerebras` class initializes the base URL, login URL, API base URL, and other important properties.
2. The `create_async_generator` method takes a model name, messages, an optional API key, and cookies as input.
3. If no API key is provided, the method attempts to retrieve it from cookies stored locally.
4. If cookies are not available, the method makes a request to the Cerebras Inference API to authenticate and retrieve a demo API key.
5. Once the API key is obtained, it calls the parent `create_async_generator` method of `OpenaiAPI` to generate an asynchronous generator of model responses.
6. This generator yields chunks of text as they become available.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Cerebras import Cerebras

async def main():
    # Create a Cerebras instance
    cerebras = Cerebras()

    # Example model and messages
    model = "llama3.1-70b"
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]

    # Get an asynchronous generator of responses
    async for chunk in cerebras.create_async_generator(model, messages):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".