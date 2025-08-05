**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `XAI` Class
=========================================================================================

Description
-------------------------
This code defines an `XAI` class that interacts with the x.ai API to perform chat completions. It allows for both non-streaming and streaming responses.

Execution Steps
-------------------------
1. **Initialization**: The `XAI` class is initialized with an API key. 
2. **Request Sending**: The `_send_request` method handles sending HTTP requests to the x.ai API, including the API key, endpoint, and data for POST/PUT requests.
3. **Chat Completion**: The `chat_completion` method sends a request for a chat completion using a chosen model (`grok-beta` by default), messages, and optional parameters like stream and temperature.
4. **Stream Chat Completion**: The `stream_chat_completion` method sends a request for a streaming chat completion, returning an iterator to process responses as they arrive.

Usage Example
-------------------------

```python
    # Example using the XAI class
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