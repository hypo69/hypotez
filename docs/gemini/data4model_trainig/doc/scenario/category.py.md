## Модуль `category`

### Обзор

Модуль предназначен для работы с категориями, в основном для PrestaShop.

### Подробней

Модуль предоставляет классы для взаимодействия и обработки данных категорий товаров, особенно актуальных для PrestaShop.

## Классы

### `Category(PrestaCategoryAsync)`

**Описание**: Обработчик категорий для категорий товаров. Наследует от `PrestaCategoryAsync`.

**Наследует**: `PrestaCategoryAsync`

**Атрибуты**:

*   `credentials` (Dict): Учетные данные.

**Методы**:

*   `__init__`: Инициализирует объект `Category`.
*   `crawl_categories_async`: Асинхронно обходит категории, создавая иерархический словарь.
*   `crawl_categories`: Рекурсивно обходит категории и строит иерархический словарь.
*   `_is_duplicate_url`: Проверяет, существует ли URL уже в словаре категорий.

### `__init__`

```python
def __init__(self, api_credentials, *args, **kwargs):
    """Initializes a Category object.

    :param api_credentials: API credentials for accessing the category data.
    :param args: Variable length argument list (unused).
    :param kwargs: Keyword arguments (unused).
    """
    ...
```

**Назначение**: Инициализирует объект `Category`.

**Параметры**:

*   `api_credentials` (Dict): Учетные данные API для доступа к данным категорий.
*   `*args`: Произвольный список аргументов (не используется).
*   `**kwargs`: Произвольные аргументы ключевых слов (не используется).

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaCategoryAsync` с переданными учетными данными API.

### `crawl_categories_async`

```python
async def crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None):
    """Asynchronously crawls categories, building a hierarchical dictionary.

    :param url: The URL of the category page.
    :param depth: The depth of the crawling recursion.
    :param driver: The Selenium WebDriver instance.
    :param locator: The XPath locator for category links.
    :param dump_file: The path to the JSON file for saving results.
    :param default_category_id: The default category ID.
    :param category: (Optional) An existing category dictionary (default=None).
    :returns: The updated or new category dictionary.
    """
    ...
```

**Назначение**: Асинхронно обходит категории, строя иерархический словарь.

**Параметры**:

*   `url` (str): URL страницы категории.
*   `depth` (int): Глубина рекурсии обхода.
*   `driver` (selenium.webdriver): Экземпляр Selenium WebDriver.
*   `locator` (str): XPath-локатор для ссылок на категории.
*   `dump_file` (str): Путь к JSON-файлу для сохранения результатов.
*   `default_category_id` (str): ID категории по умолчанию.
*   `category` (dict, optional): Существующий словарь категорий (по умолчанию `None`).

**Возвращает**:

*   `dict`: Обновленный или новый словарь категорий.

**Как работает функция**:

1.  Если словарь категорий не предоставлен, создает новый.
2.  Если глубина рекурсии равна 0 или меньше, возвращает текущий словарь категорий.
3.  Использует веб-драйвер для получения URL.
4.  Ищет ссылки на категории на странице, используя указанный локатор.
5.  Рекурсивно вызывает себя для каждой найденной ссылки на категорию, уменьшая глубину рекурсии.
6.  Сохраняет иерархический словарь категорий в JSON-файл.

### `crawl_categories`

```python
def crawl_categories(self, url, depth, driver, locator, dump_file, default_category_id, category={}):
    """
    Crawls categories recursively and builds a hierarchical dictionary.

    :param url: URL of the page to crawl.
    :param depth: Depth of recursion.
    :param driver: Selenium WebDriver instance.
    :param locator: XPath locator for finding category links.
    :param dump_file: File for saving the hierarchical dictionary.
    :param id_category_default: Default category ID.
    :param category: Category dictionary (default is empty).
    :return: Hierarchical dictionary of categories and their URLs.
    """
    ...
```

**Назначение**: Рекурсивно обходит категории и строит иерархический словарь.

**Параметры**:

*   `url` (str): URL страницы для обхода.
*   `depth` (int): Глубина рекурсии.
*   `driver` (selenium.webdriver): Экземпляр Selenium WebDriver.
*   `locator` (str): XPath-локатор для поиска ссылок на категории.
*   `dump_file` (str): Файл для сохранения иерархического словаря.
*   `id_category_default` (str): ID категории по умолчанию.
*   `category` (dict, optional): Словарь категорий (по умолчанию пустой).

**Возвращает**:

*   `dict`: Иерархический словарь категорий и их URL.

**Как работает функция**:

1.  Если глубина рекурсии равна 0 или меньше, возвращает текущий словарь категорий.
2.  Использует веб-драйвер для получения URL.
3.  Ищет ссылки на категории на странице, используя указанный локатор.
4.  Рекурсивно вызывает себя для каждой найденной ссылки на категорию, уменьшая глубину рекурсии.
5.  Сохраняет иерархический словарь категорий в JSON-файл.

### `_is_duplicate_url`

```python
def _is_duplicate_url(self, category, url):
    """
    Checks if a URL already exists in the category dictionary.

    :param category: Category dictionary.
    :param url: URL to check.
    :return: True if the URL is a duplicate, False otherwise.
    """
    ...
```

**Назначение**: Проверяет, существует ли URL уже в словаре категорий.

**Параметры**:

*   `category` (dict): Словарь категорий.
*   `url` (str): URL для проверки.

**Возвращает**:

*   `bool`: `True`, если URL является дубликатом, иначе `False`.

**Как работает функция**:

1.  Проверяет, есть ли URL в значениях `'url'` словаря `category`.

### `compare_and_print_missing_keys`

```python
def compare_and_print_missing_keys(current_dict, file_path):
    """
    Compares current dictionary with data in a file and prints missing keys.
    """
    ...
```

**Назначение**: Сравнивает текущий словарь с данными в файле и выводит отсутствующие ключи.

**Параметры**:

*   `current_dict` (dict): Текущий словарь для сравнения.
*   `file_path` (str): Путь к файлу, содержащему данные для сравнения.

**Как работает функция**:

1.  Загружает данные из файла, указанного в `file_path`.
2.  Итерируется по ключам в загруженных данных.
3.  Если ключ не найден в `current_dict`, выводит его на экран.

## Зависимости

*   `asyncio`: Для асинхронных операций.
*   `pathlib`: Для работы с путями к файлам.
*   `lxml`: Для обработки HTML.
*   `requests`: Для выполнения HTTP-запросов.
*   `src.logger.logger`: Для логирования информации о процессе выполнения скрипта.
*   `src.utils.jjson`: Для загрузки и сохранения данных в формате JSON.
*   `src.endpoints.prestashop.category_async`: Для взаимодействия с PrestaShop API (асинхронно).

## Замечания

Модуль предназначен для работы с данными категорий и содержит как асинхронные, так и синхронные методы для обхода и обработки данных. Использование асинхронных методов позволяет повысить производительность при работе с большим количеством категорий.
```python
...
```
Данный код указывает на то, что в модуле есть еще не реализованная функциональность.