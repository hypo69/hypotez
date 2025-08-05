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
This code defines a `Glider` class that represents a chat interface for the Glider AI service. It inherits from the `OpenaiTemplate` class and provides information about the service, including its label, URL, API endpoint, models, and model aliases. 

Execution Steps
-------------------------
1. **Defines the `Glider` class**: The class inherits from the `OpenaiTemplate` class.
2. **Sets class attributes**:
    - `label`: Sets the label for the service to "Glider".
    - `url`: Sets the URL for the Glider AI service.
    - `api_endpoint`: Defines the API endpoint for the chat service.
    - `working`: Indicates that the service is currently active.
    - `default_model`: Specifies the default model to use for interactions.
    - `models`: Lists available models supported by the service.
    - `model_aliases`: Creates a dictionary for mapping common model names to their actual IDs.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import Glider

# Initialize the Glider provider
glider_provider = Glider()

# Get the default model
default_model = glider_provider.default_model 

# Access the available models
available_models = glider_provider.models

# Use a model alias
model_alias = "llama-3.1-70b"
actual_model = glider_provider.model_aliases[model_alias]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".