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
This code block defines a `neural_networks` class which contains methods for interacting with different neural networks, including FLUX.1-schnell, mistral-large-2409, and gpt-4o-mini. These methods handle sending requests to the respective API endpoints and processing the responses.

Execution Steps
-------------------------
1. The `_FLUX_schnell` method sends a request to the FLUX.1-schnell API endpoint with provided prompt, size, seed, and number of inference steps. It retries the request up to 6 times using different API tokens.
2. If the request is successful, it opens the response content as an image and returns it.
3. The `__mistral_large_2407` method sends a request to the Mistral API endpoint with a provided list of messages and returns the generated message, prompt tokens, and completion tokens.
4. The `_free_gpt_4o_mini` method sends a request to the GPT-4o-mini API endpoint with a provided list of messages. It retries the request up to 6 times using different API tokens.
5. If the request is successful, it returns the generated message, prompt tokens, and completion tokens. Otherwise, it calls the `__mistral_large_2407` method to generate a response using the Mistral API.

Usage Example
-------------------------

```python
    from ToolBox.ToolBox_n_networks import neural_networks

    nn = neural_networks()

    # Generate an image using FLUX.1-schnell
    prompt = "A cat sitting on a chair"
    size = [512, 512]
    seed = randint(0, 1000)
    num_inference_steps = 50
    image = nn._FLUX_schnell(prompt, size, seed, num_inference_steps)

    # Generate text using GPT-4o-mini
    prompt = [
        {"role": "user", "content": "What is the meaning of life?"}
    ]
    response, prompt_tokens, completion_tokens = nn._free_gpt_4o_mini(prompt)

    print(f"Response: {response}")
    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Completion Tokens: {completion_tokens}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".