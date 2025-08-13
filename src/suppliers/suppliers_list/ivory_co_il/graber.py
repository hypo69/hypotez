## \file /src/suppliers/ivory/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.ivory 
	:platform: Windows, Unix
	:synopsis: Класс собирает значение полей на странице  товара `ivory.co.il`. 
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
from src.suppliers.graber import GraberBase, Config, close_pop_up



##                             DECORATOR TEMPLATE.


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
    supplier_prefix: str  = 'ivory.co.il'

    def __init__(self, driver:  = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Установка глобальные настройки через Context
        
        Config.locator_for_decorator = None # <- если будет установлено значение - то оно выполнится в декораторе `@close_pop_up`

