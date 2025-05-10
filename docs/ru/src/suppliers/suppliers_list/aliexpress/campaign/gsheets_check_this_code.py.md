# Модуль `gsheets_check_this_code`

## Обзор

Модуль предназначен для работы с Google Sheets в контексте управления рекламными кампаниями на AliExpress. Он предоставляет функциональность для чтения и записи данных кампаний, категорий и товаров, а также для форматирования листов Google Sheets.

## Подробнее

Модуль включает класс `AliCampaignGoogleSheet`, который расширяет функциональность класса `SpreadSheet` для работы с Google Sheets, используемыми в кампаниях AliExpress. Он обеспечивает автоматизацию процессов, связанных с созданием, обновлением и форматированием данных в Google Sheets, что упрощает управление рекламными кампаниями.

## Классы

### `AliCampaignGoogleSheet`

**Описание**: Класс для работы с Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:
- `spreadsheet_id` (str): Идентификатор Google Sheets таблицы.
- `spreadsheet` (SpreadSheet): Экземпляр класса `SpreadSheet` для работы с Google Sheets.
- `worksheet` (Worksheet): Экземпляр класса `Worksheet` для работы с конкретным листом Google Sheets.
- `driver` (Driver): Инстанс драйвера `Driver` для управления браузером (в данном случае, Chrome).
- `editor` (AliCampaignEditor): Инстанс класса `AliCampaignEditor` для редактирования кампании AliExpress.

**Методы**:
- `__init__(campaign_name: str, language: str | dict = None, currency: str = None)`: Инициализирует класс `AliCampaignGoogleSheet`.
- `clear()`: Очищает содержимое листов.
- `delete_products_worksheets()`: Удаляет все листы, кроме 'categories', 'product', 'category' и 'campaign'.
- `set_campaign_worksheet(campaign: SimpleNamespace)`: Записывает данные кампании на лист Google Sheets.
- `set_products_worksheet(category_name: str)`: Записывает данные о товарах на лист Google Sheets.
- `set_categories_worksheet(categories: SimpleNamespace)`: Записывает данные о категориях на лист Google Sheets.
- `get_categories()`: Получает данные о категориях из таблицы Google Sheets.
- `set_category_products(category_name: str, products: dict)`: Записывает данные о товарах категории в Google Sheets.
- `_format_categories_worksheet(ws: Worksheet)`: Форматирует лист 'categories'.
- `_format_category_products_worksheet(ws: Worksheet)`: Форматирует лист с товарами категории.

## Методы класса

### `__init__`

```python
def __init__(self, campaign_name: str, language: str | dict = None, currency: str = None):
    """ Инициализирует AliCampaignGoogleSheet с указанным ID Google Sheets и дополнительными параметрами.
    Args:
        campaign_name (str): Имя кампании.
        language (str | dict, optional): Язык для кампании. По умолчанию None.
        currency (str, optional): Валюта для кампании. По умолчанию None.
    """
```

**Назначение**: Инициализирует экземпляр класса `AliCampaignGoogleSheet`, устанавливает идентификатор Google Sheets, создает экземпляр `AliCampaignEditor` и выполняет начальную настройку листов Google Sheets.

**Параметры**:
- `campaign_name` (str): Имя кампании.
- `language` (str | dict, optional): Язык кампании. По умолчанию `None`.
- `currency` (str, optional): Валюта кампании. По умолчанию `None`.

**Как работает функция**:
1. Вызывает конструктор родительского класса `SpreadSheet` с указанным `spreadsheet_id`.
2. Создает экземпляр класса `AliCampaignEditor`, передавая имя кампании, язык и валюту.
3. Вызывает метод `clear` для очистки существующих данных.
4. Вызывает метод `set_campaign_worksheet` для записи данных кампании в лист 'campaign'.
5. Вызывает метод `set_categories_worksheet` для записи данных категорий в лист 'categories'.
6. Получает URL Google Sheets и открывает его в браузере с использованием `driver.get_url`.

**Примеры**:

```python
campaign_sheet = AliCampaignGoogleSheet(campaign_name='TestCampaign', language='ru', currency='USD')
```

### `clear`

```python
def clear(self):
    """ Очищает содержимое.
    Удаляет листы товаров и очищает данные на листах категорий и других указанных листах.
    """
```

**Назначение**: Очищает листы Google Sheets, удаляя листы товаров и очищая данные на листах категорий.

**Как работает функция**:
1. Вызывает метод `delete_products_worksheets` для удаления листов товаров.
2. Ловит исключения, возникающие в процессе очистки, и логирует их.

**Примеры**:

```python
campaign_sheet.clear()
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """ Удаляет все листы из таблицы Google Sheets, кроме 'categories', 'product', 'category' и 'campaign'.
    """
```

**Назначение**: Удаляет все листы из Google Sheets, за исключением листов 'categories', 'product', 'category' и 'campaign'.

**Как работает функция**:
1. Определяет список исключаемых листов (`excluded_titles`).
2. Получает список всех листов в Google Sheets.
3. Итерируется по списку листов и удаляет каждый лист, если его заголовок не входит в список исключений.
4. Ловит исключения, возникающие в процессе удаления, логирует их и поднимает исключение выше.

**Примеры**:

```python
campaign_sheet.delete_products_worksheets()
```

### `set_campaign_worksheet`

```python
def set_campaign_worksheet(self, campaign: SimpleNamespace):
    """ Записывает данные кампании в таблицу Google Sheets.
    Args:
        campaign (SimpleNamespace | str): Объект SimpleNamespace с полями данных кампании для записи.
        language (str): Необязательный параметр языка.
        currency (str): Необязательный параметр валюты.
    """
```

**Назначение**: Записывает данные кампании в указанный лист Google Sheets, подготавливая и выполняя пакетное обновление ячеек.

**Параметры**:
- `campaign` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные кампании.

**Как работает функция**:
1. Получает объект `Worksheet` с именем 'campaign'.
2. Формирует список операций обновления ячеек на основе данных из объекта `campaign`.
3. Выполняет пакетное обновление ячеек с использованием метода `batch_update`.
4. Логирует информацию об успешной записи данных кампании.
5. Обрабатывает исключения, возникающие в процессе записи, логирует их и поднимает исключение выше.

**Примеры**:

```python
from types import SimpleNamespace
campaign_data = SimpleNamespace(name='TestCampaign', title='Test Title', language='ru', currency='USD', description='Test Description')
campaign_sheet.set_campaign_worksheet(campaign_data)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name: str):
    """ Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.
    Args:
        category_name (str): Название категории для получения товаров.
    """
```

**Назначение**: Записывает данные о товарах из указанной категории в Google Sheets.

**Параметры**:
- `category_name` (str): Имя категории, товары которой нужно записать.

**Как работает функция**:
1. Получает данные о товарах из указанной категории, используя `AliCampaignEditor`.
2. Копирует шаблон листа 'product' и переименовывает его в соответствии с именем категории.
3. Формирует список данных для записи в лист Google Sheets на основе информации о товарах.
4. Выполняет обновление ячеек листа Google Sheets с данными о товарах.
5. Вызывает метод `_format_category_products_worksheet` для форматирования листа.
6. Логирует информацию об успешном обновлении товаров.
7. Обрабатывает исключения, возникающие в процессе записи, логирует их и поднимает исключение выше.

**Примеры**:

```python
campaign_sheet.set_products_worksheet(category_name='Category1')
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """ Записывает данные из объекта SimpleNamespace с категориями в ячейки Google Sheets.
    Args:
        categories (SimpleNamespace): Объект, где ключи — это категории с данными для записи.
    """
```

**Назначение**: Записывает данные о категориях из объекта `SimpleNamespace` в Google Sheets.

**Параметры**:
- `categories` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные о категориях.

**Как работает функция**:
1. Получает объект `Worksheet` с именем 'categories'.
2. Очищает лист Google Sheets.
3. Извлекает данные о категориях из объекта `categories`.
4. Проверяет наличие необходимых атрибутов у объектов категорий.
5. Формирует заголовки и данные для записи в лист Google Sheets.
6. Выполняет обновление ячеек листа Google Sheets с данными о категориях.
7. Вызывает метод `_format_categories_worksheet` для форматирования листа.
8. Логирует информацию об успешном обновлении данных о категориях.
9. Обрабатывает исключения, возникающие в процессе записи, логирует их и поднимает исключение выше.

**Примеры**:

```python
from types import SimpleNamespace
categories_data = SimpleNamespace(
    Category1=SimpleNamespace(name='Name1', title='Title1', description='Description1', tags=['Tag1', 'Tag2'], products_count=10),
    Category2=SimpleNamespace(name='Name2', title='Title2', description='Description2', tags=['Tag3', 'Tag4'], products_count=20)
)
campaign_sheet.set_categories_worksheet(categories_data)
```

### `get_categories`

```python
def get_categories(self):
    """ Получает данные из таблицы Google Sheets.
    Returns:
        Данные из таблицы в виде списка словарей.
    """
```

**Назначение**: Получает данные о категориях из Google Sheets.

**Возвращает**:
- `list[dict]`: Список словарей, где каждый словарь представляет собой строку данных о категории.

**Как работает функция**:
1. Получает объект `Worksheet` с именем 'categories'.
2. Извлекает все записи из листа Google Sheets с использованием метода `get_all_records`.
3. Логирует информацию об успешном извлечении данных о категориях.
4. Возвращает полученные данные.

**Примеры**:

```python
categories = campaign_sheet.get_categories()
print(categories)
```

### `set_category_products`

```python
def set_category_products(self, category_name: str, products: dict):
    """ Записывает данные о товарах в новую таблицу Google Sheets.
    Args:
        category_name Название категории.
        products Словарь с данными о товарах.
    """
```

**Назначение**: Записывает данные о товарах указанной категории в Google Sheets.

**Параметры**:
- `category_name` (str): Имя категории, для которой нужно записать товары.
- `products` (dict): Словарь с данными о товарах.

**Как работает функция**:
1. Проверяет, найдена ли категория по имени. Если нет, выводит предупреждение и завершает функцию.
2. Копирует лист 'product' и переименовывает его в соответствии с именем категории.
3. Формирует заголовки для таблицы товаров.
4. Преобразует данные о товарах в формат, подходящий для записи в Google Sheets.
5. Записывает данные в Google Sheets, обновляя соответствующие ячейки.
6. Вызывает функцию форматирования `_format_category_products_worksheet`.
7. Логирует информацию об успешном обновлении товаров.
8. Обрабатывает исключения, возникающие в процессе записи, логирует их и поднимает исключение выше.

**Примеры**:

```python
products_data = [
    {'product_id': '123', 'app_sale_price': '10.00', 'original_price': '12.00', 'sale_price': '11.00', 'discount': '10%',
     'product_main_image_url': 'http://example.com/image1.jpg', 'local_image_path': '/path/to/image1.jpg',
     'product_small_image_urls': ['http://example.com/image2.jpg', 'http://example.com/image3.jpg'],
     'product_video_url': 'http://example.com/video1.mp4', 'local_video_path': '/path/to/video1.mp4',
     'first_level_category_id': '1', 'first_level_category_name': 'Category1', 'second_level_category_id': '11',
     'second_level_category_name': 'SubCategory1', 'target_sale_price': '11.00', 'target_sale_price_currency': 'USD',
     'target_app_sale_price_currency': 'USD', 'target_original_price_currency': 'USD', 'original_price_currency': 'USD',
     'product_title': 'Product Title', 'evaluate_rate': '4.5', 'promotion_link': 'http://example.com/promo1',
     'shop_url': 'http://example.com/shop1', 'shop_id': 'Shop123', 'tags': ['tag1', 'tag2']},
    {'product_id': '456', 'app_sale_price': '20.00', 'original_price': '24.00', 'sale_price': '22.00', 'discount': '8%',
     'product_main_image_url': 'http://example.com/image4.jpg', 'local_image_path': '/path/to/image4.jpg',
     'product_small_image_urls': ['http://example.com/image5.jpg', 'http://example.com/image6.jpg'],
     'product_video_url': 'http://example.com/video2.mp4', 'local_video_path': '/path/to/video2.mp4',
     'first_level_category_id': '2', 'first_level_category_name': 'Category2', 'second_level_category_id': '22',
     'second_level_category_name': 'SubCategory2', 'target_sale_price': '22.00', 'target_sale_price_currency': 'EUR',
     'target_app_sale_price_currency': 'EUR', 'target_original_price_currency': 'EUR', 'original_price_currency': 'EUR',
     'product_title': 'Product Title 2', 'evaluate_rate': '4.0', 'promotion_link': 'http://example.com/promo2',
     'shop_url': 'http://example.com/shop2', 'shop_id': 'Shop456', 'tags': ['tag3', 'tag4']}
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
```

**Назначение**: Форматирует лист 'categories' в Google Sheets, устанавливая ширину столбцов, высоту строк и форматирование заголовков.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
1. Устанавливает ширину столбцов A, B, C, D и E.
2. Устанавливает высоту строки заголовков.
3. Определяет формат заголовков (жирный шрифт, размер шрифта, выравнивание, цвет фона).
4. Применяет формат к диапазону ячеек заголовков.
5. Логирует информацию об успешном форматировании листа категорий.
6. Обрабатывает исключения, возникающие в процессе форматирования, логирует их и поднимает исключение выше.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('categories')
campaign_sheet._format_categories_worksheet(ws)
```

### `_format_category_products_worksheet`

```python
def _format_category_products_worksheet(self, ws: Worksheet):
    """ Форматирование листа с товарами категории.
    Args:
        ws Лист Google Sheets для форматирования.
    """
```

**Назначение**: Форматирует лист с товарами категории в Google Sheets, устанавливая ширину столбцов, высоту строк и форматирование заголовков.

**Параметры**:
- `ws` (Worksheet): Лист Google Sheets для форматирования.

**Как работает функция**:
1. Устанавливает ширину столбцов от A до Y.
2. Устанавливает высоту строки заголовков.
3. Определяет формат заголовков (жирный шрифт, размер шрифта, выравнивание, цвет фона).
4. Применяет формат к диапазону ячеек заголовков.
5. Логирует информацию об успешном форматировании листа товаров категории.
6. Обрабатывает исключения, возникающие в процессе форматирования, логирует их и поднимает исключение выше.

**Примеры**:

```python
ws = campaign_sheet.get_worksheet('ProductCategory')
campaign_sheet._format_category_products_worksheet(ws)