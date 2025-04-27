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
This code block implements the `GizAI` class, which acts as a provider for the `gpt4free` API endpoint. The `GizAI` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, enabling it to handle asynchronous message generation and manage model selection. It provides methods for fetching the appropriate model, sending messages to the GizAI API, and returning the generated response.

Execution Steps
-------------------------
1. **Initialization**: The `GizAI` class initializes essential attributes like the base URL, API endpoint, and supported features. It also defines default and available models, along with aliases for compatible model names.

2. **Model Selection**: The `get_model` class method retrieves the correct model based on the provided model name, applying aliases if necessary, and defaults to the `default_model` if the input is invalid.

3. **Async Generator Creation**: The `create_async_generator` class method creates an asynchronous generator for handling messages and generating responses. It takes model, messages, and optional proxy parameters as input.

4. **API Interaction**: Inside the generator, the code constructs a JSON request payload containing the selected model, input messages, and the `mode` (set to `plan`). It then sends this request to the GizAI API endpoint using an `aiohttp` session with appropriate headers.

5. **Response Handling**: If the API returns a successful response (status code 201), the generator yields the generated output, stripping whitespace for cleaner output. If an unexpected response status is encountered, an exception is raised, including the response status code and body for debugging.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.GizAI import GizAI
    from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

    async def main():
        provider = GizAI()
        messages: Messages = [
            {"role": "user", "content": "Hello, how are you?"},
        ]
        async for response in provider.create_async_generator(model='chat-gemini-flash', messages=messages):
            print(response)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".