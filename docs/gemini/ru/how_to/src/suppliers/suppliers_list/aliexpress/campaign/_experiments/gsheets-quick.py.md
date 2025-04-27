## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует пример работы с гугл таблицами с помощью библиотеки gspread в контексте проекта `hypotez`. Он создает объект `AliCampaignGoogleSheet` и использует его для сохранения информации о кампании в гугл таблицу.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: 
    - `unicodedata`: Используется для работы с юникодом.
    - `header`: (Неопределено).
    - `types`: Используется для создания `SimpleNamespace`.
    - `gspread`: Основная библиотека для работы с гугл таблицами.
    - `src.suppliers.suppliers_list.aliexpress.campaign.AliCampaignGoogleSheet`:  Класс для работы с гугл таблицей, связанной с AliExpress кампаниями.
    - `src.suppliers.suppliers_list.aliexpress.campaign.ttypes`:  Класс, содержащий типы данных для AliExpress кампаний.
    - `src.utils.printer`:  Библиотека для вывода красивой информации в консоль.
    - `src.logger.logger`:  Библиотека для логирования.
2. **Определение параметров**:
    - `campaign_name`:  Название кампании.
    - `category_name`:  Название категории.
    - `language`:  Язык.
    - `currency`:  Валюта.
3. **Создание объекта `AliCampaignGoogleSheet`**:
    - Объект `AliCampaignGoogleSheet` создаётся с заданными параметрами `campaign_name`, `language` и `currency`.
4. **Установка рабочего листа для товаров**:
    - Метод `set_products_worksheet` объекта `AliCampaignGoogleSheet` устанавливает рабочий лист для хранения информации о товарах, задавая название категории `category_name`.
5. **Сохранение информации о кампании**:
    - Метод `save_campaign_from_worksheet` объекта `AliCampaignGoogleSheet` сохраняет информацию о кампании в гугл таблицу.

Пример использования
-------------------------

```python
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
gs.save_campaign_from_worksheet()
```

**Важно**: 

-  В примере кода комментарии `#gs.save_categories_from_worksheet(False)` предполагают, что данный код также может быть использован для сохранения информации о категориях в гугл таблицу, но в этом примере он не используется. 
-  `...` в конце кода означает, что здесь может быть продолжение кода, не показанное в примере.
-  `header` - неопределённый модуль, требуется уточнение его функционала.