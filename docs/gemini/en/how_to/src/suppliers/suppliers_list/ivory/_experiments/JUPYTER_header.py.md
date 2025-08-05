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
This code block defines a function called `start_supplier` which initializes and returns a `Supplier` object. The function takes two arguments:

- `supplier_prefix`: A string representing the supplier's prefix, defaulting to 'aliexpress'.
- `locale`: A string representing the locale, defaulting to 'en'.

The function creates a dictionary `params` containing these arguments and then uses it to create a `Supplier` object.

Execution Steps
-------------------------
1. Defines a function `start_supplier` with default arguments `supplier_prefix = 'aliexpress'` and `locale = 'en'`.
2. Creates a dictionary `params` to store the function arguments.
3. Initializes a `Supplier` object using the `params` dictionary.
4. Returns the initialized `Supplier` object.

Usage Example
-------------------------

```python
    # Call the start_supplier function to create a Supplier object
    supplier = start_supplier(supplier_prefix='amazon', locale='de') 

    # Use the Supplier object for further operations
    # ...
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".