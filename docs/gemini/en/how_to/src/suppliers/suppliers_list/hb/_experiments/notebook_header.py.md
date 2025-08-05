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
The code snippet defines a `start_supplier` function. This function takes a supplier prefix and a locale as input and creates a `Supplier` object with the provided parameters. It then returns the created `Supplier` object.

Execution Steps
-------------------------
1. The function checks if both the `supplier_prefix` and `locale` parameters are provided. If not, it returns an error message.
2. The function creates a dictionary named `params` containing the `supplier_prefix` and `locale` values.
3. The function creates a `Supplier` object using the `params` dictionary.
4. The function returns the created `Supplier` object.

Usage Example
-------------------------

```python
    # Example usage of the start_supplier function
    supplier = start_supplier('HB', 'en')
    
    # Check the supplier object attributes
    print(f'Supplier prefix: {supplier.supplier_prefix}')
    print(f'Locale: {supplier.locale}')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".