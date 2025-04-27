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
This code defines a class `BlackForestLabs_Flux1Dev` which implements an asynchronous generator provider for image generation with the Flux-1-Dev model from Black Forest Labs. It provides functions for creating a generator that streams responses, including intermediate reasoning steps, image previews, and final results.

Execution Steps
-------------------------
1. **Initialize a StreamSession**: Creates a new session object to handle communication with the Black Forest Labs Flux-1-Dev service.
2. **Format the image prompt**: Processes the given prompt text for image generation.
3. **Prepare image parameters**: Sets up image size and aspect ratio based on the provided parameters.
4. **Create a JsonConversation object**: Initializes a conversation object to track session information and tokens.
5. **Obtain Zerogpu tokens**: Retrieves the necessary tokens for accessing the service if not provided.
6. **Send a POST request**: Sends a request to the service to queue the image generation task.
7. **Handle Event Stream**: Receives responses from the service through an event stream, yielding reasoning steps, image previews, and final results.
8. **Process responses**: Decodes and interprets the responses from the event stream, providing different kinds of results to the user.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev
from hypotez.src.endpoints.gpt4free.g4f.requests import StreamSession
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Create a StreamSession object
session = StreamSession()

# Create a BlackForestLabs_Flux1Dev provider instance
provider = BlackForestLabs_Flux1Dev()

# Define a prompt and a list of messages
prompt = "A photo of a cat in a hat"
messages = Messages(messages=[{"role": "user", "content": prompt}])

# Generate images using the provider
async for response in provider.create_async_generator(messages=messages, model="flux", proxy=None):
    if isinstance(response, Reasoning):
        print(f"Reasoning: {response.status}")
    elif isinstance(response, ImagePreview):
        print(f"Preview: {response.url}")
    elif isinstance(response, ImageResponse):
        print(f"Final image: {response.url}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".