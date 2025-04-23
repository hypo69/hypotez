## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода выполняет настройку окружения для работы с проектом `hypotez`. Он добавляет необходимые пути в `sys.path`, чтобы можно было импортировать модули из различных частей проекта. Также он содержит импорты необходимых библиотек и классов для работы с поставщиками, товарами, категориями и утилитами. В конце определена функция `start_supplier` для инициализации работы с конкретным поставщиком.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки, такие как `sys`, `os`, `Path`, `json`, `re`.
2. **Настройка путей**:
   - Определяется корневая директория проекта `hypotez` с использованием `os.getcwd()` и `rfind()`.
   - Корневая директория добавляется в `sys.path`, чтобы Python мог находить модули из этой директории.
   - Директория `src` также добавляется в `sys.path`.
3. **Импорт модулей проекта**: Импортируются модули и классы из проекта `hypotez`, такие как `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `PrestaProduct` и `Supplier`.
4. **Функция `start_supplier`**: Определяется функция `start_supplier`, которая принимает префикс поставщика и локаль в качестве аргументов и возвращает экземпляр класса `Supplier`.

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
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params))

# Пример использования функции start_supplier
# supplier = start_supplier(supplier_prefix='gearbest', locale='ru')
# Теперь можно использовать объект supplier для работы с поставщиком Gearbest