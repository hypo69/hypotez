### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода настраивает окружение Python для работы с проектом `hypotez`, добавляя необходимые пути в `sys.path`, чтобы обеспечить доступ к модулям проекта. Он также импортирует необходимые библиотеки и модули, используемые в проекте. Кроме того, он определяет функцию `start_supplier`, которая создает экземпляр класса `Supplier` с заданными параметрами.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки, такие как `sys`, `os`, `Path`, `json`, `re` и другие модули проекта (`webdriver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `PrestaProduct`, `Supplier`).
2. **Настройка путей**:
   - Определяется корневая директория проекта `hypotez` с использованием `os.getcwd()` и `rfind()`.
   - Корневая директория добавляется в `sys.path`, чтобы Python мог находить модули проекта.
   - Определяется директория `src` и также добавляется в `sys.path`.
3. **Определение функции `start_supplier`**:
   - Функция `start_supplier` принимает два аргумента: `supplier_prefix` (префикс поставщика, по умолчанию `'aliexpress'`) и `locale` (локаль, по умолчанию `'en'`).
   - Создается словарь `params` с этими параметрами.
   - Создается и возвращается экземпляр класса `Supplier` с переданными параметрами.

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

from src.suppliers import Supplier  # Предполагается, что класс Supplier находится в модуле src.suppliers

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    return Supplier(**params)

# Пример использования функции start_supplier
supplier = start_supplier(supplier_prefix='my_supplier', locale='fr')
print(supplier)