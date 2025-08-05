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
This code block defines a class `G4F`, which is a subclass of `DeepseekAI_JanusPro7b`. The class inherits methods and attributes from its parent class and implements an asynchronous generator for generating image responses based on user input.

Execution Steps
-------------------------
1. **Initialization**: The class `G4F` inherits attributes and methods from `DeepseekAI_JanusPro7b`.
2. **Model Selection**: The `create_async_generator` method checks the selected model (`model` argument). If the model is "flux" or "flux-dev", it delegates the request to the `FluxDev` class.
3. **Prompt and Seed**: The method formats the user prompt (`prompt`) and generates a random seed (`seed`) if not provided by the user.
4. **API Request**: An asynchronous `ClientSession` is created, and an API request is sent to the `url_flux` endpoint with the prepared payload, including prompt, seed, dimensions, and other parameters.
5. **Token Acquisition**: If an API key is not provided, the method acquires a GPU token from the Hugging Face space.
6. **Response Handling**: The response from the API is parsed, and the image URL is extracted. An `ImageResponse` object is created and yielded.
7. **Status Updates**: During the image generation process, the generator yields `Reasoning` objects with status updates.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.G4F import G4F
    from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
    
    messages = Messages(
        [
            {"role": "user", "content": "Generate a picture of a cat sitting in a basket."},
        ]
    )
    
    async def main():
        async for chunk in G4F.create_async_generator(model="flux", messages=messages):
            print(chunk)
            if isinstance(chunk, ImageResponse):
                print(f"Image URL: {chunk.image_url}")

    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".