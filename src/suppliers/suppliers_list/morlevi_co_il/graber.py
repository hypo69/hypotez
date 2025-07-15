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
#from functools import wraps
from dataclasses import dataclass, field

import header
from src import gs
from src.suppliers.graber import Graber as SupplierGraber
from src.utils.image import save_image
from src.logger.logger import logger


@dataclass(slots=True)
class Graber(SupplierGraber):
    """Класс для операций захвата Morlevi."""

    def __post_init__(self):
        """Инициализация класса сбора полей товара."""
        
        super().__post_init__(
                            supplier_prefix = self.supplier_prefix, 
                            driver = self.driver, 
                            locator_for_decorator = self.locator_for_decorator or None,
                            lang_index = self.lang_index or 1
                            )
        ...
         

   