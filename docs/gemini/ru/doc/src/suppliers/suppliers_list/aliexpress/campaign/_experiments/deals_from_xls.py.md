# Парсер таблицы xls с портала AliExpress

## Обзор

Данный модуль содержит скрипт, который парсит таблицу xls, сгенерированную в личном кабинете портала `portals.aliexpress.com`. 

## Подробнее

Скрипт `deals_from_xls.py`  использует класс `DealsFromXLS` из модуля `src.suppliers.suppliers_list.aliexpress`. 
Данный класс  предназначен для парсинга данных о сделках с AliExpress из таблицы xls. 
Он принимает в качестве параметров язык (`language`) и валюту (`currency`) для корректного отображения информации.

##  Функции

### `deals_from_xls.py`

```python
                ## \\file /src/suppliers/aliexpress/campaign/_experiments/deals_from_xls.py
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

**Назначение**: Скрипт парсит таблицу xls, полученную с портала `portals.aliexpress.com` и выводит данные на печать.

**Параметры**:

-  `language` (str): Язык таблицы, по умолчанию - `'EN'`
-  `currency` (str): Валюта таблицы, по умолчанию - `'USD'`

**Возвращает**:
-  `None`.

**Как работает**:

1. **Инициализация**:
   -  `deals_parser = DealsFromXLS(language='EN', currency= 'USD')` создает объект `DealsFromXLS`, который будет использоваться для парсинга таблицы xls.
2. **Итерация по данным**:
   -  `for deal in deals_parser.get_next_deal():`  перебирает данные из таблицы xls.
3. **Вывод данных**:
   -  `pprint(deal)` выводит на печать информацию о текущей сделке (`deal`).

**Примеры**:

-  `deals_parser = DealsFromXLS(language='RU', currency= 'RUB')` - создаёт объект парсера для таблицы на русском языке с валютой рубль.
-  `deals_parser = DealsFromXLS(language='EN', currency= 'EUR')` - создаёт объект парсера для таблицы на английском языке с валютой евро.


## Внутренние функции

###  `get_next_deal()`

**Назначение**: Функция получает следующую сделку из таблицы xls. 

**Параметры**: 
-  `None`

**Возвращает**: 
-  `dict` - словарь, содержащий информацию о сделке или `None`, если сделок больше нет.

**Пример**:

```python
deals_parser = DealsFromXLS(language='EN', currency= 'USD')
deal = deals_parser.get_next_deal()
if deal:
    print(deal)
```


```markdown