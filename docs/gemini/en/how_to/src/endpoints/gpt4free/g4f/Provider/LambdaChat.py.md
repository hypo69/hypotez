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
This code defines the `LambdaChat` class, which represents a chat provider based on `lambda.chat`. It inherits from the `HuggingChat` class, which provides a base implementation for chatbot functionality. This class sets up key properties for the Lambda Chat provider, including its label, domain, origin, URL, working status, authentication requirements, default model, reasoning model, image models, fallback models, and model aliases.

Execution Steps
-------------------------
1. The code defines a class named `LambdaChat` that inherits from `HuggingChat`.
2. It sets the `label` property to "Lambda Chat", indicating the name of the provider.
3. It defines the `domain` property as "lambda.chat", indicating the domain name of the service.
4. It sets the `origin` property to a URL constructed using the `domain`.
5. It assigns the `url` property the same value as the `origin`.
6. It sets `working` to `True`, indicating that the provider is operational.
7. It sets `use_nodriver` to `False`, indicating that a browser driver is needed for interaction.
8. It sets `needs_auth` to `False`, indicating that no authentication is required.
9. It defines `default_model`, `reasoning_model`, `image_models`, and `fallback_models`, specifying the default model, reasoning model, and lists of models for different tasks.
10. It creates a copy of the `fallback_models` list as the `models` property.
11. It defines `model_aliases`, mapping common aliases to their corresponding model names.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.LambdaChat import LambdaChat

chat = LambdaChat()
print(chat.label) # Output: Lambda Chat
print(chat.domain) # Output: lambda.chat
print(chat.default_model) # Output: deepseek-llama3.3-70b
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".