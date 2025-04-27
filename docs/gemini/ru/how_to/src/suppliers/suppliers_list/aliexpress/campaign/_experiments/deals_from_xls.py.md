## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код парсит таблицу Excel, сгенерированную в личном кабинете портала AliExpress, для извлечения информации о предложениях. 

Шаги выполнения
-------------------------
1. Импортирует необходимые модули:
    - `header` (предположительно, модуль с настройками или глобальными переменными)
    - `DealsFromXLS` из `src.suppliers.suppliers_list.aliexpress` (класс, отвечающий за парсинг таблицы Excel)
    - `pprint` из `src.utils.printer` (функция для красивого вывода данных)
2. Создает экземпляр парсера `DealsFromXLS` с языком "EN" и валютой "USD".
3. Использует метод `get_next_deal()` для итерации по каждой строке в таблице Excel.
4. Выводит информацию о каждом предложении с помощью функции `pprint`.
5. ... (оставшийся код предполагает дальнейшую обработку информации о предложениях).


Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/campaign/_experiments/deals_from_xls.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.campaign._experiments 
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
  

""" module: src.suppliers.suppliers_list.aliexpress.campaign._experiments """


""" Парсер таблицы xls, сгенегированной в личном кабинете portals.aliexpress.com"""
...
import header
from src.suppliers.suppliers_list.aliexpress import DealsFromXLS 
from src.utils.printer import pprint

deals_parser = DealsFromXLS(language='EN', currency= 'USD')

for deal in deals_parser.get_next_deal():
    pprint(deal)
    ...
...


```