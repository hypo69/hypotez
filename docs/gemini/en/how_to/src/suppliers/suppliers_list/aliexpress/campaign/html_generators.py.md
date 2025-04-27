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
The provided code defines three classes: `ProductHTMLGenerator`, `CategoryHTMLGenerator`, and `CampaignHTMLGenerator`. These classes are responsible for generating HTML content for individual products, product categories, and the overall campaign, respectively. The generated HTML files utilize Bootstrap for styling and are saved to specific locations within the project.

Execution Steps
-------------------------
1. **ProductHTMLGenerator**:
    - **set_product_html**: This method takes a product object (`product`) and a category path (`category_path`) as input.
    - It constructs an HTML file for the product, including its title, image, price details, category, and a "Buy Now" button.
    - The HTML content is then saved to the `html_path` within the specified category directory.
2. **CategoryHTMLGenerator**:
    - **set_category_html**: This method takes a list of products (`products_list`) and a category path (`category_path`) as input.
    - It creates an HTML file for the category, listing all products within that category using a Bootstrap grid layout.
    - Each product is displayed with its title, image, price, category, and a "Buy Now" button.
    - The generated HTML is saved to the `html_path` within the specified category directory.
3. **CampaignHTMLGenerator**:
    - **set_campaign_html**: This method takes a list of categories (`categories`) and a campaign path (`campaign_path`) as input.
    - It generates an HTML file for the campaign, providing an overview of all categories.
    - Each category is listed with a link to its corresponding HTML file.
    - The HTML content is saved to the `html_path` within the specified campaign directory.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.campaign.html_generators import ProductHTMLGenerator, CategoryHTMLGenerator, CampaignHTMLGenerator
from types import SimpleNamespace
from pathlib import Path

# Example product data
product = SimpleNamespace(
    product_id=1234567890,
    product_title="Awesome Product",
    local_image_path="path/to/image.jpg",
    target_sale_price=10.99,
    target_sale_price_currency="USD",
    target_original_price=19.99,
    target_original_price_currency="USD",
    second_level_category_name="Electronics",
    promotion_link="https://www.example.com/product/1234567890"
)

# Example category path
category_path = Path("path/to/category")

# Generate HTML for the product
ProductHTMLGenerator.set_product_html(product, category_path)

# Generate HTML for the category
products_list = [product, product]  # Example list of products
CategoryHTMLGenerator.set_category_html(products_list, category_path)

# Generate HTML for the campaign
categories = ["Electronics", "Fashion", "Home"]
campaign_path = Path("path/to/campaign")
CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".