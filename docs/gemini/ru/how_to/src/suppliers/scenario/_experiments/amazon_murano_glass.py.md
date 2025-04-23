### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для запуска сценария парсинга товаров с сайта Amazon для категории "Murano Glass" (Муранское стекло). Он инициализирует поставщика (`Supplier`) для Amazon и запускает предопределенный сценарий парсинга для указанной категории.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `header` и `dict_scenarios`. Из модуля `header` импортируется функция `start_supplier`.
2. **Инициализация поставщика**: Вызывается функция `start_supplier('amazon')`, которая создает и инициализирует объект поставщика (`Supplier`) для сайта Amazon. Этот объект будет использоваться для выполнения сценария парсинга. Результат присваивается переменной `s`.
3. **Запуск сценария**: Из модуля `dict_scenarios` импортируется словарь `scenario`, содержащий различные сценарии парсинга. Вызывается метод `run_scenario` объекта `s` (типа `Supplier`), которому передается сценарий для "Murano Glass" (`scenario['Murano Glass']`). Этот метод выполняет парсинг товаров с Amazon в соответствии с указанным сценарием.
4. **Извлечение категории**: Извлекается первая категория из `s.current_scenario['presta_categories']['default_category']`.

Пример использования
-------------------------

```python
                ## \file /src/scenario/_experiments/amazon_murano_glass.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.scenario._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.scenario._experiments """


import header
#from header import j_dumps, j_loads,  logger, Category, Product, Supplier, gs, start_supplier
from header import start_supplier
s = start_supplier('amazon')
""" s - на протяжении всего кода означает класс `Supplier` """

from dict_scenarios import scenario
s.run_scenario(scenario['Murano Glass'])

k = list(s.current_scenario['presta_categories']['default_category'].keys())[0]