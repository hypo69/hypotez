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
This code block implements a provider class for the Pi.ai API. It allows interaction with the Pi.ai chatbot using the `AsyncGeneratorProvider` base class. The class utilizes the `StreamSession` for efficient handling of streamed responses.

Execution Steps
-------------------------
1. The `Pi` class initializes with necessary attributes such as API URL, supported models, and default headers and cookies.
2. `create_async_generator` is a class method that constructs an asynchronous generator for handling API interactions. It retrieves initial cookies and headers using `get_args_from_nodriver`, then establishes a `StreamSession` object for communication. 
3. If a `conversation_id` is provided, the generator directly sends the prompt for response. Otherwise, it starts a new conversation by calling `start_conversation` and then sends the formatted prompt.
4. The `start_conversation` method handles the initial chat session setup with Pi.ai, retrieving a unique conversation ID for subsequent interactions.
5. The `ask` method sends the prompt to the Pi.ai server for processing. It retrieves the streamed responses, parses JSON data from the response lines, and yields the text or title information received.
6. `get_chat_history` method retrieves the chat history for a given conversation ID.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Pi import Pi

async def main():
    provider = Pi()
    messages = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi, how can I help you?"},
    ]
    async for response in provider.create_async_generator(model="pi", messages=messages):
        print(f"Assistant: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".