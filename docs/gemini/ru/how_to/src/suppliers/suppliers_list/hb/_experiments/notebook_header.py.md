## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода настраивает среду разработки проекта "hypotez" и импортирует необходимые модули и классы. Он предназначен для использования в Jupyter Notebook.

Шаги выполнения
-------------------------
1. **Добавление корневой папки проекта в sys.path**: 
    - `dir_root: Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])` - определяет путь к корневой папке проекта,  используя текущую рабочую директорию.
    - `sys.path.append (str (dir_root) )` - добавляет путь к корневой папке в системный путь поиска модулей Python,  чтобы  программа могла находить  модули  в  этой  папке.
2. **Импорт модулей**:
    -  `from src import gs` - импортирует  модуль  `gs` из  подпапки  `src`.
    -  `from src.webdriver.driver import Driver, executor` - импортирует  классы  `Driver`  и  `executor`  из  модуля  `driver`  в  подпапке  `src/webdriver`.
    - `from src.product import Product, ProductFields` - импортирует классы `Product` и `ProductFields`  из  модуля  `product`  в  подпапке  `src`.
    - `from src.category import Category` - импортирует класс `Category` из  модуля  `category`  в  подпапке  `src`.
    - `from src.utils import StringFormatter, StringNormalizer` - импортирует классы  `StringFormatter`  и  `StringNormalizer`  из  модуля  `utils`  в  подпапке  `src`.
    - `from src.utils.printer import  pprint, save_text_file` - импортирует  функции  `pprint`  и  `save_text_file`  из  модуля  `printer`  в  подпапке  `src/utils`.
    - `from src.scenario import run_scenarios` - импортирует  функцию  `run_scenarios`  из  модуля  `scenario`  в  подпапке  `src`.
3. **Определение функции `start_supplier`**:
    - Эта функция принимает два аргумента: `supplier_prefix` (префикс поставщика) и `locale` (язык).
    -  Функция проверяет,  заданы  ли  оба  аргумента,  и  если  нет,  возвращает  сообщение  "Не  задан  сценарий  и  язык".
    -  Если  аргументы  заданы,  она  создает  словарь  `params`  с  этими  аргументами  и  возвращает  экземпляр  класса  `Supplier`  с  этим  словарям  в  качестве  параметров.


Пример использования
-------------------------
```python
# Импорт модуля
import sys
import os
from pathlib import Path

# Настройка пути к корневой папке проекта
dir_root: Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )

# Загрузка поставщика
from src.suppliers.hb._experiments.notebook_header import start_supplier

# Запуск поставщика
supplier = start_supplier('hb', 'ru')
```