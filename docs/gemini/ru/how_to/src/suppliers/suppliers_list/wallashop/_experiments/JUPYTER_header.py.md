### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для настройки окружения и импорта необходимых модулей для работы с поставщиками в проекте `hypotez`. Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также импортируются необходимые классы и функции для работы с продуктами, категориями, строками и веб-драйвером.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируются стандартные модули `sys`, `os`, `pathlib`, `json`, `re`.
2. **Настройка `sys.path`**:
   - Определяется корневая директория проекта `hypotez` на основе текущей рабочей директории.
   - Корневая директория добавляется в `sys.path`, что позволяет импортировать модули из других частей проекта.
   - Определяется директория `src` и также добавляется в `sys.path`.
3. **Импорт модулей проекта**: Импортируются классы и функции из следующих модулей:
   - `src.webdriver.driver.Driver`
   - `src.product.Product` и `src.product.ProductFields`
   - `src.category.Category`
   - `src.utils.StringFormatter`, `src.utils.StringNormalizer`
   - `src.utils.printer.pprint`
   - `src.endpoints.PrestaShop.Product`
4. **Определение функции `start_supplier`**:
   - Функция `start_supplier` принимает префикс поставщика и локаль в качестве аргументов.
   - Функция создает словарь `params` с переданными аргументами.
   - Возвращает экземпляр класса `Supplier` с переданными параметрами.

Пример использования
-------------------------

```python
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
    """ Функция запуска поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params))

# Пример использования
#from your_module import start_supplier  # Укажите правильный путь к модулю
#supplier = start_supplier(supplier_prefix='wallashop', locale='de')
#print(supplier)