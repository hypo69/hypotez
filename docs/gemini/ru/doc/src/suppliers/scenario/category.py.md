# Модуль для работы с категориями, в основном для PrestaShop
## Обзор

Модуль `category.py` предназначен для работы с категориями товаров, в частности, для платформы PrestaShop. Он предоставляет классы и функции для сбора, обработки и организации данных о категориях. Основной класс `Category` наследуется от `PrestaCategoryAsync` и предоставляет методы для рекурсивного обхода категорий веб-сайта, построения иерархического словаря категорий, а также сохранения этих данных в файл. Модуль также включает функции для проверки наличия дубликатов URL-адресов и сравнения данных с файлами.

## Подробнее

Модуль предназначен для автоматизации процесса сбора и организации категорий товаров с веб-сайтов, особенно тех, которые работают на платформе PrestaShop. Он использует библиотеки `lxml`, `requests` и `Selenium` для обхода веб-страниц и извлечения информации о категориях. Собранные данные структурируются в виде иерархического словаря, который может быть сохранен в файл для дальнейшего использования.

## Классы

### `Category`

**Описание**: Класс `Category` предназначен для обработки категорий товаров. Он наследуется от класса `PrestaCategoryAsync` и предоставляет методы для обхода категорий и построения иерархической структуры.

**Наследует**: `PrestaCategoryAsync`

**Атрибуты**:
- `credentials` (Dict): Учетные данные для доступа к API.

**Методы**:
- `__init__(self, api_credentials, *args, **kwargs)`: Инициализирует объект `Category`.
- `crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None)`: Асинхронно обходит категории и строит иерархический словарь.
- `crawl_categories(self, url, depth, driver, locator, dump_file, default_category_id, category={})`: Рекурсивно обходит категории и строит иерархический словарь.
- `_is_duplicate_url(self, category, url)`: Проверяет, существует ли URL-адрес уже в словаре категорий.

## Методы класса

### `__init__`

```python
def __init__(self, api_credentials, *args, **kwargs):
    """Инициализирует объект Category.

    Args:
        api_credentials: API credentials for accessing the category data.
        args: Variable length argument list (unused).
        kwargs: Keyword arguments (unused).
    """
```

**Назначение**: Инициализирует объект класса `Category`.

**Параметры**:
- `api_credentials` (Dict): API credentials for accessing the category data.
- `*args`: Variable length argument list (unused).
- `**kwargs`: Keyword arguments (unused).

**Как работает функция**:
- Вызывает конструктор родительского класса `PrestaCategoryAsync` с переданными аргументами.

### `crawl_categories_async`

```python
async def crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None):
    """Асинхронно обходит категории, строя иерархический словарь.

    Args:
        url: URL начальной страницы для обхода.
        depth: Глубина рекурсивного обхода категорий.
        driver: Экземпляр Selenium WebDriver для управления браузером.
        locator: XPath-локатор для поиска ссылок на категории.
        dump_file: Путь к файлу для сохранения результатов обхода.
        default_category_id: ID категории по умолчанию.
        category: (Optional) Словарь категорий для добавления новых данных (по умолчанию None).

    Returns:
        The updated or new category dictionary.
    """
```

**Назначение**: Асинхронно обходит категории веб-сайта, начиная с указанного URL, и строит иерархический словарь категорий.

**Параметры**:
- `url` (str): URL начальной страницы для обхода.
- `depth` (int): Глубина рекурсивного обхода категорий.
- `driver`: Экземпляр Selenium WebDriver для управления браузером.
- `locator` (dict): XPath-локатор для поиска ссылок на категории.
- `dump_file` (str): Путь к файлу для сохранения результатов обхода.
- `default_category_id` (int): ID категории по умолчанию.
- `category` (dict, optional): Словарь категорий для добавления новых данных (по умолчанию `None`).

**Возвращает**:
- `dict`: Обновленный или новый словарь категорий.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка во время обхода категорий.

**Внутренние функции**: Отсутствуют

**Как работает функция**:
1. Инициализирует словарь категорий, если он не был передан в качестве аргумента.
2. Проверяет глубину рекурсии и, если она меньше или равна нулю, возвращает текущий словарь категорий.
3. Использует Selenium WebDriver для открытия страницы и ожидания ее загрузки.
4. Извлекает ссылки на категории с помощью указанного локатора.
5. Если ссылки не найдены, логирует ошибку и возвращает текущий словарь категорий.
6. Создает список задач для асинхронного обхода каждой найденной категории.
7. Запускает задачи асинхронно и ожидает их завершения.
8. Возвращает обновленный словарь категорий.

**Примеры**:

```python
# Пример вызова функции crawl_categories_async
# Предположим, что у вас уже есть настроенный драйвер, локатор и URL
# url = "https://example.com/categories"
# depth = 3
# driver = webdriver.Chrome()
# locator = {"by": "xpath", "selector": "//a[@class='category-link']"}
# dump_file = "categories.json"
# default_category_id = 1

# result = await category_instance.crawl_categories_async(url, depth, driver, locator, dump_file, default_category_id)
# print(result)
```

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
```

**Назначение**: Рекурсивно обходит категории веб-сайта, начиная с указанного URL, и строит иерархический словарь категорий.

**Параметры**:
- `url` (str): URL начальной страницы для обхода.
- `depth` (int): Глубина рекурсивного обхода категорий.
- `driver`: Экземпляр Selenium WebDriver для управления браузером.
- `locator` (dict): XPath-локатор для поиска ссылок на категории.
- `dump_file` (str): Путь к файлу для сохранения результатов обхода.
- `default_category_id` (int): ID категории по умолчанию.
- `category` (dict, optional): Словарь категорий для добавления новых данных (по умолчанию `{}`).

**Возвращает**:
- `dict`: Иерархический словарь категорий и их URL-адресов.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка во время обхода категорий.

**Внутренние функции**: Отсутствуют

**Как работает функция**:
1. Проверяет глубину рекурсии и, если она меньше или равна нулю, возвращает текущий словарь категорий.
2. Использует Selenium WebDriver для открытия страницы и ожидания ее загрузки.
3. Извлекает ссылки на категории с помощью указанного локатора.
4. Если ссылки не найдены, логирует ошибку и возвращает текущий словарь категорий.
5. Для каждой найденной ссылки проверяет, не является ли URL-адрес дубликатом.
6. Если URL-адрес не является дубликатом, создает новый словарь для категории и рекурсивно вызывает себя для обхода подкатегорий.
7. Загружает данные из файла дампа и объединяет их с текущим словарем категорий.
8. Сохраняет обновленный словарь категорий в файл дампа.
9. Возвращает обновленный словарь категорий.

**Примеры**:

```python
# Пример вызова функции crawl_categories
# Предположим, что у вас уже есть настроенный драйвер, локатор и URL
# url = "https://example.com/categories"
# depth = 3
# driver = webdriver.Chrome()
# locator = {"by": "xpath", "selector": "//a[@class='category-link']"}
# dump_file = "categories.json"
# default_category_id = 1

# result = category_instance.crawl_categories(url, depth, driver, locator, dump_file, default_category_id)
# print(result)
```

### `_is_duplicate_url`

```python
def _is_duplicate_url(self, category, url):
    """
    Checks if a URL already exists in the category dictionary.

    :param category: Category dictionary.
    :param url: URL to check.
    :return: True if the URL is a duplicate, False otherwise.
    """
```

**Назначение**: Проверяет, существует ли URL-адрес уже в словаре категорий.

**Параметры**:
- `category` (dict): Словарь категорий.
- `url` (str): URL-адрес для проверки.

**Возвращает**:
- `bool`: `True`, если URL-адрес является дубликатом, `False` в противном случае.

**Как работает функция**:
- Проверяет, содержится ли URL-адрес в значениях ключа 'url' в словаре категорий.

**Примеры**:

```python
# Пример вызова функции _is_duplicate_url
# category = {"Category1": {"url": "https://example.com/category1"}, "Category2": {"url": "https://example.com/category2"}}
# url = "https://example.com/category1"
# result = category_instance._is_duplicate_url(category, url)
# print(result)  # Вывод: True
```

## Функции

### `compare_and_print_missing_keys`

```python
def compare_and_print_missing_keys(current_dict, file_path):
    """
    Compares current dictionary with data in a file and prints missing keys.
    """
```

**Назначение**: Сравнивает текущий словарь с данными в файле и выводит отсутствующие ключи.

**Параметры**:
- `current_dict` (dict): Текущий словарь для сравнения.
- `file_path` (str): Путь к файлу с данными для сравнения.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при загрузке данных из файла.

**Как работает функция**:
1. Пытается загрузить данные из файла, используя функцию `j_loads`.
2. Если загрузка не удалась, логирует ошибку и завершает работу.
3. Перебирает ключи в данных, загруженных из файла.
4. Для каждого ключа проверяет, отсутствует ли он в текущем словаре.
5. Если ключ отсутствует, выводит его на экран.

**Примеры**:

```python
# Пример вызова функции compare_and_print_missing_keys
# current_dict = {"key1": "value1", "key2": "value2"}
# file_path = "data.json"
# # Предположим, что data.json содержит {"key1": "value1", "key3": "value3"}
# compare_and_print_missing_keys(current_dict, file_path)  # Вывод: key3
```