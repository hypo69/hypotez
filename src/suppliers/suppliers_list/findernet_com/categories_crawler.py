## \file /src/suppliers/suppliers_list/findernet_com/categories_crawler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.findernet_com.categories_crawler
    :platform: Windows, Unix
    :synopsis: Module for collecting products from Findernet category pages via webdriver.

Findernet Category Page Product Scraper
=========================================================================================

This module is responsible for scraping product data from Findernet category pages using a webdriver.
Each supplier has its own category processing scenario.

- The module collects a list of categories from the seller's pages (`get_list_categories_from_site()`).
  @todo Implement checks for changes in categories on seller pages.
  Sellers may add new categories, rename, or delete/hide existing ones.
  Essentially, a table of `PrestaShop.categories <-> findernet.shop.categories` should be maintained.
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
:location: suppliers/suppliers_list/findernet_com/categories_crawler.py
"""

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
    """Returns list of product URLs from the category page.

    If pagination is needed, it should be handled.

    Args:
        d (Driver): WebDriver instance.
        l (SimpleNamespace): Object with locators for the category page,
                             including product links and pagination locators.
    
    Returns:
        List[str] | None: List of product URLs or `None` if no products are found.
    
    Example:
        >>> # Example usage (requires d and l to be configured)
        >>> # driver = Driver(...) 
        >>> # locators = SimpleNamespace(product_links=..., pagination_locators=...)
        >>> # product_urls = await get_list_products_in_category(driver, locators)
        >>> # if product_urls:
        >>> #     print(f'Found {len(product_urls)} products.')
    """


    """
       In the current version, pagination occurs by clicking a button
       https://hbdeadsea.co.il/collections/<category_name>?page=...
    """
    all_product_urls: List[str] = []
    # Extract links from the current (first) page
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

def get_list_categories_from_site(s):
    """Retrieves a list of categories from the supplier's website.

    Args:
        s: Supplier instance.

    Returns:
        list: A list of categories.
    """
    ...