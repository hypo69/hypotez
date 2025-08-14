## \file /src/suppliers/suppliers_list/etzmaleh_co_il/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.etzmaleh_co_il.scenario
    :platform: Windows, Unix
    :synopsis: Module for collecting products from Etzmaleh (Israel) category pages via webdriver.

Etzmaleh (Israel) Category Page Product Scraper
=========================================================================================

This module is responsible for scraping product data from Etzmaleh (Israel) category pages using a webdriver.
Each supplier has its own category processing scenario.

- The module collects a list of categories from the seller's pages (`get_list_categories_from_site()`).
  @todo Implement checks for changes in categories on seller pages.
  Sellers may add new categories, rename, or delete/hide existing ones.
  Essentially, a table of `PrestaShop.categories <-> etzmaleh.shop.categories` should be maintained.
- It collects a list of products from a category page (`get_list_products_in_category()`).
- Iterating through the list, it passes control to `grab_product_page()`, sending the function the current page URL.
  `grab_product_page()` processes the product fields and passes control to the `Product` class.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.supplier import Supplier # Assuming Supplier class is available

    # Example of how to use get_list_products_in_category
    # driver_instance = Driver(browser_name="Chrome")
    # class DummySupplier:
    #     def __init__(self, driver):
    #         self.driver = driver
    #         self.locators = {'category': {'product_links': 'some_xpath', 'close_banner': 'some_other_xpath'}}
    # supplier_instance = DummySupplier(driver_instance)
    # product_urls = get_list_products_in_category(supplier_instance)
    # if product_urls:
    #     print(f"Found {len(product_urls)} products.")
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/etzmaleh_co_il/scenario.py
"""




from typing import Union
from pathlib import Path

from src import gs
from src.logger.logger import logger

def get_list_products_in_category (s) -> list[str, str, None]:    
    """ Returns list of products urls from category page
    If pagination is needed, it should be handled.

    Args:
        s: Supplier instance.

    Returns:
        list or one of products urls or None.
    """
    d = s.driver
    
    
    l: dict = s.locators['category']
    
    d.execute_locator (s.locators ['product']['close_banner'] )
    
    if not l:
        """ Multiple checks because the code can be run by different executors: Supplier, Product, Scenario """
        logger.error(f"Where are the locators? {l}")
        return
    d.scroll()

    #TODO: No pagination implemented

    list_products_in_category = d.execute_locator(l['product_links'])
    """ Collected product links.  """
    
    if not list_products_in_category:
        logger.warning('No product links found. This can happen.')
        return
    
    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.info(f""" Found {len(list_products_in_category)} products """)
    

    return list_products_in_category

def get_list_categories_from_site(s):
    """Retrieves a list of categories from the supplier's website.

    Args:
        s: Supplier instance.

    Returns:
        list: A list of categories.
    """
    ...