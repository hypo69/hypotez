## Как использовать блок кода `prepare_new_campaign.py`
=========================================================================================

Описание
-------------------------
Этот блок кода реализует сценарий создания новой рекламной кампании на AliExpress. Он использует класс `AliCampaignEditor` для обработки и управления кампаниями.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `header`, `Path`, `gs`, `AliCampaignEditor`, `get_filenames`, `get_directory_names`, `pprint`, `logger`.
2. **Инициализация переменных**:
   - Определяется название кампании (`campaign_name = 'rc'`).
   - Создается объект `AliCampaignEditor` с именем `aliexpress_editor` для взаимодействия с кампанией.
3. **Запуск процесса создания новой кампании**:
   - Вызывается метод `process_new_campaign` объекта `aliexpress_editor`, передавая название кампании в качестве аргумента. Этот метод запускает процесс создания новой кампании на AliExpress.

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
```