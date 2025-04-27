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
The `RobocodersAPI` class implements an asynchronous generator for interacting with the Robocoders AI API. It handles authentication, session management, and sending prompts to the API to receive responses.

Execution Steps
-------------------------
1. **Initialize the API**: The class defines static methods for retrieving an access token and creating a session with the API. It also manages a cache file for storing session data.
2. **Create an Asynchronous Generator**: The `create_async_generator` class method is used to initiate an asynchronous generator that handles the communication with the API. It formats the prompt using the `format_prompt` helper function and sends a POST request to the API endpoint.
3. **Process Responses**: The generator iterates through the responses received from the API. It decodes the JSON data and extracts the message content. If the API indicates a resource limit, it automatically sends a "continue" request to continue the dialog.
4. **Error Handling**: The code handles potential errors like authentication issues, validation errors, and server errors, providing appropriate error messages.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def main():
    # Initialize the provider
    provider = RobocodersAPI(model="GeneralCodingAgent") 

    # Send a prompt to the API
    messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    async for response in provider.create_async_generator(messages=messages):
        print(f"Response: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".