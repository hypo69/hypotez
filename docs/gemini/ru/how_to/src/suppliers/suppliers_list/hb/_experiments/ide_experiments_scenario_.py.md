### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для инициализации и настройки окружения для тестирования и сбора данных о товарах с сайта поставщика HB (hbdeadsea.co.il). Он добавляет необходимые пути в систему, импортирует нужные модули и классы, а также настраивает объекты `Supplier`, `Product`, `Driver` и `ProductFields` для выполнения сценариев.

Шаги выполнения
-------------------------
1. **Импорт модулей и классов**:
   - Импортируются необходимые модули, такие как `os`, `sys`, `Path`, `List`, `Union`, `Dict` и `WebElement`.
   - Добавляется корневая директория проекта в `sys.path`, чтобы можно было импортировать модули из `src`.
   - Импортируются классы `Supplier`, `Product`, `ProductFields`, `Driver`, `StringFormatter`, `StringNormalizer` и другие.

2. **Инициализация объектов**:
   - Создается экземпляр класса `Supplier` с префиксом `'hb'`.
   - Создается экземпляр класса `Product`, связанный с поставщиком `s`.
   - Извлекаются локаторы продукта из `s.locators['product']` в словарь `l`.
   - Создается экземпляр класса `Driver`, связанный с поставщиком `s`.
   - Создается экземпляр класса `ProductFields`, связанный с поставщиком `s`.

3. **Настройка текущего сценария**:
   - Определяется словарь `s.current_scenario`, содержащий URL, название, условие и категории PrestaShop для текущего сценария.

4. **Выполнение сценариев**:
   - Вызывается функция `run_scenarios` для выполнения сценариев с использованием настроенных объектов и текущего сценария.

Пример использования
-------------------------

```python
## \file /src/suppliers/hb/_experiments/ide_experiments_scenario_.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.hb._experiments
    :platform: Windows, Unix
    :synopsis:

"""


"""
    :platform: Windows, Unix
    :synopsis:

"""

"""
    :platform: Windows, Unix
    :synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""

""" module: src.suppliers.hb._experiments """


"""  Файл проверки наполнения полей HB -> product_fields """



#from math import prod
import os, sys
from pathlib import Path
from typing import List, Union, Dict
from selenium.webdriver.remote.webelement import WebElement

################# добавление корневой директории позволяет мне плясать от печки ###################
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Функция добавляет корневую папку в sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))
from src.webdriver import executor
"""  добавление корневой директории позволяет мне плясать от печки. """
####################################################################################################


from src import gs

from src.product import Product, ProductFields
from src.scenario import run_scenarios

from src.logger.logger import logger, ExecuteLocatorException
from src.webdriver.driver import Driver
from src.utils import StringFormatter, StringNormalizer


s: Supplier = Supplier(supplier_prefix = 'hb')
p: Product = Product(s)
l: dict = s.locators['product']
d: Driver = s.driver
f: ProductFields = ProductFields(s)


s.current_scenario: dict =  {
      "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
      "name": "טיפוח כפות ידיים ורגליים",
      "condition": "new",
      "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
      }
    }

ret = run_scenarios(s, s.current_scenario)
...