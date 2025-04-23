### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для настройки окружения и импорта необходимых модулей для работы с поставщиками, в частности, для парсинга и обработки данных с сайта Banggood. Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также импортируются различные классы и утилиты, необходимые для работы с продуктами, категориями, строками и веб-драйвером.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируются стандартные модули `sys`, `os`, `pathlib`, `json`, `re`.
2. **Настройка `sys.path`**:
   - Определяется корневая директория проекта `hypotez` с использованием `os.getcwd()` и `rfind()`.
   - Корневая директория добавляется в `sys.path`, что позволяет импортировать модули из этой директории.
   - Директория `src` также добавляется в `sys.path`.
3. **Импорт модулей проекта**:
   - Импортируются классы `Product`, `ProductFields`, `Category` из модуля `src`.
   - Импортируются утилиты `StringFormatter`, `StringNormalizer` из модуля `src.utils`.
   - Импортируется функция `pprint` из модуля `src.utils.printer`.
   - Импортируется класс `Product` из модуля `src.endpoints.PrestaShop`.
   - Импортируются функции `save_json`, `j_loads`, `save_text_file` из модуля `src.utils.files`.
4. **Функция `start_supplier`**:
   - Определяется функция `start_supplier`, которая принимает префикс поставщика (`supplier_prefix`) и локаль (`locale`) в качестве аргументов.
   - Функция создает словарь `params` с этими параметрами.
   - Возвращается экземпляр класса `Supplier`, созданный с использованием этих параметров.

Пример использования
-------------------------

```python
import sys
import os
from pathlib import Path

# Настройка sys.path (как в исходном коде)
dir_root = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Добавляю корневую папку в sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))

from src.suppliers import Supplier  # Предполагается, что класс Supplier находится в этом модуле

# Пример использования функции start_supplier
def start_supplier(supplier_prefix: str = 'bangood', locale: str = 'en'):
    """ Старт поставщика """
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)

# Пример вызова функции
supplier = start_supplier(supplier_prefix='bangood', locale='en')
print(f"Supplier: {supplier}")