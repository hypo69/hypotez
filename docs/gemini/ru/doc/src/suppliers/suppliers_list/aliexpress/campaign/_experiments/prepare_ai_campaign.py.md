# Модуль для подготовки рекламной кампании

## Обзор

Этот модуль содержит код для подготовки рекламной кампании на AliExpress. 

## Подробней

Модуль `prepare_ai_campaign.py` содержит код для настройки рекламной кампании на AliExpress с использованием инструментов AI.  Он включает в себя:

 -  `campaign_editor` - объект класса `AliCampaignEditor`, который используется для редактирования параметров рекламной кампании.
 -  `process_llm_campaign(campaign_name)` - метод, который запускает обработку рекламной кампании с использованием модели AI (при этом используется метод `campaign_editor.process_llm_campaign`).

## Функции

### `process_all_campaigns()`

**Назначение**: Запускает обработку всех рекламных кампаний. 
**Пример**: 
```python
    # Запуск обработки всех кампаний
    process_all_campaigns() 
```

## Классы

### `AliCampaignEditor`

**Описание**: Класс, представляющий редактор рекламной кампании AliExpress.  
**Атрибуты**:
 - `campaign_name` (str): Название рекламной кампании.
 - `campaign_file` (str): Название файла с описанием кампании. 
**Методы**:
 - `process_llm_campaign(campaign_name)`:  Запускает обработку рекламной кампании с использованием модели AI.

## Параметры

### `campaign_name`
 - `campaign_name` (str): Имя рекламной кампании.

### `campaign_file`
 - `campaign_file` (str): Название файла с описанием кампании. 

## Примеры

```python
# Загрузка необходимых модулей
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.utils.printer import pprint
from src.logger.logger import logger

# Инициализация параметров
campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'

# Создание объекта редактора кампании
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file )

# Запуск обработки кампании
campaign_editor.process_llm_campaign(campaign_name)

# Запуск обработки всех кампаний
process_all_campaigns() 
```
```python
# Вывод на печать
pprint({'campaign_name':campaign_name, 'campaign_file': campaign_file})

# Логгирование
logger.info(f'Обработка кампании: {campaign_name}')