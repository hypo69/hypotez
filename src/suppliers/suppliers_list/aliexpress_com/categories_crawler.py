## \file /src/suppliers/suppliers_list/aliexpress/categories_crawler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""  
Модуль сбора товаров со страницы категорий поставщика `aliexpress` через вебдрайвер
=====================================================================================


```rst
 .. module:: src.suppliers.suppliers_list.aliexpress_com.categories_crawler
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
    Функция извлекает список URL-адресов товаров со страницы категории.
    При необходимости пролистывает страницы категорий.

    Args:
        d (Driver): Экземпляр WebDriver.
        l (SimpleNamespace): Объект с локаторами для страницы категории, 
                             включая локаторы товаров и пагинации.
    
    Returns:
        List[str] | None: Список URL-адресов товаров или `None`, если товары не найдены.
    
    Example:
        >>> # Пример использования (требует настройки d и l)
        >>> # driver = Driver(...) 
        >>> # locators = SimpleNamespace(product_links=..., pagination_locators=...)
        >>> # product_urls = await get_list_products_in_category(driver, locators)
        >>> # if product_urls:
        >>> #     print(f'Найдено {len(product_urls)} товаров.')
    """


    """
       В текущей версии пагинация происхоадит через нажати кнопки
       https://hbdeadsea.co.il/collections/<название каетегории>?page=...
    """

    """
    all_product_urls: List[str] = []
    # Извлечение ссылок на товары с текущей (первой) страницы
    while True:
        if not await d.execute_locator(l.show_more):
            break
        product_links: List[str] | str | None = await d.execute_locator(l.product_links)
        if len(all_product_urls) <  len(product_links):
            all_product_urls.extend(all_product_urls)
            time.sleep(3)
            print('Листаю')
            continue
        else:
            break

    """
    product_links: List[str] | str | None = await d.execute_locator(l.product_links)
    return product_links if isinstance(product_links, list) else [product_links]