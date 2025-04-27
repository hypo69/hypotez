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
This code snippet defines a function called `_create_completion` which interacts with the Gravity Engine API to generate text completions. It uses the `requests` library to send HTTP POST requests to the specified URL and handles the response by streaming the generated text.

Execution Steps
-------------------------
1. **Define Endpoint and Model**: The `url` and `model` variables are defined, setting the base API URL and available models for text generation.
2. **Define Function**: The `_create_completion` function is defined with parameters for the model, messages, stream, and optional keyword arguments.
3. **Construct Request Data**: The function constructs a JSON payload containing the chosen model, temperature, presence penalty, and the list of messages to be used as context for the completion.
4. **Send HTTP Request**: The function uses the `requests.post` method to send a POST request to the Gravity Engine API endpoint, providing the headers, data, and stream argument.
5. **Stream Response**: The function uses a generator to yield the generated text from the API response, allowing for streaming output.
6. **Handle API Response**: The function extracts the generated text content from the response JSON object and yields it to the caller.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers import Gravityengine

    # Example messages to pass to the model
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Can you tell me about the history of the internet?"}
    ]

    # Initialize the Gravityengine provider
    provider = Gravityengine.Gravityengine()

    # Generate a text completion using the Gravityengine provider
    for chunk in provider._create_completion(model='gpt-3.5-turbo-16k', messages=messages, stream=True):
        print(chunk, end="")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".