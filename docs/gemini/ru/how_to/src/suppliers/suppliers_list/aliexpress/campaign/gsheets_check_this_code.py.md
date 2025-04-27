## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Класс `AliCampaignGoogleSheet` предоставляет инструменты для работы с таблицей Google Sheets, связанной с рекламными кампаниями AliExpress. 

Он наследует класс `SpreadSheet` и расширяет его функциональность для:

* Управления листами Google Sheets
* Записи данных о категориях и продуктах
* Форматирования листов

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте экземпляр `AliCampaignGoogleSheet`, передав в конструктор имя кампании, язык и валюту.
    - При инициализации класс создает новый экземпляр `AliCampaignEditor` для управления данными кампании, очищает существующую таблицу Google Sheets, создает листы для кампании, категорий и продукта, а также открывает таблицу в браузере Chrome.
2. **Очистка таблицы**:
    - Метод `clear()` очищает таблицу от всех листов, кроме "categories" и "product_template". 
    - Использует метод `delete_products_worksheets()` для удаления ненужных листов. 
3. **Запись данных**:
    - Используйте `set_campaign_worksheet()` для записи данных кампании в лист "campaign". 
    - Метод `set_products_worksheet()` записывает данные о продуктах в новый лист, соответствующий категории.
    - `set_categories_worksheet()` записывает данные о категориях в лист "categories".
4. **Форматирование**:
    - Используйте методы `_format_categories_worksheet()` и `_format_category_products_worksheet()` для форматирования листов "categories" и с продуктами категорий. 

Пример использования
-------------------------
```python
from src.suppliers.aliexpress.campaign.gsheets_check_this_code import AliCampaignGoogleSheet

# Инициализация экземпляра AliCampaignGoogleSheet с именем кампании, языком и валютой
campaign_gsheet = AliCampaignGoogleSheet(
    campaign_name="My Campaign",
    language="ru",
    currency="RUB"
)

# Запись данных о кампании
campaign_gsheet.set_campaign_worksheet(
    campaign=campaign_gsheet.editor.campaign
)

# Запись данных о категории
campaign_gsheet.set_categories_worksheet(
    categories=campaign_gsheet.editor.campaign.category
)

# Запись данных о продуктах
campaign_gsheet.set_products_worksheet(
    category_name="category_name"
)
```

**Дополнительные возможности**:

* Метод `get_categories()` позволяет извлечь данные о категориях из листа "categories" в виде списка словарей.
* Метод `set_category_products()` позволяет записать данные о продуктах в новый лист, соответствующий категории. 

**Важно**:

* Класс использует `logger` для записи сообщений о работе и ошибках.
* В коде используются дополнительные библиотеки, такие как `gspread` для работы с Google Sheets, `gspread_formatting` для форматирования, `webdriver` для управления браузером и `j_dumps` для сериализации данных в JSON.