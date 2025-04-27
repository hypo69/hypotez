**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
========================================================================================

Description
-------------------------
The `AmigoChat` class implements an asynchronous generator provider for interacting with the AmigoChat API. It supports both chat and image generation models, and offers various parameters for customizing the response.

Execution Steps
-------------------------
1. **Model Selection**: The code first defines a dictionary `MODELS` containing mappings between model names and their corresponding persona IDs. These mappings are used to identify specific models within the AmigoChat API.
2. **Model Aliases**: The `model_aliases` dictionary provides a list of aliases for common models, simplifying the process of specifying models.
3. **`get_personaId` Method**: This method retrieves the persona ID for a given model based on the `MODELS` dictionary.
4. **`generate_chat_id` Method**: This static method generates a unique chat ID using UUIDs.
5. **`create_async_generator` Method**: This method is the core of the `AmigoChat` provider. It handles the following actions:
    - **Model Selection**: The provided `model` is mapped to its corresponding persona ID using `get_personaId`.
    - **Request Setup**: The method constructs a dictionary containing request parameters, including the generated chat ID, message history, model name, persona ID, and other settings.
    - **API Call**: The method sends a POST request to the specified AmigoChat API endpoint (`chat_api_endpoint` or `image_api_endpoint`) with the constructed request data.
    - **Response Handling**: If the request is successful, the method iterates through the response lines and yields each generated text chunk or image URL.
    - **Error Handling**: The code includes a retry mechanism with a maximum number of retries to handle potential network errors or API failures.
6. **Usage Example**:
    - **Import**: Import the `AmigoChat` class: 
    ```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AmigoChat import AmigoChat
    ```
    - **Create an Instance**: Create an instance of `AmigoChat`:
    ```python
    provider = AmigoChat()
    ```
    - **Use `create_async_generator`**: Generate responses using the `create_async_generator` method:
    ```python
    messages = [
        {'role': 'user', 'content': 'Hello, how are you?'},
    ]
    async for response in provider.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(response)
    ```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".