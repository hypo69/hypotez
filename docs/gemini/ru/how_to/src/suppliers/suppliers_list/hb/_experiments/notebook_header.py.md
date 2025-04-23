### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для настройки окружения и импорта необходимых модулей для работы с поставщиками в проекте `hypotez`. Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также он импортирует различные классы и функции, необходимые для работы с поставщиками, товарами, категориями, форматированием строк, нормализацией строк, печатью, сохранением файлов и запуском сценариев.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируются необходимые модули, такие как `sys`, `os`, `Path`, `json`, `re` и другие.
2. **Определение корневой директории**: Определяется корневая директория проекта `hypotez` на основе текущей рабочей директории.
3. **Добавление корневой директории в `sys.path`**: Корневая директория добавляется в `sys.path`, что позволяет импортировать модули из других частей проекта.
4. **Импорт модулей проекта**: Импортируются модули проекта, такие как `gs`, `Driver`, `executor`, `Product`, `ProductFields`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `save_text_file` и `run_scenarios`.
5. **Определение функции `start_supplier`**: Определяется функция `start_supplier`, которая принимает префикс поставщика и локаль в качестве аргументов и возвращает объект `Supplier` с переданными параметрами.

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

from src import gs
from src.webdriver.driver import Driver, executor

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.scenario import run_scenarios

# Пример использования функции start_supplier
from src.suppliers import Supplier  # Предполагается, что класс Supplier находится в модуле src.suppliers

def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)

# Пример вызова функции start_supplier
supplier = start_supplier('hb', 'ru_RU')
print(f"Supplier: {supplier}")