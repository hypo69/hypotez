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
This code block defines two functions: `parse_product` and `parse_products`. The `parse_product` function takes a single product object and modifies it by converting the `product_small_image_urls` attribute from a BeautifulSoup object to a string. The `parse_products` function iterates through a list of product objects and applies the `parse_product` function to each one, returning a new list of modified products.

Execution Steps
-------------------------
1. The `parse_product` function takes a product object as input.
2. It extracts the `product_small_image_urls` attribute from the product object.
3. It converts the extracted `product_small_image_urls` from a BeautifulSoup object to a string.
4. The function returns the modified product object.
5. The `parse_products` function takes a list of product objects as input.
6. It creates an empty list called `new_products`.
7. It iterates through each product object in the input list.
8. For each product object, it calls the `parse_product` function to modify it.
9. The modified product object is appended to the `new_products` list.
10. The function returns the `new_products` list containing the modified product objects.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.helpers.products import parse_products

# Example product data
products = [
    # ... (List of product objects)
]

# Parse the products
parsed_products = parse_products(products)

# Print the parsed products
print(parsed_products)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".