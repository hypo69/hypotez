# Модуль для работы с категориями, в основном для PrestaShop
## Обзор

Модуль предоставляет классы для взаимодействия и обработки данных категорий товаров, что особенно актуально для PrestaShop.

## Подробнее

Этот модуль предназначен для обработки категорий товаров, что особенно важно для PrestaShop. Он включает в себя функциональность для обхода категорий, создания иерархических структур данных и сохранения этих структур в файлы. Модуль использует асинхронные операции для повышения эффективности, особенно при работе с большим количеством категорий.

## Классы

### `Category(PrestaCategoryAsync)`

**Описание**: Класс `Category` предназначен для обработки категорий товаров. Он наследуется от класса `PrestaCategoryAsync` и расширяет его функциональность.

**Наследует**:

-   `PrestaCategoryAsync`: Предоставляет асинхронные методы для взаимодействия с категориями PrestaShop.

**Атрибуты**:

-   `credentials` (Dict): Учетные данные API для доступа к данным категорий.

**Методы**:

-   `__init__(self, api_credentials, *args, **kwargs)`: Инициализирует объект `Category`.
-   `crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None)`: Асинхронно обходит категории, строя иерархический словарь.
-   `crawl_categories(self, url, depth, driver, locator, dump_file, id_category_default, category={})`: Рекурсивно обходит категории и строит иерархический словарь.
-   `_is_duplicate_url(self, category, url)`: Проверяет, существует ли URL уже в словаре категорий.

### `__init__(self, api_credentials, *args, **kwargs)`

```python
def __init__(self, api_credentials, *args, **kwargs):
    """Инициализирует объект Category.

    Args:
        api_credentials: API credentials for accessing the category data.
        args: Variable length argument list (unused).
        kwargs: Keyword arguments (unused).
    """
```

**Назначение**: Инициализирует объект `Category`, вызывая конструктор родительского класса `PrestaCategoryAsync`.

**Параметры**:

-   `api_credentials` (any): Учетные данные API для доступа к данным категорий.
-   `*args`: Переменное количество позиционных аргументов (не используется).
-   `**kwargs`: Переменное количество именованных аргументов (не используется).

**Возвращает**:

-   None

**Вызывает исключения**:

-   Не вызывает исключений.

### `crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None)`

```python
async def crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None):
    """Асинхронно обходит категории, строя иерархический словарь.

    Args:
        url: The URL of the category page.
        depth: The depth of the crawling recursion.
        driver: The Selenium WebDriver instance.
        locator: The XPath locator for category links.
        dump_file: The path to the JSON file for saving results.
        default_category_id: The default category ID.
        category: (Optional) An existing category dictionary (default=None).
    Returns:
        The updated or new category dictionary.
    """
```

**Назначение**: Асинхронно обходит категории, начиная с указанного URL, и строит иерархический словарь, представляющий структуру категорий.

**Параметры**:

-   `url` (str): URL страницы категории для начала обхода.
-   `depth` (int): Глубина рекурсии обхода категорий.
-   `driver` (WebDriver): Инстанс Selenium WebDriver для управления браузером.
-   `locator` (dict): XPath-локатор для поиска ссылок на категории.
-   `dump_file` (str): Путь к JSON-файлу для сохранения результатов.
-   `default_category_id` (int): ID категории по умолчанию.
-   `category` (dict, optional): Существующий словарь категорий (по умолчанию `None`).

**Возвращает**:

-   dict: Обновленный или новый словарь категорий.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка во время обхода категорий.

**Как работает функция**:

1.  Если `category` не предоставлен, создается новый словарь для корневой категории.
2.  Если глубина рекурсии (`depth`) равна или меньше 0, возвращает текущую категорию.
3.  Использует `driver.get(url)` для открытия URL в браузере.
4.  Ожидает загрузки страницы в течение 1 секунды.
5.  Использует `driver.execute_locator(locator)` для поиска ссылок на категории на странице.
6.  Если ссылки не найдены, логирует ошибку и возвращает текущую категорию.
7.  Создает список асинхронных задач для обхода каждой найденной категории.
8.  Использует `asyncio.gather(*tasks)` для параллельного выполнения задач обхода категорий.
9.  Возвращает обновленный словарь категорий.

**Примеры**:

```python
# Пример вызова функции crawl_categories_async
# api_credentials = {...}
# driver = Driver(Chrome)
# locator = {"by": "xpath", "selector": "//a[@class='category-link']"}
# dump_file = "categories.json"
# default_category_id = 2
# category = await Category(api_credentials).crawl_categories_async("https://example.com/category", 2, driver, locator, dump_file, default_category_id)
```

### `crawl_categories(self, url, depth, driver, locator, dump_file, id_category_default, category={})`

```python
def crawl_categories(self, url, depth, driver, locator, dump_file, id_category_default, category={}):
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
```

**Назначение**: Рекурсивно обходит категории, начиная с указанного URL, и строит иерархический словарь, представляющий структуру категорий.

**Параметры**:

-   `url` (str): URL страницы категории для начала обхода.
-   `depth` (int): Глубина рекурсии обхода категорий.
-   `driver` (WebDriver): Инстанс Selenium WebDriver для управления браузером.
-   `locator` (dict): XPath-локатор для поиска ссылок на категории.
-   `dump_file` (str): Путь к JSON-файлу для сохранения результатов.
-   `id_category_default` (int): ID категории по умолчанию.
-   `category` (dict, optional): Существующий словарь категорий (по умолчанию пустой словарь).

**Возвращает**:

-   dict: Иерархический словарь категорий и их URL.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка во время обхода категорий.

**Как работает функция**:

1.  Если глубина рекурсии (`depth`) равна или меньше 0, возвращает текущую категорию.
2.  Использует `driver.get(url)` для открытия URL в браузере.
3.  Использует `driver.wait(1)` для ожидания загрузки страницы в течение 1 секунды.
4.  Использует `driver.execute_locator(locator)` для поиска ссылок на категории на странице.
5.  Если ссылки не найдены, логирует ошибку и возвращает текущую категорию.
6.  Для каждой найденной ссылки на категорию:
    -   Проверяет, не является ли URL дубликатом с помощью `self._is_duplicate_url(category, link_url)`.
    -   Если URL не является дубликатом, создает новый словарь для категории.
    -   Рекурсивно вызывает `self.crawl_categories` для обхода подкатегорий.
7.  Загружает данные из файла дампа с помощью `j_loads(dump_file)`.
8.  Обновляет словарь категорий данными из файла дампа.
9.  Сохраняет обновленный словарь категорий в файл дампа с помощью `j_dumps(category, dump_file)`.
10. Возвращает обновленный словарь категорий.

**Примеры**:

```python
# Пример вызова функции crawl_categories
# api_credentials = {...}
# driver = Driver(Chrome)
# locator = {"by": "xpath", "selector": "//a[@class='category-link']"}
# dump_file = "categories.json"
# id_category_default = 2
# category = Category(api_credentials).crawl_categories("https://example.com/category", 2, driver, locator, dump_file, id_category_default)
```

### `_is_duplicate_url(self, category, url)`

```python
def _is_duplicate_url(self, category, url):
    """
    Checks if a URL already exists in the category dictionary.

    :param category: Category dictionary.
    :param url: URL to check.
    :return: True if the URL is a duplicate, False otherwise.
    """
```

**Назначение**: Проверяет, существует ли URL уже в словаре категорий.

**Параметры**:

-   `category` (dict): Словарь категорий.
-   `url` (str): URL для проверки.

**Возвращает**:

-   bool: `True`, если URL является дубликатом, `False` в противном случае.

**Вызывает исключения**:

-   Не вызывает исключений.

**Как работает функция**:

1.  Проверяет, содержится ли URL в значениях ключа `'url'` словаря `category`.
2.  Возвращает `True`, если URL найден, и `False` в противном случае.

**Примеры**:

```python
# Пример вызова функции _is_duplicate_url
# category = {"category1": {"url": "https://example.com/category1"}, "category2": {"url": "https://example.com/category2"}}
# url = "https://example.com/category1"
# is_duplicate = Category(...)._is_duplicate_url(category, url)
# print(is_duplicate)  # Вывод: True
```

## Функции

### `compare_and_print_missing_keys(current_dict, file_path)`

```python
def compare_and_print_missing_keys(current_dict, file_path):
    """
    Compares current dictionary with data in a file and prints missing keys.
    """
```

**Назначение**: Сравнивает текущий словарь с данными в файле и выводит недостающие ключи.

**Параметры**:

-   `current_dict` (dict): Текущий словарь для сравнения.
-   `file_path` (str): Путь к файлу, содержащему данные для сравнения.

**Возвращает**:

-   None

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при загрузке данных из файла.

**Как работает функция**:

1.  Пытается загрузить данные из файла, используя `j_loads(file_path)`.
2.  Если возникает ошибка при загрузке данных, логирует ошибку и возвращает `None`.
3.  Для каждого ключа в данных из файла проверяет, отсутствует ли он в `current_dict`.
4.  Если ключ отсутствует в `current_dict`, выводит его на экран.

**Примеры**:

```python
# Пример вызова функции compare_and_print_missing_keys
# current_dict = {"key1": "value1", "key2": "value2"}
# file_path = "data.json"
# with open(file_path, "w") as f:
#     json.dump({"key1": "value1", "key2": "value2", "key3": "value3"}, f)
# compare_and_print_missing_keys(current_dict, file_path)  # Вывод: key3