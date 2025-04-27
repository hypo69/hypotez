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
The `AliAffiliatedProducts` class provides a mechanism to gather and process product data from AliExpress, specifically focusing on affiliate links, images, and videos. It utilizes the AliExpress Affiliate API to retrieve detailed product information and stores it in a structured format.

Execution Steps
-------------------------
1. **Initialization**: The `AliAffiliatedProducts` class is initialized with parameters like `campaign_name`, `campaign_category`, `language`, and `currency`.
2. **Affiliate Link Retrieval**: The `process_affiliate_products` method takes a list of product URLs or IDs and attempts to obtain affiliate links for each product.
3. **Product Details Retrieval**: It retrieves detailed product data using the `retrieve_product_details` method.
4. **Media Saving**: Images and videos associated with the products are saved locally using functions like `save_png_from_url` and `save_video_from_url`.
5. **Data Storage**: The processed product data is stored as JSON files within the campaign directory.

Usage Example
-------------------------

```python
    # Example usage:
    prod_urls = ['123', '456', ...]  # List of product URLs or IDs
    prod_urls = ['https://www.aliexpress.com/item/123.html', '456', ...]  # List of product URLs or IDs

    parser = AliAffiliatedProducts(
                                campaign_name,
                                campaign_category,
                                language,
                                currency)

    products = parser._affiliate_product(prod_urls)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".