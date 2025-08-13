## \file /src/suppliers/suppliers_list/amazon_com/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.amazon_com.graber
    :platform: Windows, Unix
    :synopsis: Module for collecting product data from Amazon.

Amazon Product Data Graber
=========================================================================================

This module provides a `Graber` class designed to extract product information from Amazon.
It extends a base `Graber` class and includes functionality to handle pop-up windows during scraping.
It allows for custom handling of product fields by overriding methods.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.amazon_com.graber import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Amazon Graber
    amazon_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use amazon_graber methods to interact with Amazon
    # For example, to grab product details from a URL:
    # product_data = amazon_graber.grab_product_details("https://www.amazon.com/dp/B0XXXXXXX")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/amazon_com/graber.py
"""

from typing import Optional, Any
from types import SimpleNamespace
import header
from src.suppliers.graber import GraberBase, Config, close_pop_up
from src.webdriver.selenium.driver import Driver
from src.logger.logger import logger



#
#
#           DECORATOR TEMPLATE. 
#
# def close_pop_up(value: Any = None) -> Callable:
#     """Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

#     Args:
#         value (Any): Дополнительное значение для декоратора.

#     Returns:
#         Callable: Декоратор, оборачивающий функцию.
#     """
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close  
#                 ... 
#             except ExecuteLocatorException as e:
#                 logger.debug(f'Ошибка выполнения локатора: {e}')
#             return await func(*args, **kwargs)  # Await the main function
#         return wrapper
#     return decorator

class Graber(GraberBase):
    """Класс для операций захвата Morlevi."""
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'amazon'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Установка глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`

        
  