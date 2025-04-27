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
The `AiChats` class implements an asynchronous generator-based provider for interacting with the `ai-chats.org` API. It supports text generation and image generation using models like `gpt-4` and `dalle`. 

Execution Steps
-------------------------
1. **Initialization**: The class initializes with the API endpoint, default model, and supported models.
2. **Asynchronous Generator Creation**: The `create_async_generator` method creates an asynchronous generator for iterating over responses from the API.
    - **Headers**: Sets up the headers for the API request, including user-agent, cookies, and content type.
    - **Request**: Sends a POST request to the API with the user prompt and chosen model.
    - **Response Handling**: Handles the response depending on the model:
        - **Dalle**: If the model is 'dalle', the code fetches the generated image URL from the response, downloads the image, and yields a `ImageResponse` object containing the base64-encoded image data.
        - **GPT-4**: If the model is 'gpt-4', the code extracts the generated text response from the response stream and yields it as a string.
3. **Asynchronous Execution**: The `create_async` method creates a single response by executing the `create_async_generator` and returning either the generated text or the base64-encoded image.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AiChats import AiChats

async def main():
    # Choose the model
    model = 'gpt-4'

    # Prepare the messages for the prompt
    messages = [
        {'role': 'user', 'content': 'Hello, how are you?'},
    ]

    # Initialize the AiChats provider
    provider = AiChats()

    # Generate a response
    response = await provider.create_async(model=model, messages=messages)

    # Print the response
    print(response)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".