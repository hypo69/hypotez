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
The code block implements the `DDG` class, which is an asynchronous generator provider for interacting with the DuckDuckGo AI Chat service. It utilizes the `AsyncGeneratorProvider` and `ProviderModelMixin` base classes to provide a robust interface for making API requests and handling responses.

Execution Steps
-------------------------
1. **Initialize and Validate Model:**
    - The `validate_model` method checks if the provided model name is supported or uses a default model if none is specified.
2. **Fetch Default Cookies:**
    - The `get_default_cookies` method obtains initial cookies required for API requests by sending a GET request to the DuckDuckGo AI Chat URL.
3. **Fetch `fe_version`:**
    - The `fetch_fe_version` method fetches the `fe-version` from the initial page load, which is essential for subsequent API requests.
4. **Fetch VQD Token and Hash:**
    - The `fetch_vqd_and_hash` method retrieves the required VQD token and hash for the chat session. It retries the request multiple times if necessary.
5. **Create Asynchronous Generator:**
    - The `create_async_generator` method is the core functionality of the class. It generates a stream of responses from the DuckDuckGo AI Chat service.
    - **Step 1**: Ensures the `fe_version` is fetched.
    - **Step 2**: Initializes or updates the conversation based on provided messages and cookies.
    - **Step 3**: Fetches the VQD token and hash if the conversation is new.
    - **Step 4**: Constructs request headers, including the `x-fe-version`, `x-vqd-4`, and `x-vqd-hash-1`.
    - **Step 5**: Prepares request data containing the model and conversation message history.
    - **Step 6**: Sends a POST request to the DuckDuckGo AI Chat API endpoint.
    - **Step 7**: Handles streaming responses and yields messages as they arrive.
    - **Step 8**: Updates the conversation with the latest information, including message history, cookies, and tokens.
6. **Handle Rate Limiting and Errors:**
    - The code implements rate limiting using the `sleep` method and handles specific errors such as `RateLimitError`, `ResponseStatusError`, `TimeoutError`, and `ConversationLimitError`.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.DDG import DDG
    from hypotez.src.endpoints.gpt4free.g4f.Provider.DDG import Conversation

    async def main():
        provider = DDG(model="gpt-4o-mini")
        conversation = Conversation(model="gpt-4o-mini")
        messages = [
            {"role": "user", "content": "Hello, how are you today?"},
        ]

        async for response in provider.create_async_generator(messages=messages, conversation=conversation):
            print(response)

    if __name__ == "__main__":
        asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".