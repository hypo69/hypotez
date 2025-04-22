# Модуль `gsheet`

## Обзор

Модуль предназначен для работы с Google Sheets в контексте управления кампаниями AliExpress. Он предоставляет классы и методы для чтения, записи и управления данными, связанными с категориями и товарами, в Google Sheets.

## Подробней

Модуль `gsheet.py` является частью проекта `hypotez` и предназначен для интеграции с Google Sheets. Он предоставляет функциональность для чтения и записи данных, связанных с кампаниями AliExpress, в Google Sheets. Модуль включает класс `GptGs`, который наследуется от `SpreadSheet` и предоставляет методы для управления листами, очистки данных, обновления информации о кампаниях и категориях, а также для работы с данными о товарах.

## Классы

### `GptGs`

**Описание**: Класс для управления Google Sheets в рамках кампаний AliExpress.

**Наследует**:
- `SpreadSheet`: Для управления Google Sheets.

**Методы**:
- `__init__`: Инициализирует класс `GptGs` с указанным ID Google Sheets.
- `clear`: Очищает содержимое листов, связанных с продуктами, категориями и кампаниями.
- `update_chat_worksheet`: Записывает данные кампании в Google Sheets.
- `get_campaign_worksheet`: Считывает данные кампании из Google Sheets.
- `set_category_worksheet`: Записывает данные о категории в Google Sheets.
- `get_category_worksheet`: Считывает данные о категории из Google Sheets.
- `set_categories_worksheet`: Записывает данные о категориях в Google Sheets.
- `get_categories_worksheet`: Считывает данные о категориях из Google Sheets.
- `set_product_worksheet`: Записывает данные о товаре в Google Sheets.
- `get_product_worksheet`: Считывает данные о товаре из Google Sheets.
- `set_products_worksheet`: Записывает данные о товарах в Google Sheets.
- `delete_products_worksheets`: Удаляет все листы, кроме указанных (категории, шаблон продукта и т.д.).
- `save_categories_from_worksheet`: Сохраняет данные категорий из Google Sheets.
- `save_campaign_from_worksheet`: Сохраняет данные рекламной кампании из Google Sheets.

## Методы класса `GptGs`

### `__init__`

```python
def __init__(self):
    """
    Инициализирует объект класса AliCampaignGoogleSheet с указанным ID Google Sheets и дополнительными параметрами.
    """
```

**Назначение**: Инициализация экземпляра класса `GptGs`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- Отсутствует

**Как работает функция**:
- Вызывает конструктор родительского класса `SpreadSheet` с ID Google Sheets (`'1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'`).

### `clear`

```python
def clear(self):
    """
    Очищает содержимое листов.
    """
```

**Назначение**: Очистка данных в Google Sheets, удаление листов продуктов и очистка данных на листах категорий и кампаний.

**Параметры**:
- Отсутствуют

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `Exception`: В случае ошибки при очистке данных.

**Как работает функция**:
- Вызывает метод `delete_products_worksheets` для удаления листов продуктов.
- Пытается очистить листы категорий и кампаний.
- Логирует ошибки, если возникают исключения.

### `update_chat_worksheet`

```python
def update_chat_worksheet(self, data: SimpleNamespace|dict|list, conversation_name:str, language: str = None):
    """
    Записывает данные кампании в Google Sheets.
    """
```

**Назначение**: Запись данных кампании в указанный лист Google Sheets.

**Параметры**:
- `data` (SimpleNamespace | dict | list): Объект `SimpleNamespace` или словарь с данными кампании для записи.
- `conversation_name` (str): Имя листа, в который записываются данные.
- `language` (str, optional): Необязательный параметр языка.

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `Exception`: В случае ошибки при записи данных кампании.

**Как работает функция**:
- Извлекает данные из объекта `SimpleNamespace` или словаря.
- Формирует список обновлений для записи в Google Sheets.
- Выполняет пакетное обновление данных в указанном листе.
- Логирует ошибки, если возникают исключения.

### `get_campaign_worksheet`

```python
def get_campaign_worksheet(self) -> SimpleNamespace:
    """
    Считывает данные кампании из листа 'campaign'.
    """
```

**Назначение**: Чтение данных кампании из листа Google Sheets с именем 'campaign'.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace` с данными кампании.

**Вызывает исключения**:
- `ValueError`: Если лист 'campaign' не найден.
- `Exception`: В случае ошибки при чтении данных кампании.

**Как работает функция**:
- Получает лист 'campaign' из Google Sheets.
- Извлекает все значения из листа.
- Создает объект `SimpleNamespace` с данными кампании.
- Логирует информацию об успешном чтении данных.

### `set_category_worksheet`

```python
def set_category_worksheet(self, category: SimpleNamespace | str):
    """
    Записывает данные категории из объекта SimpleNamespace в Google Sheets.
    """
```

**Назначение**: Запись данных категории в лист Google Sheets с именем 'category'.

**Параметры**:
- `category` (SimpleNamespace | str): Объект `SimpleNamespace` с данными категории или имя категории.

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `TypeError`: Если передан не `SimpleNamespace` объект.
- `Exception`: В случае ошибки при записи данных категории.

**Как работает функция**:
- Проверяет, является ли `category` объектом `SimpleNamespace`.
- Подготавливает данные для вертикальной записи в Google Sheets.
- Выполняет обновление данных в листе 'category'.
- Логирует информацию об успешной записи данных.

### `get_category_worksheet`

```python
def get_category_worksheet(self) -> SimpleNamespace:
    """
    Считывает данные категории из листа 'category'.
    """
```

**Назначение**: Чтение данных категории из листа Google Sheets с именем 'category'.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace` с данными категории.

**Вызывает исключения**:
- `ValueError`: Если лист 'category' не найден.
- `Exception`: В случае ошибки при чтении данных категории.

**Как работает функция**:
- Получает лист 'category' из Google Sheets.
- Извлекает все значения из листа.
- Создает объект `SimpleNamespace` с данными категории.
- Логирует информацию об успешном чтении данных.

### `set_categories_worksheet`

```python
def set_categories_worksheet(self, categories: SimpleNamespace):
    """
    Записывает данные из объекта SimpleNamespace в Google Sheets.
    """
```

**Назначение**: Запись данных о категориях из объекта `SimpleNamespace` в лист Google Sheets с именем 'categories'.

**Параметры**:
- `categories` (SimpleNamespace): Объект `SimpleNamespace` с данными о категориях.

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `Exception`: В случае ошибки при записи данных о категориях.

**Как работает функция**:
- Итерируется по атрибутам объекта `categories`.
- Извлекает данные из каждого атрибута, который является объектом `SimpleNamespace`.
- Формирует список обновлений для записи в Google Sheets.
- Выполняет пакетное обновление данных в листе 'categories'.
- Логирует информацию об успешной записи данных для каждой категории.

### `get_categories_worksheet`

```python
def get_categories_worksheet(self) -> List[List[str]]:
    """
    Считывает данные из столбцов A-E, начиная со второй строки, из листа 'categories'.
    """
```

**Назначение**: Чтение данных о категориях из листа Google Sheets с именем 'categories'.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `List[List[str]]`: Список строк с данными из столбцов A-E.

**Вызывает исключения**:
- `ValueError`: Если лист 'categories' не найден.
- `Exception`: В случае ошибки при чтении данных о категориях.

**Как работает функция**:
- Получает лист 'categories' из Google Sheets.
- Извлекает все значения из листа.
- Извлекает данные из столбцов A-E, начиная со второй строки.
- Логирует информацию об успешном чтении данных.

### `set_product_worksheet`

```python
def set_product_worksheet(self, product: SimpleNamespace | str, category_name: str):
    """
    Записывает данные товара в новый Google Sheets.
    """
```

**Назначение**: Запись данных о товаре в новый лист Google Sheets.

**Параметры**:
- `product` (SimpleNamespace | str): Объект `SimpleNamespace` с данными товара.
- `category_name` (str): Имя категории товара.

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `Exception`: В случае ошибки при записи данных о товаре.

**Как работает функция**:
- Копирует лист 'product_template' в новый лист с именем `category_name`.
- Подготавливает заголовки столбцов.
- Извлекает данные из объекта `product`.
- Выполняет обновление данных в новом листе.
- Логирует информацию об успешной записи данных.

### `get_product_worksheet`

```python
def get_product_worksheet(self) -> SimpleNamespace:
    """
    Считывает данные о товаре из листа 'products'.
    """
```

**Назначение**: Чтение данных о товаре из листа Google Sheets с именем 'products'.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace` с данными о товаре.

**Вызывает исключения**:
- `ValueError`: Если лист 'products' не найден.
- `Exception`: В случае ошибки при чтении данных о товаре.

**Как работает функция**:
- Получает лист 'products' из Google Sheets.
- Извлекает все значения из листа.
- Создает объект `SimpleNamespace` с данными о товаре.
- Логирует информацию об успешном чтении данных.

### `set_products_worksheet`

```python
def set_products_worksheet(self, category_name:str):
    """
    Записывает данные из списка объектов SimpleNamespace в Google Sheets.
    """
```

**Назначение**: Запись данных о товарах из списка объектов `SimpleNamespace` в лист Google Sheets.

**Параметры**:
- `category_name` (str): Имя категории, для которой записываются товары.

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `Exception`: В случае ошибки при записи данных о товарах.

**Как работает функция**:
- Получает данные о товарах из атрибута `products` объекта `category`.
- Формирует список обновлений для записи в Google Sheets.
- Выполняет пакетное обновление данных в листе с именем `category_name`.
- Логирует информацию об успешной записи данных.

### `delete_products_worksheets`

```python
def delete_products_worksheets(self):
    """
    Удаляет все листы из Google Sheets, кроме 'categories' и 'product_template'.
    """
```

**Назначение**: Удаление всех листов из Google Sheets, кроме листов 'categories', 'product' ,`category` и `campaign`.

**Параметры**:
- Отсутствуют

**Возвращает**:
- Отсутствует

**Вызывает исключения**:
- `Exception`: В случае ошибки при удалении листов.

**Как работает функция**:
- Получает список всех листов в Google Sheets.
- Итерируется по листам и удаляет все, кроме 'categories', 'product',`category` и `campaign`.
- Логирует информацию об успешном удалении каждого листа.

### `save_categories_from_worksheet`

```python
def save_categories_from_worksheet(self, update:bool=False):
    """
    Сохраняет данные, отредактированные в гугл таблице.
    """
```

**Назначение**: Сохранение данных о категориях, отредактированных в Google Sheets.

**Параметры**:
- `update` (bool, optional): Флаг, указывающий, нужно ли обновлять кампанию после сохранения данных. По умолчанию `False`.

**Возвращает**:
- Отсутствует

**Как работает функция**:
- Извлекает данные о категориях из Google Sheets с помощью `self.get_categories_worksheet()`.
- Преобразует данные в объекты `SimpleNamespace`.
- Обновляет атрибут `category` объекта `self.campaign`.
- Если `update` равен `True`, вызывает метод `self.update_campaign()`.

### `save_campaign_from_worksheet`

```python
def save_campaign_from_worksheet(self):
    """
    Сохраняет рекламную кампанию.
    """
```

**Назначение**: Сохранение данных рекламной кампании из Google Sheets.

**Параметры**:
- Отсутствуют

**Возвращает**:
- Отсутствует

**Как работает функция**:
- Вызывает метод `self.save_categories_from_worksheet(False)` для сохранения данных о категориях.
- Извлекает данные кампании из Google Sheets с помощью `self.get_campaign_worksheet()`.
- Обновляет атрибут `category` объекта `data`.
- Обновляет атрибут `campaign` объекта `self`.
- Вызывает метод `self.update_campaign()`.