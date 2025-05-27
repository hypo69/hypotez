## \file /src/suppliers/hb/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.hb 
	:platform: Windows, Unix
	:synopsis: Класс собирает значение полей на странице  товара `hb.co.il`. 
    Для каждого поля страницы товара сделана функция обработки поля в родительском классе.
    Если нужна нестандертная обработка, функция перегружается в этом классе.
    ------------------
    Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. 
    Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение 
    в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение


"""
from typing import Optional, Any
from types import SimpleNamespace
import header
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.webdriver.driver import Driver
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


class Graber(Grbr):
    """Класс для операций захвата Morlevi."""
    supplier_prefix: str

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'hb'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Устанавливаем глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`

    # async def description_short(self, value:Optional[Any] = None) -> bool:
    #     """Fetch and set short description.
        
    #     Args:
    #     value (Any): это значение можно передать в словаре kwargs через ключ {description_short = `value`} при определении класса.
    #     Если `value` было передано, его значение подставляется в поле `ProductFields.description_short`.
    #     """
    #     try:
    #         # Получаем значение через execute_locator
    #         #path = self.driver.current_url + '/#tab-description'
    #         #await self.driver.get_url(path)
    #         raw_data = await self.driver.execute_locator(self.product_locator.description_short)

    #         self.fields.description_short = value or normalize_string(raw_data) or ''
    #         ...
    #         return
    #     except Exception as ex:
    #         logger.error(f"Ошибка получения значения в поле `description_short`", ex)
    #         ...
    #         return

    #     self.fields.description_short = value
    #     return True

    async def default_image_url(self, value:Optional[Any] = None) -> bool:
        return True

    async def price(self, value:Optional[Any] = None) -> bool:
        """Заглушка для цены"""
        self.fields.price = 150.00
        return True


        
