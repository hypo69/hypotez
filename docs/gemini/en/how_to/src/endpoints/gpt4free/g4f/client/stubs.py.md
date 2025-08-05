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
This code defines various Pydantic models for representing responses from GPT-4Free API calls. The models are used to structure and validate the responses received from the API, ensuring data consistency and type safety.

Execution Steps
-------------------------
1. **Define Base Pydantic Models**: The code begins by defining a base `BaseModel` class that inherits from the `pydantic.BaseModel` class. This base class serves as a foundation for all subsequent models.
2. **Define UsageModel**: This model represents the usage information returned by the API, including the number of tokens used for the prompt and completion, as well as details about cached tokens.
3. **Define ToolFunctionModel**: This model describes a function that can be called by a tool in the context of a GPT-4Free conversation.
4. **Define ToolCallModel**: This model represents a call to a tool function during the conversation, including the function's name and arguments.
5. **Define ChatCompletionChunk**: This model represents a chunk of the chat completion response, which is a streaming API feature.
6. **Define ChatCompletionMessage**: This model represents a single message in the chat completion response, including the role of the sender (e.g., "assistant") and the message content.
7. **Define ChatCompletionChoice**: This model represents a single choice within the chat completion response, including the message, index, and finish reason.
8. **Define ChatCompletion**: This model represents the complete chat completion response, including the chat history and the final message.
9. **Define ChatCompletionDelta**: This model represents a delta in the chat completion response, which is used for streaming updates.
10. **Define ChatCompletionDeltaChoice**: This model represents a choice within the chat completion delta.
11. **Define Image**: This model represents an image response, which includes the image URL, base64-encoded JSON, and revised prompt.
12. **Define ImagesResponse**: This model represents the response for a request to generate multiple images.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.client.stubs import ChatCompletion

# Example response data from the API
response_data = {
    "id": "chatcmpl-1234567890",
    "object": "chat.completion",
    "created": 1688451400,
    "model": "gpt-4free",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello, world!"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 5,
        "total_tokens": 15
    }
}

# Create a ChatCompletion object from the response data
completion = ChatCompletion.model_construct(**response_data)

# Access the message content
print(completion.choices[0].message.content)  # Output: Hello, world!
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".