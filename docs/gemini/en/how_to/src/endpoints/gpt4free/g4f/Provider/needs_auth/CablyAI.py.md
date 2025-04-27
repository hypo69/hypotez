**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
========================================================================================

Description
-------------------------
This code defines a class `CablyAI` that inherits from `OpenaiTemplate`.  It represents an interface to the CablyAI API for interacting with GPT models. It handles authentication, stream processing, and other common functionalities.

Execution Steps
-------------------------
1. **Class Definition**:  The class `CablyAI` is defined, inheriting from `OpenaiTemplate`. 
2. **Class Variables**: It sets up variables for key CablyAI API endpoints and information, such as:
    - `url`: The main CablyAI chat URL.
    - `login_url`: The CablyAI login URL.
    - `api_base`: The base URL for CablyAI API requests.
    - `working`: Indicates the API is currently functioning.
    - `needs_auth`: Specifies that the API requires authentication.
    - `supports_stream`:  Indicates the API supports stream processing.
    - `supports_system_message`: Indicates the API supports system messages.
    - `supports_message_history`: Indicates the API supports message history.
3. **`create_async_generator` Method**:  The `create_async_generator` method is overridden to handle specific request details for the CablyAI API:
    - It constructs the `headers` dictionary with specific values for `Accept`, `Accept-Language`, `Authorization`, `Content-Type`, `Origin`, `Referer`, and `User-Agent`.
    -  Calls the parent class's `create_async_generator` method, passing in the necessary parameters (`model`, `messages`, `api_key`, `stream`, `headers`, and `**kwargs`).
    -  This method returns an `AsyncResult` object that handles asynchronous responses from the CablyAI API.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth import CablyAI
    from hypotez.src.endpoints.gpt4free.g4f.Messages import Messages

    api_key = "YOUR_CABLYAI_API_KEY"  # Replace with your actual API key
    model = "gpt-4"
    messages = Messages(
        [
            {"role": "user", "content": "What is the meaning of life?"}
        ]
    )

    # Instantiate the CablyAI class with API key
    cablyai_provider = CablyAI(api_key=api_key)

    # Generate a response using the CablyAI API
    response = cablyai_provider.create_async_generator(model=model, messages=messages).get()
    print(response)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".