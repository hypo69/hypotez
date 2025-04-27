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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use the AI365VIP Provider

========================================================================================

Description
-------------------------
The `AI365VIP` class provides an asynchronous generator for interacting with the AI365VIP API for generating text using a large language model (LLM). It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to leverage common functionality for interacting with providers.

Execution Steps
-------------------------
1. **Initialization:** The `AI365VIP` class is initialized with default settings, including the base URL, API endpoint, and supported models.
2. **Model Selection:** The `create_async_generator` class method is used to create an asynchronous generator for the specified model. It takes the desired model name, messages to be used as context, and optional parameters such as a proxy server.
3. **Request Preparation:** The method constructs a request to the AI365VIP API, including headers, request body, and proxy settings.
4. **API Interaction:** The request is sent to the API using an asynchronous session. The response is streamed as chunks.
5. **Response Handling:** Each chunk of the response is decoded and yielded from the generator, allowing for streaming the generated text.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AI365VIP import AI365VIP
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages(
    [
        {"role": "user", "content": "Hello, how are you?"},
    ]
)

async def main():
    provider = AI365VIP()
    async for chunk in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk, end='')

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())