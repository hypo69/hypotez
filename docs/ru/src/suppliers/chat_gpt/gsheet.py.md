# Модуль gsheet.py

## Обзор

Модуль `gsheet.py` предназначен для управления Google Sheets в контексте кампаний AliExpress. Он предоставляет классы и методы для чтения, записи и обработки данных, хранящихся в Google Sheets, таких как информация о категориях, продуктах и рекламных кампаниях.

## Подробней

Этот модуль облегчает взаимодействие с Google Sheets, позволяя автоматизировать процессы, связанные с управлением данными для рекламных кампаний AliExpress. Он включает в себя функциональность для очистки листов, обновления информации о кампаниях и категориях, а также для управления данными о продуктах. Модуль использует библиотеку `gspread` для работы с Google Sheets и предоставляет удобные методы для чтения и записи данных в формате `SimpleNamespace`.

## Классы

### `GptGs`

**Описание**: Класс для управления Google Sheets в рамках кампаний AliExpress.

**Наследует**: `SpreadSheet`

**Атрибуты**:
- Отсутствуют явно определенные атрибуты, кроме тех, что наследуются от `SpreadSheet`.

**Методы**:
- `__init__()`: Инициализирует класс `GptGs` с указанным ID Google Sheets spreadsheet.
- `clear()`: Очищает содержимое листов, удаляя листы продуктов и очищая данные на листах категорий и кампаний.
- `update_chat_worksheet()`: Записывает данные кампании в Google Sheets worksheet.
- `get_campaign_worksheet()`: Читает данные кампании из worksheet 'campaign'.
- `set_category_worksheet()`: Записывает данные категории из объекта `SimpleNamespace` в Google Sheets cells вертикально.
- `get_category_worksheet()`: Читает данные категории из worksheet 'category'.
- `set_categories_worksheet()`: Записывает данные из объекта `SimpleNamespace` в Google Sheets cells.
- `get_categories_worksheet()`: Читает данные из столбцов A-E, начиная со второй строки, из worksheet 'categories'.
- `set_product_worksheet()`: Записывает данные продукта в новый Google Sheets spreadsheet.
- `get_product_worksheet()`: Читает данные продукта из worksheet 'products'.
- `set_products_worksheet()`: Записывает данные из списка объектов `SimpleNamespace` в Google Sheets cells.
- `delete_products_worksheets()`: Удаляет все листы из Google Sheets spreadsheet, кроме 'categories' и 'product_template'.
- `save_categories_from_worksheet()`: Сохраняет данные категорий, отредактированные в Google Sheets.
- `save_campaign_from_worksheet()`: Сохраняет рекламную кампанию.

**Принцип работы**:
Класс `GptGs` наследует функциональность работы с Google Sheets от класса `SpreadSheet`. Он предоставляет методы для выполнения операций чтения и записи данных, связанных с рекламными кампаниями AliExpress. Методы класса позволяют управлять данными о категориях, продуктах и общих параметрах кампаний, обеспечивая интеграцию с Google Sheets для хранения и обмена данными.

## Методы класса

### `__init__`

```python
def __init__(self):
    """ Инициализирует AliCampaignGoogleSheet с указанным Google Sheets spreadsheet ID и дополнительными параметрами.
    Args:
        campaign_name (str): Название кампании.
        category_name (str): Название категории.
        language (str): Язык для кампании.
        currency (str): Валюта для кампании.
    """
```

**Назначение**: Инициализирует экземпляр класса `GptGs`.

**Параметры**:
- Отсутствуют явные параметры, но инициализируется ID Google Sheets spreadsheet.

**Возвращает**:
- None

**Как работает функция**:
Вызывает конструктор родительского класса `SpreadSheet` с указанным ID Google Sheets spreadsheet.

**Примеры**:
```python
gpt_gs = GptGs()
```

### `clear`

```python
def clear(self):
    """ Очистить содержимое.
    Удалить листы продуктов и очистить данные на листах категорий и других указанных листах.
    """
```

**Назначение**: Очищает содержимое листов Google Sheets, используемых для хранения данных о продуктах, категориях и кампаниях.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при очистке листов.

**Как работает функция**:
Пытается удалить все листы продуктов, а затем очищает данные на листах категорий и кампаний. В случае ошибки логирует её с использованием `logger.error`.

**Примеры**:
```python
gpt_gs = GptGs()
gpt_gs.clear()
```

### `update_chat_worksheet`

```python
def update_chat_worksheet(self, data: SimpleNamespace|dict|list, conversation_name:str, language: str = None):
    """ Записать данные кампании в Google Sheets worksheet.
    Args:
        campaign (SimpleNamespace | str): Объект SimpleNamespace с полями данных кампании для записи.
        language (str): Необязательный параметр языка.
        currency (str): Необязательный параметр валюты.
    """
```

**Назначение**: Записывает данные кампании в Google Sheets worksheet.

**Параметры**:
- `data` (SimpleNamespace | dict | list): Объект, содержащий данные для записи в worksheet.
- `conversation_name` (str): Имя worksheet, в который нужно записать данные.
- `language` (str, optional): Язык. По умолчанию `None`.

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при записи данных кампании в worksheet.

**Как работает функция**:
Извлекает данные из объекта `SimpleNamespace` и подготавливает обновления для записи в Google Sheets worksheet.

**Примеры**:
```python
data = SimpleNamespace(name='Test Campaign', title='Test Title', description='Test Description', tags=['tag1', 'tag2'], products_count=100)
gpt_gs = GptGs()
gpt_gs.update_chat_worksheet(data, 'campaign')
```

### `get_campaign_worksheet`

```python
def get_campaign_worksheet(self) -> SimpleNamespace:
    """ Читать данные кампании из worksheet 'campaign'.
    Returns:
        SimpleNamespace: Объект SimpleNamespace с полями данных кампании.
    """
```

**Назначение**: Читает данные кампании из worksheet с именем 'campaign'.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace`, содержащий данные кампании.

**Вызывает исключения**:
- `ValueError`: Если worksheet 'campaign' не найден.
- `Exception`: Если возникает ошибка при получении данных из worksheet.

**Как работает функция**:
Получает данные из worksheet 'campaign' и создает объект `SimpleNamespace` с данными кампании.

**Примеры**:
```python
gpt_gs = GptGs()
campaign_data = gpt_gs.get_campaign_worksheet()
print(campaign_data.name)
```

### `set_category_worksheet`

```python
def set_category_worksheet(self, category: SimpleNamespace | str):
    """ Записать данные из объекта SimpleNamespace в Google Sheets cells вертикально.
    Args:
        category (SimpleNamespace): Объект SimpleNamespace с полями данных для записи.
    """
```

**Назначение**: Записывает данные категории из объекта `SimpleNamespace` в Google Sheets cells вертикально.

**Параметры**:
- `category` (SimpleNamespace | str): Объект `SimpleNamespace`, содержащий данные категории.

**Возвращает**:
- None

**Вызывает исключения**:
- `TypeError`: Если передан некорректный тип данных для категории.
- `Exception`: Если возникает ошибка при установке worksheet категории.

**Как работает функция**:
Подготавливает данные для вертикальной записи в Google Sheets worksheet и записывает их.

**Примеры**:
```python
category_data = SimpleNamespace(name='Test Category', title='Test Title', description='Test Description', tags=['tag1', 'tag2'], products_count=50)
gpt_gs = GptGs()
gpt_gs.set_category_worksheet(category_data)
```

### `get_category_worksheet`

```python
def get_category_worksheet(self) -> SimpleNamespace:
    """ Читать данные категории из worksheet 'category'.
    Returns:
        SimpleNamespace: Объект SimpleNamespace с полями данных категории.
    """
```

**Назначение**: Читает данные категории из worksheet 'category'.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace`, содержащий данные категории.

**Вызывает исключения**:
- `ValueError`: Если worksheet 'category' не найден.
- `Exception`: Если возникает ошибка при получении данных из worksheet.

**Как работает функция**:
Получает данные из worksheet 'category' и создает объект `SimpleNamespace` с данными категории.

**Примеры**:
```python
gpt_gs = GptGs()
category_data = gpt_gs.get_category_worksheet()
print(category_data.name)
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """ Записать данные из объекта SimpleNamespace в Google Sheets cells.
    Args:
        categories (SimpleNamespace): Объект SimpleNamespace с полями данных для записи.
    """
```

**Назначение**: Записывает данные из объекта `SimpleNamespace` в Google Sheets cells.

**Параметры**:
- `categories` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные для записи.

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при установке worksheet категорий.

**Как работает функция**:
Итерируется по атрибутам объекта `categories`, извлекает данные и записывает их в Google Sheets worksheet.

**Примеры**:
```python
categories_data = SimpleNamespace(cat1=SimpleNamespace(name='Cat1', title='Title1', description='Desc1', tags=['tag1'], products_count=10), 
                                cat2=SimpleNamespace(name='Cat2', title='Title2', description='Desc2', tags=['tag2'], products_count=20))
gpt_gs = GptGs()
gpt_gs.set_categories_worksheet(categories_data)
```

### `get_categories_worksheet`

```python
def get_categories_worksheet(self) -> List[List[str]]:
    """ Читать данные из столбцов A-E, начиная со второй строки, из worksheet 'categories'.
    Returns:
        List[List[str]]: Список строк с данными из столбцов A-E.
    """
```

**Назначение**: Читает данные из столбцов A-E, начиная со второй строки, из worksheet 'categories'.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `List[List[str]]`: Список строк с данными из столбцов A-E.

**Вызывает исключения**:
- `ValueError`: Если worksheet 'categories' не найден.
- `Exception`: Если возникает ошибка при получении данных из worksheet.

**Как работает функция**:
Получает данные из worksheet 'categories' и возвращает список строк с данными из столбцов A-E.

**Примеры**:
```python
gpt_gs = GptGs()
categories_data = gpt_gs.get_categories_worksheet()
print(categories_data)
```

### `set_product_worksheet`

```python
def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str):
    """ Записать данные продукта в новый Google Sheets spreadsheet.
    Args:
        category_name (str): Название категории.
        product (SimpleNamespace): Объект SimpleNamespace с полями данных продукта для записи.
    """
```

**Назначение**: Записывает данные продукта в новый Google Sheets spreadsheet.

**Параметры**:
- `category_name` (str): Название категории.
- `product` (SimpleNamespace | str): Объект `SimpleNamespace`, содержащий данные продукта.

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при обновлении данных продукта в worksheet.

**Как работает функция**:
Копирует worksheet 'product_template', переименовывает его в соответствии с названием категории, затем записывает данные продукта в новую таблицу.

**Примеры**:
```python
product_data = SimpleNamespace(product_id=123, app_sale_price=10.0, original_price=20.0, sale_price=15.0, discount=0.5, product_main_image_url='http://example.com/image.jpg', local_image_path='/local/image.jpg', product_small_image_urls=['http://example.com/image1.jpg'], product_video_url='http://example.com/video.mp4', local_video_path='/local/video.mp4', first_level_category_id=1, first_level_category_name='Category1', second_level_category_id=2, second_level_category_name='Category2', target_sale_price=12.0, target_sale_price_currency='USD', target_app_sale_price_currency='USD', target_original_price_currency='USD', original_price_currency='USD', product_title='Test Product', evaluate_rate=4.5, promotion_link='http://example.com/promotion', shop_url='http://example.com/shop', shop_id=12345, tags=['tag1', 'tag2'])
gpt_gs = GptGs()
gpt_gs.set_product_worksheet(product_data, 'TestCategory')
```

### `get_product_worksheet`

```python
def get_product_worksheet(self) -> SimpleNamespace:
    """ Читать данные продукта из worksheet 'products'.
    Returns:
        SimpleNamespace: Объект SimpleNamespace с полями данных продукта.
    """
```

**Назначение**: Читает данные продукта из worksheet 'products'.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace`, содержащий данные продукта.

**Вызывает исключения**:
- `ValueError`: Если worksheet 'products' не найден.
- `Exception`: Если возникает ошибка при получении данных из worksheet.

**Как работает функция**:
Получает данные из worksheet 'products' и создает объект `SimpleNamespace` с данными продукта.

**Примеры**:
```python
gpt_gs = GptGs()
product_data = gpt_gs.get_product_worksheet()
print(product_data.name)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name:str):
    """ Записать данные из списка объектов SimpleNamespace в Google Sheets cells.
    Args:
        ns_list (List[SimpleNamespace]|SimpleNamespace): Список объектов SimpleNamespace с полями данных для записи.
    """
```

**Назначение**: Записывает данные из списка объектов `SimpleNamespace` в Google Sheets cells.

**Параметры**:
- `category_name` (str): Имя категории.

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при установке worksheet продуктов.

**Как работает функция**:
Итерируется по списку объектов `SimpleNamespace`, извлекает данные и записывает их в Google Sheets worksheet.

**Примеры**:
```python
gpt_gs = GptGs()
gpt_gs.set_products_worksheet('TestCategory')
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """ Удалить все листы из Google Sheets spreadsheet, кроме 'categories' и 'product_template'.
    """
```

**Назначение**: Удаляет все листы из Google Sheets spreadsheet, кроме 'categories', 'product', 'category' и 'campaign'.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при удалении листов.

**Как работает функция**:
Итерируется по всем worksheets и удаляет те, чьи имена не входят в список исключений.

**Примеры**:
```python
gpt_gs = GptGs()
gpt_gs.delete_products_worksheets()
```

### `save_categories_from_worksheet`

```python
def save_categories_from_worksheet(self, update:bool=False):
    """ Сохраняю данные, отредактированные в гугл таблице
    Args:
        update (bool): Если `True`, то обновить кампанию. По умолчанию `False`.
    """
```

**Назначение**: Сохраняет данные категорий, отредактированные в Google Sheets.

**Параметры**:
- `update` (bool, optional): Флаг, указывающий, нужно ли обновить кампанию. По умолчанию `False`.

**Возвращает**:
- None

**Как работает функция**:
Получает данные категорий из Google Sheets, создает объекты `SimpleNamespace` для каждой категории и сохраняет их.

**Примеры**:
```python
gpt_gs = GptGs()
gpt_gs.save_categories_from_worksheet()
```

### `save_campaign_from_worksheet`

```python
def save_campaign_from_worksheet(self):
    """ Сохраняю реклманую каманию
    """
```

**Назначение**: Сохраняет рекламную кампанию.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- None

**Как работает функция**:
Сохраняет данные категорий, затем получает данные кампании и обновляет объект кампании.

**Примеры**:
```python
gpt_gs = GptGs()
gpt_gs.save_campaign_from_worksheet()