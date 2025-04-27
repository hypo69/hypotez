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
This code defines a `Currency` class with constant string values representing different currencies.

Execution Steps
-------------------------
1. The code defines a class named `Currency`.
2. Inside the `Currency` class, several constant string variables are declared, each representing a different currency code, such as `USD`, `GBP`, `CAD`, etc.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.models.currencies import Currency

# Get the USD currency code
currency_code = Currency.USD 

# Print the currency code
print(currency_code)  # Output: USD
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".