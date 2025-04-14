# Модуль `ensure_https`

## Обзор

Модуль `ensure_https` предназначен для обеспечения наличия префикса `https://` в предоставленных URL или идентификаторах продуктов. Если на вход передается идентификатор продукта, модуль конструирует полный URL с префиксом `https://`.

## Подробнее

Этот модуль полезен для обработки URL, полученных из различных источников, где не всегда гарантируется наличие безопасного протокола `https`. Он также включает функциональность для извлечения идентификатора продукта из URL.

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

**Назначение**: Обеспечивает, чтобы предоставленные URL или идентификаторы продуктов содержали префикс `https://`. Если входные данные являются идентификатором продукта, функция создает полный URL с префиксом `https://`.

**Параметры**:
- `prod_ids` (str | list[str]): URL или список URL для проверки и изменения при необходимости.

**Возвращает**:
- `str | list[str]`: URL или список URL с префиксом `https://`.

**Вызывает исключения**:
- `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

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
```

**Назначение**: Обеспечивает, чтобы отдельный URL или идентификатор продукта содержал префикс `https://`.

**Параметры**:
- `prod_id` (str): URL или идентификатор продукта.

**Возвращает**:
- `str`: URL с префиксом `https://`.

**Вызывает исключения**:
- `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Как работает функция `ensure_https`**:

1. **Проверка типа входных данных**: Функция проверяет, является ли `prod_ids` списком или строкой.
2. **Обработка списка URL**: Если `prod_ids` является списком, функция применяет функцию `ensure_https_single` к каждому элементу списка и возвращает новый список с обработанными URL.
3. **Обработка одного URL**: Если `prod_ids` является строкой, функция вызывает `ensure_https_single` для обработки этой строки и возвращает результат.

**Как работает функция `ensure_https_single`**:

1. **Извлечение идентификатора продукта**: Функция вызывает `extract_prod_ids(prod_id)` для извлечения идентификатора продукта из предоставленной строки.
2. **Формирование URL**: Если идентификатор продукта успешно извлечен, функция формирует URL в формате `https://www.aliexpress.com/item/{_prod_id}.html` и возвращает его.
3. **Обработка ошибок**: Если извлечение идентификатора продукта не удалось (например, если `prod_id` не является допустимым URL или идентификатором), функция логирует ошибку с использованием `logger.error` и возвращает исходную строку `prod_id` без изменений.

**Примеры**:

```python
from src.suppliers.aliexpress.utils.ensure_https import ensure_https
# Пример 1: Обработка идентификатора продукта
product_id = "1234567890"
secure_url = ensure_https(product_id)
print(secure_url)  # Вывод: https://www.aliexpress.com/item/1234567890.html

# Пример 2: Обработка URL с http
url = "http://www.aliexpress.com/item/1234567890.html"
secure_url = ensure_https(url)
print(secure_url)  # Вывод: http://www.aliexpress.com/item/1234567890.html

# Пример 3: Обработка списка URL
urls = ["1234567890", "http://www.aliexpress.com/item/0987654321.html"]
secure_urls = ensure_https(urls)
print(secure_urls)
# Вывод: ['https://www.aliexpress.com/item/1234567890.html', 'http://www.aliexpress.com/item/0987654321.html']

# Пример 4: Обработка URL с https
https_url = "https://www.aliexpress.com/item/1234567890.html"
secure_url = ensure_https(https_url)
print(secure_url)  # Вывод: https://www.aliexpress.com/item/1234567890.html