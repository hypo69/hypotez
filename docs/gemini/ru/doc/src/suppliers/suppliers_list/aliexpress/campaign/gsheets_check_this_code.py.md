# Модуль `AliCampaignGoogleSheet`

## Обзор

Модуль `AliCampaignGoogleSheet` предоставляет функциональность для работы с Google Sheets в рамках кампаний AliExpress. 

## Подробнее

Модуль предоставляет класс `AliCampaignGoogleSheet`, который наследует класс `SpreadSheet`. 
Класс предоставляет методы для управления листами Google Sheets, записи данных о категориях и продуктах, и форматирования листов.

## Классы

### `class AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:

- `spreadsheet_id` (`str`): Идентификатор Google Sheets таблицы (ID).
- `spreadsheet` (`SpreadSheet`): Объект `SpreadSheet`, предоставляющий доступ к Google Sheets таблице.
- `worksheet` (`Worksheet`): Объект `Worksheet`, предоставляющий доступ к рабочему листу Google Sheets.
- `driver` (`Driver`): Объект `Driver` (вебдрайвер), используемый для взаимодействия с Google Sheets.

**Методы**:

- `__init__(self, campaign_name: str, language: str | dict = None, currency: str = None)`: 
    **Назначение**: Инициализирует объект `AliCampaignGoogleSheet` с указанным идентификатором таблицы Google Sheets и дополнительными параметрами.
    **Параметры**:
        - `campaign_name` (`str`): Название кампании.
        - `language` (`str` | `dict`, optional): Язык кампании. По умолчанию `None`.
        - `currency` (`str`, optional): Валюта кампании. По умолчанию `None`.
    **Возвращает**: None
    **Вызывает исключения**: None
    **Примеры**:
        ```python
        # Создание экземпляра класса AliCampaignGoogleSheet
        google_sheet = AliCampaignGoogleSheet(campaign_name='My Campaign', language='ru', currency='USD')
        ```
- `clear(self)`:
    **Назначение**: Очищает содержимое таблицы Google Sheets. Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
    **Параметры**: None
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при очистке.
    **Примеры**:
        ```python
        # Очистка таблицы
        google_sheet.clear()
        ```
- `delete_products_worksheets(self)`:
    **Назначение**: Удаляет все листы из таблицы Google Sheets, кроме `'categories'`, `'product'`, `'category'` и `'campaign'`.
    **Параметры**: None
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при удалении листов.
    **Примеры**:
        ```python
        # Удаление всех листов продуктов
        google_sheet.delete_products_worksheets()
        ```
- `set_campaign_worksheet(self, campaign: SimpleNamespace)`:
    **Назначение**: Записывает данные кампании в рабочий лист Google Sheets.
    **Параметры**:
        - `campaign` (`SimpleNamespace | str`): Объект `SimpleNamespace` с данными кампании для записи.
        - `language` (`str`, optional): Язык кампании. По умолчанию `None`.
        - `currency` (`str`, optional): Валюта кампании. По умолчанию `None`.
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при записи данных в рабочий лист.
    **Примеры**:
        ```python
        # Запись данных кампании в рабочий лист
        google_sheet.set_campaign_worksheet(campaign)
        ```
- `set_products_worksheet(self, category_name: str)`:
    **Назначение**: Записывает данные из списка объектов `SimpleNamespace` в ячейки Google Sheets.
    **Параметры**:
        - `category_name` (`str`): Название категории, из которой нужно получить продукты.
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при записи данных в рабочий лист.
    **Примеры**:
        ```python
        # Запись данных продуктов в рабочий лист
        google_sheet.set_products_worksheet('Electronics')
        ```
- `set_categories_worksheet(self, categories: SimpleNamespace)`:
    **Назначение**: Записывает данные из объекта `SimpleNamespace` с категориями в ячейки Google Sheets.
    **Параметры**:
        - `categories` (`SimpleNamespace`): Объект, где ключи — это категории с данными для записи.
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при записи данных в рабочий лист.
    **Примеры**:
        ```python
        # Запись данных категорий в рабочий лист
        google_sheet.set_categories_worksheet(categories)
        ```
- `get_categories(self)`:
    **Назначение**: Получение данных из таблицы Google Sheets.
    **Параметры**: None
    **Возвращает**: Список словарей с данными из таблицы.
    **Вызывает исключения**: `Exception`: Если возникает ошибка при получении данных из таблицы.
    **Примеры**:
        ```python
        # Получение данных о категориях
        categories_data = google_sheet.get_categories()
        ```
- `set_category_products(self, category_name: str, products: dict)`:
    **Назначение**: Запись данных о продуктах в новую таблицу Google Sheets.
    **Параметры**:
        - `category_name` (`str`): Название категории.
        - `products` (`dict`): Словарь с данными о продуктах.
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при записи данных в рабочий лист.
    **Примеры**:
        ```python
        # Запись данных о продуктах в рабочий лист
        google_sheet.set_category_products('Electronics', products)
        ```
- `_format_categories_worksheet(self, ws: Worksheet)`:
    **Назначение**: Форматирование листа `'categories'`.
    **Параметры**:
        - `ws` (`Worksheet`): Рабочий лист Google Sheets для форматирования.
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при форматировании рабочего листа.
    **Примеры**:
        ```python
        # Форматирование рабочего листа 'categories'
        google_sheet._format_categories_worksheet(ws)
        ```
- `_format_category_products_worksheet(self, ws: Worksheet)`:
    **Назначение**: Форматирование листа с продуктами категории.
    **Параметры**:
        - `ws` (`Worksheet`): Рабочий лист Google Sheets для форматирования.
    **Возвращает**: None
    **Вызывает исключения**: `Exception`: Если возникает ошибка при форматировании рабочего листа.
    **Примеры**:
        ```python
        # Форматирование рабочего листа с продуктами
        google_sheet._format_category_products_worksheet(ws)
        ```


## Примеры

```python
# Пример использования модуля AliCampaignGoogleSheet

from src.suppliers.aliexpress.campaign.gsheets_check_this_code import AliCampaignGoogleSheet

# Создание экземпляра класса AliCampaignGoogleSheet
google_sheet = AliCampaignGoogleSheet(campaign_name='My Campaign', language='ru', currency='USD')

# Очистка таблицы
google_sheet.clear()

# Запись данных кампании в рабочий лист
google_sheet.set_campaign_worksheet(campaign)

# Запись данных продуктов в рабочий лист
google_sheet.set_products_worksheet('Electronics')

# Запись данных категорий в рабочий лист
google_sheet.set_categories_worksheet(categories)

# Получение данных о категориях
categories_data = google_sheet.get_categories()

# Запись данных о продуктах в рабочий лист
google_sheet.set_category_products('Electronics', products)

# Форматирование рабочего листа 'categories'
google_sheet._format_categories_worksheet(ws)

# Форматирование рабочего листа с продуктами
google_sheet._format_category_products_worksheet(ws)
```

## Параметры класса

- `spreadsheet_id` (`str`): Идентификатор Google Sheets таблицы (ID).
- `spreadsheet` (`SpreadSheet`): Объект `SpreadSheet`, предоставляющий доступ к Google Sheets таблице.
- `worksheet` (`Worksheet`): Объект `Worksheet`, предоставляющий доступ к рабочему листу Google Sheets.
- `driver` (`Driver`): Объект `Driver` (вебдрайвер), используемый для взаимодействия с Google Sheets.
- `editor` (`AliCampaignEditor`): Объект `AliCampaignEditor`, используемый для управления данными кампании AliExpress.


## Дополнительные сведения

- В коде используется вебдрайвер `Driver` из модуля `src.webdriver.driver`. 
- Модуль использует библиотеку `gspread` для взаимодействия с Google Sheets. 
- Модуль использует библиотеку `gspread_formatting` для форматирования листов Google Sheets.
- Модуль использует библиотеку `src.utils.jjson` для обработки JSON-данных.
- Модуль использует библиотеку `src.utils.printer` для вывода данных в консоль.
- Модуль использует библиотеку `src.logger.logger` для логгирования.
- Модуль использует библиотеку `src.llm.openai` для работы с моделью OpenAI.


```markdown