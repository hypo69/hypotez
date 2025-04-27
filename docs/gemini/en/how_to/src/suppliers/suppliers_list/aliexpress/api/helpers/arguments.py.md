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
This code snippet provides helper functions for processing AliExpress product IDs and lists of product IDs. 

Execution Steps
-------------------------
1. **`get_list_as_string(value)`:**
    - Checks if `value` is `None`, if so returns `None`.
    - If `value` is a string, it returns the string directly.
    - If `value` is a list, it joins the elements of the list with commas and returns the resulting string.
    - If `value` is not a string or list, it raises an `InvalidArgumentException` with a message indicating the expected data type.

2. **`get_product_ids(values)`:**
    - If `values` is a string, it splits the string by commas and converts it to a list.
    - If `values` is not a list or string, it raises an `InvalidArgumentException` with a message indicating the expected data type.
    - Iterates through the list of `values` and for each value:
        - Calls the `get_product_id()` function to obtain the product ID.
        - Appends the retrieved product ID to the `product_ids` list.
    - Returns the `product_ids` list.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.helpers.arguments import get_list_as_string, get_product_ids

# Example 1: Using get_list_as_string
product_ids_list = ["1234567890", "9876543210"]
product_ids_string = get_list_as_string(product_ids_list)
print(product_ids_string)  # Output: "1234567890,9876543210"

# Example 2: Using get_product_ids
product_ids_string_or_list = "1234567890,9876543210"
processed_product_ids = get_product_ids(product_ids_string_or_list)
print(processed_product_ids)  # Output: [Processed product IDs]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".