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
The code block defines an `AutonomousAI` class, representing a provider for the Autonomous AI chatbot API. This class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, and it implements functionality to interact with the Autonomous AI API to generate text responses. 

Execution Steps
-------------------------
1. **Initialize the `AutonomousAI` class**: Creates an instance of the `AutonomousAI` class, which represents an interaction with the Autonomous AI API.
2. **Define API Endpoints**: Sets the API endpoints for different models offered by Autonomous AI, including "llama", "qwen_coder", "hermes", "vision", and "summary".
3. **Establish API Connection**: The `create_async_generator` method establishes an asynchronous connection to the Autonomous AI API.
4. **Send Messages**: The code prepares a message request and encodes it into base64 format.
5. **Send Request**: The `session.post` function sends an HTTP POST request to the chosen API endpoint with the encoded message.
6. **Handle Response**: The code parses the response from the API in a streaming manner, yielding content chunks as they become available.
7. **Decode and Process Chunks**: Each chunk of the response is decoded and parsed as JSON, checking for content and finish reason.
8. **Yield Content**: The generated text content is yielded as it becomes available, allowing for streaming output.
9. **Yield Finish Reason**: When the API indicates the end of the response, a `FinishReason` object is yielded.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AutonomousAI import AutonomousAI

async def main():
    provider = AutonomousAI()
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    async for chunk in provider.create_async_generator(model="llama", messages=messages):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".