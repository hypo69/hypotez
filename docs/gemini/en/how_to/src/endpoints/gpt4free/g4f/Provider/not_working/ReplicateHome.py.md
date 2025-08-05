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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use This Code Block
=========================================================================================

### Description
-------------------------
The code snippet implements the `ReplicateHome` class, a provider for the Replicate API that allows interaction with both text and image models. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` classes, enabling asynchronous generation and model management.

### Execution Steps
-------------------------
1. **Model and Version Setup**:
    - The class defines a list of supported text and image models, their aliases, and corresponding versions.
    - These models are used for generating text or images based on provided prompts.
2. **Async Generator Creation**:
    - The `create_async_generator` class method is responsible for initiating and handling the generation process.
    - It receives the model name, user messages, and optional prompt as input.
3. **API Request**:
    - The method constructs a POST request to the Replicate API endpoint (`https://homepage.replicate.com/api/prediction`) with the model name, version, and user prompt.
    - The response is checked for success and errors.
4. **Polling for Results**:
    - After initiating the prediction, the method polls a URL to check the status of the request.
    - It performs up to 30 attempts with a 5-second delay between each attempt.
5. **Output Handling**:
    - Upon successful completion, the method yields the generated results in the desired format:
        - For image models, it yields an `ImageResponse` object containing the image URL and prompt.
        - For text models, it yields individual chunks of generated text.
6. **Error Handling**:
    - The method handles potential errors during the prediction process, raising exceptions for failed or timed-out requests.

### Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ReplicateHome import ReplicateHome

async def generate_image(prompt: str):
    provider = ReplicateHome()
    async for response in provider.create_async_generator(model='sd-3', prompt=prompt):
        print(response)

async def main():
    await generate_image("A beautiful sunset over a calm ocean")

if __name__ == "__main__":
    asyncio.run(main())