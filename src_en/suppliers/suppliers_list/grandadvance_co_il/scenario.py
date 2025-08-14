# # \file /src/suppliers/bangood/scenario.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

"""Module for collecting goods from the page of the supplier categories Bangood.co.il through the webdraiter
==========================================================================================================

Each supplier has its own scenario of the capture of categories

-Modul collects a list of categories from the seller’s pages. `get_list_categories_from_site ()`.
@todo make a test for changing categories on the seller’s pages. 
The seller can add new categories, rename or delete/hide existing. 
By and large, you need to keep the category table `Prestashop.categories <-> aliexpress_com.shop.categoies`
- collects a list of goods from the page of the category `get_list_products_in_category ()` `
- Iteriyah according to the list transfers control to `grab_product_page ()` Determining the function of the current URL page  
`grab_product_page ()` processes the fields of the goods and transfers control to the class `Product`"""




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