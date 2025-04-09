# Модуль: Редактор рекламной кампании AliExpress через Google Sheets

## Обзор

Модуль предоставляет класс `AliCampaignGoogleSheet`, который используется для управления рекламными кампаниями AliExpress посредством Google Sheets. Он позволяет автоматизировать запись и форматирование данных о кампаниях, категориях и продуктах в Google Sheets, упрощая процесс редактирования и управления рекламными материалами.

## Подробнее

Этот модуль предоставляет инструменты для интеграции с Google Sheets, позволяя автоматически создавать листы, записывать данные и форматировать их в соответствии с требованиями рекламной кампании. Он упрощает взаимодействие с данными AliExpress, делая их более доступными и удобными для редактирования.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:

-   `spreadsheet_id` (str): Идентификатор Google Sheets таблицы.
-   `spreadsheet` (SpreadSheet): Экземпляр класса `SpreadSheet` для работы с Google Sheets.
-   `worksheet` (Worksheet): Экземпляр класса `Worksheet` для работы с конкретным листом Google Sheets.

**Методы**:

-   `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует экземпляр класса `AliCampaignGoogleSheet`.
-   `clear()`: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на других указанных листах.
-   `delete_products_worksheets()`: Удаляет все листы из Google Sheets, кроме листов с категориями и шаблонами продуктов.
-   `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании в лист Google Sheets.
-   `set_products_worksheet(category_name: str)`: Записывает данные о продуктах в лист Google Sheets.
-   `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях в лист Google Sheets.
-   `get_categories()`: Получает данные о категориях из Google Sheets.
-   `set_category_products(category_name: str, products: dict)`: Записывает данные о продуктах категории в Google Sheets.
-   `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист с категориями.
-   `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист с продуктами категории.

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """
    Args:
        campaign_name (str): Название кампании.
        language (str | dict, optional): Язык кампании. По умолчанию `None`.
        currency (str, optional): Валюта кампании. По умолчанию `None`.

    Raises:
        Exception: Если возникает ошибка при инициализации.
    """
```

**Назначение**: Инициализирует класс `AliCampaignGoogleSheet`, устанавливая идентификатор таблицы Google Sheets и вызывая конструктор родительского класса `SpreadSheet`.

**Параметры**:

-   `campaign_name` (str): Название кампании.
-   `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
-   `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

-   Вызывает конструктор родительского класса `SpreadSheet` с указанным `spreadsheet_id`.

### `clear`

```python
def clear(self):
    """
    Очищает содержимое Google Sheets.
    """
```

**Назначение**: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на листах категорий и других указанных листах.

**Как работает функция**:

1.  Вызывает метод `delete_products_worksheets()` для удаления листов продуктов.
2.  Ловит исключения, которые могут возникнуть при удалении листов, и логирует ошибки.

**Примеры**:

```python
sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
sheet.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """
    Удаляет все листы, кроме 'categories', 'product', 'category', 'campaign'.
    """
```

**Назначение**: Удаляет все листы из Google Sheets, кроме листов с названиями 'categories', 'product', 'category' и 'campaign'.

**Как работает функция**:

1.  Определяет список исключенных названий листов (`excluded_titles`).
2.  Получает список всех листов в Google Sheets.
3.  Перебирает листы и удаляет те, которые не входят в список исключенных.
4.  Ловит исключения, которые могут возникнуть при удалении листов, и логирует ошибки.

**Примеры**:

```python
sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
sheet.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """
    Args:
        campaign (SimpleNamespace): Объект SimpleNamespace с данными кампании.

    Raises:
        Exception: Если возникает ошибка при записи данных кампании.
    """
```

**Назначение**: Записывает данные кампании в лист Google Sheets с именем 'campaign'.

**Параметры**:

-   `campaign` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные кампании.

**Как работает функция**:

1.  Получает лист Google Sheets с именем 'campaign'.
2.  Формирует список операций обновления для записи данных кампании в вертикальном формате (столбец A - заголовки, столбец B - значения).
3.  Выполняет пакетное обновление листа Google Sheets с данными кампании.
4.  Ловит исключения, которые могут возникнуть при записи данных, и логирует ошибки.

**Примеры**:

```python
from types import SimpleNamespace

campaign_data = SimpleNamespace(
    campaign_name='Test Campaign',
    title='Test Title',
    language='en',
    currency='USD',
    description='Test Description'
)

sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
sheet.set_campaign_worksheet(campaign_data)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name: str):
    """
    Args:
        category_name (str): Имя категории.

    Raises:
        Exception: Если возникает ошибка при записи данных о продуктах.
    """
```

**Назначение**: Записывает данные о продуктах из указанной категории в лист Google Sheets.

**Параметры**:

-   `category_name` (str): Название категории, для которой нужно записать данные о продуктах.

**Как работает функция**:

1.  Копирует лист 'product' и переименовывает его в `category_name`.
2.  Извлекает данные о продуктах из атрибута `products` объекта категории.
3.  Формирует список строк с данными о продуктах для записи в Google Sheets.
4.  Обновляет лист Google Sheets данными о продуктах.
5.  Форматирует лист с использованием метода `_format_category_products_worksheet`.
6.  Ловит исключения, которые могут возникнуть при записи данных, и логирует ошибки.

**Примеры**:

```python
sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
sheet.set_products_worksheet(category_name='test_category')
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """
    Args:
        categories (SimpleNamespace): Объект SimpleNamespace с данными о категориях.

    Raises:
        Exception: Если возникает ошибка при записи данных о категориях.
    """
```

**Назначение**: Записывает данные о категориях из объекта `SimpleNamespace` в лист Google Sheets с именем 'categories'.

**Параметры**:

-   `categories` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные о категориях.

**Как работает функция**:

1.  Получает лист Google Sheets с именем 'categories'.
2.  Очищает лист Google Sheets.
3.  Извлекает данные о категориях из объекта `SimpleNamespace`.
4.  Формирует заголовки для таблицы категорий.
5.  Формирует список строк с данными о категориях для записи в Google Sheets.
6.  Обновляет лист Google Sheets данными о категориях.
7.  Форматирует лист с использованием метода `_format_categories_worksheet`.
8.  Ловит исключения, которые могут возникнуть при записи данных, и логирует ошибки.

**Примеры**:

```python
from types import SimpleNamespace

categories_data = SimpleNamespace()
categories_data.category1 = SimpleNamespace(name='Category 1', title='Title 1', description='Description 1', tags=['tag1', 'tag2'], products_count=10)
categories_data.category2 = SimpleNamespace(name='Category 2', title='Title 2', description='Description 2', tags=['tag3', 'tag4'], products_count=20)

sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
sheet.set_categories_worksheet(categories_data)
```

### `get_categories`

```python
def get_categories(self):
    """
    Returns:
        list[dict]: Данные о категориях в виде списка словарей.
    """
```

**Назначение**: Получает данные о категориях из листа Google Sheets с именем 'categories'.

**Возвращает**:

-   `list[dict]`: Список словарей, где каждый словарь представляет данные об одной категории.

**Как работает функция**:

1.  Получает лист Google Sheets с именем 'categories'.
2.  Извлекает все записи из листа.
3.  Логирует информацию об извлечении данных.
4.  Возвращает полученные данные.

**Примеры**:

```python
sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
categories = sheet.get_categories()
print(categories)
```

### `set_category_products`

```python
def set_category_products(self, category_name: str, products: dict):
    """
    Args:
        category_name (str): Название категории.
        products (dict): Словарь с данными о продуктах.

    Raises:
        Exception: Если возникает ошибка при записи данных о продуктах.
    """
```

**Назначение**: Записывает данные о продуктах в новую таблицу Google Sheets.

**Параметры**:

-   `category_name` (str): Название категории.
-   `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:

1.  Копирует лист 'product' и переименовывает его в `category_name`.
2.  Определяет заголовки для таблицы продуктов.
3.  Формирует список строк с данными о продуктах для записи в Google Sheets.
4.  Обновляет лист Google Sheets данными о продуктах.
5.  Форматирует лист с использованием метода `_format_category_products_worksheet`.
6.  Ловит исключения, которые могут возникнуть при записи данных, и логирует ошибки.

**Примеры**:

```python
products_data = [
    {'product_id': '1', 'app_sale_price': '10.00', 'original_price': '12.00', 'sale_price': '11.00', 'discount': '10%',
     'product_main_image_url': 'http://example.com/image1.jpg', 'local_image_path': '/path/to/image1.jpg',
     'product_small_image_urls': ['http://example.com/small_image1.jpg', 'http://example.com/small_image2.jpg'],
     'product_video_url': 'http://example.com/video1.mp4', 'local_video_path': '/path/to/video1.mp4',
     'first_level_category_id': '1001', 'first_level_category_name': 'Category 1',
     'second_level_category_id': '2001', 'second_level_category_name': 'Subcategory 1',
     'target_sale_price': '10.50', 'target_sale_price_currency': 'USD',
     'target_app_sale_price_currency': 'USD', 'target_original_price_currency': 'USD',
     'original_price_currency': 'USD', 'product_title': 'Product Title 1', 'evaluate_rate': '4.5',
     'promotion_link': 'http://example.com/promotion1', 'shop_url': 'http://example.com/shop1', 'shop_id': 'Shop123',
     'tags': ['tag1', 'tag2']},
    {'product_id': '2', 'app_sale_price': '20.00', 'original_price': '24.00', 'sale_price': '22.00', 'discount': '8%',
     'product_main_image_url': 'http://example.com/image2.jpg', 'local_image_path': '/path/to/image2.jpg',
     'product_small_image_urls': ['http://example.com/small_image3.jpg', 'http://example.com/small_image4.jpg'],
     'product_video_url': 'http://example.com/video2.mp4', 'local_video_path': '/path/to/video2.mp4',
     'first_level_category_id': '1002', 'first_level_category_name': 'Category 2',
     'second_level_category_id': '2002', 'second_level_category_name': 'Subcategory 2',
     'target_sale_price': '21.00', 'target_sale_price_currency': 'USD',
     'target_app_sale_price_currency': 'USD', 'target_original_price_currency': 'USD',
     'original_price_currency': 'USD', 'product_title': 'Product Title 2', 'evaluate_rate': '4.7',
     'promotion_link': 'http://example.com/promotion2', 'shop_url': 'http://example.com/shop2', 'shop_id': 'Shop456',
     'tags': ['tag3', 'tag4']}
]

sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
sheet.set_category_products(category_name='test_category', products=products_data)
```

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(self, ws: Worksheet):
    """
    Args:
        ws (Worksheet): Лист Google Sheets для форматирования.

    Raises:
        Exception: Если возникает ошибка при форматировании листа.
    """
```

**Назначение**: Форматирует лист Google Sheets с категориями, устанавливая ширину столбцов, высоту строк и форматирование заголовков.

**Параметры**:

-   `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1.  Устанавливает ширину столбцов A, B, C, D и E.
2.  Устанавливает высоту первой строки (заголовки).
3.  Определяет формат заголовков (жирный шрифт, размер 12, выравнивание по центру, серый фон).
4.  Применяет формат к диапазону ячеек A1:E1 (заголовки).
5.  Ловит исключения, которые могут возникнуть при форматировании, и логирует ошибки.

**Примеры**:

```python
sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
ws = sheet.get_worksheet('categories')
sheet._format_categories_worksheet(ws)
```

### `_format_category_products_worksheet`

```python
def _format_category_products_worksheet(self, ws: Worksheet):
    """
    Args:
        ws (Worksheet): Лист Google Sheets для форматирования.

    Raises:
        Exception: Если возникает ошибка при форматировании листа.
    """
```

**Назначение**: Форматирует лист Google Sheets с продуктами категории, устанавливая ширину столбцов, высоту строк и форматирование заголовков.

**Параметры**:

-   `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1.  Устанавливает ширину столбцов от A до Y.
2.  Устанавливает высоту первой строки (заголовки).
3.  Определяет формат заголовков (жирный шрифт, размер 12, выравнивание по центру, серый фон).
4.  Применяет формат к диапазону ячеек A1:Y1 (заголовки).
5.  Ловит исключения, которые могут возникнуть при форматировании, и логирует ошибки.

**Примеры**:

```python
sheet = AliCampaignGoogleSheet(campaign_name='test_campaign')
ws = sheet.get_worksheet('test_category')
sheet._format_category_products_worksheet(ws)