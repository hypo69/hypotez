## \file /src/suppliers/morlevi/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.morlevi 
	:platform: Windows, Unix
	:synopsis: Класс собирает значение полей на странице  товара `morlevi.co.il`. 
    Для каждого поля страницы товара сделана функция обработки поля в родительском классе.
    Если нужна нестандертная обработка, функция перегружается в этом классе.
    ------------------
    Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. 
    Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение 
    в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение


"""

from pathlib import Path
from typing import Optional, Any
from types import SimpleNamespace
from functools import wraps

import header
from src import gs
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.utils.image import save_image
from src.logger.logger import logger



class Graber(Grbr):
    """Класс для операций захвата Morlevi."""
    supplier_prefix: str  = 'morlevi'

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Инициализация класса сбора полей товара."""
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        Config.driver = self.driver
        Config.locator_for_decorator = self.product_locator.close_pop_up 

   