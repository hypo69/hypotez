# Модуль для обеспечения HTTPS

## Обзор

Модуль `ensure_https.py` предназначен для проверки и добавления префикса `https://` к URL-адресам, связанным с AliExpress. Если предоставлен идентификатор товара, модуль формирует полный URL-адрес с использованием этого идентификатора и префикса `https://`.

## Подробней

Этот модуль гарантирует, что все URL-адреса товаров AliExpress используют безопасный протокол HTTPS. Он принимает на вход как отдельные URL-адреса, так и списки URL-адресов или идентификаторов товаров. В случае, если передан идентификатор товара, модуль формирует полный URL-адрес, добавляя префикс `https://` и доменное имя AliExpress.

## Функции

### `ensure_https`

```python
def ensure_https(prod_ids: str | list[str]) -> str | list[str]:
    """ Ensures that the provided URL string(s) contain the https:// prefix.
    If the input is a product ID, it constructs a full URL with https:// prefix.

    Args:
        prod_ids (str | list[str]): A URL string or a list of URL strings to check and modify if necessary.

    Returns:
        str | list[str]: The URL string or list of URL strings with the https:// prefix.

    Raises:
        ValueError: If `prod_ids` is an instance of `WindowsPath`.

    Examples:
        >>> ensure_https("example_product_id")
        'https://www.aliexpress.com/item/example_product_id.html'

        >>> ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
        ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

        >>> ensure_https("https://www.example.com/item/example_product_id")
        'https://www.example.com/item/example_product_id'
    """
```

**Назначение**: Обеспечивает наличие префикса `https://` в предоставленной строке URL или списке URL. Если входные данные являются идентификатором товара, функция создает полный URL-адрес с префиксом `https://`.

**Параметры**:
- `prod_ids` (str | list[str]): URL-адрес или список URL-адресов для проверки и изменения при необходимости.

**Возвращает**:
- `str | list[str]`: URL-адрес или список URL-адресов с префиксом `https://`.

**Вызывает исключения**:
- `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

**Как работает функция**:
- Функция проверяет, является ли входной параметр списком или строкой.
- Если это список, функция применяет внутреннюю функцию `ensure_https_single` к каждому элементу списка.
- Если это строка, функция напрямую применяет `ensure_https_single` к этой строке.

**Внутренние функции**:

#### `ensure_https_single`

```python
 def ensure_https_single(prod_id: str) -> str:
        """ Ensures a single URL or product ID string has the https:// prefix.

        Args:
            prod_id (str): The URL or product ID string.

        Returns:
            str: The URL string with the https:// prefix.

        Raises:
            ValueError: If `prod_id` is an instance of `WindowsPath`.

        Examples:
            >>> ensure_https_single("example_product_id")
            'https://www.aliexpress.com/item/example_product_id.html'

            >>> ensure_https_single("https://www.example.com/item/example_product_id")
            'https://www.example.com/item/example_product_id'
        """
        ...
        _prod_id = extract_prod_ids(prod_id)
        if _prod_id:
            return f"https://www.aliexpress.com/item/{_prod_id}.html"
        else:
            logger.error(f"Invalid product ID or URL: {prod_id=}", exc_info=False)
            return prod_id
```

**Назначение**: Обеспечивает наличие префикса `https://` в предоставленной строке URL или идентификаторе товара.

**Параметры**:
- `prod_id` (str): URL-адрес или идентификатор товара.

**Возвращает**:
- `str`: URL-адрес с префиксом `https://`.

**Вызывает исключения**:
- `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Как работает функция**:
- Функция извлекает идентификатор товара из предоставленного URL-адреса или идентификатора товара с помощью функции `extract_prod_ids`.
- Если идентификатор товара успешно извлечен, функция формирует полный URL-адрес с префиксом `https://` и возвращает его.
- Если идентификатор товара недействителен, функция логирует ошибку и возвращает исходный URL-адрес.

**Примеры**:

```python
ensure_https("example_product_id")
# => 'https://www.aliexpress.com/item/example_product_id.html'

ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
# => ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

ensure_https("https://www.example.com/item/example_product_id")
# => 'https://www.example.com/item/example_product_id'