**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the XAI API Client
=========================================================================================

Description
-------------------------
The code provides a Python client for interacting with the xAI API, allowing you to send chat requests and receive responses, both in standard and streaming formats.

Execution Steps
-------------------------
1. **Initialize the Client**: Create an instance of the `XAI` class and provide your xAI API key.
2. **Define Chat Messages**: Create a list of messages formatted as dictionaries, including the message role (system, user) and content.
3. **Send Chat Completion Request**: Use the `chat_completion` method to send a request to the xAI model and receive a non-streaming response.
4. **Send Streaming Chat Completion Request**: Use the `stream_chat_completion` method to send a request to the xAI model and receive a streaming response, iterating over the received lines.

Usage Example
-------------------------

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Replace with your actual API key
xai = XAI(api_key)

messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
    },
    {
        "role": "user",
        "content": "What is the answer to life and universe?"
    }
]

# Non-streaming request
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Streaming request
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".