### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для настройки окружения и импорта необходимых модулей для работы с поставщиком (например, eBay) в проекте Hypotez. Он добавляет корневую директорию проекта в `sys.path`, чтобы обеспечить доступ к модулям, а также импортирует различные утилиты, классы и библиотеки, необходимые для работы с данными о товарах, категориями и веб-драйвером.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки, такие как `sys`, `os`, `Path` (из `pathlib`), `json`, и `re`.
2. **Настройка `sys.path`**:
   - Определяется корневая директория проекта Hypotez.
   - Корневая директория добавляется в `sys.path`, чтобы Python мог находить модули из этой директории.
   - Аналогично добавляется директория `src` в `sys.path`.
3. **Импорт модулей проекта**: Импортируются специфические модули проекта, такие как:
   - `Driver` из `src.webdriver.driver` (для управления веб-браузером).
   - `Product` и `ProductFields` из `src.product` (для работы с информацией о товарах).
   - `Category` из `src.category` (для работы с категориями товаров).
   - `StringFormatter` и `StringNormalizer` из `src.utils` (для форматирования и нормализации строк).
   - `pprint` из `src.utils.printer` (для "красивого" вывода данных).
   - `Product` из `src.endpoints.PrestaShop` (для работы с API PrestaShop).
   - `save_text_file` из `src.utils` (для сохранения текста в файл).
4. **Определение функции `start_supplier`**: Функция `start_supplier` принимает префикс поставщика (например, 'aliexpress') и локаль (например, 'en') в качестве аргументов и возвращает объект класса `Supplier`, инициализированный с этими параметрами.

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

from src.webdriver.driver import Driver
from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)

# Пример использования функции start_supplier
supplier = start_supplier(supplier_prefix='ebay', locale='ru')
print(f"Инициализирован поставщик: {supplier}")