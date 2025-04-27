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
The `AIUncensored` class provides an asynchronous generator-based implementation of the `AIUncensored.info` API for generating text with a large language model (LLM). 

Execution Steps
-------------------------
1. **Initialization**:
   - The class initializes with predefined API endpoint (`url`), API key (`api_key`), and configuration settings for supported features (e.g., streaming, system messages, message history).
   - It also defines the default model (`default_model`) and available models (`models`).

2. **Signature Calculation**:
   - The `calculate_signature` method generates a secure signature for the API request. 
   - It uses a timestamp, the request payload, and a secret key to calculate the signature using an HMAC-SHA256 hash function.

3. **Server URL Selection**:
   - The `get_server_url` method randomly selects a server URL from a list of available servers.

4. **Asynchronous Generator Creation**:
   - The `create_async_generator` method creates an asynchronous generator that handles the communication with the API. 
   - It builds the request payload (including the `model`, `messages`, and `stream` parameters), calculates the signature, sets up the headers, and sends a POST request to the chosen server.

5. **Response Handling**:
   - The code checks for successful API responses and handles both streamed responses and non-streamed responses.
   - For streamed responses, it iterates over the content lines, parses the JSON data (if present), and yields the received text.
   - For non-streamed responses, it decodes the JSON content and yields the generated text.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AIUncensored import AIUncensored

    async def main():
        provider = AIUncensored()
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
        ]
        async for response in provider.create_async_generator(model="hermes3-70b", messages=messages, stream=True):
            if isinstance(response, str):
                print(response)
            else:
                print(f"Finish reason: {response}")

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".