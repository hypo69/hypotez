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
This code snippet defines a class `RubiksAI` that provides an asynchronous generator interface for interacting with the Rubiks AI API. It supports various models, stream responses, and custom system messages and history.

Execution Steps
-------------------------
1. The class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, implementing functionalities for asynchronous generators and model handling.
2. It defines various properties related to the API endpoint, supported models, aliases, and capabilities.
3. The `generate_mid` method creates a unique ID string following a specific pattern.
4. The `create_referer` method generates a Referer URL with encoded parameters based on the query (`q`), model (`model`), and unique ID (`mid`).
5. The `create_async_generator` method, a class method, is responsible for creating the asynchronous generator.
    - It takes `model`, `messages`, `proxy`, `web_search`, and `temperature` as parameters.
    - It generates a unique ID, constructs a Referer URL, prepares the request data, and sets headers.
    - It establishes an asynchronous session and sends a POST request to the Rubiks AI API endpoint with the generated data and headers.
    - The response is then handled in a stream-like manner, yielding content chunks and managing search sources, if enabled.

Usage Example
-------------------------
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RubiksAI import RubiksAI

async def main():
    provider = RubiksAI()
    model = "gpt-4o-mini"
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for response in provider.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".