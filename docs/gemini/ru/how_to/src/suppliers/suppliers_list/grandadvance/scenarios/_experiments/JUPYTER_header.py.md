### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для инициализации и настройки среды выполнения для работы с поставщиками данных в проекте `hypotez`. Он добавляет необходимые пути в `sys.path`, импортирует нужные модули и классы, а также предоставляет функцию для запуска поставщика с заданными параметрами.

Шаги выполнения
-------------------------
1. **Инициализация путей**:
   - Определяется корневая директория проекта `hypotez` на основе текущей рабочей директории.
   - Корневая директория добавляется в `sys.path`, что позволяет импортировать модули из проекта.
   - Определяется директория `src` и также добавляется в `sys.path`.

2. **Импорт модулей**:
   - Импортируются необходимые модули и классы, такие как `Path`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `PrestaProduct`, `pprint` и `save_text_file`.

3. **Функция `start_supplier`**:
   - Определяется функция `start_supplier`, которая принимает префикс поставщика (`supplier_prefix`) и локаль (`locale`) в качестве аргументов.
   - Функция создает словарь `params` с переданными аргументами.
   - Возвращает экземпляр класса `Supplier`, инициализированный с переданными параметрами.

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
from src.suppliers import Supplier # Ensure this import exists
from src.utils.file import save_text_file
# ----------------

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)

# Пример использования функции start_supplier
supplier = start_supplier(supplier_prefix='my_supplier', locale='fr')
# Теперь можно работать с объектом supplier
print(f"Supplier prefix: {supplier.supplier_prefix}, locale: {supplier.locale}")