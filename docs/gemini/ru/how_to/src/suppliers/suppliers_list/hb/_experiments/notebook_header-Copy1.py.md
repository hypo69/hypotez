## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода определяет функцию `start_supplier`, которая запускает сценарий для поставщика.

### Шаги выполнения
-------------------------
1. **Проверка входных параметров**: Функция проверяет, заданы ли сценарий `supplier_prefix` и язык `locale`. Если нет, то функция возвращает сообщение об ошибке.
2. **Создание словаря параметров**:  Создается словарь `params` с ключами `supplier_prefix` и `locale`, содержащий значения, переданные в функцию.
3. **Создание объекта поставщика**:  Создается объект `Supplier` с использованием словаря параметров `params`.


### Пример использования
-------------------------

```python
    # Запускаем сценарий для поставщика "hb" на языке "ru"
    start_supplier(supplier_prefix="hb", locale="ru")
```


### Изменения:
- Переименовал `params` в `supplier_params` для более точного описания.
- Уточнил описание функции `start_supplier`.
- Добавил пример использования функции.

### Улучшенный код:

```python
                ## \\file /src/suppliers/hb/_experiments/notebook_header-Copy1.py
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


import sys
import os
from pathlib import Path

# ----------------
dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )  # Добавляю корневую папку в sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) 
# ----------------

from pathlib import Path
import json
import re



from src import gs
from src.webdriver.driver import Driver, executor

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
, save_text_file
from src.scenario import run_scenarios
# ----------------

def start_supplier(supplier_prefix, locale):
    """ Запускает сценарий для поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    supplier_params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**supplier_params)
                ```