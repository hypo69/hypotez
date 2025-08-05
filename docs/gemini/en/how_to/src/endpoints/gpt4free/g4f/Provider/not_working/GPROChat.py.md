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
The `GPROChat` class provides an asynchronous generator for interacting with the `gprochat.com` API, allowing for streaming responses from the API.

Execution Steps
-------------------------
1. The `GPROChat` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, implementing methods for asynchronous generation and handling model selections.
2. The `create_async_generator` class method takes parameters such as the model name (`model`), messages (`messages`), and optional proxy (`proxy`).
3. The method formats the prompt using `format_prompt`, generates a signature using `generate_signature`, and sets up headers for the API request.
4. The code makes an asynchronous POST request to the API endpoint (`api_endpoint`) with the formatted prompt, timestamp, and signature.
5. The `response.content.iter_any()` method iterates over chunks of the response, decoding and yielding each chunk asynchronously.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.GPROChat import GPROChat

async def main():
    provider = GPROChat()
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for chunk in provider.create_async_generator(model="gemini-1.5-pro", messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".