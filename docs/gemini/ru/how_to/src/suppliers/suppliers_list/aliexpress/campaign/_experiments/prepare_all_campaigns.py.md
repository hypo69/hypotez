### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для запуска процесса подготовки рекламных кампаний AliExpress для различных языков и категорий. Он импортирует необходимые модули и функции для обработки рекламных кампаний и использует их для запуска процесса подготовки кампании.

Шаги выполнения
-------------------------
1. Импорт необходимых модулей:
   - Импортируется модуль `header`.
   - Импортируются функции `process_all_campaigns` и `main_process` из модуля `src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns`.

2. Вызов функции `process_campaign`:
   - Вызывается функция `process_campaign` с параметрами:
     - `campaign_name` (имя кампании).
     - `language` (язык).
     - `currency` (валюта).
     - `campaign_file` (файл кампании).
   - Если рекламной кампании с указанным именем не существует, будет создана новая.

3. Вызов функции `main_process`:
   - Вызывается функция `main_process` с параметрами:
     - `'brands'` (категория кампании).
     - `['mrgreen']` (список брендов).

4. Закомментированный вызов функции `process_all_campaigns`:
   - Строка `#process_all_campaigns()` закомментирована, что означает, что функция `process_all_campaigns` не будет вызвана.

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/campaign/_experiments/prepare_all_campaigns.py
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



""" Прогоняет все рекламные кампании для всех языков с поиском названий категорий из директорий """
...
import header
from src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns import process_all_campaigns, main_process

# locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
campaign_name:str = 'rc'
language: str = 'EN'
currency: str = 'USD'
campaign_file:str = None
# # Если текой рекламной кампании не существует - будет создана новая

process_campaign(campaign_name = campaign_name, language = language, currency = currency, campaign_file = campaign_file)
main_process('brands',['mrgreen'])
#process_all_campaigns()