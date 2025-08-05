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
The `Gemini` class provides an asynchronous generator-based provider for interacting with the Google Gemini AI model. It handles authentication, model selection, image uploading, and conversation management.

Execution Steps
-------------------------
1. **Initialization**: The `Gemini` class initializes with authentication and model-specific settings.
2. **Authentication**: The class uses `nodriver` (if available) or cookies to authenticate with Google Gemini.
3. **Model Selection**: The user can choose a specific Gemini model (e.g., `gemini-2.0-flash`) or use the default model.
4. **Conversation Management**: The `create_async_generator` method manages conversations with Gemini, allowing users to send messages, receive responses, upload images, and manage conversation history.
5. **Response Processing**: The code processes the Gemini responses, extracting text, reasoning, images, and YouTube links.
6. **Automatic Cookie Refresh**: The `start_auto_refresh` method ensures that the authentication cookies are automatically refreshed in the background for long-term usage.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Gemini import Gemini

    async def main():
        gemini = Gemini()
        async for response in gemini.create_async_generator(model="gemini-2.0-flash", messages=[{"role": "user", "content": "Hello, how are you?"}]):
            print(response)

    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".