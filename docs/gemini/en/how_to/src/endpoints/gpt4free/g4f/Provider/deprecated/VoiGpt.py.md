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
The code block defines a `VoiGpt` class which is a provider for `VoiGpt.com`. This class allows you to interact with the VoiGpt API to generate responses using its models. 

Execution Steps
-------------------------
1. **Class Definition**: The code defines a class called `VoiGpt` that inherits from `AbstractProvider`. 
2. **Class Attributes**: The class has several attributes, including:
    - `url`: The base URL for the VoiGpt API.
    - `working`: Indicates whether the provider is working, set to `False` by default.
    - `supports_gpt_35_turbo`: Indicates whether the provider supports the `gpt-3.5-turbo` model.
    - `supports_message_history`: Indicates whether the provider supports message history.
    - `supports_stream`: Indicates whether the provider supports streaming responses.
    - `_access_token`: Stores the access token used for authentication.
3. **Class Method `create_completion`**: The class defines a `create_completion` method that handles the generation of responses from the VoiGpt API.
4. **Model and Access Token Handling**: The method first checks for the model and access token. If they are not provided, it uses default values.
5. **Get Access Token**: If an access token is not available, the method makes a GET request to the VoiGpt website to retrieve the `csrftoken` from the response cookies and sets it as the `access_token`.
6. **API Request**: The method constructs a POST request to the `generate_response` endpoint of the VoiGpt API, sending the provided messages in the JSON payload. 
7. **Response Handling**: The method attempts to parse the JSON response from the API and yields the `response` from the JSON. If an error occurs during response parsing, it raises a `RuntimeError` with details about the API response.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt

# Example usage 
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]
provider = VoiGpt(model="gpt-3.5-turbo", access_token="your_access_token")
response = provider.create_completion(messages=messages)

# Process the response
print(next(response))
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".