## \file /src/suppliers/aliexpress/campaign/prepare_campaigns (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.suppliers_list.aliexpress_com.campaign """



"""
This module prepares AliExpress campaigns by processing categories, handling campaign data, and generating promotional materials.

### Examples:
To run the script for a specific campaign:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py summer_sale -c electronics -l EN -cu USD -f

To process all campaigns:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py --all -l EN -cu USD
"""
import header
import argparse
import asyncio
import datetime
import html
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress_com.campaign.html_generators import (
    ProductHTMLGenerator,
    CategoryHTMLGenerator,
    CampaignHTMLGenerator,
)
from src.utils import get_directory_names, get_filenames, save_text_file
from src.utils.jjson import j_dumps
from src.logger.logger import logger

# Define the path to the directory with campaigns
campaigns_directory = gs.path.google_drive / "aliexpress" / "campaigns"
locales = {"EN": "USD", "HE": "ILS", "RU": "ILS"}

def process_new_campaign(self, campaign_name: str):
    """"""
    AliCampaignEditor(campaign_name).process_new_campaign()

def process_campaign_category(
    campaign_name: str, category_name: str, language: str, currency: str
) -> List[str]:
    """Processes a specific category within a campaign for all languages and currencies.

    Args:
        campaign_name (str): Name of the advertising campaign.
        category_name (str): Category for the campaign.
        language (str): Language for the campaign.
        currency (str): Currency for the campaign.

    Returns:
        List[str]: List of product titles within the category.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    campaign_editor = AliCampaignEditor(
        campaign_name=campaign_name, language=language, currency=currency
    )

    # Process category products and get the list of products
    campaign_editor.process
    products = campaign_editor.process_category_products(category_name)

    # # Extract product titles
    # product_titles = [product["product_title"] for product in products]

    # return product_titles


def process_campaign(
    campaign_name: str,
    language: str,
    currency: str,
    campaign_file: Optional[str] = None,
) -> bool:
    """Processes a campaign and handles the campaign's setup and processing.

    Args:
        campaign_name (str): Name of the advertising campaign.
        language (str): Language for the campaign.
        currency (str): Currency for the campaign.
        campaign_file (Optional[str]): Optional path to a specific campaign file.

    Example:
        >>> res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")
    Returns:
        True is campaign processed else False
    """
    
    return AliCampaignEditor(
            campaign_name=campaign_name,
            language=language,
            currency=currency,
            campaign_file=campaign_file,
        ).process_campaign()

def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Processes all campaigns in the 'campaigns' directory for the specified language and currency.

    Args:
        language (str): Language for the campaigns.
        currency (str): Currency for the campaigns.

    Example:
        >>> process_all_campaigns("EN", "USD")
    """
    for language, currency in locales.items():
        campaign_dirs = get_directory_names(campaigns_directory)
        for campaign_name in campaign_dirs:
            campaign_editor = AliCampaignEditor(
                campaign_name=campaign_name, language=language, currency=currency
            )
            logger.info(f"start {campaign_name=}, {language=}, {currency=} ")
            campaign_editor.process_campaign()

async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
    """
    Saves product data in various formats:

    - `<product_id>.json`: Contains all product parameters, one file per product.
    - `ai_{timestamp}.json`: A common file for all products with specific keys.
    - `promotion_links.txt`: A list of product links, created in the `save_promotion_links()` function.
    - `category_products_titles.json`: File containing title, `product_id`, `first_category_name`, and `second_category_name` of each product in the category.

    Args:
        campaign_name (str): The name of the campaign for the output files.
        category_path (str | Path): The path to save the output files.
        products_list (list[SimpleNamespace] | SimpleNamespace): List of products or a single product to save.

    Returns:
        None

    Example:
        >>> products_list: list[SimpleNamespace] = [
        ...     SimpleNamespace(product_id="123", product_title="Product A", promotion_link="http://example.com/product_a", 
        ...                     first_level_category_id=1, first_level_category_name="Category1",
        ...                     second_level_category_id=2, second_level_category_name="Subcategory1", 
        ...                     product_main_image_url="http://example.com/image.png", product_video_url="http://example.com/video.mp4"),
        ...     SimpleNamespace(product_id="124", product_title="Product B", promotion_link="http://example.com/product_b",
        ...                     first_level_category_id=1, first_level_category_name="Category1",
        ...                     second_level_category_id=3, second_level_category_name="Subcategory2",
        ...                     product_main_image_url="http://example.com/image2.png", product_video_url="http://example.com/video2.mp4")
        ... ]
        >>> category_path: Path = Path("/path/to/category")
        >>> await generate_output("CampaignName", category_path, products_list)

    Flowchart:
        ┌───────────────────────────────┐
        │  Start `generate_output`      │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │ Format `timestamp` for file   │
        │ names.                        │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │ Check if `products_list` is   │
        │ a list; if not, convert it to │
        │ a list.                       │
        └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Initialize `_data_for_openai`,│
    │ `_promotion_links_list`, and  │
    │ `_product_titles` lists.      │
    └───────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ For each `product` in `products_list`:  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 1. Create `categories_convertor` dictionary   │
│ for `product`.                                │
└───────────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 2. Add `categories_convertor` to `product`.   │
└───────────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 3. Save `product` as `<product_id>.json`.     │
└───────────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────┐
│ 4. Append `product_title` and                 │
│ `promotion_link` to their respective lists.   │
└───────────────────────────────────────────────┘
                    │                                               
                    ▼
    ┌───────────────────────────────┐
    │ Call `save_product_titles`    │
    │ with `_product_titles` and    │
    │ `category_path`.              │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Call `save_promotion_links`   │
    │ with `_promotion_links_list`  │
    │ and `category_path`.          │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │ Call `generate_html` with         │
    │ `campaign_name`, `category_path`, │
    │ and `products_list`.              │
    └───────────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  End `generate_output`        │
    └───────────────────────────────┘

    ```

    ### Flowchart Description

    1. **Start `generate_output`**: The function begins execution.
    2. **Format `timestamp` for file names**: Generate a timestamp to use in filenames.
    3. **Check if `products_list` is a list**: Ensure that `products_list` is in list format.
    4. **Initialize `_data_for_openai`, `_promotion_links_list`, and `_product_titles` lists**: Prepare empty lists to collect data.
    5. **For each `product` in `products_list`**: Process each product in the list.
    - **Create `categories_convertor` dictionary for `product`**: Create a dictionary for category conversion.
    - **Add `categories_convertor` to `product`**: Attach this dictionary to the product.
    - **Save `product` as `<product_id>.json`**: Save product details in a JSON file.
    - **Append `product_title` and `promotion_link` to their respective lists**: Collect titles and links.
    6. **Call `save_product_titles` with `_product_titles` and `category_path`**: Save titles data to a file.
    7. **Call `save_promotion_links` with `_promotion_links_list` and `category_path`**: Save promotion links to a file.
    8. **Call `generate_html` with `campaign_name`, `category_path`, and `products_list`**: Generate HTML output for products.
    9. **End `generate_output`**: The function completes execution.

    This flowchart captures the key steps and processes involved in the `generate_output` function.

    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H%M%S")
    products_list = products_list if isinstance(products_list, list) else [products_list]
    _data_for_openai: dict = {}
    _promotion_links_list: list = []
    _product_titles: list = []

    for product in products_list:
        # Adding the categories_convertor dictionary
        categories_convertor = {
            str(product.first_level_category_id): {
                "ali_category_name": product.first_level_category_name,
                "ali_parent": "",
                "PrestaShop_categories": [],
                "PrestaShop_main_category": ""
            },
            str(product.second_level_category_id): {
                "ali_category_name": product.second_level_category_name,
                "ali_parent": str(product.first_level_category_id),
                "PrestaShop_categories": [],
                "PrestaShop_main_category": ""
            }
        }
        product.categories_convertor = categories_convertor

        # Save individual product JSON
        j_dumps(product, Path(category_path / f"{self.language}_{self.currency}" / f"{product.product_id}.json"), exc_info=False)
        _product_titles.append(product.product_title)
        _promotion_links_list.append(product.promotion_link)

    await self.save_product_titles(product_titles=_product_titles, category_path=category_path)
    await self.save_promotion_links(promotion_links=_promotion_links_list, category_path=category_path)
    await self.generate_html(campaign_name=campaign_name, category_path=category_path, products_list=products_list)

async def save_product_titles(self, product_titles: list[str] | str, category_path: str | Path ):
    """ Сохраняю названия товаров для последующей обработки в ИИ """
    ...
    product_titles_path:Path = Path(category_path) / f"{self.language}_{self.currency}" / 'product_titles.txt'
    save_text_file(product_titles, product_titles_path)

async def save_promotion_links(self, promotion_links: list[str] | str, category_path: str | Path ) -> str | list[str]:
    """
    Save the list of promotion links to a file and return the saved links.

    @param promotion_links: List of promotion links or a single promotion link to save.
    @param category_path: Path to save the file.
    @return: The saved promotion links as a single string if input was a single string, or as a list of strings if input was a list.
    """
    ...
    promotion_links_path:Path = Path(category_path) / f"{self.language}_{self.currency}" / 'promotion_links.txt'
    save_text_file(promotion_links, promotion_links_path)

async def generate_html(self, campaign_name:str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace):
    """ Creates an HTML file for the category and a root index file.
    
    @param products_list: List of products to include in the HTML.
    @param category_path: Path to save the HTML file.
    """
    ...
    products_list = products_list if isinstance(products_list, list) else [products_list]

    category_name = Path(category_path).name
    category_html_path:Path = Path(category_path) /  f"{self.language}_{self.currency}" / f'{category_name}.html'
    
    # Initialize the category dictionary to store product titles
    category = {
        "products_titles": []
    }
    
    html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} Products</title>
    <link rel="stylesheet" href="styles.css">
    </head>
    <body>
    <h1>{category_name} Products</h1>
    <div class="product-grid">
    """

    for product in products_list:
        # Add the product's details to the category's products_titles
        category["products_titles"].append({
            "title": product.product_title,
            "product_id": product.product_id,
            "first_category_name": product.first_level_category_name,
            "second_category_name": product.second_level_category_name
        })

        html_content += f"""
        <div class="product-card">
        <img src="{product.local_image_path}" alt="{html.escape(product.product_title)}" class="product-image">
        <div class="product-info">
        <h2 class="product-title">{html.escape(product.product_title)}</h2>
        <p class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</p>
        <p class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</p>
        <p class="product-category">Category: {product.second_level_category_name}</p>
        <a href="{product.promotion_link}" class="product-link">Buy Now</a>
        </div>
        </div>
        """

    html_content += """
    </div>
    </body>
    </html>
    """

    # Save the HTML content
    save_text_file(html_content, category_html_path)

    ...
    # Generate the main index.html file
    campaign_path  = gs.path.google_drive / 'aliexpress' / 'campaigns' / campaign_name
    campaign_path.mkdir(parents=True, exist_ok=True)
    index_html_path = campaign_path / 'index.html'
        

    # Collect all category links
    category_links = []
    categories =  get_directory_names(campaign_path / 'category')
    for _category_path in categories:
        category_name = Path(_category_path).name
        category_link = f"{category_name}/{category_name}.html"
        category_links.append(f"<li><a href='{category_link}'>{html.escape(category_name)}</a></li>")

    index_html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Categories</title>
    <link rel="stylesheet" href="styles.css">
    </head>
    <body>
    <h1>Product Categories</h1>
    <ul>
    {"\n".join(category_links)}
    </ul>
    </body>
    </html>
    """

    save_text_file(index_html_content, index_html_path)

def generate_html_for_campaign(self, campaign_name: str):
    """Генерирует HTML-страницы для рекламной кампании.

    Args:
        campaign_name (str): Имя рекламной кампании.

    Example:
        >>> campaign.generate_html_for_campaign("HolidaySale")
    """
    campaign_root = Path(gs.path.google_drive / "aliexpress" / "campaigns" / campaign_name)
    categories = get_filenames(campaign_root / "category", extensions="")

    # Генерация HTML страниц для каждой категории
    for category_name in categories:
        category_path = campaign_root / "category" / category_name
        products = self.get_category_products(category_name=category_name)

        if products:
            # Генерация страниц для каждого товара
            for product in products:
                ProductHTMLGenerator.set_product_html(product, category_path)

            # Генерация страницы категории
            CategoryHTMLGenerator.set_category_html(products, category_path)
        else:
            logger.warning(f"No products found for category {category_name}.")

    # Генерация страницы рекламной кампании
    CampaignHTMLGenerator.set_campaign_html(categories, campaign_root)
                                                          
                                                          
async def async_main(
    campaign_name: str, categories: List[str], language: str, currency: str
) -> None:
    """Asynchronous main function to process a campaign.

    Args:
        campaign_name (str): Name of the advertising campaign.
        categories (List[str]): List of categories for the campaign.
        language (str): Language for the campaign.
        currency (str): Currency for the campaign.

    Example:
        >>> asyncio.run(async_main("summer_sale", ["electronics"], "EN", "USD"))
    """
    if not categories:
        # Always get all categories from the directory
        categories = get_directory_names(
            campaigns_directory / campaign_name / "category"
        )

    await asyncio.gather(
        *[
            process_campaign_category(campaign_name, category, language, currency)
            for category in categories
        ]
    )


def main() -> None:
    """Main function to parse arguments and initiate processing.

    Example:
        >>> main()
    """
    parser = argparse.ArgumentParser(description="Prepare AliExpress Campaign")
    parser.add_argument("campaign_name", type=str, help="Name of the campaign")
    parser.add_argument(
        "-c",
        "--categories",
        nargs="+",
        help="List of categories (if not provided, all categories will be used)",
    )
    parser.add_argument(
        "-l", "--language", type=str, default="EN", help="Language for the campaign"
    )
    parser.add_argument(
        "-cu", "--currency", type=str, default="USD", help="Currency for the campaign"
    )
    parser.add_argument(
        "-f", "--force_update", action="store_true", help="Force update categories"
    )
    parser.add_argument("--all", action="store_true", help="Process all campaigns")

    args = parser.parse_args()
                    
    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            async_main(
                args.campaign_name, args.categories or [], args.language, args.currency
            )
        )


if __name__ == "__main__":
    main()


# asyncio.run( self.generate_output( campaign_name = self.campaign.campaign_name, 
#                 category_path = Path(path_to_save_images_and_products), 
#                 products_list = affiliated_products_list 
#                 ))
# """TODO: 
# Переделать генерацию выходных данных"""