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
This code block implements a custom `ChatAI` class that extends the `ChatOpenAI` class from the `langchain_community` library. It overrides the `convert_message_to_dict` method to handle `ChatCompletionMessage` objects specifically, ensuring compatibility with the `g4f` library.

Execution Steps
-------------------------
1. **Overrides `convert_message_to_dict`**: The code defines a new function `new_convert_message_to_dict` that handles the conversion of `BaseMessage` objects to dictionaries. It specifically checks if the message is a `ChatCompletionMessage` and formats it accordingly, including tool calls if present.
2. **Assigns Custom Conversion Function**: The overridden `convert_message_to_dict` function is assigned to the `openai` module. This ensures that the custom conversion logic is used when interacting with `ChatOpenAI` instances.
3. **Defines `ChatAI` Class**: The `ChatAI` class is created, inheriting from `ChatOpenAI`. It sets the default `model_name` to "gpt-4o".
4. **Validates Environment**: The `validate_environment` class method checks for the necessary environment variables and initializes the `Client` and `AsyncClient` objects for interacting with the `g4f` API.

Usage Example
-------------------------

```python
from g4f.integration.langchain import ChatAI

# Initialize ChatAI with your API key
chat_ai = ChatAI(api_key="your_api_key")

# Send a message to the model
response = chat_ai("Hello, how are you?")

# Print the response
print(response)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".