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
This code block defines a class `Dynaspark` which implements a GPT-4-powered AI provider. It's a part of the `hypotez` project.  `Dynaspark` inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, ensuring compatibility with the project's AI infrastructure. It handles asynchronous requests to the `Dynaspark` API, allowing for interaction with a GPT-4 model.

Execution Steps
-------------------------
1. **Initialize Class**: The class `Dynaspark` is initialized with various attributes like `url`, `api_endpoint`, `models`, and `model_aliases`. These attributes define the connection details, supported models, and potential aliases.

2. **Create Async Generator**: The `create_async_generator` class method is used to generate an asynchronous stream of responses from the GPT-4 model. It takes parameters like `model`, `messages`, `proxy`, and `media` to control the request.

3. **Format Prompt**: The provided `messages` are formatted into a string suitable for sending to the GPT-4 API using the `format_prompt` function.

4. **Send Request**: An asynchronous request is sent to the `Dynaspark` API (`api_endpoint`) using `ClientSession`. The request includes the formatted prompt, the chosen model, and optional media (images).

5. **Handle Response**: The response from the API is handled. The status code is checked using `raise_for_status`. The response text is parsed into JSON and yielded as a stream of responses.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Dynaspark import Dynaspark
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.image import load_image

# Initialize the Dynaspark provider
dynaspark_provider = Dynaspark()

# Define the conversation messages
messages = Messages(
    [
        {"role": "user", "content": "What is the meaning of life?"},
    ]
)

# Load an image (optional)
image = load_image('path/to/image.jpg')
media = [image] if image else None

# Create an asynchronous generator for responses
async_generator = dynaspark_provider.create_async_generator(
    model='gemini-1.5-flash', 
    messages=messages,
    media=media
)

# Iterate through the asynchronous generator to receive responses
async for response_part in async_generator:
    print(response_part)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".