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
The `MetaAIAccount` class inherits from `MetaAI` and represents a specific provider for AI interactions with MetaAI. This class requires authentication (needs_auth = True), utilizes the parent class "MetaAI" for functionalities, and supports image generation using the "meta" model. The `create_async_generator` method generates an asynchronous stream of responses based on the provided messages, model, proxy, and cookies.

Execution Steps
-------------------------
1. The `create_async_generator` method receives parameters like `model`, `messages`, `proxy`, and `cookies`.
2. If no cookies are provided, it retrieves cookies from the ".meta.ai" domain using the `get_cookies` helper function.
3. It initializes a `MetaAI` object with the provided proxy.
4. It formats the input `messages` into a prompt using the `format_prompt` helper function.
5. The method iterates asynchronously over the output of the `prompt` method of the `MetaAI` object, which takes the formatted prompt and cookies as arguments.
6. For each chunk of data received from the `prompt` method, it yields the chunk using the `async for` loop, making it an asynchronous generator.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAIAccount import MetaAIAccount

# Define messages for the prompt
messages = [
    {"role": "user", "content": "Generate an image of a cat."},
]

# Create an asynchronous generator for the MetaAI response
async_generator = MetaAIAccount.create_async_generator(
    model="meta",  # Specify the "meta" model for image generation
    messages=messages, 
    proxy="your_proxy_server",  # Optional proxy
    cookies="your_cookies_dictionary",  # Optional cookies
)

# Process the asynchronous response
async for chunk in async_generator:
    print(chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".