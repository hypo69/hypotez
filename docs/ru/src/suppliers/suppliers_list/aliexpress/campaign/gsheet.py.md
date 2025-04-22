# Модуль `gsheet.py`

## Обзор

Модуль `gsheet.py` предназначен для работы с Google Sheets в контексте управления рекламными кампаниями на AliExpress. Он предоставляет функциональность для чтения, записи и форматирования данных кампаний и категорий товаров в Google Sheets. Модуль включает в себя класс `AliCampaignGoogleSheet`, который наследует класс `SpreadSheet` и расширяет его возможности для работы с данными AliExpress.

## Подробнее

Модуль обеспечивает интеграцию с Google Sheets для автоматизации процессов управления рекламными кампаниями, таких как обновление информации о кампаниях, категориях и продуктах. Он использует библиотеку `gspread` для взаимодействия с Google Sheets API.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс `AliCampaignGoogleSheet` предназначен для работы с Google Sheets в рамках кампаний AliExpress. Он наследует класс `SpreadSheet` и предоставляет дополнительные методы для управления листами Google Sheets, записи данных о категориях и продуктах, и форматирования листов.

**Наследует**:
- `SpreadSheet`

**Атрибуты**:
- `spreadsheet_id` (str): Идентификатор Google Sheets таблицы.
- `spreadsheet` (SpreadSheet): Объект SpreadSheet для работы с Google Sheets.
- `worksheet` (Worksheet): Объект Worksheet для работы с листом Google Sheets.

**Методы**:
- `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует объект `AliCampaignGoogleSheet` с указанным идентификатором Google Sheets и дополнительными параметрами.
- `clear()`: Очищает содержимое листов, удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
- `delete_products_worksheets()`: Удаляет все листы из Google Sheets, кроме листов 'categories', 'product', 'category' и 'campaign'.
- `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании в лист Google Sheets.
- `set_products_worksheet(category_name: str)`: Записывает данные о продуктах в лист Google Sheets.
- `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях в лист Google Sheets.
- `get_categories()`: Получает данные о категориях из листа Google Sheets.
- `set_category_products(category_name: str, products: dict)`: Записывает данные о продуктах категории в лист Google Sheets.
- `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист 'categories' в Google Sheets.
- `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист с продуктами категории в Google Sheets.

## Методы класса

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """ Инициализация AliCampaignGoogleSheet с указанным идентификатором Google Sheets и дополнительными параметрами.

    Args:
        campaign_name (str): Название кампании.
        language (str | dict, optional): Язык кампании. По умолчанию None.
        currency (str, optional): Валюта кампании. По умолчанию None.
    """
```

**Назначение**:
Инициализирует класс `AliCampaignGoogleSheet`, устанавливая идентификатор таблицы Google Sheets и дополнительные параметры, такие как название кампании, язык и валюта.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `SpreadSheet`, передавая `spreadsheet_id`.
- Сохраняет значения параметров `campaign_name`, `language` и `currency` для дальнейшего использования.

**Примеры**:

```python
campaign_sheet = AliCampaignGoogleSheet(campaign_name='TestCampaign', language='ru', currency='USD')
```

### `clear`

```python
def clear(self):
    """ Очистка содержимого.

    Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
    """
```

**Назначение**:
Метод `clear` предназначен для очистки данных в Google Sheets, связанных с рекламной кампанией. Он удаляет листы продуктов и очищает данные на листах категорий.

**Как работает функция**:
- Вызывает метод `delete_products_worksheets` для удаления листов продуктов.
- Обрабатывает исключения, возникающие при очистке, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """ Удаление всех листов из Google Sheets, кроме 'categories', 'product', 'category' и 'campaign'.
    """
```

**Назначение**:
Удаляет все листы из Google Sheets, связанные с продуктами, за исключением листов 'categories', 'product', 'category' и 'campaign'.

**Как работает функция**:
- Получает список всех листов в Google Sheets.
- Итерируется по листам и удаляет те, у которых заголовок не входит в список исключенных (`excluded_titles`).
- Логирует успешное удаление каждого листа.
- Обрабатывает исключения, возникающие при удалении листов, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """ Запись данных кампании в лист Google Sheets.

    Args:
        campaign (SimpleNamespace | str): Объект SimpleNamespace с данными кампании для записи.
    """
```

**Назначение**:
Записывает данные кампании в лист Google Sheets, используя данные из объекта `SimpleNamespace`.

**Параметры**:
- `campaign` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные кампании.

**Как работает функция**:
- Получает лист Google Sheets с именем 'campaign'.
- Формирует список операций обновления для записи данных кампании в вертикальном формате.
- Выполняет пакетное обновление листа Google Sheets с данными кампании.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие при записи данных, и логирует ошибки.

**Примеры**:

```python
from types import SimpleNamespace
campaign_data = SimpleNamespace(
    campaign_name='TestCampaign',
    title='Test Title',
    language='ru',
    currency='USD',
    description='Test Description'
)
campaign_sheet.set_campaign_worksheet(campaign_data)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name: str):
    """ Запись данных из списка объектов SimpleNamespace в ячейки Google Sheets.

    Args:
        category_name (str): Название категории для получения продуктов.
    """
```

**Назначение**:
Записывает данные о продуктах из списка объектов `SimpleNamespace` в ячейки Google Sheets.

**Параметры**:
- `category_name` (str): Название категории для получения продуктов.

**Как работает функция**:
- Получает категорию и список продуктов из атрибута `editor.campaign.category`.
- Копирует лист 'product' и переименовывает его в соответствии с названием категории.
- Формирует список данных о продуктах для записи в Google Sheets.
- Обновляет лист Google Sheets данными о продуктах.
- Форматирует лист с продуктами.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие при записи данных, и логирует ошибки.

**Примеры**:

```python
campaign_sheet.set_products_worksheet(category_name='TestCategory')
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """ Запись данных из объекта SimpleNamespace с категориями в ячейки Google Sheets.

    Args:
        categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
    """
```

**Назначение**:
Записывает данные о категориях из объекта `SimpleNamespace` в ячейки Google Sheets.

**Параметры**:
- `categories` (SimpleNamespace): Объект, где ключи — это категории с данными для записи.

**Как работает функция**:
- Получает лист Google Sheets с именем 'categories'.
- Очищает лист Google Sheets перед записью данных.
- Получает данные о категориях из объекта `SimpleNamespace`.
- Проверяет, что все объекты категории имеют необходимые атрибуты (`name`, `title`, `description`, `tags`, `products_count`).
- Формирует заголовки для таблицы.
- Формирует список данных о категориях для записи в Google Sheets.
- Обновляет лист Google Sheets данными о категориях.
- Форматирует таблицу.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие при записи данных, и логирует ошибки.

**Примеры**:

```python
from types import SimpleNamespace
categories_data = SimpleNamespace()
categories_data.category1 = SimpleNamespace(
    name='Category1',
    title='Category Title 1',
    description='Category Description 1',
    tags=['tag1', 'tag2'],
    products_count=10
)
categories_data.category2 = SimpleNamespace(
    name='Category2',
    title='Category Title 2',
    description='Category Description 2',
    tags=['tag3', 'tag4'],
    products_count=20
)
campaign_sheet.set_categories_worksheet(categories_data)
```

### `get_categories`

```python
def get_categories(self):
    """ Получение данных из таблицы Google Sheets.

    Returns:
        Данные из таблицы в виде списка словарей.
    """
```

**Назначение**:
Получает данные о категориях из таблицы Google Sheets.

**Возвращает**:
- `list[dict]`: Данные из таблицы в виде списка словарей.

**Как работает функция**:
- Получает лист Google Sheets с именем 'categories'.
- Извлекает все записи из листа Google Sheets.
- Логирует информацию об успешном получении данных.
- Возвращает данные в виде списка словарей.

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
        category_name (str): Название категории.
        products (dict): Словарь с данными о продуктах.
    """
```

**Назначение**:
Записывает данные о продуктах в новую таблицу Google Sheets.

**Параметры**:
- `category_name` (str): Название категории.
- `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:
- Получает категорию и список продуктов из атрибута `editor.campaign.category`.
- Копирует лист 'product' и переименовывает его в соответствии с названием категории.
- Формирует заголовки для таблицы.
- Формирует список данных о продуктах для записи в Google Sheets.
- Обновляет лист Google Sheets данными о продуктах.
- Форматирует лист с продуктами.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие при записи данных, и логирует ошибки.

**Примеры**:

```python
products_data = [
    {'product_id': '123', 'app_sale_price': '10.00', 'original_price': '12.00', 'sale_price': '11.00', 'discount': '10%', 'product_title': 'Product 1'},
    {'product_id': '456', 'app_sale_price': '20.00', 'original_price': '22.00', 'sale_price': '21.00', 'discount': '5%', 'product_title': 'Product 2'}
]
campaign_sheet.set_category_products(category_name='TestCategory', products=products_data)
```

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(self, ws: Worksheet):
    """ Форматирование листа 'categories'.

    Args:
        ws (Worksheet): Лист Google Sheets для форматирования.
    """
```

**Назначение**:
Форматирует лист 'categories' в Google Sheets, устанавливая ширину столбцов, высоту строк и форматирование заголовков.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
- Устанавливает ширину столбцов A, B, C, D и E.
- Устанавливает высоту строки заголовков.
- Форматирует заголовки, устанавливая жирный шрифт, размер шрифта, выравнивание и цвет фона.
- Логирует информацию об успешном форматировании листа.
- Обрабатывает исключения, возникающие при форматировании листа, и логирует ошибки.

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
        ws (Worksheet): Лист Google Sheets для форматирования.
    """
```

**Назначение**:
Форматирует лист с продуктами категории в Google Sheets, устанавливая ширину столбцов, высоту строк и форматирование заголовков.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
- Устанавливает ширину столбцов A по Y.
- Устанавливает высоту строки заголовков.
- Форматирует заголовки, устанавливая жирный шрифт, размер шрифта, выравнивание и цвет фона.
- Логирует информацию об успешном форматировании листа.
- Обрабатывает исключения, возникающие при форматировании листа, и логирует ошибки.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('TestCategory')
campaign_sheet._format_category_products_worksheet(ws)