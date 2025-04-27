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
This code block defines a provider class for H2o AI's GPT-GM API, enabling interactions with the model for text generation.

Execution Steps
-------------------------
1. **Initialization**: The code sets up the necessary components for interacting with the H2o GPT-GM API.
    - Defines `url` and `model` variables to store the API endpoint and supported models, respectively.
    - Defines `supports_stream` and `needs_auth` variables to indicate the API's capabilities.
    - Creates a dictionary named `models` mapping model names to their corresponding H2o model identifiers.
2. **`_create_completion` function**: This function creates and sends a completion request to the H2o GPT-GM API.
    - It constructs a conversation string by concatenating the messages passed as input.
    - It creates a `requests` session object to handle API calls.
    - It sets up necessary headers for API interaction.
    - It performs a GET request to the H2o GPT-GM website to verify the connection.
    - It performs a POST request to `/settings` to send user preferences.
    - It performs a POST request to `/conversation` to initiate a conversation with the model.
    - It performs a POST request to `/conversation/{conversationId}` to send the user's conversation prompt.
    - It retrieves the response from the API as a stream of text.
    - It yields individual tokens from the response stream until the end-of-text marker is encountered.
3. **Function Parameters**: 
    - `model`: The name of the GPT-GM model to use for text generation.
    - `messages`: A list of messages in the conversation history.
    - `stream`: Flag indicating whether to stream the response or receive it as a single text block.
    - `kwargs`: Additional parameters for the model, such as temperature, truncate length, maximum new tokens, sampling, repetition penalty, and return full text flags.
4. **Usage Example**:

```python
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import H2o

provider = H2o()

messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you. How are you?'},
]
model = 'falcon-7b'

response = provider.completion(model=model, messages=messages, temperature=0.7)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".