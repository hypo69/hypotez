# Модуль для извлечения ID продуктов из URL-адресов AliExpress

## Обзор

Модуль `extract_product_id.py` предназначен для извлечения идентификаторов (ID) товаров из URL-адресов страниц товаров AliExpress. Он предоставляет функцию, которая может принимать как один URL, так и список URL-ов, а также напрямую принимать ID товаров. Модуль использует регулярные выражения для поиска и извлечения ID из URL-ов и возвращает извлеченные ID в виде списка или строки.
Для логирования событий используется модуль `logger` из `src.logger.logger`.

## Подробней

Этот модуль облегчает процесс автоматического извлечения ID товаров из различных источников, таких как результаты поиска, списки товаров или другие веб-страницы. Он может быть полезен для сбора данных о товарах, мониторинга цен, отслеживания изменений в ассортименте и других задач, связанных с анализом данных AliExpress.

## Функции

### `extract_prod_ids`

```python
def extract_prod_ids(urls: str | list[str]) -> str | list[str] | None:
    """ Extracts item IDs from a list of URLs or directly returns IDs if given.

    Args:
        urls (str | list[str]): A URL, a list of URLs, or product IDs.

    Returns:
        str | list[str] | None: A list of extracted item IDs, a single ID, or `None` if no valid ID is found.

    Examples:
        >>> extract_prod_ids("https://www.aliexpress.com/item/123456.html")
        '123456'

        >>> extract_prod_ids(["https://www.aliexpress.com/item/123456.html", "7891011.html"])
        ['123456', '7891011']

        >>> extract_prod_ids(["https://www.example.com/item/123456.html", "https://www.example.com/item/abcdef.html"])
        ['123456']

        >>> extract_prod_ids("7891011")
        '7891011'

        >>> extract_prod_ids("https://www.example.com/item/abcdef.html")
        None
    """
    ...
```

**Назначение**: Извлекает ID товаров из списка URL-адресов или возвращает ID, если он предоставлен напрямую.

**Параметры**:
- `urls` (str | list[str]): URL-адрес, список URL-адресов или ID товара.

**Возвращает**:
- `str | list[str] | None`: Список извлеченных ID товаров, один ID или `None`, если не найдено ни одного допустимого ID.

**Как работает функция**:

1.  **Определение регулярного выражения**: Функция инициализирует регулярное выражение `pattern` для поиска идентификаторов продуктов в URL-адресах.
2.  **Вложенная функция `extract_id`**: Определяется функция `extract_id`, которая пытается извлечь ID из одного URL-адреса.
3.  **Проверка входных данных**: Проверяется, является ли входное значение списком или строкой.
4.  **Обработка списка URL-адресов**: Если входные данные - это список, функция применяет `extract_id` к каждому URL-адресу в списке, фильтруя `None` значения.
5.  **Обработка одного URL-адреса**: Если входные данные - это строка, функция напрямую вызывает `extract_id` для извлечения ID.
6.  **Возврат результата**: Функция возвращает список извлеченных ID (если входные данные - список) или один ID (если входные данные - строка). Если ID не найден, возвращается `None`.

**Внутренние функции**:

### `extract_id`

```python
def extract_id(url: str) -> str | None:
    """ Extracts a product ID from a given URL or validates a product ID.

    Args:
        url (str): The URL or product ID.

    Returns:
        str | None: The extracted product ID or the input itself if it's a valid ID, or `None` if no valid ID is found.

    Examples:
        >>> extract_id("https://www.aliexpress.com/item/123456.html")
        '123456'

        >>> extract_id("7891011")
        '7891011'

        >>> extract_id("https://www.example.com/item/abcdef.html")
        None
    """
    ...
```

**Назначение**: Извлекает ID товара из заданного URL-адреса или проверяет ID товара.

**Параметры**:
- `url` (str): URL-адрес или ID товара.

**Возвращает**:
- `str | None`: Извлеченный ID товара или сам ввод, если это допустимый ID, или `None`, если не найден допустимый ID.

**Как работает функция**:

1.  **Проверка на число**: Сначала функция проверяет, является ли входная строка `url` числом с помощью метода `isdigit()`.
2.  **Извлечение ID из URL**: Если `url` не является числом, функция пытается извлечь ID товара из URL-адреса, используя регулярное выражение `pattern.search(url)`.
3.  **Возврат результата**: Если `url` является числом, функция возвращает `url` как ID товара. Если ID успешно извлечен из URL-адреса, функция возвращает извлеченный ID. В противном случае возвращает `None`.

**ASCII flowchart функции `extract_prod_ids`**:

```
    Начало
    │
    ├───> Проверка: Входные данные - список?
    │     ├─── ДА ───> Применить extract_id к каждому URL в списке
    │     │            │
    │     │            └───> Фильтрация None значений
    │     │            │
    │     │            └───> Возврат списка извлеченных ID
    │     │
    │     └─── НЕТ ───> Вызов extract_id для одного URL
    │                  │
    │                  └───> Возврат ID или None
    │
    └───> Конец
```

**Примеры**:

```python
>>> extract_prod_ids("https://www.aliexpress.com/item/123456.html")
'123456'

>>> extract_prod_ids(["https://www.aliexpress.com/item/123456.html", "7891011.html"])
['123456', '7891011']

>>> extract_prod_ids(["https://www.example.com/item/123456.html", "https://www.example.com/item/abcdef.html"])
['123456']

>>> extract_prod_ids("7891011")
'7891011'

>>> extract_prod_ids("https://www.example.com/item/abcdef.html")
None