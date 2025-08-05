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
This code block implements a provider for the Bing search engine, allowing users to interact with the Bing AI chatbot using the `gpt-4` model. It provides functions for creating conversations, streaming responses, and generating completions based on user prompts.

Execution Steps
-------------------------
1. **Establish a Connection:**
    - Initializes an `aiohttp` session and connects to the Bing ChatHub websocket endpoint using the `ws_connect` method.
    - Sends a handshake message to establish the protocol and version.
2. **Create a Conversation:**
    - Uses the `create_conversation` function to initiate a new conversation with Bing AI, obtaining the conversation ID, client ID, and conversation signature.
3. **Stream Generate:**
    - The `stream_generate` function takes a user prompt, optional mode settings (defaulting to the "jailbreak" mode), and optional context from previous messages.
    - It constructs a message structure containing the prompt, mode, location, conversation details, and optional context.
    - Sends the message to the Bing ChatHub server and waits for the response.
4. **Process Responses:**
    - The code continuously receives and processes messages from the server, splitting them into individual JSON objects using the delimiter.
    - Extracts the chat content from the received messages, handling different message types and content origins.
    - Yields the extracted text to the caller, allowing for streaming output.
5. **Completion Generation:**
    - The `_create_completion` function wraps the `stream_generate` function, providing an interface compatible with the `g4f` framework.
    - Takes user messages as input and generates completions based on the Bing AI responses.
    - Yields individual tokens of the completion for streaming output.

Usage Example
-------------------------

```python
from g4f.Providers.Bing import _create_completion

# Define user messages
messages = [
    {'role': 'user', 'content': 'Hello, Bing! What is the meaning of life?'},
]

# Generate completion using the Bing provider
for token in _create_completion(model='gpt-4', messages=messages, stream=True):
    print(token, end='')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".