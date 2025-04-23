# Модуль `gsheet`

## Обзор

Модуль `gsheet` предназначен для управления Google Sheets в рамках кампаний AliExpress. Он предоставляет функциональность для чтения, записи и очистки данных в Google Sheets, а также для управления листами продуктов и категорий.

## Подробнее

Модуль `gsheet` наследует функциональность из классов `SpreadSheet` для работы с Google Sheets и предназначен для управления данными, связанными с категориями и продуктами AliExpress, в Google Sheets. Он обеспечивает возможность автоматизации работы с Google Sheets для целей управления кампаниями, включая обновление данных о категориях и продуктах, а также очистку устаревших данных.

## Классы

### `GptGs`

**Описание**: Класс `GptGs` предназначен для управления Google Sheets в рамках кампаний AliExpress.

**Наследует**:
- `SpreadSheet`: Предоставляет функциональность для работы с Google Sheets.

**Методы**:
- `__init__`: Инициализирует объект класса `GptGs`.
- `clear`: Очищает содержимое Google Sheets.
- `update_chat_worksheet`: Обновляет данные чата в Google Sheets.
- `get_campaign_worksheet`: Получает данные кампании из Google Sheets.
- `set_category_worksheet`: Записывает данные о категории в Google Sheets.
- `get_category_worksheet`: Получает данные о категории из Google Sheets.
- `set_categories_worksheet`: Записывает данные о категориях в Google Sheets.
- `get_categories_worksheet`: Получает данные о категориях из Google Sheets.
- `set_product_worksheet`: Записывает данные о продукте в Google Sheets.
- `get_product_worksheet`: Получает данные о продукте из Google Sheets.
- `set_products_worksheet`: Записывает данные о продуктах в Google Sheets.
- `delete_products_worksheets`: Удаляет листы продуктов из Google Sheets.
- `save_categories_from_worksheet`: Сохраняет отредактированные в Google Sheets данные о категориях.
- `save_campaign_from_worksheet`: Сохраняет рекламную кампанию из данных в Google Sheets.

### `__init__`

```python
def __init__(self):
    """
    Инициализирует объект класса `GptGs`.

    Args:
        campaign_name (str): Название кампании.
        category_name (str): Название категории.
        language (str): Язык кампании.
        currency (str): Валюта кампании.
    """
```

**Назначение**:
Инициализирует экземпляр класса `GptGs`, вызывая конструктор родительского класса `SpreadSheet` с указанием ID Google Sheets.

**Как работает функция**:
- Вызывает конструктор базового класса `SpreadSheet` с ID таблицы Google Sheets `'1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'`.

### `clear`

```python
def clear(self):
    """
    Очищает содержимое Google Sheets.
    Удаляет листы продуктов и очищает данные на листах категорий и других указанных листах.
    """
```

**Назначение**:
Очистка содержимого Google Sheets, включая удаление листов продуктов и очистку данных на листах категорий и других указанных листах.

**Как работает функция**:
- Вызывает метод `delete_products_worksheets` для удаления листов продуктов.
- Попытка очистки листов `'category'`, `'categories'`, `'campaign'` (закомментировано в коде).
- Обрабатывает исключения, возникающие в процессе очистки, и логирует ошибки.

**Пример**:
```python
gpt_gs = GptGs()
gpt_gs.clear()
```

### `update_chat_worksheet`

```python
def update_chat_worksheet(self, data: SimpleNamespace|dict|list, conversation_name:str, language: str = None):
    """
    Записывает данные кампании на лист Google Sheets.

    Args:
        data (SimpleNamespace | dict | list): Объект SimpleNamespace с полями данных кампании для записи.
        conversation_name (str): Имя листа для записи.
        language (str, optional): Параметр языка.
        currency (str, optional): Параметр валюты.

    Raises:
        Exception: Если возникает ошибка при записи данных кампании на лист.
    """
```

**Назначение**:
Запись данных кампании на указанный лист Google Sheets.

**Как работает функция**:
- Извлекает данные из объекта `SimpleNamespace` (или словаря) `data`.
- Формирует список обновлений для записи в Google Sheets.
- Выполняет пакетное обновление данных на листе Google Sheets.
- Обрабатывает исключения, возникающие в процессе записи, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
data = SimpleNamespace(name='test', title='Test Campaign', description='Description', tags=['tag1', 'tag2'], products_count=100)
gpt_gs = GptGs()
gpt_gs.update_chat_worksheet(data, 'campaign')
```

### `get_campaign_worksheet`

```python
def get_campaign_worksheet(self) -> SimpleNamespace:
    """
    Считывает данные кампании из листа 'campaign'.

    Returns:
        SimpleNamespace: Объект SimpleNamespace с полями данных кампании.

    Raises:
        ValueError: Если лист 'campaign' не найден.
        Exception: Если возникает ошибка при получении данных из листа.
    """
```

**Назначение**:
Чтение данных кампании из листа `'campaign'` Google Sheets.

**Как работает функция**:
- Получает объект листа `'campaign'` из Google Sheets.
- Извлекает все значения из листа.
- Создает объект `SimpleNamespace` с данными кампании.
- Логирует информацию об успешном чтении данных.
- Обрабатывает исключения, возникающие в процессе чтения, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
gpt_gs = GptGs()
campaign_data = gpt_gs.get_campaign_worksheet()
print(campaign_data.name)
```

### `set_category_worksheet`

```python
def set_category_worksheet(self, category: SimpleNamespace | str):
    """
    Записывает данные из объекта SimpleNamespace в ячейки Google Sheets по вертикали.

    Args:
        category (SimpleNamespace | str): Объект SimpleNamespace с полями данных для записи.

    Raises:
        TypeError: Если передан не SimpleNamespace объект.
        Exception: Если возникает ошибка при записи данных о категории.
    """
```

**Назначение**:
Запись данных из объекта `SimpleNamespace` в ячейки Google Sheets по вертикали.

**Как работает функция**:
- Получает объект листа `'category'` из Google Sheets.
- Извлекает данные из объекта `SimpleNamespace` `category`.
- Формирует данные для вертикальной записи в Google Sheets.
- Выполняет обновление данных на листе Google Sheets.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие в процессе записи, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
category_data = SimpleNamespace(name='test', title='Test Category', description='Description', tags=['tag1', 'tag2'], products_count=100)
gpt_gs = GptGs()
gpt_gs.set_category_worksheet(category_data)
```

### `get_category_worksheet`

```python
def get_category_worksheet(self) -> SimpleNamespace:
    """
    Считывает данные о категории из листа 'category'.

    Returns:
        SimpleNamespace: Объект SimpleNamespace с полями данных о категории.

    Raises:
        ValueError: Если лист 'category' не найден.
        Exception: Если возникает ошибка при получении данных из листа.
    """
```

**Назначение**:
Чтение данных о категории из листа `'category'` Google Sheets.

**Как работает функция**:
- Получает объект листа `'category'` из Google Sheets.
- Извлекает все значения из листа.
- Создает объект `SimpleNamespace` с данными о категории.
- Логирует информацию об успешном чтении данных.
- Обрабатывает исключения, возникающие в процессе чтения, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
gpt_gs = GptGs()
category_data = gpt_gs.get_category_worksheet()
print(category_data.name)
```

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """
    Записывает данные из объекта SimpleNamespace в ячейки Google Sheets.

    Args:
        categories (SimpleNamespace): Объект SimpleNamespace с полями данных для записи.
    Raises:
        Exception: Если возникает ошибка при записи данных о категориях.
    """
```

**Назначение**:
Запись данных из объекта `SimpleNamespace` в ячейки Google Sheets.

**Как работает функция**:
- Получает объект листа `'categories'` из Google Sheets.
- Итерируется по атрибутам объекта `categories`.
- Извлекает данные из каждого атрибута, являющегося объектом `SimpleNamespace`.
- Формирует список обновлений для записи в Google Sheets.
- Выполняет пакетное обновление данных на листе Google Sheets.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие в процессе записи, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
categories_data = SimpleNamespace(cat1=SimpleNamespace(name='test1', title='Test Category 1', description='Description 1', tags=['tag1', 'tag2'], products_count=100), cat2=SimpleNamespace(name='test2', title='Test Category 2', description='Description 2', tags=['tag3', 'tag4'], products_count=200))
gpt_gs = GptGs()
gpt_gs.set_categories_worksheet(categories_data)
```

### `get_categories_worksheet`

```python
def get_categories_worksheet(self) -> List[List[str]]:
    """
    Считывает данные из столбцов A по E, начиная со второй строки, из листа 'categories'.

    Returns:
        List[List[str]]: Список строк с данными из столбцов A по E.

    Raises:
        ValueError: Если лист 'categories' не найден.
        Exception: Если возникает ошибка при получении данных из листа.
    """
```

**Назначение**:
Чтение данных из столбцов A по E, начиная со второй строки, из листа `'categories'` Google Sheets.

**Как работает функция**:
- Получает объект листа `'categories'` из Google Sheets.
- Извлекает все значения из листа.
- Извлекает данные из столбцов A по E, начиная со второй строки.
- Логирует информацию об успешном чтении данных.
- Обрабатывает исключения, возникающие в процессе чтения, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
gpt_gs = GptGs()
categories_data = gpt_gs.get_categories_worksheet()
print(categories_data)
```

### `set_product_worksheet`

```python
def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str):
    """
    Записывает данные о продукте в новый лист Google Sheets.

    Args:
        category_name (str): Название категории.
        product (SimpleNamespace): Объект SimpleNamespace с полями данных продукта для записи.

    Raises:
        Exception: Если возникает ошибка при обновлении данных продукта.
    """
```

**Назначение**:
Запись данных о продукте в новый лист Google Sheets.

**Как работает функция**:
- Копирует лист `'product_template'` в новый лист с именем `category_name`.
- Формирует заголовки для записи в первую строку листа.
- Извлекает данные из объекта `SimpleNamespace` `product`.
- Формирует данные для записи во вторую строку листа.
- Выполняет обновление данных на листе Google Sheets.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие в процессе записи, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
product_data = SimpleNamespace(product_id='123', app_sale_price=100, original_price=200, sale_price=150, discount=50, product_main_image_url='http://example.com/image.jpg', local_image_path='/tmp/image.jpg', product_small_image_urls=['http://example.com/image1.jpg', 'http://example.com/image2.jpg'], product_video_url='http://example.com/video.mp4', local_video_path='/tmp/video.mp4', first_level_category_id=1, first_level_category_name='Category 1', second_level_category_id=2, second_level_category_name='Category 2', target_sale_price=120, target_sale_price_currency='USD', target_app_sale_price_currency='USD', target_original_price_currency='USD', original_price_currency='USD', product_title='Product Title', evaluate_rate=4.5, promotion_link='http://example.com/promotion', shop_url='http://example.com/shop', shop_id=123, tags=['tag1', 'tag2'])
gpt_gs = GptGs()
gpt_gs.set_product_worksheet(product_data, 'test_category')
```

### `get_product_worksheet`

```python
def get_product_worksheet(self) -> SimpleNamespace:
    """
    Считывает данные о продукте из листа 'products'.

    Returns:
        SimpleNamespace: Объект SimpleNamespace с полями данных о продукте.

    Raises:
        ValueError: Если лист 'products' не найден.
        Exception: Если возникает ошибка при получении данных из листа.
    """
```

**Назначение**:
Чтение данных о продукте из листа `'products'` Google Sheets.

**Как работает функция**:
- Получает объект листа `'products'` из Google Sheets.
- Извлекает все значения из листа.
- Создает объект `SimpleNamespace` с данными о продукте.
- Логирует информацию об успешном чтении данных.
- Обрабатывает исключения, возникающие в процессе чтения, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
gpt_gs = GptGs()
product_data = gpt_gs.get_product_worksheet()
print(product_data.name)
```

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name:str):
    """
    Записывает данные из списка объектов SimpleNamespace в ячейки Google Sheets.

    Args:
        ns_list (List[SimpleNamespace] | SimpleNamespace): Список объектов SimpleNamespace с полями данных для записи.
    """
```

**Назначение**:
Запись данных из списка объектов `SimpleNamespace` в ячейки Google Sheets.

**Как работает функция**:
- Получает объект листа с именем `category_name` из Google Sheets.
- Итерируется по списку объектов `SimpleNamespace`.
- Извлекает данные из каждого объекта `SimpleNamespace`.
- Формирует список обновлений для записи в Google Sheets.
- Выполняет пакетное обновление данных на листе Google Sheets.
- Логирует информацию об успешной записи данных.
- Обрабатывает исключения, возникающие в процессе записи, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
# product1 = SimpleNamespace(product_id='1', product_title='Product 1', title='Title 1', local_image_path='/path/to/image1.jpg', product_video_url='http://example.com/video1.mp4', original_price=100, app_sale_price=80, target_sale_price=70)
# product2 = SimpleNamespace(product_id='2', product_title='Product 2', title='Title 2', local_image_path='/path/to/image2.jpg', product_video_url='http://example.com/video2.mp4', original_price=200, app_sale_price=160, target_sale_price=140)
# products_data = SimpleNamespace(products=[product1, product2])
# gpt_gs = GptGs()
# gpt_gs.set_products_worksheet(products_data, 'test_category')
```

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """
    Удаляет все листы из Google Sheets, кроме 'categories' и 'product_template'.
    """
```

**Назначение**:
Удаление всех листов из Google Sheets, кроме `'categories'`, `'product'`, `'category'` и `'campaign'`.

**Как работает функция**:
- Получает список всех листов в Google Sheets.
- Итерируется по списку листов.
- Удаляет каждый лист, если его заголовок не входит в список исключений (`{'categories', 'product', 'category', 'campaign'}`).
- Логирует информацию об успешном удалении листа.
- Обрабатывает исключения, возникающие в процессе удаления, логирует ошибки и пробрасывает исключение.

**Пример**:
```python
gpt_gs = GptGs()
gpt_gs.delete_products_worksheets()
```

### `save_categories_from_worksheet`

```python
def save_categories_from_worksheet(self, update:bool=False):
    """
    Сохраняет данные, отредактированные в гугл таблице.

    Args:
        update (bool, optional): Флаг, указывающий, нужно ли обновлять кампанию. По умолчанию `False`.
    """
```

**Назначение**:
Сохранение данных о категориях, отредактированных в Google Sheets.

**Как работает функция**:
- Получает отредактированные данные о категориях из Google Sheets с помощью метода `get_categories_worksheet`.
- Создает объекты `SimpleNamespace` для каждой категории на основе полученных данных.
- Устанавливает атрибут `category` объекта `campaign` равным созданному объекту `SimpleNamespace`.
- Если флаг `update` установлен в `True`, вызывает метод `update_campaign` для обновления кампании.

### `save_campaign_from_worksheet`

```python
def save_campaign_from_worksheet(self):
    """
    Сохраняет рекламную кампанию.
    """
```

**Назначение**:
Сохранение рекламной кампании из данных в Google Sheets.

**Как работает функция**:
- Сохраняет данные о категориях из Google Sheets с помощью метода `save_categories_from_worksheet`.
- Получает данные кампании из Google Sheets с помощью метода `get_campaign_worksheet`.
- Устанавливает атрибут `category` объекта `data` равным атрибуту `category` объекта `campaign`.
- Устанавливает атрибут `campaign` равным объекту `data`.
- Вызывает метод `update_campaign` для обновления кампании.