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
This code block defines the `AliexpressApi` class, which provides methods for interacting with the AliExpress Open Platform API. It allows users to retrieve product details, generate affiliate links, search for hot products, and get a list of categories. 

Execution Steps
-------------------------
1. **Initialization**: The `__init__` method initializes the `AliexpressApi` object with API credentials, language, currency, and optional tracking ID. It sets up the necessary parameters for making API calls.
2. **Retrieving Product Details**: The `retrieve_product_details` method allows you to get information about specific products by providing their IDs or links. It uses the `AliexpressAffiliateProductdetailGetRequest` object to make a request to the API.
3. **Generating Affiliate Links**: The `get_affiliate_links` method converts a list of links into affiliate links. It utilizes the `AliexpressAffiliateLinkGenerateRequest` object for making the API call.
4. **Searching Hot Products**: The `get_hotproducts` method enables you to search for products with high commission rates. It leverages the `AliexpressAffiliateHotproductQueryRequest` object to interact with the API.
5. **Getting Categories**: The `get_categories` method retrieves all available categories, including parent and child categories. It uses the `AliexpressAffiliateCategoryGetRequest` object to fetch data from the API.
6. **Getting Parent Categories**: The `get_parent_categories` method provides a convenient way to obtain only the parent categories. It filters the categories retrieved from the API.
7. **Getting Child Categories**: The `get_child_categories` method allows you to retrieve child categories associated with a specific parent category. It filters the categories based on the provided parent category ID.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.api import AliexpressApi
from src.suppliers.aliexpress.api.models import Language, Currency, LinkType

# Initialize the AliexpressApi object with your API credentials
api = AliexpressApi(
    key="YOUR_API_KEY",
    secret="YOUR_API_SECRET",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="YOUR_TRACKING_ID",
)

# Retrieve product details for a specific product ID
product_details = api.retrieve_product_details(product_ids="1000000000000")
pprint(product_details)

# Generate an affiliate link for a product
affiliate_links = api.get_affiliate_links(links="https://www.aliexpress.com/item/1000000000000.html", link_type=LinkType.NORMAL)
pprint(affiliate_links)

# Search for hot products in a specific category
hot_products = api.get_hotproducts(category_ids=1000000000000)
pprint(hot_products.products)

# Get all available categories
categories = api.get_categories()
pprint(categories)

# Get parent categories
parent_categories = api.get_parent_categories()
pprint(parent_categories)

# Get child categories for a specific parent category
child_categories = api.get_child_categories(parent_category_id=1000000000000)
pprint(child_categories)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".