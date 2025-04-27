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
This code block defines a class `Voodoohop_Flux1Schnell` which extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes, implementing an image generation API provider.

Execution Steps
-------------------------
1. **Initialization:** The class is initialized with attributes like its label, URL, API endpoint, default model, and supported model aliases. 
2. **Async Generator Creation:** The `create_async_generator` method is used to generate an asynchronous generator that handles the image generation process.
    - **Input Parameters:** Takes parameters like model, messages, proxy, prompt, image dimensions, number of inference steps, and seed.
    - **Prompt Formatting:** The prompt is formatted based on the messages and provided prompt.
    - **Payload Creation:** A payload containing the prompt, seed, dimensions, and inference steps is created.
    - **API Request:** An API request is sent to the specified endpoint using `aiohttp` with the prepared payload.
    - **Status Monitoring:** The code continuously monitors the API response for status updates.
    - **Event Handling:** It checks for events like `error` or `complete` and handles them accordingly.
    - **Image Response:** If the event is `complete`, the code extracts the image URL and yields an `ImageResponse` containing the image URL.
    - **Generator Termination:** Once the event `complete` is received, the generator is terminated.


Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Voodoohop_Flux1Schnell import Voodoohop_Flux1Schnell

    async def generate_image(prompt: str):
        provider = Voodoohop_Flux1Schnell()
        async for response in provider.create_async_generator(model="flux-schnell", prompt=prompt):
            image_url = response.images[0]
            print(f"Image URL: {image_url}")

    if __name__ == "__main__":
        import asyncio
        asyncio.run(generate_image(prompt="A beautiful sunset over a vast ocean"))

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".