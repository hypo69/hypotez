### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для инициализации окружения и импорта необходимых модулей для работы с поставщиками (например, Amazon) в проекте `hypotez`. Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также он импортирует различные утилиты, классы и модули, необходимые для работы с продуктами, категориями, строками и веб-драйвером. В конце блока определяется функция `start_supplier`, которая инициализирует поставщика с заданными параметрами.

Шаги выполнения
-------------------------
1. **Инициализация путей**:
   - Определяется корневая директория проекта `hypotez` на основе текущей рабочей директории.
   - Корневая директория добавляется в `sys.path`, что позволяет импортировать модули из любой части проекта.
   - Определяется директория `src` внутри корневой директории и также добавляется в `sys.path`.

2. **Импорт модулей**:
   - Импортируются необходимые модули и классы из различных частей проекта, такие как:
     - `gs`
     - `Driver` и `executor` из `src.webdriver.driver`
     - `Product` и `ProductFields` из `src.product`
     - `Category` из `src.category`
     - `StringFormatter` и `StringNormalizer` из `src.utils`
     - `pprint` и `save_text_file` из `src.utils.printer`

3. **Определение функции `start_supplier`**:
   - Определяется функция `start_supplier`, которая принимает префикс поставщика (`supplier_prefix`) и локаль (`locale`) в качестве аргументов.
   - Функция проверяет, заданы ли оба параметра. Если нет, возвращает сообщение об ошибке.
   - Создается словарь `params` с параметрами поставщика.
   - Инициализируется класс `Supplier` с переданными параметрами и возвращается.

Пример использования
-------------------------

```python
import sys
import os
from pathlib import Path

# Инициализация путей
dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )  # Добавляю корневую папку в sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) 

# Импорт модулей
from src import gs
from src.webdriver.driver import Driver, executor
from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint, save_text_file
from src.suppliers.suppliers import Supplier  # Предположим, что класс Supplier находится здесь

# Определение функции start_supplier
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)

# Пример вызова функции start_supplier
supplier = start_supplier('amazon', 'ru_RU')
print(f"Поставщик: {supplier}")