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
This code block defines a function called `start_supplier` that initializes a supplier instance based on the provided `supplier_prefix` and `locale`.

Execution Steps
-------------------------
1. **Check for valid input:** The code first checks if both `supplier_prefix` and `locale` are provided. If either is missing, it returns an error message indicating that the scenario and language are not set.
2. **Create a dictionary of parameters:** The code then creates a dictionary called `params` to store the `supplier_prefix` and `locale` values.
3. **Initialize the Supplier instance:** The code uses the `Supplier` class (which is not shown in this snippet) to create a new instance with the provided parameters.
4. **Return the Supplier instance:** The function returns the initialized `Supplier` object.

Usage Example
-------------------------

```python
    # Example usage:
    supplier_instance = start_supplier('HB', 'en')
    print(f"Started supplier: {supplier_instance}")

    # Example usage with missing parameters:
    result = start_supplier(None, None)
    print(f"Result: {result}")  # Output: "Result: Не задан сценарий и язык"
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".