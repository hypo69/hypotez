### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода выполняет настройку окружения для работы с проектом `hypotez`. Он добавляет корневую директорию проекта и директорию `src` в `sys.path`, что позволяет импортировать модули из этих директорий. Также импортируются необходимые библиотеки и модули для работы с проектом. В конце определяется функция `start_supplier`, которая создает экземпляр класса `Supplier` с заданными параметрами.

Шаги выполнения
-------------------------
1. **Импорт библиотек и модулей**:
   - Импортируются необходимые библиотеки, такие как `sys`, `os`, `Path` из `pathlib`, `json`, `re`.
   - Импортируются модули из проекта `hypotez`, такие как `Driver` из `src.webdriver.driver`, `Product`, `ProductFields` из `src.product`, `Category` из `src.category`, `StringFormatter`, `StringNormalizer` из `src.utils`, `pprint` из `src.utils.printer`, `Product` из `src.endpoints.PrestaShop` и `save_text_file`.

2. **Настройка `sys.path`**:
   - Определяется корневая директория проекта `hypotez` с использованием `os.getcwd()` и `rfind()`.
   - Корневая директория и директория `src` добавляются в `sys.path`, чтобы Python мог находить и импортировать модули из этих директорий.

3. **Определение функции `start_supplier`**:
   - Функция `start_supplier` принимает два аргумента: `supplier_prefix` (префикс поставщика, по умолчанию `'aliexpress'`) и `locale` (локаль, по умолчанию `'en'`).
   - Функция создает словарь `params` с переданными аргументами.
   - Функция создает и возвращает экземпляр класса `Supplier` с параметрами из словаря `params`.

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
sys.path.append (str (dir_src) ) 
# ----------------

from pathlib import Path
import json
import re

from src.webdriver.driver import Driver
from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
from src.utils.files import save_text_file

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    # Предполагается, что класс Supplier импортирован и доступен
    # from your_module import Supplier  # Замените your_module на имя вашего модуля
    
    # return Supplier(**params) #  <-  Что то возвращаем
    return params