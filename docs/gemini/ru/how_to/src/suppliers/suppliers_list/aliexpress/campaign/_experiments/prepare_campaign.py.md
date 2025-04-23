### **Инструкция по использованию блока кода подготовки рекламной кампании**

=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для подготовки и запуска процесса создания или обновления рекламной кампании на платформе AliExpress. Он импортирует необходимые модули и задает параметры для рекламной кампании, такие как имя, язык и валюта. Если рекламная кампания с указанным именем не существует, она будет создана.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируются модули `header` и `process_campaign` из соответствующих директорий проекта. Модуль `process_campaign` отвечает за создание и обработку рекламной кампании.
2. **Определение параметров**:
   - Определяется словарь `locales`, содержащий соответствия между языками и валютами.
   - Задаются параметры рекламной кампании:
     - `language`: Язык кампании (по умолчанию 'EN').
     - `currency`: Валюта кампании (по умолчанию 'USD').
     - `campaign_name`: Имя кампании (по умолчанию 'brands').
3. **Запуск процесса кампании**: Вызывается функция `process_campaign` с указанным именем кампании. Функция отвечает за создание или обновление рекламной кампании на основе заданных параметров.

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/campaign/_experiments/prepare_campaign.py
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


""" Проверка создания affiliate для рекламной кампании  
Если текой рекламной кампании не существует - будет создана новая"""

...
import header
from src.suppliers.suppliers_list.aliexpress.campaign import process_campaign

locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
language: str = 'EN'
currency: str = 'USD'
campaign_name:str = 'brands'
# Если текой рекламной кампании не существует - будет создана новая

#process_campaign(campaign_name = campaign_name, language = language, currency = currency, campaign_file = campaign_file)
process_campaign(campaign_name = campaign_name)