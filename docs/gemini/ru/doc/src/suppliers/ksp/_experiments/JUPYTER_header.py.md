# Модуль _experiments

## Обзор

Модуль содержит экспериментальный код, связанный с поставщиком KSP. Включает в себя импорты библиотек, настройку путей, а также функцию для запуска поставщика.

## Подробней

Этот модуль, кажется, является частью экспериментального кода, связанного с поставщиком KSP. Он содержит импорты библиотек, настройку путей и функцию для запуска поставщика. Код модуля предназначен для использования в среде Windows и Unix.

## Настройка окружения

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
```

Этот блок кода настраивает окружение выполнения, добавляя корневую директорию проекта `hypotez` и директорию `src` в `sys.path`. Это позволяет импортировать модули из этих директорий.

- `dir_root`: Определяет корневую директорию проекта `hypotez`, находя ее в текущей рабочей директории.
- `sys.path.append(str(dir_root))`: Добавляет корневую директорию в список путей поиска модулей.
- `dir_src`: Определяет директорию `src` внутри корневой директории.
- `sys.path.append(str(dir_root))`:  Повторно добавляет корневую директорию в `sys.path`.  Это может быть избыточным, так как корневая директория уже была добавлена ранее.

## Импорт модулей

```python
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
, save_text_file
```

Этот блок кода импортирует необходимые модули и классы, которые будут использоваться в дальнейшем коде.

- `Path` из `pathlib`: Для работы с путями к файлам и директориям.
- `json`: Для работы с данными в формате JSON.
- `re`: Для работы с регулярными выражениями.
- `Driver` из `src.webdriver.driver`: Класс для управления веб-драйвером (например, для Chrome или Firefox).
- `Supplier` из `src.suppliers`: Класс, представляющий поставщика товаров.
- `Product`, `ProductFields` из `src.product`: Классы для работы с информацией о продуктах.
- `Category` из `src.category`: Класс для работы с категориями товаров.
- `StringFormatter`, `StringNormalizer` из `src.utils`: Классы для форматирования и нормализации строк.
- `pprint` из `src.utils.printer`: Функция для "красивой" печати данных.
- `PrestaProduct` из `src.endpoints.PrestaShop`: Класс для работы с продуктами в PrestaShop.
- `save_text_file`: Функция для сохранения текстовых файлов.

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
    
    return Supplier(**params))
```

Функция создает и возвращает экземпляр класса `Supplier`.

**Назначение**: Запускает поставщика с указанными параметрами.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика. По умолчанию 'aliexpress'.
- `locale` (str): Локаль. По умолчанию 'en'.

**Возвращает**:
- Экземпляр класса `Supplier`.

**Как работает функция**:
- Создает словарь `params` с параметрами `supplier_prefix` и `locale`.
- Возвращает экземпляр класса `Supplier`, инициализированный с использованием распакованного словаря `params`.

**Примеры**:

```python
supplier = start_supplier(supplier_prefix='amazon', locale='de')
print(type(supplier))  # Output: <class 'src.suppliers.Supplier'>
```

```python
supplier = start_supplier()
print(type(supplier))  # Output: <class 'src.suppliers.Supplier'>