## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода демонстрирует создание и запуск рекламной кампании на AliExpress с использованием модели LLM.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
    - `header`: импортирует настройки конфигурации.
    - `Pathlib`:  предоставляет инструменты работы с путями к файлам.
    - `AliCampaignEditor`:  предоставляет методы для редактирования и обработки рекламных кампаний на AliExpress.
    - `gs`:  предоставляет функциональность для работы с Google Sheets.
    - `process_campaign_category`, `process_campaign`, `process_all_campaigns`:  функции для обработки категорий, отдельных кампаний и всех кампаний соответственно.
    - `get_filenames`, `get_directory_names`:  функции для получения имен файлов и каталогов.
    - `pprint`: функция для форматированного вывода данных.
    - `logger`:  предоставляет инструменты для логирования.

2. **Инициализация переменных**: 
    - `campaign_name`:  имя кампании, например, "lighting".
    - `campaign_file`:  имя файла, содержащего информацию о кампании, например, "EN_US.JSON".
    - `campaign_editor`:  создание экземпляра класса `AliCampaignEditor`,  передавая имя кампании и имя файла.

3. **Обработка кампании с помощью модели LLM**: 
    - Вызывается метод `process_llm_campaign`  у экземпляра `campaign_editor`, передавая имя кампании. 
    - Этот метод будет обрабатывать кампанию с использованием LLM для оптимизации настроек.

4. **Дополнительные операции**: 
    - Комментарии `#process_all_campaigns()`  показывают, что можно также использовать функцию  `process_all_campaigns()`  для обработки всех кампаний.
    - Комментарий `#locales = {\'EN\': \'USD\', \'HE\': \'ILS\', \'RU\': \'ILS\'} ` демонстрирует возможность настройки локальных настроек.

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/campaign/_experiments/prepare_ai_campaign.py
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

""" Проверка создания рекламной кампании """


import header
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src import gs
from src.suppliers.suppliers_list.aliexpress.campaign import process_campaign_category, process_campaign,  process_all_campaigns
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

#locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file )
campaign_editor.process_llm_campaign(campaign_name)
#process_all_campaigns()

```