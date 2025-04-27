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
This code defines a `PerplexityApi` class that represents the Perplexity API. It inherits from the `OpenaiTemplate` class. 

Execution Steps
-------------------------
1. The code defines the `PerplexityApi` class, which inherits from `OpenaiTemplate`.
2. The `label` attribute is set to "Perplexity API", representing the API's name.
3. The `url` attribute is set to the Perplexity website's URL.
4. The `login_url` attribute is set to the URL for the API settings page.
5. The `working` attribute is set to `True`, indicating the API is functional.
6. The `needs_auth` attribute is set to `True`, indicating the API requires authentication.
7. The `api_base` attribute is set to the base URL for the API.
8. The `default_model` attribute is set to the default model used by the API.
9. The `models` attribute is a list containing all available models offered by the API.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.PerplexityApi import PerplexityApi

# Create an instance of the PerplexityApi class
perplexity_api = PerplexityApi()

# Access the API's information
print(perplexity_api.label)  # Output: "Perplexity API"
print(perplexity_api.url)  # Output: "https://www.perplexity.ai"
print(perplexity_api.default_model)  # Output: "llama-3-sonar-large-32k-online"

# Access the available models
print(perplexity_api.models)  # Output: A list of available models
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".