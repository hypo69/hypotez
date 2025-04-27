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
This code block sets up the environment for working with the `gearbest` supplier in the `hypotez` project. It imports necessary modules, configures paths, and defines a function to start the supplier.

Execution Steps
-------------------------
1. **Imports:** The code imports modules like `sys`, `os`, `Path`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `PrestaProduct`, and `save_text_file`.
2. **Path Configuration:** It defines the root directory of the project (`dir_root`) and adds it to the `sys.path`. Then, it sets the `dir_src` path pointing to the `src` directory.
3. **Function Definition:** The `start_supplier` function takes two parameters: `supplier_prefix` and `locale`.
4. **Parameter Setup:** Inside the function, a dictionary `params` is created with the `supplier_prefix` and `locale` values.
5. **Supplier Initialization:** The function returns a `Supplier` object initialized with the `params` dictionary.

Usage Example
-------------------------

```python
    # Start the gearbest supplier with English locale
    supplier = start_supplier(supplier_prefix='gearbest', locale='en')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".