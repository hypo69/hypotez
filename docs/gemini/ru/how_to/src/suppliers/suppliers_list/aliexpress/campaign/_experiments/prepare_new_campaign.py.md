### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода инициализирует и запускает процесс создания новой рекламной кампании на AliExpress. Он использует класс `AliCampaignEditor` для управления процессом создания кампании и включает в себя импорт необходимых модулей и настройку переменных.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `header`, `Path`, `gs`, `AliCampaignEditor`, `get_filenames`, `get_directory_names`, `pprint` и `logger`.
2. **Инициализация имени кампании**:
   - Задаётся имя кампании `campaign_name` как `'rc'`.
3. **Создание экземпляра `AliCampaignEditor`**:
   - Создается экземпляр класса `AliCampaignEditor` с именем кампании `campaign_name`.
4. **Запуск процесса создания кампании**:
   - Вызывается метод `process_new_campaign` экземпляра `aliexpress_editor` с именем кампании `campaign_name` для запуска процесса создания новой рекламной кампании.

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/campaign/_experiments/prepare_new_campaign.py
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




""" Эксперименты над сценарием новой рекламной камании """
...
import header

from pathlib import Path

from src import gs

from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.utils import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

campaign_name = 'rc'
aliexpress_editor =  AliCampaignEditor(campaign_name)
aliexpress_editor.process_new_campaign(campaign_name)