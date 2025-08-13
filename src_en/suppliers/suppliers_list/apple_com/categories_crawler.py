# # \file /src/suppliers/suppliers_list/apple_com/categories_crawler.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
""".. module:: src.suppliers.suppliers_list.apple_com.categories_crawler
    :platform: Windows, Unix
    :synopsis: Module for collecting products from Apple category pages via webdriver.

Apple Category Page Product Scraper
=========================================================================================

This module is responsible for scraping product data from Apple category pages using a webdriver.
Each supplier has its own category processing scenario.

- The module collects a list of categories from the seller's pages (`get_list_categories_from_site()`).
  @todo Implement checks for changes in categories on seller pages.
  Sellers may add new categories, rename, or delete/hide existing ones.
  Essentially, a table of `PrestaShop.categories <-> apple.shop.categories` should be maintained.
- It collects a list of products from a category page (`get_list_products_in_category()`).
- Iterating through the list, it passes control to `grab_product_page()`, sending the function the current page URL.
  `grab_product_page()` processes the product fields and passes control to the `Product` class.

Example usage
-------------

```python
    import asyncio
    from src.webdriver.selenium.driver import Driver
    from types import SimpleNamespace

    async def main():
        driver = Driver() # Initialize your driver
        locators = SimpleNamespace(product_links="...", show_more="...") # Define your locators
        product_urls = await get_list_products_in_category(driver, locators)
        if product_urls:
            print(f'Found {len(product_urls)} products.')

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/apple_com/categories_crawler.py"""

import asyncio
from typing import List, Any, Dict # Added Any, Dict
from types import SimpleNamespace # Added SimpleNamespace
import time

import header # Added header import
from header import __root__ # Added __root__ import
from src import gs # Ensured gs import
from src.logger.logger import logger
from src.webdriver.selenium.driver import Driver


async def get_list_products_in_category (d: Driver, l: SimpleNamespace) -> list:    
    """The function extracts a list of URLs of goods from the category page.
    If necessary, flip through the pages of categories.

    Args:
        D (Driver): Corporal WebDriver.
        L (Simplenamespace): Object with locators for the category page, 
                             Including the locators of goods and pagination.
    
    Returns:
        List [str] | None: a list of URLs of goods or `none` if the goods are not found.
    
    Example:
        >>> # Example of use (requires tuning d and l)
        >>> # driver = driver (...)
        >>> # locators = simplenamespace (product_links = ..., passing_locators = ...)
        >>> # Product_URLS = AWAIT GET_LIST_PRODUCTS_in_CATEGORY (Driver, Locators)
        >>> # If Product_urls:
        >>> # print (f'niden {len (product_urls)} goods. ')"""


    """In the current version, the pagination originates through press the buttons
       https://hbdeadsea.co.il/collections/ <shapping of Katakegory>? Page = ..."""
    all_product_urls: List[str] = []
    # Extracting links to goods from the current (first) page
    while True:
        if not await d.execute_locator(l.show_more):
            break
        product_links: List[str] | str | None = await d.execute_locator(l.product_links)
        if len(all_product_urls) <  product_links:
            all_product_urls.extend(all_product_urls)
            time.sleep(3)
            continue
        else:
            break

    
    return product_links if isinstance(product_links, list) else [product_links]