# Модуль `gsheets_check_this_code.py`

## Обзор

Модуль предназначен для работы с Google Sheets в рамках управления рекламными кампаниями на AliExpress. Он предоставляет функциональность для чтения, записи и форматирования данных кампаний, категорий и товаров в Google Sheets. Модуль использует библиотеку `gspread` для взаимодействия с Google Sheets API, а также другие вспомогательные модули для управления драйверами веб-браузеров и обработки данных.

## Подробнее

Модуль содержит класс `AliCampaignGoogleSheet`, который наследует класс `SpreadSheet` и расширяет его функциональность для работы с данными AliExpress кампаний. Он позволяет автоматизировать процесс обновления и управления данными кампаний, категорий и товаров через Google Sheets, что упрощает взаимодействие с рекламными кампаниями и обеспечивает удобный интерфейс для редактирования и анализа данных.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:
- `spreadsheet_id` (str): Идентификатор Google Sheets spreadsheet.
- `spreadsheet` (SpreadSheet): Объект для работы с Google Sheets.
- `worksheet` (Worksheet): Объект для работы с отдельным листом Google Sheets.
- `driver` (Driver): Драйвер веб-браузера для взаимодействия с Google Sheets.
- `editor` (AliCampaignEditor): Редактор кампании AliExpress.

**Методы**:
- `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует класс `AliCampaignGoogleSheet`.
- `clear()`: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на других листах.
- `delete_products_worksheets()`: Удаляет все листы из Google Sheets, кроме 'categories', 'product', 'category' и 'campaign'.
- `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании в лист Google Sheets.
- `set_products_worksheet(category_name: str)`: Записывает данные о продуктах в лист Google Sheets.
- `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях в лист Google Sheets.
- `get_categories()`: Извлекает данные о категориях из листа Google Sheets.
- `set_category_products(category_name: str, products: dict)`: Записывает данные о продуктах категории в лист Google Sheets.
- `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист 'categories' в Google Sheets.
- `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист с продуктами категории в Google Sheets.

## Методы класса

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """ Инициализация AliCampaignGoogleSheet с указанным ID Google Sheets и дополнительными параметрами.
    Args:
        campaign_name (str): Название кампании.
        language (str | dict, optional): Язык для кампании. По умолчанию `None`.
        currency (str, optional): Валюта для кампании. По умолчанию `None`.
    """
```

**Назначение**: Инициализирует объект класса `AliCampaignGoogleSheet`.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:
- Вызывает конструктор родительского класса `SpreadSheet` с указанием `spreadsheet_id`.
- Создает экземпляр класса `AliCampaignEditor` для редактирования кампании.
- Вызывает методы `clear()`, `set_campaign_worksheet()`, `set_categories_worksheet()` для очистки и заполнения данными листов Google Sheets.
- Открывает URL Google Sheets в браузере с использованием драйвера.

**Примеры**:
```python
campaign_sheet = AliCampaignGoogleSheet(campaign_name='Test Campaign', language='en', currency='USD')
```

### `clear`

```python
def clear(self):
    """ Очистка содержимого.
    Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
    """
```

**Назначение**: Очищает содержимое Google Sheets, удаляя листы продуктов и очищая данные на других листах.

**Как работает функция**:
- Вызывает метод `delete_products_worksheets()` для удаления листов продуктов.
- Ловит исключения, возникающие при удалении листов, и логирует их.

**Примеры**:
```python
campaign_sheet.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """ Удаление всех листов из Google Sheets, кроме 'categories', 'product', 'category', 'campaign'.
    """
```

**Назначение**: Удаляет все листы из Google Sheets, кроме 'categories', 'product', 'category' и 'campaign'.

**Как работает функция**:
- Получает список всех листов в Google Sheets.
- Перебирает листы и удаляет те, у которых заголовок не входит в список исключений (`excluded_titles`).
- Ловит исключения, возникающие при удалении листов, и логирует их.

**Примеры**:
```python
campaign_sheet.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """ Запись данных кампании в лист Google Sheets.
    Args:
        campaign (SimpleNamespace | str): Объект SimpleNamespace с полями данных кампании для записи.
    """
```

**Назначение**: Записывает данные кампании в лист Google Sheets.

**Параметры**:
- `campaign` (SimpleNamespace): Объект `SimpleNamespace` с данными кампании.

**Как работает функция**:
- Получает лист Google Sheets с именем 'campaign'.
- Формирует список операций обновления для записи данных кампании в вертикальном формате.
- Выполняет пакетное обновление листа Google Sheets.
- Ловит исключения, возникающие при записи данных, и логирует их.

**Примеры**:
```python
campaign_data = SimpleNamespace(name='Test Campaign', title='Test', language='en', currency='USD', description='Description')
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

**Назначение**: Записывает данные о продуктах из указанной категории в лист Google Sheets.

**Параметры**:
- `category_name` (str): Название категории, продукты которой нужно записать.

**Как работает функция**:
- Получает категорию по имени из объекта `self.editor.campaign.category`.
- Получает список продуктов из категории.
- Копирует лист 'product' и переименовывает его в имя категории.
- Записывает данные о продуктах в лист Google Sheets.
- Форматирует лист с продуктами.
- Ловит исключения, возникающие при записи данных, и логирует их.

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
```

**Назначение**: Записывает данные о категориях из объекта `SimpleNamespace` в лист Google Sheets.

**Параметры**:
- `categories` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные о категориях.

**Как работает функция**:
- Получает лист Google Sheets с именем 'categories'.
- Очищает лист.
- Извлекает данные о категориях из объекта `SimpleNamespace`.
- Записывает заголовки и данные о категориях в лист Google Sheets.
- Форматирует лист с категориями.
- Ловит исключения, возникающие при записи данных, и логирует их.

**Примеры**:
```python
categories_data = SimpleNamespace(**{'Category1': SimpleNamespace(name='Cat1', title='Category 1', description='Desc1', tags=['tag1', 'tag2'], products_count=10)})
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

**Назначение**: Извлекает данные о категориях из листа Google Sheets.

**Возвращает**:
- (list[dict]): Список словарей, представляющих данные о категориях.

**Как работает функция**:
- Получает лист Google Sheets с именем 'categories'.
- Извлекает все записи из листа.
- Логирует информацию об извлечении данных.

**Примеры**:
```python
categories = campaign_sheet.get_categories()
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

**Назначение**: Записывает данные о продуктах для указанной категории в новый лист Google Sheets.

**Параметры**:
- `category_name` (str): Название категории для записи продуктов.
- `products` (dict): Словарь с данными о продуктах.

**Как работает функция**:
- Получает категорию по имени из объекта `self.editor.campaign.category`.
- Получает список продуктов из категории.
- Копирует лист 'product' и переименовывает его в имя категории.
- Записывает заголовки и данные о продуктах в лист Google Sheets.
- Форматирует лист с продуктами.
- Ловит исключения, возникающие при записи данных, и логирует их.

**Примеры**:
```python
products_data = [{'product_id': '123', 'app_sale_price': '10.00', 'original_price': '15.00', 'sale_price': '12.00', 'discount': '20%'}]
campaign_sheet.set_category_products(category_name='Category1', products=products_data)
```

### `_format_categories_worksheet`

```python
def _format_categories_worksheet(self, ws: Worksheet):
    """ Форматирование листа 'categories'.
    Args:
        ws (Worksheet): Лист Google Sheets для форматирования.
    """
```

**Назначение**: Форматирует лист 'categories' в Google Sheets.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
- Устанавливает ширину столбцов.
- Устанавливает высоту строк.
- Форматирует заголовки (жирный шрифт, размер шрифта, выравнивание, цвет фона).
- Ловит исключения, возникающие при форматировании, и логирует их.

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

**Назначение**: Форматирует лист с продуктами категории в Google Sheets.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
- Устанавливает ширину столбцов.
- Устанавливает высоту строк.
- Форматирует заголовки (жирный шрифт, размер шрифта, выравнивание, цвет фона).
- Ловит исключения, возникающие при форматировании, и логирует их.

**Примеры**:
```python
ws = campaign_sheet.get_worksheet('Category1')
campaign_sheet._format_category_products_worksheet(ws)
```