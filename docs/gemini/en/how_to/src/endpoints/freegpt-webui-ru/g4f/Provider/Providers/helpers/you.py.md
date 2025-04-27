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
This code block implements a `you.com` provider for the `g4f` project. It takes a list of messages as input and sends a request to the `you.com` API to get a response.

Execution Steps
-------------------------
1. **Read Configuration**: The code first reads the configuration from the command-line argument `sys.argv[1]`, which is expected to be a JSON string. The configuration contains a list of messages representing a conversation history.
2. **Extract Messages**: The `transform` function extracts the relevant question-answer pairs from the list of messages. It processes each message based on its role (`user`, `assistant`, or `system`) and creates a list of dictionaries containing question and answer pairs.
3. **Prepare Request**: The code prepares a request to the `you.com` API using the `urllib.parse` module. It sets the `q` parameter to the last user message (if it exists) and the `chat` parameter to the transformed list of messages.
4. **Send Request**: The code uses the `curl_cffi` library to send a GET request to the `you.com` API with the prepared parameters and headers. The `content_callback` parameter specifies the `output` function to handle the streamed response.
5. **Process Response**: The `output` function processes each chunk of the streamed response. If the chunk contains the `youChatToken`, the code extracts the token from the JSON data and prints it to the console.
6. **Loop for Stream**: The code continues to loop, sending requests and processing the response, until a complete response is received.

Usage Example
-------------------------

```python
# Example configuration (JSON string)
config = '{"messages": [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I am doing well, thank you. How can I help you today?"}]}'

# Execute the code
python you.py '{}'
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".