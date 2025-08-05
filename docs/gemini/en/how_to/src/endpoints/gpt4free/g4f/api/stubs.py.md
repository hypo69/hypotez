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
This code defines models for configuration and responses from the gpt4free API. 

Execution Steps
-------------------------
1. **Imports**: Imports necessary libraries like `pydantic`, `typing`, and `g4f.typing` to define data structures.
2. **Model Definitions**: Defines Pydantic models for various configurations and responses:
    - `ChatCompletionsConfig`: Represents the configuration for chat completion requests.
    - `ImageGenerationConfig`: Represents the configuration for image generation requests.
    - `ProviderResponseModel`: Represents the response from a provider.
    - `ProviderResponseDetailModel`: Provides more detailed information about a provider.
    - `ModelResponseModel`: Represents the response for a specific model.
    - `UploadResponseModel`: Represents the response for an uploaded file.
    - `ErrorResponseModel`: Represents an error response.
    - `ErrorResponseMessageModel`: Represents the error message within an error response.
    - `FileResponseModel`: Represents the response for a downloaded file.
3. **Field Definitions**: Each model defines various fields (parameters) with their respective data types and optional values.

Usage Example
-------------------------

```python
from g4f.api.stubs import ChatCompletionsConfig, ImageGenerationConfig

# Chat completion configuration example
chat_config = ChatCompletionsConfig(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ],
    model="gpt-3.5-turbo",
    temperature=0.7,
)

# Image generation configuration example
image_config = ImageGenerationConfig(
    prompt="A photo of a cat wearing a hat",
    model="stable-diffusion",
    width=512,
    height=512,
)

# You can access the fields of the configuration models using dot notation
print(chat_config.messages)  # Output: The list of messages
print(image_config.prompt)  # Output: The image generation prompt
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".