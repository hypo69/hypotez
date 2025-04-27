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
The code block defines a function `get_product_id` that extracts the product ID from a given text string. It utilizes the `extract_prod_ids` function from the `src.suppliers.suppliers_list.aliexpress.utils.extract_product_id` module. The `get_product_id` function is designed to handle different formats of product IDs, including those found in URLs.

Execution Steps
-------------------------
1. The `get_product_id` function takes a `raw_product_id` string as input.
2. It calls the `extract_prod_ids` function, passing the `raw_product_id` as an argument. 
3. The `extract_prod_ids` function attempts to extract the product ID from the given text string.
4. If a product ID is found, the `get_product_id` function returns the extracted product ID.
5. If no product ID is found, the function raises a `ProductIdNotFoundException` with an error message indicating that the product ID was not found.

Usage Example
-------------------------

```python
    from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id

    raw_product_id = 'https://www.aliexpress.com/item/4000000000000.html'
    try:
        product_id = get_product_id(raw_product_id)
        print(f"Extracted product ID: {product_id}")
    except ProductIdNotFoundException as e:
        print(f"Error: {e}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".