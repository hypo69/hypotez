## \file /src/suppliers/morlevi/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3



"""
модуль для работы с Morlevi.co.il
==================================
Класс собирает значение полей на странице  товара `morlevi.co.il`. 
    Для каждого поля страницы товара сделана функция обработки поля в родительском классе.
    Если нужна нестандертная обработка, функция перегружается в этом классе.
    ------------------
    Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. 
    Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение 
    в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение

```rst
.. module:: src.suppliers.morlevi 
	:platform: Windows, Unix
	:synopsis: 
```
"""

from pathlib import Path
from typing import Optional, Any
from types import SimpleNamespace
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.webdriver.driverless.use_pydoll import Driver

import header
from src import gs
from src.suppliers.graber import GraberBase
from src.utils.image import save_image
from src.logger.logger import logger


@dataclass(slots=True, kw_only=True)
class Graber(GraberBase):
    """ Класс для операций захвата полей со страниц Morlevi.

    Attrs:
        supplier_prefix (str): Префикс поставщика. По умолчанию 'morlevi.co.il'.
        driver (Driver): Экземпляр драйвера браузера.
        locator_for_decorator (SimpleNamespace): Локаторы для использования в декораторах.
        lang_index (int): Индекс языка для локализации (1 — англ, 2 — иврит, 3 — русский). По умолчанию 1.
    """

    supplier_prefix: str = 'morlevi.co.il'
    # driver: 'Driver' = None
    # locator_for_decorator: Optional[SimpleNamespace] = None
    # lang_index: int = 1

    # def __post_init__(self):
    #     GraberBase.__post_init__()        
