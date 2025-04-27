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
This code block implements an `AsyncGeneratorProvider` class called `GithubCopilot`, which provides a mechanism to interact with the GitHub Copilot service. It allows sending prompts and receiving responses asynchronously, with the ability to stream responses.

Execution Steps
-------------------------
1. The code defines a `Conversation` class representing a conversation with GitHub Copilot. 
2. The `GithubCopilot` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`. It defines properties like `label`, `url`, `working`, `needs_auth`, `supports_stream`, `default_model`, and `models`.
3. The `create_async_generator` class method:
    - Retrieves cookies from the browser for `github.com`.
    - Retrieves an API key if not provided.
    - Creates a new conversation thread if a conversation ID is not provided.
    - Sends the prompt to the Copilot API and yields the streamed responses.
4. The code formats the prompt and retrieves the last user message.
5. The code sends a POST request to the API endpoint and iterates through the streamed response lines.
6. It yields the response content after parsing the JSON data.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot

async def main():
    # Initialize GitHub Copilot provider
    copilot = GithubCopilot()

    # Define the prompt
    messages = [
        {"role": "user", "content": "Write a Python function to reverse a string."}
    ]

    # Send the prompt and receive streamed responses
    async for response in copilot.create_async_generator(messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".