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
The `MagickPen` class provides an asynchronous generator for interacting with the MagickPen API, a free GPT-4 alternative. 

Execution Steps
-------------------------
1. **Fetch API Credentials**: The `fetch_api_credentials` class method retrieves the necessary API credentials from the MagickPen website by extracting data from a JavaScript file.
2. **Create Async Generator**: The `create_async_generator` method initializes an asynchronous generator that interacts with the MagickPen API.
3. **Set Headers**: The method sets required headers, including API secret, timestamp, nonce, and signature, for authorization.
4. **Format Prompt**: The user prompt is formatted for the API request using the `format_prompt` helper function.
5. **Send API Request**: The code sends a POST request to the MagickPen API endpoint with the formatted prompt and authentication data.
6. **Stream Response**: The response is streamed in chunks, decoding each chunk and yielding it to the generator.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen

async def main():
    provider = MagickPen()
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    async for chunk in provider.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(chunk, end='')

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".