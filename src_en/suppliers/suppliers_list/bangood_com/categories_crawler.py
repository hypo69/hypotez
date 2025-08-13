# # \file /src/suppliers/suppliers_list/bangood_com/categories_crawler.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
""".. module:: src.suppliers.suppliers_list.bangood_com.categories_crawler
    :platform: Windows, Unix
    :synopsis: Module for collecting products from Banggood category pages via webdriver.

Banggood Category Page Product Scraper
=========================================================================================

This module is responsible for scraping product data from Banggood category pages using a webdriver.
Each supplier has its own category processing scenario.

- The module collects a list of categories from the seller's pages (`get_list_categories_from_site()`).
  @todo Implement checks for changes in categories on seller pages.
  Sellers may add new categories, rename, or delete/hide existing ones.
  Essentially, a table of `PrestaShop.categories <-> bangood.shop.categories` should be maintained.
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
    # def __init__(self, driver):
    # self.driver = driver
    # self.locators = {'category': {'product_links': 'some_xpath', 'close_banner': 'some_other_xpath'}}
    # supplier_instance = DummySupplier(driver_instance)
    # product_urls = get_list_products_in_category(supplier_instance)
    # if product_urls:
    # print(f"Found {len(product_urls)} products.")
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/bangood_com/categories_crawler.py"""




from typing import Union
from pathlib import Path

from src import gs
from src.logger.logger import logger

def get_list_products_in_category (s) -> list[str, str, None]:    
    """Returns List of Products Urls from Category Page
    If you need to strain - pages of categories - leaf through ??????

    Attrs:
        S - Supplier
    @returns
        List ONE of Products urls or none"""
    d = s.driver
    
    
    l: dict = s.locators['category']
    
    d.execute_locator (s.locators ['product']['close_banner'] )
    
    if not l:
        """There are many inspections, because the code can be launched on behalf of different of their fillers: Supplier, Product, Scenario"""
        logger.error(f"А где локаторы? {l}")
        return
    d.scroll()

    # Todo: No leaflet

    list_products_in_category = d.execute_locator(l['product_links'])
    """Collected links to goods."""
    
    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        return
    
    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.info(f"""Found {len (list_products_in_category)} goods""")
    

    return list_products_in_category

def get_list_categories_from_site(s):
    ...