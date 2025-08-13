# # \file /src/suppliers/suppliers_list/amazon_com/categories_crawler.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
""".. module:: src.suppliers.suppliers_list.amazon_com.categories_crawler
    :platform: Windows, Unix
    :synopsis: Module for collecting products from Amazon category pages via webdriver.

Amazon Category Page Product Scraper
=========================================================================================

This module is responsible for scraping product data from Amazon category pages using a webdriver.
Each supplier has its own category processing scenario.

- The module collects a list of categories from the seller's pages (`get_list_categories_from_site()`).
  @todo Implement checks for changes in categories on seller pages.
  Sellers may add new categories, rename, or delete/hide existing ones.
  Essentially, a table of `PrestaShop.categories <-> amazon.shop.categories` should be maintained.
- It collects a list of products from a category page (`get_list_products_in_category()`).
- Iterating through the list, it passes control to `grab_product_page()`, sending the function the current page URL.
  `grab_product_page()` processes the product fields and passes control to the `Product` class.

Example usage
-------------

```python
    import asyncio
    from src.webdriver.selenium.driver import Driver

    async def main():
        driver = Driver() # Initialize your driver
        locators = {'product_links': 'some_xpath_or_css_selector_for_product_links'}
        product_urls = await get_list_products_in_category(driver, locators)
        if product_urls:
            print(f'Found {len(product_urls)} products.')

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/amazon_com/categories_crawler.py"""

import header # Standard import
from header import __root__ # Standard import
from src import gs # Standard import

from typing import List, Dict, Any 
from pathlib import Path # Path is not used in the fragment provided, but left in case of expansion

from src.logger.logger import logger
from src.webdriver.selenium.driver import Driver # Driver class import


async def get_list_products_in_category(d: Driver, l: Dict[str, Any]) -> List[str] | None:    
    """The function extracts a list of URLs of goods from the category page.
    If the page has a pagination, it must be treated (the current implementation does not include pagination).

    Args:
        D (Driver): WebDriver copy for interacting with a page.
        l (dict [str, a any]): a dictionary of locators, where the key 'product_Links' 
                            Contains a locator for links to goods.
    
    Returns:
        List [str] | None: a list of URLs of goods or `none` if the goods are not found.
    
    Example:
        >>> # For this example, a configured Driver and Locators is needed
        >>> # driver = driver (...)
        >>> # locators = {'Product_LINKS': 'Soxpath_or_css_selector_for_product_Links'}
        >>> # Product_URLS = AWAIT GET_LIST_PRODUCTS_in_CATEGORY (Driver, Locators)
        >>> # If Product_urls:
        >>> # print (f'niden {len (product_urls)} goods. ')"""
    list_products_from_locator: List[str] | str | None 
    processed_list_products: List[str] | None # For the final result

    d.scroll() # Scrolling the page

    # TODO: implement pagination (leaflet) for pages of categories.
    
    # The function extracts links to goods.
    list_products_from_locator = await d.execute_locator(l['product_links'])
    
    if not list_products_from_locator:
        logger.warning('Нет ссылок на товары')
        return None # None return if nothing is found
    
    # Converting the result to the list if execute_Locator has returned one line
    if isinstance(list_products_from_locator, str):
        processed_list_products = [list_products_from_locator]
    elif isinstance(list_products_from_locator, list):
        processed_list_products = list_products_from_locator
    else:
        # Processing of an unexpected type of data, if necessary
        logger.warning(f'execute_locator вернул неожиданный тип: {type(list_products_from_locator)}')
        return None


    logger.info(f'Найдено {len(processed_list_products)} товаров')
    
    # """I check the availability of goods in the database of the store"""
    # for asin in processed_list_products: # Заменено list_products_in_category на processed_list_products
    # _asin = asin.split(f'''None''')[-2]
    # # _sku = f '' '{s.supplier_id} _ _ asin}' '' ' #' s' (superlier instance) is not defined in this function
    # # if PrestaShopProduct.check(_sku) == False:
    # #     """Syntax in order to remember
    # # that I check the lack of goods in the database
    # None
    # #     continue
    # # else:
    # #     """Product in the database"""
    # #     continue
    # #TODO: Logic

    return processed_list_products