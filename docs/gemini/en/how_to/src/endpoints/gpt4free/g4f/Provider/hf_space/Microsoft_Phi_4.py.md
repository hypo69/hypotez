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
This code block defines a `Microsoft_Phi_4` class that represents a provider for the Microsoft Phi-4 multimodal model, which utilizes the Hugging Face Spaces infrastructure. The code implements the necessary methods and attributes for interacting with the Phi-4 model through its API endpoints, enabling the generation of both text and image responses.

Execution Steps
-------------------------
1. **Class Definition**:  The code defines the `Microsoft_Phi_4` class, inheriting from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing the base functionalities for asynchronous data generation and model-specific settings.
2. **Class Attributes**: The class initializes various attributes:
    - `label`: Specifies the label for the provider.
    - `space`:  Identifies the Hugging Face Spaces URL for the model.
    - `url`: Defines the main URL for the model's website.
    - `api_url`: Sets the URL for the model's API endpoint.
    - `referer`:  Specifies the referer header for API requests.
    - `working`: Indicates the provider's current working status.
    - `supports_stream`:  Defines whether the provider supports streamed responses.
    - `supports_system_message`:  Defines whether the provider supports system messages.
    - `supports_message_history`:  Defines whether the provider supports message history.
    - `default_model`:  Defines the default model to use.
    - `default_vision_model`: Defines the default vision model.
    - `model_aliases`:  Maps model aliases to the default model.
    - `vision_models`:  Lists the available vision models.
    - `models`:  Lists all available models.
3. **`run` Method**: The `run` method encapsulates the logic for interacting with the API endpoints based on the requested action (`predict`, `post`, or `get`).
4. **`create_async_generator` Method**: This method handles the asynchronous generation of responses from the model:
    - It formats the prompt based on the provided messages.
    - It handles session management (creating a new session or using an existing one).
    - It handles image upload if `media` is provided.
    - It iterates through the response stream and yields the generated content.
5. **Error Handling**: The code incorporates error handling mechanisms to catch and manage potential issues during communication with the API.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
    from hypotez.src.endpoints.gpt4free.g4f.Provider.base_provider import Messages

    provider = Microsoft_Phi_4()

    # Create a message history
    messages = Messages(
        [
            {
                "role": "user",
                "content": "Hello, how are you?"
            },
            {
                "role": "assistant",
                "content": "I am doing well, thank you for asking. How can I assist you today?"
            }
        ]
    )

    # Generate a response
    async for response in provider.create_async_generator(messages=messages):
        print(f"Response: {response}")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".