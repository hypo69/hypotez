### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для парсинга данных о сделках из XLS-файла, сгенерированного в личном кабинете на portals.aliexpress.com. Он использует класс `DealsFromXLS` для извлечения информации о каждой сделке и выводит её на экран.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируется модуль `header` (содержимое не предоставлено, подразумевается, что он содержит необходимые заголовки или настройки).
   - Импортируется класс `DealsFromXLS` из модуля `src.suppliers.suppliers_list.aliexpress`.
   - Импортируется функция `pprint` из модуля `src.utils.printer` для удобного вывода данных.

2. **Создание экземпляра класса `DealsFromXLS`**:
   - Создается экземпляр класса `DealsFromXLS` с параметрами `language='EN'` и `currency='USD'`. Это указывает на то, что парсер должен обрабатывать данные на английском языке и в долларах США.

3. **Итерация по сделкам**:
   - Используется цикл `for deal in deals_parser.get_next_deal():` для получения каждой сделки из XLS-файла. Метод `get_next_deal()` класса `DealsFromXLS` возвращает данные о следующей сделке.

4. **Вывод данных о сделке**:
   - Функция `pprint(deal)` выводит информацию о текущей сделке в удобном для чтения формате.

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