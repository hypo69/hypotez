Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода выполняет настройку окружения и импорт необходимых модулей для работы с поставщиками данных в проекте "hypotez". Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также импортируются необходимые библиотеки и модули, такие как `pathlib`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `PrestaProduct` и `Supplier`. Определяется функция `start_supplier` для запуска поставщика с заданными параметрами.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируются необходимые модули, такие как `sys`, `os`, `Path`, `json`, `re` и другие модули из проекта `hypotez`.
2. **Определение корневой директории**: Определяется корневая директория проекта `hypotez` и добавляется в `sys.path` для возможности импорта модулей из разных частей проекта.
3. **Импорт модулей из проекта**: Импортируются модули `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `PrestaProduct` и `Supplier` из проекта `hypotez`.
4. **Определение функции `start_supplier`**: Определяется функция `start_supplier`, которая принимает префикс поставщика (`supplier_prefix`) и локаль (`locale`) в качестве аргументов. Она создает и возвращает объект класса `Supplier` с переданными параметрами.

Пример использования
-------------------------

```python
import sys
import os
from pathlib import Path

# Определение корневой директории проекта
dir_root = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Добавление корневой папки в sys.path

from src.suppliers.supplier import Supplier  # Предполагается, что Supplier находится в этом модуле

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en'):
    """Старт поставщика"""
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    return Supplier(**params)

# Пример использования функции start_supplier
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
print(f"Supplier: {supplier}")