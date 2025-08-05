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
This code defines a class `ChatGptEs` that is responsible for interacting with the chatgpt.es website. The class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, which provides the core functionality for asynchronous message generation and model management. The class uses curl_cffi for making HTTP requests with automatic Cloudflare bypass and handles the extraction of necessary parameters for communication with the chatgpt.es API.

Execution Steps
-------------------------
1. The code defines the `ChatGptEs` class with attributes such as `url`, `api_endpoint`, `working`, `supports_stream`, `supports_system_message`, `supports_message_history`, `default_model`, `models`, and `SYSTEM_PROMPT`.
2. It implements the `create_async_generator` class method, which handles the asynchronous message generation process.
3. It uses curl_cffi to make a GET request to the chatgpt.es website, retrieves the necessary information from the HTML response, and extracts `nonce_`, `post_id`, and other parameters.
4. It prepares data for a POST request to the chatgpt.es API using the extracted parameters, `model`, and the formatted message.
5. It sends a POST request to the API with the prepared data using curl_cffi and checks the status code of the response.
6. It processes the JSON response, extracts the generated message, and yields it using the `yield` statement.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import ChatGptEs

messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
]

async def main():
    provider = ChatGptEs()
    async for message in provider.create_async_generator(model='gpt-4o', messages=messages):
        print(message)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".