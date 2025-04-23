### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для инициализации и настройки окружения для работы с поставщиками в проекте `hypotez`. Он добавляет необходимые пути в `sys.path`, импортирует нужные модули и классы, а также определяет функцию для запуска поставщика.

Шаги выполнения
-------------------------
1. **Импорт модулей**:
   - Импортируются стандартные модули `sys`, `os`, `pathlib`.
   - Импортируются модули для работы с данными: `json`, `re`.
   - Импортируются классы и функции из проекта `hypotez`:
     - `Product`, `ProductFields` из `src.product`.
     - `Category` из `src.category`.
     - `StringFormatter`, `StringNormalizer` из `src.utils`.
     - `pprint` из `src.utils.printer`.
     - `Product` из `src.endpoints.PrestaShop`.
     - `save_text_file` из неопределенного модуля (требуется уточнение).

2. **Настройка путей**:
   - Определяется корневая директория проекта `hypotez` с использованием `os.getcwd()` и `rfind('hypotez')`.
   - Корневая директория добавляется в `sys.path`, чтобы обеспечить импорт модулей из проекта.
   - Директория `src` также добавляется в `sys.path`.

3. **Определение функции `start_supplier`**:
   - Функция `start_supplier` принимает два аргумента: `supplier_prefix` (префикс поставщика, по умолчанию `'aliexpress'`) и `locale` (локаль, по умолчанию `'en'`).
   - Функция создает словарь `params` с этими параметрами.
   - Функция возвращает экземпляр класса `Supplier`, инициализированного с этими параметрами (класс `Supplier` не определен в данном блоке кода, требуется его импорт или определение).

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

from src.suppliers import Supplier # Предполагается, что Supplier находится в этом модуле

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)

# Пример вызова функции start_supplier
supplier = start_supplier(supplier_prefix='my_supplier', locale='fr')
print(f"Supplier: {supplier}")