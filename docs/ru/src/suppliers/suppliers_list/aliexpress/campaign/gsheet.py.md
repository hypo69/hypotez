# Модуль: `aliexpress.campaign.gsheet`

## Обзор

Модуль предназначен для работы с Google Sheets в рамках рекламных кампаний AliExpress. Он предоставляет инструменты для создания, редактирования и форматирования Google Sheets, используемых для управления данными кампаний, категориями товаров и информацией о товарах.

## Подробней

Модуль содержит класс `AliCampaignGoogleSheet`, который наследует функциональность базового класса `SpreadSheet` и добавляет специфические методы для работы с данными AliExpress. Он позволяет автоматизировать запись и чтение данных из Google Sheets, упрощая процесс управления рекламными кампаниями. В частности, реализована поддержка записи данных о кампаниях, категориях и товарах, а также форматирование листов для улучшения читаемости и удобства работы.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**:
- `SpreadSheet`: Предоставляет базовую функциональность для работы с Google Sheets.

**Атрибуты**:
- `spreadsheet_id` (str): ID таблицы Google Sheets, используемой для кампании AliExpress.
- `spreadsheet` (SpreadSheet): Экземпляр класса `SpreadSheet` для работы с Google Sheets.
- `worksheet` (Worksheet): Текущий рабочий лист Google Sheets.

**Методы**:
- `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует экземпляр класса `AliCampaignGoogleSheet`.
- `clear()`: Очищает содержимое листов Google Sheets, используемых для кампании.
- `delete_products_worksheets()`: Удаляет все листы, кроме 'categories', 'product', 'category', 'campaign'.
- `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании в лист Google Sheets.
- `set_products_worksheet(category_name: str)`: Записывает данные о товарах категории в лист Google Sheets.
- `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях в лист Google Sheets.
- `get_categories()`: Получает данные о категориях из листа Google Sheets.
- `set_category_products(category_name: str, products: dict)`: Записывает данные о товарах для указанной категории в Google Sheets.
- `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист Google Sheets с категориями.
- `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист Google Sheets с товарами категории.

## Методы класса

### `__init__`

```python
def __init__(campaign_name: str, language: str | dict = None, currency: str = None):
    """ Инициализация AliCampaignGoogleSheet с указанным ID Google Sheets и дополнительными параметрами.
    Args:
        campaign_name (str): Название кампании.
        language (str | dict, optional): Язык для кампании. По умолчанию None.
        currency (str, optional): Валюта для кампании. По умолчанию None.
    """
```

**Назначение**: Инициализирует экземпляр класса `AliCampaignGoogleSheet` с указанными параметрами.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (str | dict, optional): Язык для кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта для кампании. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор базового класса `SpreadSheet`, передавая `spreadsheet_id`.
- Инициализирует атрибуты `campaign_name`, `language` и `currency`.

**Примеры**:

```python
campaign_sheet = AliCampaignGoogleSheet(campaign_name='SummerSale', language='en', currency='USD')
```

### `clear`

```python
def clear():
    """ Очистка содержимого.
    Удаляет листы товаров и очищает данные на листах категорий и других указанных листах.
    """
```

**Назначение**: Очищает содержимое листов Google Sheets, используемых для кампании.

**Как работает функция**:
- Вызывает метод `delete_products_worksheets()` для удаления листов товаров.
- Обрабатывает исключения, возникающие в процессе очистки, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets():
    """ Удаляет все листы из таблицы Google Sheets, кроме 'categories', 'product', 'category', 'campaign'.
    """
```

**Назначение**: Удаляет все листы из Google Sheets, кроме листов с категориями и шаблонами товаров.

**Как работает функция**:
- Получает список всех листов в Google Sheets.
- Итерируется по листам и удаляет каждый лист, если его название не входит в список исключений (`excluded_titles`).
- Логирует успешное удаление каждого листа.
- Обрабатывает исключения, возникающие в процессе удаления, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(campaign: SimpleNamespace):
    """ Записывает данные кампании в лист Google Sheets.
    Args:
        campaign (SimpleNamespace): Объект SimpleNamespace с полями данных кампании для записи.
    """
```

**Назначение**: Записывает данные кампании в лист Google Sheets.

**Параметры**:
- `campaign` (SimpleNamespace): Объект `SimpleNamespace` с данными кампании для записи.

**Как работает функция**:
- Получает рабочий лист с названием 'campaign'.
- Формирует список операций обновления для записи данных кампании в вертикальном формате.
- Выполняет пакетное обновление листа Google Sheets с данными кампании.
- Логирует успешную запись данных кампании.
- Обрабатывает исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
campaign_data = SimpleNamespace(
    campaign_name='SummerSale',
    title='Летняя распродажа',
    language='ru',
    currency='RUB',
    description='Большая летняя распродажа!'
)
campaign_sheet.set_campaign_worksheet(campaign_data)
```

### `set_products_worksheet`

```python
def set_products_worksheet(category_name: str):
    """ Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.
    Args:
        category_name (str): Название категории для получения товаров.
    """
```

**Назначение**: Записывает данные о товарах категории в лист Google Sheets.

**Параметры**:
- `category_name` (str): Название категории, товары которой нужно записать в лист.

**Как работает функция**:
- Копирует лист 'product' и переименовывает его в название категории.
- Итерируется по списку товаров и записывает данные каждого товара в отдельную строку листа Google Sheets.
- Форматирует лист с товарами категории.
- Логирует успешную запись данных о товарах.
- Обрабатывает исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.set_products_worksheet(category_name='Electronics')
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(categories: SimpleNamespace):
    """ Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.
    Args:
        categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
    """
```

**Назначение**: Записывает данные о категориях в лист Google Sheets.

**Параметры**:
- `categories` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные о категориях.

**Как работает функция**:
- Получает рабочий лист с названием 'categories'.
- Очищает рабочий лист перед записью данных.
- Итерируется по категориям и записывает данные каждой категории в отдельную строку листа Google Sheets.
- Форматирует лист с категориями.
- Логирует успешную запись данных о категориях.
- Обрабатывает исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
categories_data = SimpleNamespace(
    Category1=SimpleNamespace(name='Category1', title='Категория 1', description='Описание 1', tags=['tag1', 'tag2'], products_count=10),
    Category2=SimpleNamespace(name='Category2', title='Категория 2', description='Описание 2', tags=['tag3', 'tag4'], products_count=20)
)
campaign_sheet.set_categories_worksheet(categories_data)
```

### `get_categories`

```python
def get_categories():
    """ Получение данных из таблицы Google Sheets.
    Returns:
        Данные из таблицы в виде списка словарей.
    """
```

**Назначение**: Получает данные о категориях из листа Google Sheets.

**Возвращает**:
- `list[dict]`: Список словарей, представляющих данные о категориях.

**Как работает функция**:
- Получает рабочий лист с названием 'categories'.
- Извлекает все записи из листа Google Sheets.
- Логирует успешное получение данных о категориях.
- Возвращает полученные данные.

**Примеры**:

```python
categories = campaign_sheet.get_categories()
```

### `set_category_products`

```python
def set_category_products(category_name: str, products: dict):
    """ Запись данных о товарах в новую таблицу Google Sheets.
    Args:
        category_name Название категории.
        products Словарь с данными о товарах.
    """
```

**Назначение**: Записывает данные о товарах для указанной категории в Google Sheets.

**Параметры**:
- `category_name` (str): Название категории.
- `products` (dict): Словарь с данными о товарах.

**Как работает функция**:
- Копирует лист 'product' и переименовывает его в название категории.
- Формирует заголовки для таблицы товаров.
- Итерируется по списку товаров и записывает данные каждого товара в отдельную строку листа Google Sheets.
- Форматирует лист с товарами категории.
- Логирует успешную запись данных о товарах.
- Обрабатывает исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
products_data = [
    {'product_id': '1', 'app_sale_price': '10.00', 'original_price': '12.00', 'sale_price': '11.00', 'discount': '0.09',
     'product_main_image_url': 'url1', 'local_image_path': 'path1', 'product_small_image_urls': [],
     'product_video_url': 'url2', 'local_video_path': 'path2', 'first_level_category_id': '100',
     'first_level_category_name': 'Category1', 'second_level_category_id': '200', 'second_level_category_name': 'Subcategory1',
     'target_sale_price': '9.00', 'target_sale_price_currency': 'USD', 'target_app_sale_price_currency': 'USD',
     'target_original_price_currency': 'USD', 'original_price_currency': 'USD', 'product_title': 'Product1',
     'evaluate_rate': '4.5', 'promotion_link': 'link1', 'shop_url': 'shop_url1', 'shop_id': 'shop_id1', 'tags': []},
    {'product_id': '2', 'app_sale_price': '20.00', 'original_price': '24.00', 'sale_price': '22.00', 'discount': '0.08',
     'product_main_image_url': 'url3', 'local_image_path': 'path3', 'product_small_image_urls': [],
     'product_video_url': 'url4', 'local_video_path': 'path4', 'first_level_category_id': '100',
     'first_level_category_name': 'Category1', 'second_level_category_id': '200', 'second_level_category_name': 'Subcategory1',
     'target_sale_price': '18.00', 'target_sale_price_currency': 'USD', 'target_app_sale_price_currency': 'USD',
     'target_original_price_currency': 'USD', 'original_price_currency': 'USD', 'product_title': 'Product2',
     'evaluate_rate': '4.7', 'promotion_link': 'link2', 'shop_url': 'shop_url2', 'shop_id': 'shop_id2', 'tags': []}
]
campaign_sheet.set_category_products(category_name='Electronics', products=products_data)
```

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(ws: Worksheet):
    """ Форматирование листа 'categories'.
    Args:
        ws Лист Google Sheets для форматирования.
    """
```

**Назначение**: Форматирует лист Google Sheets с категориями.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
- Устанавливает ширину столбцов для различных атрибутов категорий.
- Устанавливает высоту строк для заголовков.
- Форматирует заголовки, делая их жирными, центрированными и с серым фоном.
- Логирует успешное форматирование листа категорий.
- Обрабатывает исключения, возникающие в процессе форматирования, и логирует ошибки.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('categories')
campaign_sheet._format_categories_worksheet(ws)
```

### `_format_category_products_worksheet`

```python
def _format_category_products_worksheet(ws: Worksheet):
    """ Форматирование листа с товарами категории.
    Args:
        ws Лист Google Sheets для форматирования.
    """
```

**Назначение**: Форматирует лист Google Sheets с товарами категории.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
- Устанавливает ширину столбцов для различных атрибутов товаров.
- Устанавливает высоту строк для заголовков.
- Форматирует заголовки, делая их жирными, центрированными и с серым фоном.
- Логирует успешное форматирование листа товаров категории.
- Обрабатывает исключения, возникающие в процессе форматирования, и логирует ошибки.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('Electronics')
campaign_sheet._format_category_products_worksheet(ws)