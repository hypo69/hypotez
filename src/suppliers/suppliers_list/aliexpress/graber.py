## \file /src/suppliers/suppliers_list/aliexpress/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
rst```
.. module:: src.suppliers.suppliers_list.aliexpress 
	:platform: Windows, Unix
	:synopsis: Модуль для сбора данных о товарах с AliExpress
```
Модуль для сбора данных о товарах с Amazon.
=========================================================================================

Модуль содержит класс :class:`Graber`, который используется для сбора данных о товарах
с веб-сайта `aliexpress.com`. Он наследуется от базового класса :class:`src.suppliers.graber.Graber`.

Класс `Graber` предоставляет методы для обработки различных полей товара на странице.
В случае необходимости нестандартной обработки поля, метод может быть переопределен.

Перед отправкой запроса к веб-драйверу могут быть выполнены предварительные действия
с использованием декоратора. Декоратор по умолчанию находится в родительском классе.
Для активации декоратора необходимо передать значение в `Context.locator`.
Также возможно реализовать свой собственный декоратор, раскомментировав соответствующие строки кода
и переопределив его поведение.
"""
from typing import Optional, Any
from types import SimpleNamespace
from typing import Any, Callable
from functools import wraps
# from src.utils.jjson import j_loads, j_loads_ns
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.webdriver.driver import Driver
from src.logger.logger import logger
from src.logger.exceptions import ExecuteLocatorException

#
#
#           DECORATOR TEMPLATE. 
#
# def close_pop_up(value: Any = None) -> Callable:
#     """
#     Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.
    
#     :param value: Дополнительное значение для декоратора.
#     :type value: Any
#     :return: Декоратор, оборачивающий функцию.
#     :rtype: Callable
    
#     """
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 # проверяет наличие локатора для закрытия всплывающего окна
#                 if Config.locator_for_decorator and Config.locator_for_decorator.close_pop_up:
#                      # исполняет локатор закрытия всплывающего окна
#                     await Context.driver.execute_locator(Config.locator_for_decorator.close_pop_up) 
#                 ...
#             except ExecuteLocatorException as ex:
#                 # логирует ошибку выполнения локатора
#                 logger.debug(f'Ошибка выполнения локатора: ', ex)
#             # ожидает выполнения основной функции
#             return await func(*args, **kwargs)  
#         return wrapper
#     return decorator


class Graber(Grbr):
    """
    Класс для сбора данных о товарах с AliExpress.
    """
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """
        Инициализация класса сбора полей товара.

        :param driver: Экземпляр веб-драйвера для взаимодействия с браузером.
        :type driver: Driver
        """
        self.supplier_prefix = 'aliexpress'
        # вызов конструктора родительского класса
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)

        # устанавливает значение локатора для декоратора в `None`
        # если будет установленно значение - то оно выполнится в декораторе `@close_pop_up`
        Config.locator_for_decorator = None
