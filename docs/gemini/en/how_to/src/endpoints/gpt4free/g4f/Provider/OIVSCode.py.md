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
This code block defines a class named `OIVSCode` which represents a specific OpenAI provider for using OpenAI models. 

Execution Steps
-------------------------
1. The `OIVSCode` class inherits from the `OpenaiTemplate` class.
2. It defines various attributes that describe the provider:
    - `label`: The display name of the provider ("OI VSCode Server").
    - `url`: The base URL of the provider.
    - `api_base`: The base URL for the API endpoints.
    - `working`: Indicates whether the provider is currently operational (`True`).
    - `needs_auth`: Whether the provider requires authentication (`False`).
    - `supports_stream`: Whether the provider supports streaming responses (`True`).
    - `supports_system_message`: Whether the provider supports system messages (`True`).
    - `supports_message_history`: Whether the provider supports message history (`True`).
    - `default_model`: The default model to use with the provider ("gpt-4o-mini-2024-07-18").
    - `default_vision_model`: The default vision model ("gpt-4o-mini-2024-07-18").
    - `vision_models`: A list of vision models supported by the provider.
    - `models`: A list of all models supported by the provider.
    - `model_aliases`: A dictionary that maps model aliases to their actual names.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.OIVSCode import OIVSCode

# Create an instance of the OIVSCode provider
provider = OIVSCode()

# Access provider attributes
print(provider.label)  # Output: "OI VSCode Server"
print(provider.default_model)  # Output: "gpt-4o-mini-2024-07-18"

# Access model aliases
print(provider.model_aliases["gpt-4o-mini"])  # Output: "gpt-4o-mini-2024-07-18"

# Use the provider in a request
# (Example using a hypothetical 'make_request' function)
response = make_request(provider, 'Hello world!', model="deepseek-v3") 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".