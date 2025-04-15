# Модуль для работы с Google Sheets в кампаниях AliExpress
## Обзор

Модуль `gsheets_check_this_code.py` предназначен для интеграции с Google Sheets в рамках управления рекламными кампаниями на AliExpress. Он предоставляет функциональность для чтения и записи данных о кампаниях, категориях и продуктах, а также для форматирования листов Google Sheets в соответствии с потребностями кампании.

## Подробнее

Модуль содержит класс `AliCampaignGoogleSheet`, который наследует класс `SpreadSheet` из модуля `src.goog.spreadsheet.spreadsheet`. Этот класс предоставляет методы для автоматизации работы с Google Sheets, включая создание, удаление и форматирование листов, а также запись данных о категориях и продуктах.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**:

- `SpreadSheet` из модуля `src.goog.spreadsheet.spreadsheet`.

**Атрибуты**:

- `spreadsheet_id` (str): Идентификатор Google Sheets spreadsheet.
- `spreadsheet` (SpreadSheet): Объект SpreadSheet для работы с Google Sheets.
- `worksheet` (Worksheet): Объект Worksheet для работы с конкретным листом Google Sheets.
- `driver` (Driver): Драйвер для управления браузером (например, Chrome) для доступа к Google Sheets.
- `editor` (AliCampaignEditor): Объект AliCampaignEditor для редактирования кампании AliExpress.

**Методы**:

- `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализация класса `AliCampaignGoogleSheet` с указанным идентификатором Google Sheets spreadsheet и дополнительными параметрами.
- `clear()`: Очистка содержимого Google Sheets, удаление листов продуктов и очистка данных на листах категорий и других указанных листах.
- `delete_products_worksheets()`: Удаление всех листов из Google Sheets spreadsheet, кроме 'categories', 'product', 'category' и 'campaign'.
- `set_campaign_worksheet(campaign: SimpleNamespace)`: Запись данных о кампании в Google Sheets worksheet.
- `set_products_worksheet(category_name: str)`: Запись данных из списка объектов SimpleNamespace в ячейки Google Sheets.
- `set_categories_worksheet(categories: SimpleNamespace)`: Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.
- `get_categories()`: Получение данных из таблицы Google Sheets.
- `set_category_products(category_name: str, products: dict)`: Запись данных о продуктах в новую таблицу Google Sheets.
- `_format_categories_worksheet(ws: Worksheet)`: Форматирование листа 'categories'.
- `_format_category_products_worksheet(ws: Worksheet)`: Форматирование листа с продуктами категории.

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """ Инициализация AliCampaignGoogleSheet с указанным Google Sheets spreadsheet ID и дополнительными параметрами.
    Args:
        campaign_name (str): Имя кампании.
        language (str | dict, optional): Язык для кампании. По умолчанию None.
        currency (str, optional): Валюта для кампании. По умолчанию None.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `AliCampaignGoogleSheet`.

**Параметры**:

- `campaign_name` (str): Имя кампании.
- `language` (str | dict, optional): Язык кампании. Может быть строкой или словарем. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:

- Вызывает конструктор родительского класса `SpreadSheet` с идентификатором spreadsheet.
- Создает экземпляр класса `AliCampaignEditor` для редактирования кампании.
- Вызывает методы для очистки листов, установки листов для кампании и категорий.
- Открывает URL Google Sheets в браузере с использованием драйвера.

**Примеры**:

```python
campaign_sheet = AliCampaignGoogleSheet(campaign_name='TestCampaign', language='en', currency='USD')
```

### `clear`

```python
def clear(self):
    """ Clear contents.
    Delete product sheets and clear data on the categories and other specified sheets.
    """
    ...
```

**Назначение**: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на листах категорий и других указанных листах.

**Как работает функция**:

- Вызывает метод `delete_products_worksheets` для удаления листов продуктов.
- Ловит исключения, возникающие в процессе очистки, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """ Delete all sheets from the Google Sheets spreadsheet except 'categories' and 'product_template'.
    """
    ...
```

**Назначение**: Удаляет все листы из Google Sheets spreadsheet, кроме 'categories', 'product', 'category' и 'campaign'.

**Как работает функция**:

- Получает список всех листов в spreadsheet.
- Перебирает листы и удаляет те, которые не входят в список исключенных ('categories', 'product', 'category', 'campaign').
- Логирует информацию об удаленных листах.
- Ловит исключения, возникающие в процессе удаления, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """ Write campaign data to a Google Sheets worksheet.
    Args:
        campaign (SimpleNamespace | str): SimpleNamespace object with campaign data fields for writing.
    """
    ...
```

**Назначение**: Записывает данные о кампании в Google Sheets worksheet.

**Параметры**:

- `campaign` (SimpleNamespace): Объект SimpleNamespace с данными о кампании.

**Как работает функция**:

- Получает worksheet 'campaign'.
- Готовит данные для вертикальной записи в worksheet.
- Обновляет ячейки worksheet данными о кампании.
- Логирует информацию о записи данных.
- Ловит исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
campaign_data = SimpleNamespace(name='TestCampaign', title='Test Title', language='en', currency='USD', description='Test Description')
campaign_sheet.set_campaign_worksheet(campaign_data)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name: str):
    """ Write data from a list of SimpleNamespace objects to Google Sheets cells.
    Args:
        category_name (str): The name of the category to fetch products from.
    """
    ...
```

**Назначение**: Записывает данные о продуктах из указанной категории в Google Sheets.

**Параметры**:

- `category_name` (str): Название категории, продукты из которой нужно записать.

**Как работает функция**:

- Получает данные о продуктах из указанной категории.
- Копирует worksheet 'product' и переименовывает его в название категории.
- Записывает данные о продуктах в worksheet.
- Форматирует worksheet.
- Логирует информацию о записи данных.
- Ловит исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.set_products_worksheet(category_name='Category1')
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """ Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.
    Args:
        categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
    """
    ...
```

**Назначение**: Записывает данные о категориях из объекта `SimpleNamespace` в Google Sheets.

**Параметры**:

- `categories` (`SimpleNamespace`): Объект, содержащий данные о категориях.

**Как работает функция**:

1.  Получает worksheet с именем `categories`.
2.  Очищает worksheet перед записью данных.
3.  Извлекает данные о категориях из объекта `SimpleNamespace`.
4.  Проверяет, что все объекты категорий имеют необходимые атрибуты (`name`, `title`, `description`, `tags`, `products_count`).
5.  Записывает заголовки таблицы (`Name`, `Title`, `Description`, `Tags`, `Products Count`).
6.  Записывает данные о категориях в worksheet.
7.  Вызывает метод `_format_categories_worksheet` для форматирования таблицы.
8.  Логирует информацию о записи данных.
9.  Ловит исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
categories_data = SimpleNamespace(
    Category1=SimpleNamespace(name='Category1', title='Category 1 Title', description='Category 1 Description', tags=['tag1', 'tag2'], products_count=10),
    Category2=SimpleNamespace(name='Category2', title='Category 2 Title', description='Category 2 Description', tags=['tag3', 'tag4'], products_count=20)
)
campaign_sheet.set_categories_worksheet(categories_data)
```

### `get_categories`

```python
def get_categories(self):
    """ Получение данных из таблицы Google Sheets.
    @return Данные из таблицы в виде списка словарей.
    """
    ...
```

**Назначение**: Получает данные из таблицы Google Sheets.

**Возвращает**:

- `data` (list[dict]): Список словарей, представляющих данные из таблицы.

**Как работает функция**:

1.  Получает worksheet с именем `categories`.
2.  Извлекает все записи из worksheet.
3.  Логирует информацию о получении данных.
4.  Возвращает полученные данные.

**Примеры**:

```python
categories = campaign_sheet.get_categories()
print(categories)
```

### `set_category_products`

```python
def set_category_products(self, category_name: str, products: dict):
    """ Запись данных о продуктах в новую таблицу Google Sheets.
    Args:
        category_name Название категории.
        products Словарь с данными о продуктах.
    """
    ...
```

**Назначение**: Записывает данные о продуктах в новую таблицу Google Sheets.

**Параметры**:

- `category_name` (str): Название категории.
- `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:

1.  Проверяет, что указано имя категории.
2.  Получает данные о продуктах из указанной категории.
3.  Копирует worksheet с именем `product` и переименовывает его в имя категории.
4.  Определяет заголовки для таблицы продуктов.
5.  Записывает данные о продуктах в worksheet.
6.  Форматирует worksheet.
7.  Логирует информацию о записи данных.
8.  Ловит исключения, возникающие в процессе записи, и логирует ошибки.

**Примеры**:

```python
products_data = [
    {'product_id': '123', 'app_sale_price': '10.00', 'original_price': '12.00', 'sale_price': '11.00', 'discount': '10%', 'product_title': 'Product 1'},
    {'product_id': '456', 'app_sale_price': '20.00', 'original_price': '22.00', 'sale_price': '21.00', 'discount': '5%', 'product_title': 'Product 2'}
]
campaign_sheet.set_category_products(category_name='Category1', products=products_data)
```

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(self, ws: Worksheet):
    """ Форматирование листа 'categories'.
    Args:
        ws Лист Google Sheets для форматирования.
    """
    ...
```

**Назначение**: Форматирует лист 'categories' в Google Sheets.

**Параметры**:

- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1.  Устанавливает ширину столбцов (`A:A`, `B:B`, `C:C`, `D:D`, `E:E`).
2.  Устанавливает высоту строки заголовков (`1:1`).
3.  Определяет формат заголовков (жирный шрифт, размер 12, выравнивание по центру, вертикальное выравнивание по середине, цвет фона).
4.  Применяет формат заголовков к диапазону ячеек `A1:E1`.
5.  Логирует информацию о форматировании worksheet.
6.  Ловит исключения, возникающие в процессе форматирования, и логирует ошибки.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('categories')
campaign_sheet._format_categories_worksheet(ws)
```

### `_format_category_products_worksheet`

```python
def _format_category_products_worksheet(self, ws: Worksheet):
    """ Форматирование листа с продуктами категории.
    Args:
        ws Лист Google Sheets для форматирования.
    """
    ...
```

**Назначение**: Форматирует лист с продуктами категории в Google Sheets.

**Параметры**:

- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:

1.  Устанавливает ширину столбцов (`A:A` - `Y:Y`).
2.  Устанавливает высоту строки заголовков (`1:1`).
3.  Определяет формат заголовков (жирный шрифт, размер 12, выравнивание по центру, вертикальное выравнивание по верхнему краю, цвет фона).
4.  Применяет формат заголовков к диапазону ячеек `A1:Y1`.
5.  Логирует информацию о форматировании worksheet.
6.  Ловит исключения, возникающие в процессе форматирования, и логирует ошибки.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('Category1')
campaign_sheet._format_category_products_worksheet(ws)
```