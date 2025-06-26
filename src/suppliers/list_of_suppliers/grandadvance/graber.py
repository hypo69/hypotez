## \file /src/suppliers/grandadvance/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

""" Модуль для сбора данных о товарах с Grandadvance.
=========================================================================================

Модуль содержит класс :class:`Graber`, который используется для сбора данных о товарах
с веб-сайта `bangood.com`. Он наследуется от базового класса :class:`src.suppliers.graber.Graber`.

Класс `Graber` предоставляет методы для обработки различных полей товара на странице.
В случае необходимости нестандартной обработки поля, метод может быть переопределен.

Для каждого поля страницы товара сделана функция обработки поля в родительском `Graber`.
Если нужна нестандертная обработка, можно перегрузить метод здесь, в этом классе.
------------------
Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. 
Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение 
в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение.
Вы также можете реализовать свой собственный декоратор, раскомментировав соответствующие строки кода

```rst
.. module:: src.suppliers.suppliers_list.grandadvance
```
"""

from typing import Optional, Any
from types import SimpleNamespace
import header
from header import __root__
from src import gs
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.utils.jjson import j_loads_ns
from src.webdriver.driver import Driver
from types import SimpleNamespace
from src.logger.logger import logger


ENDPOINT = 'grandadvance'

#############################################################

class Graber(Grbr):
    """Класс населедутет Graber."""

    def __init__(self, driver: Driver, lang_index:int):
        config:SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / ENDPOINT / f'{ENDPOINT}.json')
        locator: SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / ENDPOINT / 'locators' / 'product.json')
        super().__init__(supplier_prefix=ENDPOINT, driver=driver, lang_index=lang_index)
        Config.locator_for_decorator = self.product_locator.click_to_specifications # <- if locator not definded decorator 

