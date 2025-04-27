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
This code block defines a class `HotProductsResponse` which represents the response from the AliExpress API when retrieving a list of hot products.

Execution Steps
-------------------------
1. The code imports the `Product` class from the `src.suppliers.aliexpress.api.models` module.
2. The `HotProductsResponse` class is defined.
3. The class has four attributes:
    - `current_page_no`: An integer representing the current page number in the response.
    - `current_record_count`: An integer representing the number of records on the current page.
    - `total_record_count`: An integer representing the total number of records available.
    - `products`: A list of `Product` objects representing the hot products returned in the response.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.models.hotproducts import HotProductsResponse

# Example response data
response_data = {
    "current_page_no": 1,
    "current_record_count": 10,
    "total_record_count": 100,
    "products": [
        # Product objects
    ]
}

# Create a HotProductsResponse object from the response data
hot_products_response = HotProductsResponse(**response_data)

# Access the attributes of the HotProductsResponse object
current_page = hot_products_response.current_page_no
total_records = hot_products_response.total_record_count
hot_products = hot_products_response.products

# Iterate over the hot products
for product in hot_products:
    print(product.title)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".