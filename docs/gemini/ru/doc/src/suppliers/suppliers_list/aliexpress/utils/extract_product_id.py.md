# Модуль для извлечения идентификаторов товаров из URL-адресов AliExpress

## Обзор

Модуль предназначен для извлечения идентификаторов товаров (product IDs) из URL-адресов сайта AliExpress. Он предоставляет функцию, способную обрабатывать как отдельные URL, так и списки URL-адресов, извлекая или проверяя идентификаторы товаров.

## Подробней

Модуль содержит функцию `extract_prod_ids`, которая использует регулярные выражения для поиска и извлечения идентификаторов товаров из URL-адресов AliExpress. Если передан список URL-адресов, функция возвращает список извлеченных идентификаторов. Если передан один URL, функция возвращает один извлеченный идентификатор. Если идентификатор не найден, функция возвращает `None`.

## Функции

### `extract_prod_ids`

**Назначение**: Извлечение идентификаторов товаров из списка URL-адресов или проверка идентификатора товара.

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
    # Regular expression to find product identifiers
    pattern = re.compile(r"(?:item/|/)?(\\d+)\\.html")

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
        # Check if the input is a valid product ID
        if url.isdigit():
            return url

        # Otherwise, try to extract the ID from the URL
        match = pattern.search(url)
        if match:
            return match.group(1)
        return

    if isinstance(urls, list):
        extracted_ids = [extract_id(url) for url in urls if extract_id(url) is not None]
        return extracted_ids if extracted_ids else None
    else:
        return extract_id(urls)
```

**Параметры**:

-   `urls` (str | list[str]): URL-адрес или список URL-адресов для извлечения ID товаров.

**Возвращает**:

-   `str | list[str] | None`: Список извлеченных ID товаров, отдельный ID, или `None`, если не найдено ни одного допустимого ID.

**Как работает функция**:

1.  Определяется регулярное выражение `pattern` для поиска идентификаторов товаров в URL-адресах.
2.  Определяется внутренняя функция `extract_id`, которая извлекает ID из одного URL-адреса.
    *   Функция `extract_id` проверяет, является ли входная строка допустимым ID товара (состоит только из цифр). Если да, то возвращает эту строку.
    *   Если входная строка не является допустимым ID, функция пытается извлечь ID из URL-адреса с помощью регулярного выражения.
    *   Если ID успешно извлечен, функция возвращает его, иначе возвращает `None`.
3.  Если `urls` является списком, то функция применяет `extract_id` к каждому элементу списка и возвращает список извлеченных ID.
4.  Если `urls` не является списком, то функция применяет `extract_id` к `urls` и возвращает результат.

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
    # Check if the input is a valid product ID
    if url.isdigit():
        return url

    # Otherwise, try to extract the ID from the URL
    match = pattern.search(url)
    if match:
        return match.group(1)
    return
```

**Назначение**: Извлечение идентификатора товара из заданного URL или проверка идентификатора товара.

**Параметры**:

-   `url` (str): URL-адрес или ID товара.

**Возвращает**:

-   `str | None`: Извлеченный ID товара или входные данные, если они являются допустимым ID, или `None`, если допустимый ID не найден.

**Как работает функция**:

1.  Проверяет, является ли входная строка числом. Если да, то возвращает эту строку как ID товара.
2.  Если входная строка не является числом, пытается извлечь ID из URL с помощью регулярного выражения.
3.  Если ID успешно извлечен, функция возвращает его.
4.  Если ID не найден, функция возвращает `None`.

**Примеры**:

```python
extract_prod_ids("https://www.aliexpress.com/item/123456.html")
# => '123456'

extract_prod_ids(["https://www.aliexpress.com/item/123456.html", "7891011.html"])
# => ['123456', '7891011']

extract_prod_ids(["https://www.example.com/item/123456.html", "https://www.example.com/item/abcdef.html"])
# => ['123456']

extract_prod_ids("7891011")
# => '7891011'

extract_prod_ids("https://www.example.com/item/abcdef.html")
# => None