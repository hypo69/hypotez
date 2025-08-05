**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `PrestaShopShop` Class
=========================================================================================

Description
-------------------------
The `PrestaShopShop` class provides functionality for interacting with PrestaShop stores. It inherits from the `PrestaShop` class and extends its capabilities with additional features specific to store management.

Execution Steps
-------------------------
1. **Initialization**: The `PrestaShopShop` class is initialized with either a `credentials` dictionary or separate `api_domain` and `api_key` parameters.
2. **API Domain and Key Validation**: The code checks if both `api_domain` and `api_key` are provided. If not, it raises a `ValueError` to ensure that the essential credentials are present.
3. **Inheritance**: The class inherits from the `PrestaShop` class, inheriting its methods and properties. This allows the `PrestaShopShop` class to leverage the existing PrestaShop API functionalities.

Usage Example
-------------------------

```python
from src.endpoints.prestashop.shop import PrestaShopShop

# Using credentials dictionary
credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
shop = PrestaShopShop(credentials=credentials)

# Using separate api_domain and api_key parameters
shop = PrestaShopShop(api_domain='example.com', api_key='your_api_key')

# Access inherited methods and properties
print(shop.api_domain)  # Output: example.com
shop.get_products()  # Calls the get_products method from the PrestaShop class
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".