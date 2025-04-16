## \file /src/suppliers/suppliers_list/hb/sceanrio.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3
"""  
Модуль сбора товаров со страницы категорий поставщика hb.co.il через вебдрайвер
=====================================================================================

У каждого поставщика свой сценарий обреботки категорий

-Модуль Собирает список категорий со страниц продавца . `get_list_categories_from_site()`.
@todo Сделать проверку на изменение категорий на страницах продавца. 
Продавец может добавлять новые категории, переименовывать или удалять/прятать уже существующие. 
По большому счету надо держать таблицу категории `PrestaShop.categories <-> aliexpress.shop.categoies`
- Собирает список товаров со страницы категории `get_list_products_in_category()`
- Итерируясь по списку передает управление в `grab_product_page()` отсылая функции текущий url страницы  
`grab_product_page()` обрабатывает поля товара и передает управление классу `Product` 

"""
...
import asyncio
from typing import Dict, List
from pathlib import Path

from src import gs
from src.logger.logger import logger
from src.webdriver.driver import Driver




async def get_list_products_in_category (d: Driver, l:'SimpleNamespace') -> list[str, str, None]:    
    """ Returns list of products urls from category page
    Если надо пролистстать - страницы категорий - листаю ??????

    Attrs:
        s - Supplier
    @returns
        list or one of products urls or None
    """
    ...
    d.wait(1)
    d.scroll()
    ...

    list_products_in_category: List = await d.execute_locator(l.product_links)

    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        ...
        return
    ...
    while d.current_url != d.previous_url:
        if await paginator(d,l,list_products_in_category):
            list_products_in_category.append(await d.execute_locator(l.product_links))
        else:
            break
        
    list_products_in_category:list = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.debug(f""" Found {len(list_products_in_category)} items in  """)
    
    return list_products_in_category

async def paginator(d:Driver, locator: dict, list_products_in_category: list):
    """ Листалка """
    response = await d.execute_locator(locator.pagination.__dict__['<-'])
    if not response or (isinstance(response, list) and len(response) == 0): 
        ...
        return
    return True

def build_list_categories_from_site(s):
    """ сборщик актуальных категорий с сайта """
    ...

