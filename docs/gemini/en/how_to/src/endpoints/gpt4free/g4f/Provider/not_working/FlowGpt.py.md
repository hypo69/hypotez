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
The `FlowGpt` class represents a provider for FlowGPT API interactions, allowing asynchronous generation of responses based on user prompts and model selection. It implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces for consistent interaction with other providers.

Execution Steps
-------------------------
1. **Initialize Provider**: The code initializes a `FlowGpt` instance, setting its essential properties like API URL, supported models, and default model.
2. **Generate Response**: The `create_async_generator` class method handles the generation of responses. It takes model type, messages, optional parameters (proxy, temperature, etc.), and returns an asynchronous generator.
3. **Construct Request**: The method builds a request to the FlowGPT API with relevant data, including model, message history, system message, and parameters.
4. **Send Request**: An asynchronous HTTP POST request is sent to the API endpoint using `aiohttp`.
5. **Process Response**: The code iterates through response chunks, parses them as JSON objects, and filters for relevant "text" events.
6. **Yield Responses**: For each valid response, the code yields the corresponding text content.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FlowGpt import FlowGpt

async def main():
    provider = FlowGpt()
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I am an AI, I don't have feelings, but I am here to help!"},
    ]
    async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(f"Response: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".