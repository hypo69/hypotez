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
This code snippet defines a function `start_supplier` that takes a `supplier_prefix` as input and creates a `Supplier` object with the given prefix. It then initializes a `Scenario` object using the created `Supplier` and runs the scenario's predefined test cases.

Execution Steps
-------------------------
1. **`start_supplier` function:**
    - Takes a `supplier_prefix` as input.
    - Creates a dictionary `params` with the `supplier_prefix`.
    - Instantiates a `Supplier` object using the `params` dictionary.
    - Returns the created `Supplier` object.
2. **Initialization of variables:**
    - Sets `supplier_prefix` to `'aliexpress'`.
    - Calls `start_supplier` with `supplier_prefix` to create a `Supplier` object and assigns it to the variable `s`.
    - Creates a `Scenario` object using the `s` (Supplier) object.
3. **Scenario execution:**
    - Calls the `run_scenarios` method of the `Scenario` object to execute the predefined test cases.

Usage Example
-------------------------

```python
    from hypotez import gs
    from src.utils.printer import  pprint
    from src.scenario import Scenario
    from src.suppliers.scenario._experiments.test_scenario import start_supplier

    supplier_prefix = 'aliexpress'  # Replace with the desired supplier prefix
    s = start_supplier(supplier_prefix)
    scenario = Scenario(s)
    scenario.run_scenarios()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".