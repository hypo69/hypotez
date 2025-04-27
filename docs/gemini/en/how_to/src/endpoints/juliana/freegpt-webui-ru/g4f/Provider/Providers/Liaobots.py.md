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
This code block defines a provider for Liaobots, a service that allows access to GPT-3.5-turbo and GPT-4 models. It sets up the provider's information, including its URL, supported models, and whether it requires authentication. The `_create_completion` function handles the actual interaction with the Liaobots API, sending requests and receiving responses.

Execution Steps
-------------------------
1. Defines the provider's URL, supported models, and authentication requirements.
2. Creates a dictionary `models` to store information about each supported model, including its ID, name, and maximum message length.
3. Defines the `_create_completion` function, which takes the model name, messages, and stream flag as arguments.
4. Sets up the headers for the HTTP request to the Liaobots API.
5. Constructs the JSON data for the request, including the conversation ID, model information, messages, and prompt.
6. Sends a POST request to the Liaobots API with the constructed JSON data.
7. Iterates over the response in chunks, yielding each token to the caller.

Usage Example
-------------------------

```python
    from g4f.Provider.Providers.Liaobots import _create_completion

    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    auth_key = "your_auth_key"
    response = _create_completion("gpt-3.5-turbo", messages, stream=False, auth=auth_key)
    print(response)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".