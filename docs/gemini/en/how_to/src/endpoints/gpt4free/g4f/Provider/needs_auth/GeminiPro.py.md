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
This code block defines a class called `GeminiPro` that implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces. This class provides an asynchronous generator interface to access Google Gemini API endpoints for text generation and other language tasks.

Execution Steps
-------------------------
1. The code defines the class `GeminiPro` and sets its attributes, including the label, URL, login URL, API base URL, and default model. 
2. It defines the `get_models` class method to retrieve a list of available Gemini models. This method uses a GET request to the API endpoint `/models` and parses the response to extract the model names.
3. The `create_async_generator` class method is the core of the class. It takes several arguments, including the model name, messages, and API key. It constructs a POST request to the API endpoint for text generation, sends the request, and asynchronously yields the generated text, finish reason, and usage information.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GeminiPro import GeminiPro

# Initialize GeminiPro instance
gemini_pro = GeminiPro()

# Get available Gemini models
models = gemini_pro.get_models(api_key="YOUR_API_KEY")

# Generate text
messages = [
    {"role": "user", "content": "Hello, world!"},
]

async def generate_text():
    async for response in gemini_pro.create_async_generator(model="gemini-pro", messages=messages, api_key="YOUR_API_KEY"):
        print(response)

# Run the asynchronous function
asyncio.run(generate_text())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".