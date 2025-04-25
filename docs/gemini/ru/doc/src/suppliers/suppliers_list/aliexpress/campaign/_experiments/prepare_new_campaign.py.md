# Модуль для подготовки новой рекламной кампании AliExpress

## Обзор

Этот модуль содержит код для подготовки новой рекламной кампании на AliExpress. Он использует класс `AliCampaignEditor` для работы с кампаниями.

## Подробности

Модуль `prepare_new_campaign.py`  находится в каталоге `hypotez/src/suppliers/aliexpress/campaign/_experiments`. 
Он отвечает за подготовку новой рекламной кампании на AliExpress, используя  класс `AliCampaignEditor` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`. 
Модуль использует стандартную библиотеку `Pathlib` для работы с файлами и каталогами, а также функции `get_filenames`, `get_directory_names` из модуля `src.utils` для получения имен файлов и каталогов.
Он также использует `pprint` для вывода информации в удобочитаемом виде. 

## Классы

### `AliCampaignEditor`

**Описание**: Класс `AliCampaignEditor`  предназначен для работы с рекламными кампаниями на AliExpress.

**Атрибуты**:

- `campaign_name` (str): Имя кампании, с которой работает класс. 

**Методы**:

- `process_new_campaign(campaign_name:str)`: Основной метод, который используется для запуска процесса подготовки новой кампании.

##  Функции

### `prepare_new_campaign.py` 

**Назначение**:  Код модуля `prepare_new_campaign.py`  запускает  процесс подготовки новой рекламной кампании на AliExpress.

**Как работает**:

1. **Инициализация**: Модуль `prepare_new_campaign.py` импортирует необходимые библиотеки,  включая  `Pathlib`,  `gs`,  `AliCampaignEditor`,  `get_filenames`,  `get_directory_names`,  `pprint`,  `logger`.
2. **Настройка**: В модуле устанавливается имя кампании (`campaign_name`). 
3. **Инициализация редактора кампаний**: Создается экземпляр класса `AliCampaignEditor`  с заданным именем кампании (`campaign_name`).
4. **Запуск процесса**:  Вызывается метод `process_new_campaign` у объекта `aliexpress_editor`  для запуска процесса подготовки новой кампании. 

**Пример**:

```python
## \\file /src/suppliers/aliexpress/campaign/_experiments/prepare_new_campaign.py
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

**Пример вызова**:

```python
# Импорт необходимых модулей
from src.suppliers.aliexpress.campaign._experiments.prepare_new_campaign import prepare_new_campaign

# Запуск процесса подготовки новой кампании с заданным именем
prepare_new_campaign('rc')
```


##  Параметры 

- `campaign_name` (str): Имя новой кампании.


##  Примечания:

-  Модуль `prepare_new_campaign.py`  использует класс `AliCampaignEditor` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.
-  Модуль использует функцию `pprint` для вывода информации в удобочитаемом виде.
-  Модуль использует `logger` для записи информации в лог.


##  Внутренние функции: 

-  `process_new_campaign()`:  функция, которая выполняет процесс подготовки новой рекламной кампании.