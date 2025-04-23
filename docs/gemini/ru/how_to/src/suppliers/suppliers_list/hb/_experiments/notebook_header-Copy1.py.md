### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для настройки окружения и импорта необходимых модулей для работы с поставщиками в проекте Hypotez. Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из разных частей проекта. Также он импортирует необходимые классы и функции для работы с продуктами, категориями, форматированием строк, веб-драйвером и сценариями. В конце определяется функция `start_supplier`, которая запускает поставщика на основе переданных параметров.

Шаги выполнения
-------------------------
1. **Определение корневой директории проекта**:
   - С помощью `os.getcwd()` определяется текущая рабочая директория.
   - `os.getcwd().rfind('hypotez')+7` находит индекс последнего вхождения подстроки 'hypotez' и добавляет 7, чтобы получить индекс конца этой подстроки.
   - `Path(...)` создает объект `Path` для корневой директории проекта.
   ```python
   dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
   ```
2. **Добавление корневой директории в `sys.path`**:
   - `sys.path.append(str(dir_root))` добавляет корневую директорию проекта в список путей, по которым Python ищет модули.
   ```python
   sys.path.append (str (dir_root) )
   ```
3. **Определение директории `src`**:
   - `Path(dir_root, 'src')` создает объект `Path` для директории `src`, которая находится в корневой директории проекта.
   ```python
   dir_src = Path (dir_root, 'src')
   ```
4. **Повторное добавление корневой директории в `sys.path`**:
   - `sys.path.append(str(dir_root))` еще раз добавляет корневую директорию проекта в `sys.path`.
   ```python
   sys.path.append (str (dir_root) )
   ```
5. **Импорт необходимых модулей и классов**:
   - Импортируются модули `json`, `re`, классы `Product`, `ProductFields`, `Category`, `StringFormatter`, `StringNormalizer` и другие необходимые функции и классы.
   ```python
   from pathlib import Path
   import json
   import re

   from src import gs
   from src.webdriver.driver import Driver, executor

   from src.product import Product, ProductFields
   from src.category import Category
   from src.utils import StringFormatter, StringNormalizer
   from src.utils.printer import  pprint, save_text_file
   from src.scenario import run_scenarios
   ```
6. **Определение функции `start_supplier`**:
   - Функция принимает параметры `supplier_prefix` и `locale`.
   - Если параметры не заданы, функция возвращает сообщение об ошибке.
   - Функция создает словарь `params` с переданными параметрами.
   - Функция возвращает экземпляр класса `Supplier`, созданный с использованием переданных параметров.
   ```python
   def start_supplier(supplier_prefix, locale):
       """ Старт поставщика """
       if not supplier_prefix and not locale: return "Не задан сценарий и язык"

       params: dict = \
       {
           'supplier_prefix': supplier_prefix,
           'locale': locale
       }

       return Supplier(**params)
   ```

Пример использования
-------------------------

```python
import os
from pathlib import Path
import sys

# Определение корневой директории проекта
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append(str(dir_root))

from src.suppliers.hb._experiments.notebook_header-Copy1 import start_supplier

# Запуск поставщика с префиксом 'hb' и локалью 'ru_RU'
supplier = start_supplier('hb', 'ru_RU')

# Вывод информации о поставщике (если это необходимо)
print(supplier)