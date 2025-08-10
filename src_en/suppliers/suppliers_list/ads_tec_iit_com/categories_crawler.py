## \file /src/suppliers/suppliers_list/ads_tec_iit_com/categories_crawler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Module for collecting products from the category pages of the Ads-Tec IIT supplier via webdriver
=====================================================================================

Defines the category processing scenario for each supplier.

- The module collects a list of categories from the seller's pages (`get_list_categories_from_site()`).
@todo Add a check for changes in categories on the seller's pages.
Sellers can add new categories, rename or delete/hide existing ones.
Essentially, a table of categories `PrestaShop.categories <-> aliexpress_com.shop.categories` should be maintained.
- Collects a list of products from the category page (`get_list_products_in_category()`).
- Iterating through the list, it passes control to `grab_product_page()`, sending the current page URL to the function.
`grab_product_page()` processes the product fields and passes control to the `Product` class.

```rst
 .. module:: src.suppliers.suppliers_list.ads_tec_iit_com.categories_crawler
```
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
    """ 
    The function extracts a list of product URLs from the category page.
    If necessary, it scrolls through category pages.

    Args:
        d (Driver): WebDriver instance.
        l (SimpleNamespace): Object with locators for the category page,
                             including product and pagination locators.

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
       https://hbdeadsea.co.il/collections/<category name>?page=...
    """
    all_product_urls: List[str] = []
    # Extract product links from the current (first) page
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
