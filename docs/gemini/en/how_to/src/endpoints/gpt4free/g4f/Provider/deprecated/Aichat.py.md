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
This code snippet defines an `Aichat` class, which is a subclass of `AsyncProvider`, designed to interact with the chat-gpt.org API. It provides functionality to send prompts and receive responses using a configured `StreamSession` with specific headers and cookies.

Execution Steps
-------------------------
1. **Define the Class**: The `Aichat` class is defined, inheriting from `AsyncProvider`. It sets a default URL for the chat-gpt.org API, initializes `working` as False (not currently used), and sets `supports_gpt_35_turbo` to True, indicating compatibility with the GPT-3.5 Turbo model.

2. **Create Asynchronous Session**: The `create_async` class method is defined to initiate an asynchronous session with the chat-gpt.org API.

3. **Retrieve Cookies**: The method first attempts to retrieve cookies from the chat-gpt.org website. If no cookies are found, it raises a `RuntimeError`, suggesting users refresh the website in Chrome to obtain necessary cookies.

4. **Configure Headers**: The method sets specific headers for the HTTP request to chat-gpt.org, including `authority`, `accept`, `accept-language`, `content-type`, `origin`, `referer`, and `user-agent`.

5. **Initialize StreamSession**: An `StreamSession` object is created with the specified headers, cookies, a 6-second timeout, optional proxy configuration, Chrome 110 impersonation, and disabling SSL verification.

6. **Prepare Request Data**: The prompt is formatted using the `format_prompt` function, and a JSON payload is constructed with `message`, `temperature`, `presence_penalty`, `top_p`, and `frequency_penalty` parameters.

7. **Send POST Request**: The `StreamSession` makes a POST request to the "https://chat-gpt.org/api/text" endpoint with the JSON data.

8. **Handle Response**: The response is checked for errors using `response.raise_for_status()`. The response is then converted to JSON format.

9. **Validate Response**: The response is validated by checking if a response message exists. If not, an exception is raised.

10. **Return Response**: Finally, the response message is returned as the output.


Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aichat import Aichat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    # Define the prompt
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    # Initialize Aichat provider
    provider = Aichat()
    # Send the prompt to the provider
    response = await provider.create_async("gpt-3.5-turbo", messages)
    # Print the response
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".