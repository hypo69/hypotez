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
The `Jmuz` class provides an interface for interacting with the Jmuz GPT API. It inherits from the `OpenaiTemplate` class and defines specific attributes and methods for the Jmuz API.

Execution Steps
-------------------------
1. The class defines the API URL, API key, and whether the API is currently working.
2. It also specifies the default model and provides aliases for different models.
3. The `get_models` method retrieves available models from the API.
4. The `create_async_generator` method creates an asynchronous generator that yields chunks of text from the API response.
5. The method filters out unwanted messages from the API response, including messages about Discord invites and promotional messages.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider import Jmuz

    # Initialize the Jmuz provider
    jmuz = Jmuz()

    # Specify the model and messages
    model = 'gpt-4o'
    messages = [
        {'role': 'user', 'content': 'What is the meaning of life?'}
    ]

    # Create an asynchronous generator for the response
    async_generator = jmuz.create_async_generator(model=model, messages=messages)

    # Iterate over the response chunks
    async for chunk in async_generator:
        print(chunk)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".