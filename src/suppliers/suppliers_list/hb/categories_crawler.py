## \file /src/suppliers/suppliers_list/hb/sceanrio.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""  
Модуль сбора товаров со страницы категорий поставщика hb.co.il через вебдрайвер
=====================================================================================

Определение сценария обработки категорий для каждого поставщика.

- Модуль собирает список категорий со страниц продавца (`get_list_categories_from_site()`).
@todo Сделать проверку на изменение категорий на страницах продавца. 
Продавец может добавлять новые категории, переименовывать или удалять/прятать уже существующие. 
По большому счету надо держать таблицу категории `PrestaShop.categories <-> aliexpress.shop.categoies`
- Собирает список товаров со страницы категории (`get_list_products_in_category()`).
- Итерируясь по списку, передает управление в `grab_product_page()`, отсылая функции текущий URL страницы.  
`grab_product_page()` обрабатывает поля товара и передает управление классу `Product`.

```rst
 .. module:: src.suppliers.suppliers_list.hb.sceanrio
```
"""

import asyncio
from typing import List, Any, Dict # Added Any, Dict
from types import SimpleNamespace # Added SimpleNamespace

import header # Added header import
from header import __root__ # Added __root__ import
from src import gs # Ensured gs import
from src.logger.logger import logger
from src.webdriver.driver import Driver


async def get_list_products_in_category (d: Driver, l: SimpleNamespace) -> List[str] | None:    
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
       В текущей версии пагинация происхоадит через 
       https://hbdeadsea.co.il/collections/<название каетегории>?page=...
    """
    all_product_urls: List[str] = []
    # Извлечение ссылок на товары с текущей (первой) страницы
    while await d.execute_locator(l.show_more):
        continue

    product_links: List[str] | str | None = await d.execute_locator(l.product_links)
    return product_links

