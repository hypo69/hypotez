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
This code block defines a function called `start_supplier` which initializes a supplier object based on the provided `supplier_prefix` and `locale`.

Execution Steps
-------------------------
1. **Define Parameters**: The function takes two parameters: `supplier_prefix` (a string representing the supplier's prefix, e.g., "aliexpress") and `locale` (a string representing the language locale, e.g., "en").
2. **Create Parameter Dictionary**: It creates a dictionary `params` containing the passed parameters.
3. **Instantiate Supplier Object**: It creates an instance of the `Supplier` class using the `params` dictionary and returns it.

Usage Example
-------------------------

```python
    from src.suppliers.suppliers_list.morlevi._experiments.JUPYTER_header import start_supplier

    # Initialize an AliExpress supplier in English
    supplier = start_supplier(supplier_prefix='aliexpress', locale='en') 

    # Access supplier properties
    print(supplier.supplier_prefix)  # Output: 'aliexpress'
    print(supplier.locale)  # Output: 'en' 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".