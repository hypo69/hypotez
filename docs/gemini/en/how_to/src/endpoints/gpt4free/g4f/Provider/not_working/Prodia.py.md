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
This code block defines the `Prodia` class, which is a provider for generating images using the Prodia API. It implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces, providing asynchronous image generation capabilities. 

Execution Steps
-------------------------
1. The code initializes the `Prodia` class with the API endpoint (`api_endpoint`) and the default model (`default_model`).
2. It defines a list of available image models (`image_models`) and a list of all available models (`models`), which includes both image and text models.
3. The `get_model` class method retrieves the specified model from the available models list or uses the default model if the provided model is not found.
4. The `create_async_generator` class method is used to create an asynchronous generator for image generation. It accepts various parameters, including the model, prompt, negative prompt, steps, cfg, seed, sampler, and aspect ratio.
5. It retrieves the prompt from the messages list and sets up a dictionary (`params`) with the provided parameters.
6. It sends a GET request to the Prodia API endpoint with the parameters using an `aiohttp` session.
7. The response data includes the job ID.
8. The `_poll_job` class method is used to monitor the job status until it is completed or fails. It sends a GET request to the job status endpoint and checks the status of the job.
9. If the job is successful, the image URL is extracted and an `ImageResponse` object is returned. 
10. If the job fails, an exception is raised.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Prodia import Prodia

    async def generate_image():
        provider = Prodia()
        messages = [
            {'role': 'user', 'content': 'A cute cat wearing a hat'}
        ]
        async for response in provider.create_async_generator(model='absolutereality_v181.safetensors [3d9d4d2b]', messages=messages):
            print(response.image_url)
            # Do something with the image, e.g., save it to a file
            # ...

    asyncio.run(generate_image())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".