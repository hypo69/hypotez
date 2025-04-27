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
This code block defines a function named `start_supplier` which is responsible for initializing a supplier based on provided parameters. It sets up the necessary environment by adding the project's root directory to the `sys.path` and imports relevant modules. It then defines a dictionary `params` containing the `supplier_prefix` and `locale` values, and finally, it returns a Supplier object initialized with these parameters.

Execution Steps
-------------------------
1. **Imports Necessary Modules:** The code starts by importing various modules like `sys`, `os`, `pathlib`, `gs`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, and `save_text_file`.
2. **Sets Up Environment:** The code adds the project's root directory to the `sys.path` to ensure proper module imports.
3. **Defines `start_supplier` Function:** The function takes `supplier_prefix` and `locale` as arguments and returns a Supplier object.
4. **Creates Parameter Dictionary:** Inside the function, a dictionary `params` is created to store the `supplier_prefix` and `locale` values.
5. **Initializes Supplier Object:** The function then returns a Supplier object initialized with the `params` dictionary.

Usage Example
-------------------------

```python
    # Example usage
    supplier_prefix = 'amazon'  # Set the supplier prefix
    locale = 'en'  # Set the locale

    # Start the supplier
    supplier = start_supplier(supplier_prefix, locale)

    # Use the supplier object to access supplier-specific functions
    print(supplier.get_products())  # Example call to get products
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".