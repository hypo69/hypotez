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
The code block defines a class `Chatgpt4o` that provides an asynchronous interface for interacting with a chatbot service. The `create_async` method sends a request to the chatbot service with a user prompt and returns the chatbot's response.

Execution Steps
-------------------------
1. **Initialization**:
    - The `create_async` method is called with user prompt, model name, and optional parameters such as `proxy`, `timeout`, and `cookies`.
2. **Retrieve post ID and nonce**:
    - If the `_post_id` or `_nonce` attributes are not set, the code makes a GET request to the chatbot's website to retrieve the post ID and nonce. 
    - The post ID and nonce are extracted from the HTML response using regular expressions.
3. **Format prompt**:
    - The user's prompt is formatted into a string suitable for the chatbot service.
4. **Send POST request**:
    - The code constructs a POST request with the formatted prompt, post ID, nonce, and other parameters.
    - The request is sent to the chatbot service's API endpoint.
5. **Process response**:
    - The response from the chatbot service is parsed as JSON.
    - The chatbot's response is extracted from the JSON and returned to the caller.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Chatgpt4o import Chatgpt4o

async def main():
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    model = "gpt-4o-mini-2024-07-18"
    response = await Chatgpt4o.create_async(model=model, messages=messages)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".