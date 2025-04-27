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
The code block defines a `Copilot` class that implements the `AbstractProvider` interface, allowing it to interact with the Microsoft Copilot API. The class provides methods to create and manage conversations with Copilot, send messages, and receive responses, including text and image generations. 

Execution Steps
-------------------------
1. **Imports**: Necessary libraries are imported, including `curl_cffi` for websocket connections, `nodriver` for browser automation, and other modules related to request handling, error management, and media processing.
2. **Initialization**: The `Copilot` class is initialized with key parameters, such as the API URL, websocket URL, and default model.
3. **Model Management**: The `get_model` method handles model alias resolution, mapping user-provided model names to the corresponding internal names supported by the API.
4. **Authorization**: The `create_completion` method checks for access tokens and cookies. If none are found, it attempts to retrieve them from saved HAR files. If still unavailable, it prompts the user to authenticate through a browser.
5. **Conversation Management**: The `create_completion` method handles conversation creation and message sending. It sends prompts to the Copilot API via websocket connections and processes responses, including text and image generations.
6. **Stream Processing**: The `create_completion` method supports streaming responses. It yields individual text chunks as they become available, enabling real-time output display.
7. **Error Handling**: The code handles various potential errors, such as missing requirements, missing authentication information, invalid HAR files, and network issues.
8. **Media Processing**: The code allows sending media attachments to the Copilot API, including images. It converts images to bytes, uploads them, and includes their URLs in the prompt.
9. **Response Processing**: The code handles different types of responses, including text, images, and suggested follow-ups. It parses the responses and yields them to the caller.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import Copilot

# Initialize the Copilot provider
copilot = Copilot()

# Create a conversation with a prompt
messages = [{"role": "user", "content": "Write a Python function to reverse a string."}]
response_generator = copilot.create_completion(model="Copilot", messages=messages, stream=True)

# Process the streamed response
for response in response_generator:
    if isinstance(response, str):
        print(response, end="")
    elif isinstance(response, ImageResponse):
        # Handle image response
        print(f"Generated Image URL: {response.url}")
    elif isinstance(response, FinishReason):
        print(f"Conversation finished: {response.reason}")
    else:
        # Handle other response types as needed
        print(response)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".