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
The code block defines a `PerplexityLabs` class that implements an asynchronous generator for interacting with the Perplexity Labs API. This class uses the `StreamSession` class for sending and receiving data over websockets. The `create_async_generator` method handles the communication with the API, sending the user's prompts and receiving the generated text responses.

Execution Steps
-------------------------
1. The `create_async_generator` method creates a `StreamSession` instance with specific headers and proxy settings.
2. It then initiates a websocket connection to the Perplexity Labs API using the `ws_connect` method.
3. After establishing the connection, it sends the user's prompts to the API via the websocket.
4. It then receives the generated text responses from the API and yields them as an asynchronous generator.
5. The `yield Sources(data["citations"])` line indicates that the code also retrieves and yields source citations for the generated text.
6. The `yield FinishReason("stop")` line indicates that the code has finished generating text for the given prompt.
7. The `raise ResponseError` line handles any potential errors that occur during the communication with the API.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.PerplexityLabs import PerplexityLabs

    messages = [
        {"role": "user", "content": "What is the meaning of life?"},
    ]

    async def main():
        async for message in PerplexityLabs.create_async_generator(model="r1-1776", messages=messages):
            print(message)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".