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
The code block defines a `Upstage` class that implements an asynchronous generator for interacting with the Upstage AI API. It provides methods to generate text responses from different Upstage models and allows for asynchronous stream handling.

Execution Steps
-------------------------
1. **Class Definition**: The `Upstage` class is defined, inheriting from `AsyncGeneratorProvider` and `ProviderModelMixin`. It defines the base URL for the Upstage AI API, the default model, and a list of available models.

2. **Model Selection**: The `get_model` class method handles the selection of the appropriate model based on the provided model name. It checks for exact matches or aliases and defaults to the `default_model` if no match is found.

3. **Async Generator Creation**: The `create_async_generator` class method creates an asynchronous generator for generating text responses from the Upstage API. It takes the model name, user messages, and optional proxy settings as input.

4. **API Request**: Inside the method, an API request is made to the Upstage API endpoint using `aiohttp.ClientSession`. The request includes the selected model, user messages, and streaming option.

5. **Stream Handling**: The response from the API is handled as a stream. Each line of the response is decoded, and if it contains text data, it is yielded to the caller, building the complete response in `response_text`. 

6. **Error Handling**: The code includes `try-except` blocks to handle potential JSON decoding errors during stream processing.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Upstage import Upstage

async def main():
    provider = Upstage()
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    async for response_chunk in provider.create_async_generator(model="solar-pro", messages=messages):
        print(response_chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".