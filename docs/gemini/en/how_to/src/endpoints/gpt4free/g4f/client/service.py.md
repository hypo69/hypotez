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
This code block defines two functions: `convert_to_provider` and `get_model_and_provider`.

- `convert_to_provider`: Converts a provider string into a ProviderType object. It handles single provider names and provider lists.
- `get_model_and_provider`: Retrieves the model and provider based on input parameters, handling various scenarios for model and provider input, including string identifiers, objects, and default values. The function also checks provider availability, streaming support, and logs the chosen provider and model.

Execution Steps
-------------------------
1. **`convert_to_provider` Function:**
    - Takes a provider string as input.
    - If the provider string contains spaces, it splits it into individual providers and checks if they exist in the `ProviderUtils.convert` dictionary.
    - If any provider is not found, it raises a `ProviderNotFoundError`.
    - If all providers are found, it creates an `IterListProvider` object with the list of providers.
    - If the provider string is a single name, it checks if it exists in the `ProviderUtils.convert` dictionary.
    - If the provider is found, it retrieves the corresponding `ProviderType` object from the dictionary.
    - If the provider is not found, it raises a `ProviderNotFoundError`.
    - The function returns the converted provider object.

2. **`get_model_and_provider` Function:**
    - Takes model, provider, stream, ignore_working, ignore_stream, and logging arguments.
    - Converts the provider string into a `ProviderType` object using `convert_to_provider`.
    - Converts the model string into a `Model` object using `ModelUtils.convert`.
    - If no provider is provided, it determines the default model and provider based on the presence of images and the `default` and `default_vision` objects.
    - If no model is provided, it uses the default model or retrieves the default model associated with the provider.
    - If the provider is not found, it raises a `ProviderNotFoundError`.
    - Checks if the provider is working and raises a `ProviderNotWorkingError` if it's not working.
    - Checks if the provider supports streaming and raises a `StreamNotSupportedError` if it doesn't support streaming and the `stream` argument is True.
    - Logs the selected provider and model using the debug module.
    - Stores the last used provider and model in the debug module.
    - Returns the model name and provider type as a tuple.

Usage Example
-------------------------

```python
from g4f.client.service import get_model_and_provider

# Use the default model and provider
model, provider = get_model_and_provider(None, None, stream=False)
print(f"Using {provider} and {model}")

# Use a specific model and provider
model, provider = get_model_and_provider("text-davinci-003", "OpenAI", stream=True)
print(f"Using {provider} and {model}")

# Use a specific model and ignore provider check
model, provider = get_model_and_provider("text-davinci-003", None, stream=True, ignore_working=True)
print(f"Using {provider} and {model}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".