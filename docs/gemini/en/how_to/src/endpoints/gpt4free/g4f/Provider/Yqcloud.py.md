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
The code block defines a class `Yqcloud` that implements an asynchronous generator provider for the Yqcloud GPT-4 free API. It supports features like stream responses, system messages, and message history, and allows for optional conversation management and model selection. 

Execution Steps
-------------------------
1. The code defines a `Conversation` class to store user ID and message history for a chat session.
2. The `Yqcloud` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing base functionality for asynchronous generation and model handling.
3. The class defines attributes like `url`, `api_endpoint`, `supports_stream`, `supports_system_message`, `supports_message_history`, `default_model`, and `models`.
4. The `create_async_generator` method is responsible for handling asynchronous generation requests.
5. The method retrieves the model, prepares headers, and initializes a `Conversation` instance if needed.
6. It extracts the system message from the message history if present.
7. It formats the prompt using the `format_prompt` helper function.
8. It sends a POST request to the Yqcloud API endpoint with the formatted prompt and other relevant data.
9. The method iterates through the response chunks and yields them as they arrive, enabling stream responses.
10. If `return_conversation` is set to `True`, the method appends the assistant's response to the message history and yields the updated conversation.
11. Finally, it yields a `FinishReason` indicating the end of the generation process.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Yqcloud import Yqcloud, Conversation

# Define the model and messages
model = "gpt-4"
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Create a conversation instance
conversation = Conversation(model)

# Use the Yqcloud provider to generate responses
async for chunk in Yqcloud.create_async_generator(model=model, messages=messages, conversation=conversation, stream=True):
    print(chunk, end="")

# Access the updated conversation history after generation
print(conversation.message_history)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".