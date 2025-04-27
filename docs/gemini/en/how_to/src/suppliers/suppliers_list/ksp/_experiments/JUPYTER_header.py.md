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
This code block defines a function called `start_supplier`. The function takes two arguments: `supplier_prefix` and `locale`. It creates a dictionary `params` with these arguments.  It then returns a `Supplier` object initialized with these `params`. 

Execution Steps
-------------------------
1. **Define the `start_supplier` function:**
   - The function takes two arguments:
     - `supplier_prefix`: A string representing the supplier prefix (e.g., 'aliexpress').
     - `locale`: A string representing the locale (e.g., 'en').
2. **Create a dictionary `params`:**
   - This dictionary holds the `supplier_prefix` and `locale` values.
3. **Initialize a `Supplier` object:**
   - The function calls the `Supplier` class constructor with the `params` dictionary.
4. **Return the `Supplier` object:**
   - The function returns the newly created `Supplier` object.

Usage Example
-------------------------

```python
    # Start the 'aliexpress' supplier in English
    supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

    # Use the supplier object
    print(supplier)  # Output: <Supplier object>
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".