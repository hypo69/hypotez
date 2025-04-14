# Модуль для экспериментов с поставщиком VisualDG
## Обзор

Модуль содержит экспериментальный код для работы с поставщиком VisualDG. Включает в себя импорты различных библиотек и модулей, необходимых для работы с поставщиками, веб-драйвером, продуктами и категориями. Также содержит функцию `start_supplier` для инициализации поставщика.
## Подробней
Данный код является частью проекта `hypotez` и предназначен для экспериментов с поставщиком VisualDG. Он содержит импорты необходимых модулей и функцию для запуска поставщика. Расположение файла в проекте указывает на то, что это экспериментальный код, который может быть изменен или удален в будущем.

## Подключение зависимостей

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
from src.suppliers import Supplier
from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
from src.utils import save_text_file
```

Здесь происходит импорт необходимых модулей и библиотек для работы с проектом. В частности, импортируются модули для работы с поставщиками, продуктами, категориями, веб-драйвером и другими утилитами.

- `sys`: Модуль для работы с системными параметрами и функциями.
- `os`: Модуль для работы с операционной системой.
- `pathlib.Path`: Класс для представления путей к файлам и каталогам.
- `json`: Модуль для работы с JSON-данными.
- `re`: Модуль для работы с регулярными выражениями.
- `src.webdriver.driver.Driver`: Класс для работы с веб-драйвером.
- `src.suppliers.Supplier`: Класс для работы с поставщиками.
- `src.product.Product`: Класс для работы с продуктами.
- `src.category.Category`: Класс для работы с категориями.
- `src.utils.StringFormatter`: Класс для форматирования строк.
- `src.utils.StringNormalizer`: Класс для нормализации строк.
- `src.utils.printer.pprint`: Функция для красивой печати данных.
- `src.endpoints.PrestaShop.Product`: Класс для работы с продуктами в PrestaShop.
- `src.utils.save_text_file`: Функция для сохранения текста в файл.

Также добавляется корневая папка проекта в `sys.path`, что позволяет импортировать модули из других частей проекта.

## Функции
### `start_supplier`
```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Функция для запуска поставщика.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль поставщика. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект поставщика, созданный с указанными параметрами.

**Как работает функция**:
Функция создает словарь `params` с параметрами поставщика, используя переданные аргументы `supplier_prefix` и `locale`. Затем она создает экземпляр класса `Supplier` с использованием этих параметров и возвращает его.

**Примеры**:
```python
# Запуск поставщика с префиксом 'aliexpress' и локалью 'en'
supplier = start_supplier()

# Запуск поставщика с префиксом 'amazon' и локалью 'de'
supplier = start_supplier(supplier_prefix='amazon', locale='de')