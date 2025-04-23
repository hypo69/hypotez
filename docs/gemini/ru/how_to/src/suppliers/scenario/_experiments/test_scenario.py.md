### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для запуска сценариев поставщика. Он инициализирует поставщика с заданным префиксом, создает объект сценария и запускает сценарии.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `sys`, `os`, `Path`, `json`, `re`, `gs`, `pprint`, `Scenario`, `Supplier`.
2. **Добавление корневой папки в `sys.path`**: Добавляется корневая папка проекта в `sys.path`, чтобы обеспечить возможность импорта модулей из других частей проекта.
3. **Определение функции `start_supplier`**: Функция `start_supplier` принимает префикс поставщика в качестве аргумента и возвращает объект поставщика (`Supplier`) с заданным префиксом.
4. **Определение префикса поставщика**: Задается префикс поставщика (`supplier_prefix`), который может быть одним из значений: `'aliexpress'`, `'amazon'`, `'kualastyle'` или `'ebay'`.
5. **Инициализация поставщика**: Вызывается функция `start_supplier` с заданным префиксом поставщика, и результат присваивается переменной `s`.
6. **Создание объекта сценария**: Создается объект сценария (`Scenario`) с использованием инициализированного объекта поставщика `s`.
7. **Запуск сценариев**: Вызывается метод `run_scenarios()` объекта сценария для запуска сценариев.

Пример использования
-------------------------

```python
import sys
import os
path = os.getcwd()[:os.getcwd().rfind(r'hypotez')]
sys.path.append(path)  # Добавляю корневую папку в sys.path

from pathlib import Path
import json
import re

from hypotez import gs
from src.utils.printer import pprint

from src.scenario import Scenario
from src.suppliers import Supplier


def start_supplier(supplier_prefix: str) -> Supplier:
    """
    Инициализирует поставщика с заданным префиксом.

    Args:
        supplier_prefix (str): Префикс поставщика.

    Returns:
        Supplier: Объект поставщика.
    """
    params: dict = {
        'supplier_prefix': supplier_prefix
    }

    return Supplier(**params)


supplier_prefix = 'aliexpress'
# supplier_prefix = 'amazon'
# supplier_prefix = 'kualastyle'
# supplier_prefix = 'ebay'

s = start_supplier(supplier_prefix)
""" s - на протяжении всего кода означает класс `Supplier` """

print(" Можно продолжать ")

scenario = Scenario(s)

scenario.run_scenarios()
```