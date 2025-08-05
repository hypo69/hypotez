# Модуль для работы с категориями
====================================================

Этот модуль предоставляет классы для взаимодействия с категориями товаров, особенно с PrestaShop.

## Обзор

Модуль `category.py` определяет класс `Category`, который наследует от класса `PrestaCategoryAsync`. Он предоставляет методы для асинхронного сбора данных о категориях товаров и построения иерархического словаря категорий. 

## Классы

### `Category`

**Описание**: Класс `Category` обрабатывает информацию о категориях товаров и наследует функциональность от `PrestaCategoryAsync`.

**Наследует**:
    - `PrestaCategoryAsync`

**Атрибуты**:
    - `credentials` (Dict): Словарь с учетными данными API для доступа к данным о категориях.

**Методы**:
    - `__init__(self, api_credentials, *args, **kwargs)`: Инициализирует объект класса `Category`.
    - `crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None)`: Асинхронно перебирает категории товаров, создавая иерархический словарь.
    - `crawl_categories(self, url, depth, driver, locator, dump_file, default_category_id, category={})`: Рекурсивно перебирает категории товаров и строит иерархический словарь.
    - `_is_duplicate_url(self, category, url)`: Проверяет, существует ли URL уже в словаре категорий.

#### `__init__(self, api_credentials, *args, **kwargs)`:

**Назначение**: Инициализирует объект класса `Category` и устанавливает учетные данные API.

**Параметры**:
    - `api_credentials` (Dict): Словарь с учетными данными API.
    - `*args`: Список аргументов переменной длины (не используется).
    - `**kwargs`: Словарь с ключевыми аргументами (не используется).

**Возвращает**: None

**Вызывает исключения**: None

**Примеры**:

```python
# Инициализация объекта Category
category = Category(api_credentials={'api_key': 'YOUR_API_KEY', 'api_secret': 'YOUR_API_SECRET'})
```


#### `crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None)`:

**Назначение**: Асинхронно перебирает категории товаров, создавая иерархический словарь. 

**Параметры**:
    - `url` (str): URL страницы категории.
    - `depth` (int): Глубина рекурсивного перебора.
    - `driver` (WebDriver): Экземпляр Selenium WebDriver.
    - `locator` (Dict): XPath-локатор для поиска ссылок на категории.
    - `dump_file` (str): Путь к JSON-файлу для сохранения результатов.
    - `default_category_id` (int): Идентификатор категории по умолчанию.
    - `category` (Dict): (Опционально) Существующий словарь категорий (по умолчанию None).

**Возвращает**:
    - `Dict`: Обновленный или новый словарь категорий.

**Вызывает исключения**:
    - `Exception`: В случае ошибки во время перебора категорий.

**Пример**:

```python
# Перебор категорий с глубиной рекурсии 2
category_dict = await category.crawl_categories_async(
    url='https://www.example.com/category-page',
    depth=2,
    driver=driver,
    locator={'by': 'XPATH', 'selector': '//a[contains(@href, "/category")]'},
    dump_file='categories.json',
    default_category_id=1
)
```


#### `crawl_categories(self, url, depth, driver, locator, dump_file, default_category_id, category={})`

**Назначение**: Рекурсивно перебирает категории товаров и строит иерархический словарь.

**Параметры**:
    - `url` (str): URL страницы, с которой начинается перебор.
    - `depth` (int): Глубина рекурсивного перебора.
    - `driver` (WebDriver): Экземпляр Selenium WebDriver.
    - `locator` (Dict): XPath-локатор для поиска ссылок на категории.
    - `dump_file` (str): Путь к JSON-файлу для сохранения результатов.
    - `id_category_default` (int): Идентификатор категории по умолчанию.
    - `category` (Dict): Словарь категорий (по умолчанию пустой словарь).

**Возвращает**:
    - `Dict`: Иерархический словарь категорий и их URL-адресов.

**Вызывает исключения**:
    - `Exception`: В случае ошибки во время перебора категорий.

**Пример**:

```python
# Перебор категорий с глубиной рекурсии 2
category_dict = category.crawl_categories(
    url='https://www.example.com/category-page',
    depth=2,
    driver=driver,
    locator={'by': 'XPATH', 'selector': '//a[contains(@href, "/category")]'},
    dump_file='categories.json',
    default_category_id=1
)
```


#### `_is_duplicate_url(self, category, url)`

**Назначение**: Проверяет, существует ли URL уже в словаре категорий.

**Параметры**:
    - `category` (Dict): Словарь категорий.
    - `url` (str): URL-адрес для проверки.

**Возвращает**:
    - `bool`: True, если URL является дубликатом, иначе False.

**Вызывает исключения**: None

**Пример**:

```python
# Проверка, является ли URL дубликатом
is_duplicate = category._is_duplicate_url(
    category={'category1': {'url': 'https://www.example.com/category1'}},
    url='https://www.example.com/category1'
)

# is_duplicate = True
```

## Функции

### `compare_and_print_missing_keys(current_dict, file_path)`

**Назначение**: Сравнивает текущий словарь с данными в файле и печатает отсутствующие ключи.

**Параметры**:
    - `current_dict` (Dict): Текущий словарь.
    - `file_path` (str): Путь к файлу.

**Возвращает**: None

**Вызывает исключения**:
    - `Exception`: В случае ошибки при загрузке данных из файла.

**Пример**:

```python
# Сравнение словаря с файлом
compare_and_print_missing_keys(
    current_dict={'name': 'Alice', 'age': 30},
    file_path='data.json'
)

# Вывод:
# age
```

## Примеры

```python
# Инициализация объекта Category
category = Category(api_credentials={'api_key': 'YOUR_API_KEY', 'api_secret': 'YOUR_API_SECRET'})

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Перебор категорий асинхронно с глубиной рекурсии 2
category_dict = await category.crawl_categories_async(
    url='https://www.example.com/category-page',
    depth=2,
    driver=driver,
    locator={'by': 'XPATH', 'selector': '//a[contains(@href, "/category")]'},
    dump_file='categories.json',
    default_category_id=1
)

# Перебор категорий с глубиной рекурсии 2
category_dict = category.crawl_categories(
    url='https://www.example.com/category-page',
    depth=2,
    driver=driver,
    locator={'by': 'XPATH', 'selector': '//a[contains(@href, "/category")]'},
    dump_file='categories.json',
    default_category_id=1
)

# Сравнение словаря с файлом
compare_and_print_missing_keys(
    current_dict={'name': 'Alice', 'age': 30},
    file_path='data.json'
)
```