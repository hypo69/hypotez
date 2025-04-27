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
This code snippet defines a `Product` class that represents product data from AliExpress API.

Execution Steps
-------------------------
1. The code defines a `Product` class.
2. It defines various attributes for the `Product` class that represent different aspects of a product, such as price, currency, category, images, URLs, etc.
3. The attributes are defined with their respective data types: `str`, `int`, and `List[str]`.

Usage Example
-------------------------

```python
    from src.suppliers.aliexpress.api.models.product import Product

    product_data = {
        "app_sale_price": "10.99",
        "app_sale_price_currency": "USD",
        "commission_rate": "0.05",
        # ... other product data
    }

    product = Product(**product_data)

    print(product.product_title)
    print(product.sale_price)
    print(product.product_detail_url)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".