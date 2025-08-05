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
The code block implements a class `ChatGptt` for interacting with the chatgptt.me API, which provides access to a GPT-based chatbot.

Execution Steps
-------------------------
1. **Initialization:** The `ChatGptt` class is initialized with the base URL and API endpoint for chatgptt.me. It also defines various attributes, such as model availability, streaming support, and message history support.

2. **Model Selection:** The `get_model` method ensures that the selected model is valid.

3. **Request Preparation:** 
    - The `create_async_generator` method prepares an asynchronous generator that yields responses from the API.
    - It creates a client session with appropriate headers for chatgptt.me.
    - The code fetches the initial page content to extract necessary authentication tokens (nonce and post ID).

4. **Authentication Token Extraction:** 
    - The code uses regular expressions to extract the nonce and post ID from the initial HTML content.
    - If these tokens are not found, an error is raised.

5. **Payload Construction:** 
    - The code constructs a payload containing the extracted authentication tokens, the user's message, chatbot ID, client ID, and a flag indicating whether to use history.

6. **API Request and Response:**
    - The code sends a POST request to the API endpoint with the constructed payload.
    - It handles potential errors using `raise_for_status`.
    - It parses the JSON response and yields the data.

7. **Data Streaming:** 
    - The generator yields the data from the API response, allowing for streaming of the chatbot's response.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt import ChatGptt

async def main():
    # Initialize the provider
    provider = ChatGptt()

    # Set the model
    model = "gpt-4"

    # Prepare the messages
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]

    # Create the asynchronous generator
    async for response in provider.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".