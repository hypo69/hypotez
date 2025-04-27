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
This code block defines a function `get_locales` to load locales data from a JSON file and stores it in a variable `locales`. It also defines a global variable `locales` which gets its value from the `get_locales` function. The `locales` variable is used to store a list of dictionaries, each containing a locale code and its corresponding currency.

Execution Steps
-------------------------
1. The `get_locales` function takes a path to a JSON file as input.
2. The function reads the JSON data from the file using `j_loads_ns`.
3. The function returns the `locales` attribute from the loaded data.
4. The `locales` global variable is assigned the result of calling `get_locales` with a path to the "locales.json" file located in the project directory.

Usage Example
-------------------------

```python
    from src.suppliers.suppliers_list.aliexpress.utils.locales import locales

    # Access the locales data
    print(locales) 
    # Output: [{'EN': 'USD'}, {'HE': 'ILS'}, {'RU': 'ILS'}, {'EN': 'EUR'}, {'EN': 'GBR'}, {'RU': 'EUR'}]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".