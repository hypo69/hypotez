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
The `AliApi` class extends the `AliexpressApi` class and provides custom methods for interacting with the AliExpress API. It inherits the functionalities of the parent class and introduces new methods specific to certain tasks.

Execution Steps
-------------------------
1. **Initialization**: The `__init__` method sets up the class by initializing the parent class (`AliexpressApi`) with necessary credentials and configurations (like API key, secret, language, currency, and tracking ID).
2. **Product Detail Retrieval**: The `retrieve_product_details_as_dict` method sends a list of product IDs to the AliExpress API and retrieves detailed information about those products as a list of dictionaries. 
3. **Affiliate Link Generation**: The `get_affiliate_links` method takes a list of product links and generates affiliate links for those products based on the specified link type. This functionality leverages the `get_affiliate_links` method of the parent class (`AliexpressApi`).

Usage Example
-------------------------

```python
    # Import the necessary modules
    from src.suppliers.suppliers_list.aliexpress.aliapi import AliApi
    from src import gs

    # Create an instance of the AliApi class
    api = AliApi(language='en', currency='usd')

    # Get product details for a list of product IDs
    product_ids = [1234567890, 9876543210]
    product_details = api.retrieve_product_details_as_dict(product_ids)

    # Print the retrieved product details
    print(product_details)

    # Generate affiliate links for a list of product URLs
    product_urls = ['https://www.aliexpress.com/item/1005001234567.html', 'https://www.aliexpress.com/item/9876543210123.html']
    affiliate_links = api.get_affiliate_links(product_urls)

    # Print the generated affiliate links
    print(affiliate_links)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".