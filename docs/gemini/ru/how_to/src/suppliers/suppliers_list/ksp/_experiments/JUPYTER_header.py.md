### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для настройки окружения и импорта необходимых модулей для работы с поставщиками в проекте `hypotez`. Он добавляет корневую директорию проекта и директорию `src` в `sys.path`, что позволяет импортировать модули из этих директорий. Также он импортирует различные модули, такие как `pathlib`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `PrestaProduct` и `Supplier`. Кроме того, он определяет функцию `start_supplier` для инициализации поставщика.

Шаги выполнения
-------------------------
1. **Определение корневой директории**: Определяется корневая директория проекта `hypotez` на основе текущей рабочей директории.
2. **Добавление в `sys.path`**: Корневая директория и директория `src` добавляются в `sys.path`, что позволяет импортировать модули из этих директорий.
3. **Импорт модулей**: Импортируются необходимые модули, такие как `pathlib`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `PrestaProduct` и `Supplier`.
4. **Определение функции `start_supplier`**: Определяется функция `start_supplier`, которая принимает префикс поставщика и локаль в качестве аргументов и возвращает экземпляр класса `Supplier`.

Пример использования
-------------------------

```python
import sys
import os
from pathlib import Path

# Определение корневой директории проекта
dir_root = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Добавление корневой папки в sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_src))

# Импорт необходимых модулей
from src.suppliers.supplier import Supplier
from src.utils.printer import pprint

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en'):
    """ Функция для старта поставщика """
    params = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    return Supplier(**params)

# Пример использования функции start_supplier
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
pprint(f"Поставщик: {supplier}")
```