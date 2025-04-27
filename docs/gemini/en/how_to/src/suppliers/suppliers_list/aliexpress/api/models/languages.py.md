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
This code defines a class named `Language` that acts as a container for language codes used in the AliExpress API. 

Execution Steps
-------------------------
1. The `Language` class is defined, encapsulating language codes as class attributes.
2. Each attribute represents a supported language code with its corresponding value, e.g., `EN = 'EN'`.
3. These language codes can be accessed directly using the class name and attribute, e.g., `Language.EN`.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.models.languages import Language

# Retrieve the language code for English
language_code = Language.EN  # 'EN'

# Use the language code in your API request
print(f"The language code is: {language_code}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".