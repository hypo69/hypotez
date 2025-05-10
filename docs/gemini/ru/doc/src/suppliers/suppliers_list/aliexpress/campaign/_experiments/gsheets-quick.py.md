# Работа с гугл таблицами

## Обзор

Файл `hypotez/src/suppliers/aliexpress/campaign/_experiments/gsheets-quick.py` содержит код, демонстрирующий простой пример работы с гугл таблицами. 

Файл демонстрирует основные операции: 

- чтение данных из таблицы
- сохранение данных в таблицу

## Подробнее

Файл демонстрирует пример работы с гугл таблицами с помощью библиотеки `gspread`. 

### Принцип работы кода:

- **Настройка**: 
    - В начале кода определяются параметры кампании: `campaign_name`, `category_name`, `language` и `currency`.
    - Создается экземпляр класса `AliCampaignGoogleSheet`, передавая в него заданные параметры.
    - Вызывается метод `set_products_worksheet` для указания рабочей таблицы с товарами.
- **Чтение данных**:
    - Код демонстрирует как можно использовать класс `AliCampaignGoogleSheet` для чтения данных из таблицы.
    - Запускается метод `save_campaign_from_worksheet` для сохранения данных из таблицы.
- **Сохранение данных**:
    - Код демонстрирует как можно использовать класс `AliCampaignGoogleSheet` для сохранения данных в таблицу.

### Пример использования:

```python
from unicodedata import category
import header
from types import SimpleNamespace
from gspread import Worksheet, Spreadsheet
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignGoogleSheet
from src.suppliers.suppliers_list.aliexpress.campaign.ttypes import CampaignType, CategoryType, ProductType
from src.utils.printer import pprint
from src.logger.logger import logger

campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
#gs.save_categories_from_worksheet(False)
gs.save_campaign_from_worksheet()
```

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с гугл таблицами кампаний AliExpress.

**Атрибуты**:

- `campaign_name` (str): Название кампании.
- `language` (str): Язык кампании.
- `currency` (str): Валюта кампании.

**Методы**:

- `set_products_worksheet(category_name: str) -> None`: Устанавливает рабочую таблицу для товаров.
- `save_categories_from_worksheet(write_header: bool = True) -> None`: Сохраняет категории из таблицы.
- `save_campaign_from_worksheet() -> None`: Сохраняет данные кампании из таблицы.

## Внутренние функции

### `main`

**Назначение**: Точка входа в скрипт.
**Как работает**:
-  Создается объект `gs` класса `AliCampaignGoogleSheet` с заданными параметрами.
-  Устанавливается рабочая таблица для товаров с помощью метода `set_products_worksheet`.
-  Вызывается метод `save_campaign_from_worksheet` для сохранения данных из таблицы.
-  Пример использования класса `AliCampaignGoogleSheet` для чтения и записи данных в гугл таблицы.

## Примеры

```python
from unicodedata import category
import header
from types import SimpleNamespace
from gspread import Worksheet, Spreadsheet
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignGoogleSheet
from src.suppliers.suppliers_list.aliexpress.campaign.ttypes import CampaignType, CategoryType, ProductType
from src.utils.printer import pprint
from src.logger.logger import logger

campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
#gs.save_categories_from_worksheet(False)
gs.save_campaign_from_worksheet()
```

```python
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignGoogleSheet

# Создаем объект AliCampaignGoogleSheet
gs = AliCampaignGoogleSheet(campaign_name='test_campaign', language='EN', currency='USD')

# Устанавливаем рабочую таблицу для товаров
gs.set_products_worksheet('chandeliers')

# Сохраняем категории из таблицы
gs.save_categories_from_worksheet()

# Сохраняем данные кампании из таблицы
gs.save_campaign_from_worksheet()