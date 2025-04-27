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
The `PrestaCategory` class provides methods for managing categories in PrestaShop. This specific code block focuses on the `get_parent_categories_list` method, which retrieves a list of parent categories for a given category ID. 

Execution Steps
-------------------------
1. **Validate Input**: Checks if the `id_category` parameter is provided. If not, logs an error and returns an empty list.
2. **Fetch Category Data**: Uses the `get` method inherited from the `PrestaShop` class to retrieve the category data from the PrestaShop API, including the `id_parent` attribute.
3. **Construct Parent Category List**: If the `parent_categories_list` parameter is not provided, initializes an empty list. Then, adds the `_parent_category` value to the list.
4. **Recursively Traverse Parents**: If the `_parent_category` is less than or equal to 2 (indicating the root category), returns the constructed list. Otherwise, recursively calls `get_parent_categories_list` with the `_parent_category` as the new `id_category` and the updated list as `parent_categories_list`.

Usage Example
-------------------------

```python
    # Initialize PrestaCategory object
    category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')

    # Get parent categories for category with ID '10'
    parent_categories = category.get_parent_categories_list(id_category='10')

    # Print the list of parent categories
    print(parent_categories)  # Output: [2, 10] 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".