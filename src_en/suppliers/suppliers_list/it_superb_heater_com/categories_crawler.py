# # \file /src/suppliers/suppliers_list/hb/sceanrio.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
"""The module for collecting goods from the page of the categories of the supplier HB.co.il through the webdraiter
==========================================================================================================

Determining the scenario of processing categories for each supplier.

- The module collects a list of categories from the seller’s pages (`get_list_categories_from_site ()`).
@todo make a test for changing categories on the seller’s pages. 
The seller can add new categories, rename or delete/hide existing. 
By and large, you need to keep the category table `Prestashop.categories <-> aliexpress_com.shop.categoies`
- collects a list of goods from the category page (`get_list_products_in_category ()`).
- Iterii on the list, reports control to `Grab_product_Page ()`, sending the function of the current URL page.  
`Grab_product_page ()` processes the fields of the goods and transfers control to the class `Product`.

`` `RST
 .. Module :: src.suppliers.suppliers_list.hb.sceanrio
`` `"""

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

