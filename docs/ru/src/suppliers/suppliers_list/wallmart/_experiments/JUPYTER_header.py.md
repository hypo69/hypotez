# src.suppliers.wallmart._experiments.JUPYTER_header

## Обзор

Модуль содержит набор экспериментов и вспомогательных функций для работы с поставщиком Wallmart, включая инструменты для настройки путей, импорта необходимых модулей, создания и управления объектами товаров и категорий, а также для взаимодействия с веб-драйвером и API PrestaShop.

## Подробней

Этот модуль предназначен для экспериментов и разработки функциональности, связанной с парсингом и обработкой данных о товарах с сайта Wallmart. Он включает в себя настройку путей к директориям проекта, импорт необходимых библиотек и модулей, а также определение функций для работы с данными о товарах и категориях. Модуль также содержит функции для взаимодействия с веб-драйвером и API PrestaShop, что позволяет автоматизировать процесс сбора и публикации информации о товарах.

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

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
from src.utils.files import save_json, j_loads, j_dumps, read_json, save_text_file
# ----------------
```

В этой секции происходит импорт необходимых библиотек и модулей, а также настройка путей к директориям проекта.
- `sys` и `os`: Используются для работы с системными переменными и путями.
- `pathlib.Path`: Используется для удобной работы с путями к файлам и директориям.
- `json`: Используется для работы с данными в формате JSON.
- `re`: Используется для работы с регулярными выражениями.
- `src.webdriver.driver.Driver`: Класс для управления веб-драйвером.
- `src.product.Product`, `src.product.ProductFields`: Классы для представления товаров и их полей.
- `src.category.Category`: Класс для представления категорий товаров.
- `src.utils.StringFormatter`, `src.utils.StringNormalizer`: Классы для форматирования и нормализации строк.
- `src.utils.printer.pprint`: Функция для красивой печати данных.
- `src.endpoints.PrestaShop.Product as PrestaProduct`: Класс для взаимодействия с API PrestaShop для товаров.
- `src.utils.files.save_json`, `src.utils.files.j_loads`, `src.utils.files.j_dumps`, `src.utils.files.read_json`, `src.utils.files.save_text_file`: Функции для работы с файлами JSON и текстовыми файлами.
- Определяются переменные `dir_root` и `dir_src` для хранения путей к корневой директории проекта и директории `src` соответственно. Корневая директория добавляется в `sys.path`, чтобы обеспечить возможность импорта модулей из этой директории.

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

**Назначение**: Функция для запуска поставщика.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика. По умолчанию `'aliexpress'`.
- `locale` (str): Локаль. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект поставщика, созданный на основе переданных параметров.

**Как работает функция**:
- Функция создает словарь `params` с параметрами поставщика, используя переданные аргументы `supplier_prefix` и `locale`.
- Затем функция возвращает объект класса `Supplier`, созданный с использованием словаря `params` в качестве аргументов.

**Примеры**:

```python
supplier = start_supplier(supplier_prefix='wallmart', locale='ru')
# Создается объект поставщика Wallmart с русской локалью.
```
```python
supplier = start_supplier()
# Создается объект поставщика Aliexpress с английской локалью (параметры по умолчанию).