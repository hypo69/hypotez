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
The `HuggingChat` class implements an asynchronous, authenticated provider for interacting with Hugging Face's chat API. It supports both text-based and image-based prompts, stream responses, and model selection.

Execution Steps
-------------------------
1. **Initialization:** The class initializes essential attributes like domain, origin, URL, and model-related information (default models, aliases, etc.).
2. **Model Discovery:** The `get_models` method retrieves a list of available models by fetching data from Hugging Face's chat API.
3. **Authentication:** The `on_auth_async` method handles authentication by either using pre-existing cookies or prompting for user login.
4. **Conversation Creation:** The `create_authed` method initiates a conversation with the selected model by creating a new conversation ID and fetching the initial message ID.
5. **Prompt Formatting:** The `format_prompt` method processes user messages into a format suitable for the Hugging Face API.
6. **Request Preparation:** The `create_authed` method prepares the request data, including the formatted prompt, user messages, media files (if any), and model-specific settings.
7. **API Request:** The method uses `curl_cffi` to make a multipart POST request to Hugging Face's chat API endpoint.
8. **Response Handling:** The `create_authed` method iterates through the stream response, parsing JSON data and yielding either stream responses, final answers, images, or other responses.
9. **Model Selection:** The `get_model` method selects the appropriate model based on the user's input.
10. **Conversation Creation:** The `create_conversation` method creates a new conversation with the chosen model by sending a POST request to the API.
11. **Message ID Fetching:** The `fetch_message_id` method retrieves the message ID for the newly created conversation by making a GET request to the API.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingChat import HuggingChat

async def main():
    # Initialize the provider
    provider = HuggingChat()

    # Authenticate (use pre-existing cookies or prompt for login)
    auth_result = await provider.authenticate(cookies={'hf-chat': 'your_session_id'}) 

    # Send a text prompt
    messages = [
        {'role': 'user', 'content': 'Hello, how are you?'},
    ]
    async for response in provider.generate_response(model='gpt2', messages=messages, auth_result=auth_result):
        print(response)

    # Send an image prompt
    messages = [
        {'role': 'user', 'content': 'Describe this image', 'image': 'path/to/image.jpg'}
    ]
    async for response in provider.generate_response(model='dalle2', messages=messages, auth_result=auth_result):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".