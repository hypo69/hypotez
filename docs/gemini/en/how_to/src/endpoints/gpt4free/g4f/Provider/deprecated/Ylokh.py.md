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
The code block defines a class `Ylokh` that inherits from `AsyncGeneratorProvider` and provides functionality for interacting with the Ylokh chat API. The class provides a method `create_async_generator` for generating asynchronous responses from the API, which can be used to stream responses or retrieve full chat completions.

Execution Steps
-------------------------
1. **Initialization**: The class initializes with the base URL of the Ylokh API and sets up default values for parameters like `working`, `supports_message_history`, and `supports_gpt_35_turbo`.
2. **Async Generator Creation**: The `create_async_generator` method is called with the desired model, messages, and other optional parameters.
3. **Model and Headers Setup**: The method sets up the model and headers for the API request, including the origin and referer for the Ylokh website.
4. **Request Data Preparation**: The method constructs the data for the API request, including messages, model parameters, and optional settings.
5. **API Call**: The method uses a `StreamSession` to make a POST request to the Ylokh chat API endpoint with the prepared data.
6. **Response Handling**: The method handles both streamed responses and full chat completions:
    - **Streamed Responses**: For streamed responses, the method iterates over the lines of the response and extracts the content of the `delta` field, yielding the content as it becomes available.
    - **Full Chat Completions**: For full chat completions, the method waits for the complete response and then extracts the content of the `message` field.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Ylokh import Ylokh
    from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    async def main():
        provider = Ylokh()
        async for response in provider.create_async_generator(messages=messages, model="gpt-3.5-turbo"):
            print(response)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".