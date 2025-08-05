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
This code block implements the `Goabror` class, which acts as a provider for generating text using the Goabror API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to provide asynchronous text generation capabilities. The class defines the necessary URL endpoints, default model, and model options for interacting with the Goabror API.

Execution Steps
-------------------------
1. **Initialization**: The `Goabror` class defines the URL endpoints (`url` and `api_endpoint`), default model (`default_model`), and supported models (`models`) for interacting with the Goabror API.
2. **Asynchronous Text Generation**: The `create_async_generator` method is called to initiate asynchronous text generation. This method takes the model name, messages (input text), optional proxy settings, and additional keyword arguments.
3. **API Request**: The method constructs a GET request to the Goabror API endpoint using `aiohttp.ClientSession`. The request parameters include the formatted prompt (`user`) and optional system prompt (`system`).
4. **Response Handling**: The method handles the API response, checking for success (using `raise_for_status`) and decoding the JSON response.
5. **Yielding Output**: The method yields the generated text, either as a JSON object (`json_response["data"]`) or as raw text, based on the response format.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Goabror import Goabror

async def generate_text(messages: list[dict]) -> list[str]:
    """
    Generates text using the Goabror API.
    
    Args:
        messages (list[dict]): A list of messages representing the conversation history.

    Returns:
        list[str]: A list of generated text responses.
    """
    provider = Goabror()
    async for response in provider.create_async_generator(model='gpt-4', messages=messages):
        yield response

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".