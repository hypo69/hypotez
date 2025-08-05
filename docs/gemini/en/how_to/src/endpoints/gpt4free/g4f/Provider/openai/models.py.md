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
This code block defines a list of available models for text and image generation. It also sets default models for text and image generation.

Execution Steps
-------------------------
1. **Defines default models**: Sets `default_model` to "auto" for text generation and `default_image_model` to "dall-e-3" for image generation.
2. **Creates lists of available models**: 
    - `image_models`: contains the default image model, "dall-e-3".
    - `text_models`: contains the default text model "auto" and other available text models.
    - `vision_models`:  is a copy of `text_models`, indicating that the available vision models are the same as the text models.
3. **Combines text and image models**: Creates a list `models` that includes both text and image models.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.openai.models import models, text_models, image_models

# Access available models
print(models)  # Prints the combined list of text and image models
print(text_models) # Prints the list of available text models
print(image_models) # Prints the list of available image models

# Use a specific model
selected_model = "gpt-4"  # Choose a specific model
if selected_model in text_models:
    # Use selected_model for text generation
    ...
elif selected_model in image_models:
    # Use selected_model for image generation
    ...
else:
    print(f"Invalid model: {selected_model}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".