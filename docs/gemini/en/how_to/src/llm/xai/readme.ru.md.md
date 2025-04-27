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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use the xAI API Client

This document provides a step-by-step guide on how to use the xAI API client.

### Initializing the Client

1. **Import the necessary library:**
   ```python
   from xai import XAI
   ```

2. **Set your API key:**
   ```python
   api_key = "your_api_key_here"  # Replace with your actual API key
   ```

3. **Initialize the `XAI` object:**
   ```python
   xai = XAI(api_key)
   ```

### Making a Chat Completion Request

1. **Define the chat messages:**
   ```python
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
   ```

2. **Send a chat completion request using the `chat_completion` method:**
   ```python
   completion_response = xai.chat_completion(messages)
   ```

3. **Print the response:**
   ```python
   print("Non-streaming response:", completion_response)
   ```

### Streaming Chat Completion Responses

1. **Send a stream chat completion request using the `stream_chat_completion` method:**
   ```python
   stream_response = xai.stream_chat_completion(messages)
   ```

2. **Iterate through the stream response and print each line:**
   ```python
   print("Streaming response:")
   for line in stream_response:
       if line.strip():
           print(json.loads(line))
   ```

### Example Usage

This code snippet demonstrates how to use the `XAI` client for both non-streaming and streaming chat completion requests.

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