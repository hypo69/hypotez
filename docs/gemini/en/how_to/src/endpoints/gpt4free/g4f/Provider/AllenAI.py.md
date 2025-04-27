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
This code block defines the `AllenAI` class, an implementation of the `AsyncGeneratorProvider` for interacting with the AllenAI Playground API for generating text. 

Execution Steps
-------------------------
1. **Initialization**: The `AllenAI` class is initialized with various attributes including the API endpoint, default model, supported models, and authentication requirements.
2. **Model Alias Handling**: The `model_aliases` dictionary maps commonly used model names to their corresponding official names in the AllenAI Playground API. 
3. **Asynchronous Generator Creation**: The `create_async_generator` method handles the asynchronous generation of text from the AllenAI Playground API.
4. **Prompt Formatting**: The `format_prompt` function (from `helper.py`) is used to format the user's input prompts for the API.
5. **Conversation Management**: The `Conversation` class manages the conversation history, including user prompts and assistant responses.
6. **Multipart Form Data Creation**: The code constructs a multipart form data payload with the formatted prompt, model selection, and other parameters for the API request.
7. **API Request**: An asynchronous HTTP POST request is made to the AllenAI Playground API endpoint using `aiohttp`. 
8. **Response Processing**: The code streams the API response, parses JSON data, and yields the assistant's generated text chunks.
9. **Conversation Update**: The `parent` attribute of the `Conversation` object is updated to track the conversation history.
10. **Final Response**: The `finish_reason` and `final` flags in the API response signal the completion of the text generation. 
11. **Return Values**: The `create_async_generator` method returns an asynchronous result (`AsyncResult`) with generated text chunks and conversation information.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.AllenAI import AllenAI
from hypotez.src.endpoints.gpt4free.g4f.Provider.Conversation import Conversation
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Initialize a conversation object
conversation = Conversation("tulu3-405b")

# Define user prompts
messages: Messages = [
    {"role": "user", "content": "What is the meaning of life?"},
    {"role": "assistant", "content": "That's a big question!"},
]

# Instantiate the AllenAI provider 
provider = AllenAI()

# Generate text asynchronously 
async for chunk in provider.create_async_generator(model="tulu3-405b", messages=messages, conversation=conversation):
    print(chunk)

# Access conversation history
print(conversation.messages)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".