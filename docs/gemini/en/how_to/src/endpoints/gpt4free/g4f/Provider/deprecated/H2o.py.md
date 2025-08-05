**Instructions for Generating Code Documentation**

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code defines a class `H2o` that extends the base provider class `AsyncGeneratorProvider` and implements an asynchronous generator for interacting with the GPT-4Free service from h2o.ai.

Execution Steps
-------------------------
1. **Initialization**: The class defines the base URL (`url`) and model (`model`) for the GPT-4Free service.
2. **Creating an Asynchronous Generator**: The `create_async_generator` class method is responsible for creating an asynchronous generator that yields text responses from the GPT-4Free model.
3. **Setting up the Session**: An `aiohttp.ClientSession` is created with the necessary headers and proxy configuration.
4. **Setting Model and Conversation**:  The code sends a `POST` request to `/settings` to set the active model and other settings. It then makes another `POST` request to `/conversation` to initiate a conversation.
5. **Sending Prompt**: The `format_prompt` function is used to prepare the user prompt for the GPT-4Free model. The prompt is then sent to the `/conversation/{conversationId}` endpoint.
6. **Stream Response**: The `POST` request to `/conversation/{conversationId}` is configured to stream the response. An asynchronous loop iterates over the streamed data, extracting text tokens and yielding them.
7. **Cleaning up**:  After the response stream is complete, a `DELETE` request is sent to `/conversation/{conversationId}` to clean up the conversation session.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.H2o import H2o

async def main():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for response in H2o.create_async_generator(messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```