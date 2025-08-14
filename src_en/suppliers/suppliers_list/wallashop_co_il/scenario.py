# # \file /src/suppliers/suppliers_list/kualastyle/sceanrio.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3


"""Module for collecting goods from the page of the supplier of Kualastyle.il through the webdraiter
=========================================================================================================================================

Each supplier has its own scenario of the capture of categories

-Modul collects a list of categories from the seller’s pages. `get_list_categories_from_site ()`.
@todo make a test for changing categories on the seller’s pages. 
The seller can add new categories, rename or delete/hide existing. 
By and large, you need to keep the category table `Prestashop.categories <-> aliexpress_com.shop.categoies`
- collects a list of goods from the page of the category `get_list_products_in_category ()` `
- Iteriyah according to the list transfers control to `grab_product_page ()` Determining the function of the current URL page  
`grab_product_page ()` processes the fields of the goods and transfers control to the class `Product`"""
...

from typing import Dict, List
from pathlib import Path

from src import gs
from src.logger.logger import logger
from src.webdriver.selenium.driver import Driver




def get_list_products_in_category (s: Supplier) -> list[str, str, None]:    
    """Returns List of Products Urls from Category Page
    If you need to strain - pages of categories - leaf through ??????

    Attrs:
        S - Supplier
    @returns
        List ONE of Products urls or none"""
    ...
    d:Driver = s.driver
    l: dict = s.locators['category']
    ...
    d.wait(1)
    d.execute_locator (s.locators ['product']['close_banner'] )
    d.scroll()
    ...

    list_products_in_category: List = d.execute_locator(l['product_links'])

    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        ...
        return
    ...
    while d.current_url != d.previous_url:
        if paginator(d,l,list_products_in_category):
            list_products_in_category.append(d.execute_locator(l['product_links']))
        else:
            break
        
    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.debug(f"""Found {len(list_products_in_category)} items in category {s.current_scenario['name']}""")
    
    return list_products_in_category

def paginator(d:Driver, locator: dict, list_products_in_category: list):
    """Sheet"""
    response = d.execute_locator(locator['pagination']['<-'])
    if not response or (isinstance(response, list) and len(response) == 0): 
        ...
        return
    return True

def get_list_categories_from_site(s):
    """Assembly of current categories from the site"""
    ...

