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
This code defines a class `PollinationsImage` which inherits from `PollinationsAI`. This class represents a provider for generating images using the Pollinations.AI API. It defines default image models and methods for creating an asynchronous generator to generate images based on given prompts.

Execution Steps
-------------------------
1. **Class Definition**: Defines a class `PollinationsImage` that inherits from `PollinationsAI`.
2. **Class Attributes**: Initializes default image models (`default_model`, `default_image_model`), a list of available image models (`image_models`), and a flag for model loading (`_models_loaded`).
3. **`get_models` Method**: This method retrieves and updates the list of available image models from the parent class (`PollinationsAI`) and adds any extra models specified in `extra_image_models`. It ensures that models are loaded only once.
4. **`create_async_generator` Method**: This method creates an asynchronous generator that yields image chunks generated using the Pollinations.AI API. It takes prompt, model, and other parameters as input, formats the prompt using `format_image_prompt`, and calls `_generate_image` to generate image chunks. 

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage

# Instantiate the PollinationsImage provider
provider = PollinationsImage()

# Create a list of messages
messages = [
    {"role": "user", "content": "Generate an image of a cat playing with a ball of yarn."}
]

# Generate an image using the provider
async for chunk in provider.create_async_generator(model='flux', messages=messages, n=1):
    # Process the image chunk
    print(chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".