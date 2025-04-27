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
The code defines a `Pizzagpt` class that implements an asynchronous generator for interacting with the PizzaGPT API. This class allows for generating responses from the PizzaGPT model based on provided messages.

Execution Steps
-------------------------
1. **Initialization**: The `Pizzagpt` class is initialized with the base URL and API endpoint for the PizzaGPT service.
2. **Async Generator Creation**: The `create_async_generator` class method is called to initiate the asynchronous generator.
    - It takes the desired model, messages, and optional proxy as input.
    - It sets up HTTP headers, including a secret key, and a user agent.
    - It constructs the prompt based on the provided messages using the `format_prompt` helper function.
    - It sends a POST request to the PizzaGPT API endpoint with the formatted prompt.
    - It raises an exception if the API request fails.
    - It processes the API response, extracting the generated content.
    - It yields the generated content and a "stop" finish reason to signal the end of the response.
    - If the response contains a "Misuse detected" message, it raises a ValueError.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt
    from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

    # Create a list of messages
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    # Create a Pizzagpt instance
    pizzagpt = Pizzagpt()

    # Get the response from the PizzaGPT API
    async for response in pizzagpt.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(response)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".