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
This code snippet demonstrates how to interact with the `gpt4free` API to get completions from a large language model (LLM). 
It sends two requests to the API:
    1. The first request introduces a user ("Heiner") to the API.
    2. The second request asks the LLM to provide information about the user's name.

Execution Steps
-------------------------
1. **Imports**: The code imports the necessary libraries for making HTTP requests (`requests`) and working with JSON data (`json`). It also imports `uuid` to generate unique conversation IDs.
2. **API Endpoint**: The API endpoint URL is defined as `url` and will be used to send HTTP requests. 
3. **Conversation ID**: A unique conversation ID is generated using `uuid.uuid4()` and converted to a string.
4. **First Request**:
    - A dictionary `body` is created to represent the request data.
    - This dictionary includes the desired model (`model`), the provider (`provider`), and the message ("Hello, i am Heiner. How are you?") sent by the user.
    - The `conversation_id` is added to the dictionary to uniquely identify the conversation. 
    - The code sends a POST request to the API endpoint with the `body` and sets the `stream` parameter to `True` to receive the response in chunks. 
    - The response is checked for errors and processed chunk by chunk using the `iter_lines` method.
    - If the response contains an error, the error is printed.
    - If the response contains a valid completion, the `content` is printed.
5. **Second Request**:
    - A similar request is sent with a different message ("Tell me somethings about my name").
    - The conversation ID generated in step 3 is used to continue the conversation.
    - The response is processed in the same way as the first request.


Usage Example
-------------------------

```python
import requests
import json
import uuid

url = "http://localhost:1337/v1/chat/completions"
conversation_id = str(uuid.uuid4())
body = {
    "model": "",
    "provider": "Copilot", 
    "stream": True,
    "messages": [
        {"role": "user", "content": "Hello, i am Heiner. How are you?"}
    ],
    "conversation_id": conversation_id
}
response = requests.post(url, json=body, stream=True)
response.raise_for_status()
for line in response.iter_lines():
    if line.startswith(b"data: "):
        try:
            json_data = json.loads(line[6:])
            if json_data.get("error"):
                print(json_data)
                break
            content = json_data.get("choices", [{"delta": {}}])[0]["delta"].get("content", "")
            if content:
                print(content, end="")
        except json.JSONDecodeError:
            pass
print()
print()
print()
body = {
    "model": "",
    "provider": "Copilot",
    "stream": True, 
    "messages": [
        {"role": "user", "content": "Tell me somethings about my name"}
    ],
    "conversation_id": conversation_id
}
response = requests.post(url, json=body, stream=True)
response.raise_for_status()
for line in response.iter_lines():
    if line.startswith(b"data: "):
        try:
            json_data = json.loads(line[6:])
            if json_data.get("error"):
                print(json_data)
                break
            content = json_data.get("choices", [{"delta": {}}])[0]["delta"].get("content", "")
            if content:
                print(content, end="")
        except json.JSONDecodeError:
            pass

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".