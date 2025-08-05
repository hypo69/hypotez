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
The code defines a `ThebApi` class, which provides an interface for interacting with TheB.AI API. This class extends the `OpenaiTemplate` class and inherits its methods, but adds specific configurations and functionalities for TheB.AI.

Execution Steps
-------------------------
1. Defines a dictionary `models` mapping model names to human-readable names.
2. Defines the `ThebApi` class, inheriting from `OpenaiTemplate`.
3. Sets class attributes like `label`, `url`, `login_url`, `api_base`, `working`, `needs_auth`, `default_model`, and `fallback_models` to configure the TheB.AI API connection.
4. Defines a class method `create_async_generator` that prepares data for sending a request to TheB.AI API.
5. Extracts the system message from the `messages` list and filters out system messages from the list.
6. Creates a dictionary `data` containing model parameters like `system_prompt`, `temperature`, and `top_p`.
7. Calls the superclass `create_async_generator` method to initiate a request to TheB.AI API.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import ThebApi

# Initialize ThebApi class
theb_api = ThebApi()

# Create a list of messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "system", "content": "Be polite and informative."},
]

# Send a request to Theb.AI API
response = theb_api.create_async_generator(model="theb-ai", messages=messages)

# Process the response
print(response)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".