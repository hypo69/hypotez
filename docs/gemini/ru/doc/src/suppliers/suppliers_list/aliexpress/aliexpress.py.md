# Модуль AliExpress

## Обзор

Модуль `aliexpress` предоставляет класс `Aliexpress`, который интегрирует функциональность из `Supplier`, `AliRequests` и `AliApi` для работы с AliExpress.

## Подробнее

Модуль `aliexpress` используется для взаимодействия с платформой AliExpress, предоставляя функциональность для:

- Загрузки данных товаров (имена, описания, изображения, цены) с помощью `AliRequests` и `AliApi`.
- Обработки данных товаров с использованием класса `Supplier`.
- Взаимодействия с веб-браузером с помощью Selenium WebDriver, если это необходимо.

## Классы

### `Aliexpress`

**Описание**: Основной класс для работы с AliExpress. Комбинирует функциональность из `Supplier`, `AliRequests` и `AliApi` для удобства взаимодействия с платформой.

**Наследует**: `AliRequests`, `AliApi`

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика, используемый для идентификации AliExpress. По умолчанию установлен в `'aliexpress'`.
- `locale` (dict): Словарь, содержащий настройки языка и валюты.

**Методы**:

- `__init__(self, webdriver: bool | str = False, locale: str | dict = {'EN': 'USD'}, *args, **kwargs)`: Инициализирует класс `Aliexpress`.

    **Параметры**:

    - `webdriver` (bool | str, optional): Указывает режим использования Selenium WebDriver. Возможные значения:
        - `False` (по умолчанию): WebDriver не используется.
        - `'chrome'`: Используется Chrome WebDriver.
        - `'mozilla'`: Используется Mozilla WebDriver.
        - `'edge'`: Используется Edge WebDriver.
        - `'default'`: Используется WebDriver по умолчанию для системы.
    - `locale` (str | dict, optional): Настройки языка и валюты. По умолчанию используется словарь `{'EN': 'USD'}`.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `None`

    **Примеры**:

    ```python
    # Запуск без WebDriver
    a = Aliexpress()

    # Запуск с Chrome WebDriver
    a = Aliexpress('chrome')
    ```

- `parse_items_from_html(self, html: str, *args, **kwargs) -> dict | None`: Парсинг HTML-кода для извлечения данных о товарах.

    **Параметры**:

    - `html` (str): HTML-код, полученный с AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товарах или `None` в случае ошибки.

    **Примеры**:

    ```python
    html = """
    <html>
        <body>
            <div class="item">
                <div class="name">Товар 1</div>
                <div class="price">100 USD</div>
            </div>
            <div class="item">
                <div class="name">Товар 2</div>
                <div class="price">200 USD</div>
            </div>
        </body>
    </html>
    """
    items = a.parse_items_from_html(html)
    ```

- `get_items_by_url(self, url: str, *args, **kwargs) -> dict | None`: Получение данных о товарах с помощью URL.

    **Параметры**:

    - `url` (str): URL-адрес страницы с товарами на AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товарах или `None` в случае ошибки.

    **Примеры**:

    ```python
    url = 'https://www.aliexpress.com/wholesale?SearchText=phone'
    items = a.get_items_by_url(url)
    ```

- `get_item_by_id(self, id: str, *args, **kwargs) -> dict | None`: Получение данных о товаре по его ID.

    **Параметры**:

    - `id` (str): ID товара на AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товаре или `None` в случае ошибки.

    **Примеры**:

    ```python
    id = '1234567890'
    item = a.get_item_by_id(id)
    ```

- `get_items_by_keywords(self, keywords: str, *args, **kwargs) -> dict | None`: Получение данных о товарах по ключевым словам.

    **Параметры**:

    - `keywords` (str): Ключевые слова для поиска товаров на AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товарах или `None` в случае ошибки.

    **Примеры**:

    ```python
    keywords = 'phone case'
    items = a.get_items_by_keywords(keywords)
    ```

- `get_items_by_category(self, category: str, *args, **kwargs) -> dict | None`: Получение данных о товарах по категории.

    **Параметры**:

    - `category` (str): Категория товаров на AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товарах или `None` в случае ошибки.

    **Примеры**:

    ```python
    category = 'Phones & Telecommunications'
    items = a.get_items_by_category(category)
    ```

- `get_items_by_store(self, store_id: str, *args, **kwargs) -> dict | None`: Получение данных о товарах из конкретного магазина.

    **Параметры**:

    - `store_id` (str): ID магазина на AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товарах или `None` в случае ошибки.

    **Примеры**:

    ```python
    store_id = '1234567890'
    items = a.get_items_by_store(store_id)
    ```

- `get_reviews(self, item_id: str, *args, **kwargs) -> dict | None`: Получение отзывов к товару по его ID.

    **Параметры**:

    - `item_id` (str): ID товара на AliExpress.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с отзывами к товару или `None` в случае ошибки.

    **Примеры**:

    ```python
    item_id = '1234567890'
    reviews = a.get_reviews(item_id)
    ```

## Примеры

**Пример 1**: Получение данных о товарах с помощью ключевых слов

```python
from src.suppliers.suppliers_list.aliexpress import Aliexpress

# Создание экземпляра класса Aliexpress
a = Aliexpress()

# Получение данных о товарах по ключевым словам
keywords = 'phone case'
items = a.get_items_by_keywords(keywords)

# Вывод результатов
print(items)
```

**Пример 2**: Получение данных о товаре по ID

```python
from src.suppliers.suppliers_list.aliexpress import Aliexpress

# Создание экземпляра класса Aliexpress
a = Aliexpress()

# Получение данных о товаре по ID
id = '1234567890'
item = a.get_item_by_id(id)

# Вывод результатов
print(item)
```

**Пример 3**: Получение данных о товарах из конкретного магазина

```python
from src.suppliers.suppliers_list.aliexpress import Aliexpress

# Создание экземпляра класса Aliexpress
a = Aliexpress()

# Получение данных о товарах из конкретного магазина
store_id = '1234567890'
items = a.get_items_by_store(store_id)

# Вывод результатов
print(items)
```

## Внутренние функции

- `_parse_html(self, html: str, *args, **kwargs) -> dict | None`: Внутренняя функция для парсинга HTML-кода.

    **Параметры**:

    - `html` (str): HTML-код для парсинга.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с результатами парсинга или `None` в случае ошибки.

- `_get_items_from_html(self, html: str, *args, **kwargs) -> dict | None`: Внутренняя функция для извлечения данных о товарах из HTML-кода.

    **Параметры**:

    - `html` (str): HTML-код для извлечения данных.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товарах или `None` в случае ошибки.

- `_get_item_from_html(self, html: str, *args, **kwargs) -> dict | None`: Внутренняя функция для извлечения данных о конкретном товаре из HTML-кода.

    **Параметры**:

    - `html` (str): HTML-код для извлечения данных.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о товаре или `None` в случае ошибки.

- `_get_reviews_from_html(self, html: str, *args, **kwargs) -> dict | None`: Внутренняя функция для извлечения отзывов к товару из HTML-кода.

    **Параметры**:

    - `html` (str): HTML-код для извлечения отзывов.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с отзывами к товару или `None` в случае ошибки.

- `_get_store_data_from_html(self, html: str, *args, **kwargs) -> dict | None`: Внутренняя функция для извлечения данных о магазине из HTML-кода.

    **Параметры**:

    - `html` (str): HTML-код для извлечения данных.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о магазине или `None` в случае ошибки.

- `_get_category_data_from_html(self, html: str, *args, **kwargs) -> dict | None`: Внутренняя функция для извлечения данных о категории из HTML-кода.

    **Параметры**:

    - `html` (str): HTML-код для извлечения данных.
    - `*args`: Дополнительные позиционные аргументы.
    - `**kwargs`: Дополнительные именованные аргументы.

    **Возвращает**: `dict | None`: Словарь с данными о категории или `None` в случае ошибки.

## Параметры класса

- `webdriver` (bool | str): Указывает режим использования Selenium WebDriver. Возможные значения:
    - `False`: WebDriver не используется.
    - `'chrome'`: Используется Chrome WebDriver.
    - `'mozilla'`: Используется Mozilla WebDriver.
    - `'edge'`: Используется Edge WebDriver.
    - `'default'`: Используется WebDriver по умолчанию для системы.

- `locale` (dict): Словарь, содержащий настройки языка и валюты.

- `supplier_prefix` (str): Префикс поставщика, используемый для идентификации AliExpress. По умолчанию установлен в `'aliexpress'`.

## Как работает класс

Класс `Aliexpress` предоставляет функциональность для взаимодействия с AliExpress, комбинируя функциональность из `Supplier`, `AliRequests` и `AliApi`. Он позволяет:

- Получать данные о товарах с AliExpress с использованием `AliRequests` и `AliApi`.
- Парсить HTML-код для извлечения данных о товарах.
- Выполнять поиск товаров по ключевым словам, категории, магазину или ID.
- Получать отзывы к товару.

## Дополнительные замечания

- Модуль `aliexpress` использует Selenium WebDriver для автоматизации взаимодействия с веб-браузером, если это необходимо.
- Класс `Aliexpress` наследует функциональность из `AliRequests` и `AliApi`, предоставляя удобный интерфейс для работы с AliExpress.
- Для использования модуля `aliexpress` необходимо установить необходимые зависимости, включая `selenium`, `requests`, `fake_useragent` и другие.