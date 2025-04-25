# Модуль `JUPYTER_header.py`

## Обзор

Модуль `JUPYTER_header.py` предоставляет набор функций и классов для работы с поставщиками. В нем  определен набор импортов и конфигураций, необходимых для работы с поставщиками. 

## Подробнее

Модуль `JUPYTER_header.py`  - это заготовка для создания файлов с конфигурацией. Модуль содержит набор конфигурационных переменных для разных платформ (Windows, Unix).
В модуле `JUPYTER_header.py`  происходит инициализация переменных, необходимых для  работы с поставщиками (например, `supplier_prefix`, `locale`).

## Функции

### `start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en')`

**Назначение**:
  - Создает экземпляр объекта `Supplier` и возвращает его.

**Параметры**:
  - `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
  - `locale` (str, optional): Язык. По умолчанию `'en'`.

**Возвращает**:
  - `Supplier`: Объект `Supplier` с заданными параметрами.

**Пример**:
```python
supplier = start_supplier(supplier_prefix='gearbest', locale='ru')
```
**Как работает функция**:
  -  Функция принимает два параметра: `supplier_prefix` и `locale`. 
  -  Создается словарь `params`  с ключами `'supplier_prefix'` и `'locale'` и значениями, полученными из входных параметров.
  -  Создается объект `Supplier` с помощью `Supplier(**params)` и возвращается. 


## Примеры

```python
## \\file /src/suppliers/gearbest/_experiments/JUPYTER_header.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.gearbest._experiments 
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
  
""" module: src.suppliers.gearbest._experiments """


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


#from settings import gs
from src.webdriver.driver import Driver

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
, save_text_file
# ----------------

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)