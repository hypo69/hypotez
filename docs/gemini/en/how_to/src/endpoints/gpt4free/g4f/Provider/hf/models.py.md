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
This code block defines several lists and dictionaries containing model names and aliases for different GPT4Free providers. It includes:
- `default_model`, `default_image_model`: Default model names for text and image generation.
- `text_models`, `image_models`: Lists of supported text and image models.
- `fallback_models`: A list of fallback models to use if the preferred model is unavailable.
- `model_aliases`: A dictionary mapping model aliases to their full names.
- `extra_models`: A list of additional models not included in the primary lists.
- `default_vision_model`, `default_llama_model`: Default models for vision and llama generation.
- `vision_models`: A list of supported vision models.

Execution Steps
-------------------------
1. Defines `default_model` and `default_image_model` variables to hold the default model names.
2. Creates `image_models` list with default image model and "black-forest-labs/FLUX.1-schnell" model.
3. Creates `text_models` list with default model, "meta-llama/Llama-3.3-70B-Instruct", and other text generation models.
4. Combines `text_models` and `image_models` into `fallback_models` list.
5. Defines `model_aliases` dictionary to map aliases to full model names.
6. Defines `extra_models` list with additional models.
7. Defines `default_vision_model` and `default_llama_model` for vision and llama generation.
8. Creates `vision_models` list with default vision model and "Qwen/Qwen2-VL-7B-Instruct" model.

Usage Example
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.hf.models import text_models, model_aliases

# Get a list of supported text models
print(text_models)

# Get the full name of a model by its alias
model_name = model_aliases["llama-3.3-70b"]
print(model_name)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".