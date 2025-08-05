**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use `PrestaProductAsync` Class
=========================================================================================

Description
-------------------------
The `PrestaProductAsync` class defines methods for interacting with PrestaShop products asynchronously. It inherits from the `PrestaShopAsync` class and adds methods for creating new products, retrieving parent categories, and uploading images.

Execution Steps
-------------------------
1. **Initialize a `PrestaProductAsync` Object:** Create an instance of the `PrestaProductAsync` class.
2. **Define Product Fields:** Create a `ProductFields` object containing product data, including name, price, description, etc.
3. **Add a New Product:** Use the `add_new_product_async` method to add a new product to PrestaShop based on the provided `ProductFields` object.
4. **Retrieve Parent Categories:** Use the `get_parent_categories_list` method (from `PrestaCategoryAsync`) to retrieve a list of parent categories for a given category ID.
5. **Upload Product Image:** The `create_binary` method uploads a product image to PrestaShop.

Usage Example
-------------------------

```python
    # Example usage
    product = PrestaProductAsync()
    product_fields = ProductFields(
        lang_index = 1,
        name='Test Product Async',
        price=19.99,
        description='This is an asynchronous test product.',
    )
    
    # Get parent categories for category ID 3
    parent_categories = await product.presta_category_async.get_parent_categories_list(id_category=3)
    print(f'Parent categories: {parent_categories}')

    # Add a new product
    new_product = await product.add_new_product_async(product_fields)
    if new_product:
        print(f'New product id = {new_product.id_product}')
    else:
        print(f'Error adding new product')

    # Fetch data asynchronously (not shown in this example)
    await product.fetch_data_async()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".