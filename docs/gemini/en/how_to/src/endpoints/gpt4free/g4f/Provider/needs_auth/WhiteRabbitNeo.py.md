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
The `WhiteRabbitNeo` class is a provider for the `gpt4free` endpoint, allowing you to send messages and receive responses from the WhiteRabbit Neo API. It uses an asynchronous generator to stream responses and handles authentication, cookies, and request parameters.

Execution Steps
-------------------------
1. **Initialization**: The `create_async_generator` class method is used to initialize the asynchronous generator, setting up parameters like `model`, `messages`, `cookies`, and `connector`.
2. **Cookies Handling**: If no cookies are provided, the `get_cookies` helper function fetches cookies from the `www.whiterabbitneo.com` domain.
3. **Request Headers**: Sets up headers for the HTTP request, including user agent, accept, language, referer, and content type.
4. **Session Creation**: Creates an asynchronous HTTP session with the configured headers, cookies, and connector.
5. **Data Preparation**: Creates a request body (`data`) containing the messages, a unique identifier (`id`), and flags for prompt enhancement and function usage.
6. **API Request**: Sends a POST request to the `www.whiterabbitneo.com/api/chat` endpoint with the prepared data.
7. **Response Handling**:
    - **Error Handling**: Uses `raise_for_status` to raise an exception if the request fails.
    - **Response Stream**: Iterates over chunks of the response content, decodes them, and yields each chunk, allowing for streaming responses.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import WhiteRabbitNeo

async def main():
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    async for chunk in await WhiteRabbitNeo.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".