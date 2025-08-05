# Модуль JUPYTER_header 

## Обзор

Модуль `JUPYTER_header` предоставляет функции для запуска поставщика. 

## Подробнее 

Этот модуль используется в рамках проекта `hypotez` для запуска различных поставщиков данных. Модуль `JUPYTER_header` содержит функцию `start_supplier`, которая инициализирует поставщика с заданным префиксом и языком. 

## Функции

### `start_supplier`

**Назначение**: Инициализирует поставщика с заданным префиксом и языком.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика. По умолчанию `aliexpress`.
- `locale` (str): Язык. По умолчанию `en`.

**Возвращает**: 
- Объект класса `Supplier`.

**Пример**:

```python
from src.suppliers.kualastyle._experiments.JUPYTER_header import start_supplier

# Запускаем поставщика с префиксом 'aliexpress' и языком 'en'
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
```

**Как работает**:
- Функция создает словарь параметров `params`, включающий `supplier_prefix` и `locale`.
- Затем функция создает экземпляр класса `Supplier` с использованием словаря `params`.
- Функция возвращает объект класса `Supplier`.

**Внутренние функции**: 
- Нет.

**Примеры**:
-  `start_supplier(supplier_prefix='aliexpress', locale='en')` - запускает поставщика с префиксом 'aliexpress' и языком 'en'.
- `start_supplier(supplier_prefix='kualastyle', locale='ru')` - запускает поставщика с префиксом 'kualastyle' и языком 'ru'.

```python
## \file /src/suppliers/kualastyle/_experiments/JUPYTER_header.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.kualastyle._experiments 
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
  
""" module: src.suppliers.kualastyle._experiments """


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
    
    return Supplier(**params))