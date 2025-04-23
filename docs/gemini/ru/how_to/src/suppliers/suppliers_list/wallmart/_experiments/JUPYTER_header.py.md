### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода инициализирует основные компоненты для работы с поставщиком данных (например, AliExpress). Он настраивает пути, добавляет необходимые каталоги в `sys.path`, импортирует нужные модули и классы, а также предоставляет функцию для старта работы с поставщиком.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `sys`, `os`, `Path`, `json`, `re`, а также пользовательские модули и классы, такие как `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `PrestaProduct`, `pprint` и `save_text_file`.
2. **Определение корневой директории проекта**: Определяется корневая директория проекта `hypotez` и добавляется в `sys.path`, чтобы можно было импортировать модули из этой директории.
3. **Инициализация поставщика**: Функция `start_supplier` принимает префикс поставщика и локаль, создает параметры и возвращает экземпляр класса `Supplier` с этими параметрами.

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
from src.suppliers import Supplier
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

# Пример использования:
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
# Теперь можно использовать объект supplier для работы с данными от AliExpress
```