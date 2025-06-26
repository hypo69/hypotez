## \file /src/suppliers/suppliers_list/amazon/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""  
Модуль сбора товаров со страницы категорий поставщика Amazon через вебдрайвер
=============================================================================================

У каждого поставщика свой сценарий обработки категорий.

- Модуль собирает список категорий со страниц продавца (`get_list_categories_from_site()`).
@todo Сделать проверку на изменение категорий на страницах продавца. 
Продавец может добавлять новые категории, переименовывать или удалять/прятать уже существующие. 
По большому счету надо держать таблицу категории `PrestaShop.categories <-> amazon.shop.categoies` (Заменено aliexpress на amazon)
- Собирает список товаров со страницы категории (`get_list_products_in_category()`).
- Итерируясь по списку, передает управление в `grab_product_page()`, отсылая функции текущий URL страницы.  
`grab_product_page()` обрабатывает поля товара и передает управление классу `Product`.

```rst
.. module:: src.suppliers.suppliers_list.amazon
```
"""

import header # Стандартный импорт
from header import __root__ # Стандартный импорт
from src import gs # Стандартный импорт

from typing import List, Dict, Any 
from pathlib import Path # Path не используется в предоставленном фрагменте, но оставлен на случай расширения

from src.logger.logger import logger
from src.webdriver.driver import Driver # Импорт класса Driver


async def get_list_products_in_category(d: Driver, l: Dict[str, Any]) -> List[str] | None:    
    """ 
    Функция извлекает список URL-адресов товаров со страницы категории.
    Если на странице есть пагинация, она должна быть обработана (текущая реализация не включает пагинацию).

    Args:
        d (Driver): Экземпляр WebDriver для взаимодействия со страницей.
        l (Dict[str, Any]): Словарь локаторов, где ключ 'product_links' 
                            содержит локатор для ссылок на товары.
    
    Returns:
        List[str] | None: Список URL-адресов товаров или `None`, если товары не найдены.
    
    Example:
        >>> # Для этого примера необходим настроенный driver и locators
        >>> # driver = Driver(...) 
        >>> # locators = {'product_links': 'some_xpath_or_css_selector_for_product_links'}
        >>> # product_urls = await get_list_products_in_category(driver, locators)
        >>> # if product_urls:
        >>> #     print(f'Найдено {len(product_urls)} товаров.')
    """
    list_products_from_locator: List[str] | str | None 
    processed_list_products: List[str] | None # Для конечного результата

    d.scroll() # Прокрутка страницы

    # TODO: Реализовать пагинацию (листалку) для страниц категорий.
    
    # Функция извлекает ссылки на товары.
    list_products_from_locator = await d.execute_locator(l['product_links'])
    
    if not list_products_from_locator:
        logger.warning('Нет ссылок на товары')
        return None # Возврат None, если ничего не найдено
    
    # Преобразование результата в список, если execute_locator вернул одну строку
    if isinstance(list_products_from_locator, str):
        processed_list_products = [list_products_from_locator]
    elif isinstance(list_products_from_locator, list):
        processed_list_products = list_products_from_locator
    else:
        # Обработка неожиданного типа данных, если необходимо
        logger.warning(f'execute_locator вернул неожиданный тип: {type(list_products_from_locator)}')
        return None


    logger.info(f'Найдено {len(processed_list_products)} товаров')
    
    #""" Проверяю наличие товара в базе данных магазина """
    #for asin in processed_list_products: # Заменено list_products_in_category на processed_list_products
    #    _asin = asin.split(f'''/''')[-2]
    #    # _sku = f'''{s.supplier_id}_{_asin}''' # 's' (supplier instance) не определен в этой функции
    #    # if PrestaShopProduct.check(_sku) == False:
    #    #     """ Синтаксис для того, чтобы помнить,
    #    #     что я проверяю ОТСУТСТВИЕ товара в базе данных
    #    #     """
    #    #     continue
    #    # else:
    #    #     """ Товар в базе данных """
    #    #     continue
    #        #TODO: Логику 

    return processed_list_products
