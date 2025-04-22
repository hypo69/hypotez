# Модуль `ensure_https`

## Обзор

Модуль `ensure_https` предназначен для обеспечения наличия префикса `https://` в предоставленных URL или ID товаров. Если входные данные являются ID товара, модуль формирует полный URL с использованием префикса `https://`.

## Подробнее

Модуль содержит функцию `ensure_https`, которая принимает строку или список строк (URL или ID товаров) и возвращает строку или список строк, в которых URL гарантированно начинается с `https://`. В случае, если передается ID товара, функция формирует полный URL для товара на сайте AliExpress.

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

**Назначение**:
Функция проверяет и, при необходимости, добавляет префикс `https://` к предоставленным URL или ID товаров. Если входные данные представлены в виде ID товара, функция формирует полный URL товара на AliExpress.

**Параметры**:
- `prod_ids` (str | list[str]): URL или список URL для проверки и модификации.

**Возвращает**:
- `str | list[str]`: URL или список URL с префиксом `https://`.

**Вызывает исключения**:
- `ValueError`: Если `prod_ids` является экземпляром `WindowsPath`.

**Как работает функция**:
1. Функция принимает на вход строку `prod_ids`, которая может быть как отдельным URL или ID товара, так и списком таких строк.
2. Функция проверяет, является ли `prod_ids` списком.
3. Если `prod_ids` является списком, функция применяет внутреннюю функцию `ensure_https_single` к каждому элементу списка и возвращает новый список с обработанными URL.
4. Если `prod_ids` не является списком, функция вызывает `ensure_https_single` для обработки отдельной строки.

**Внутренние функции**:

### `ensure_https_single`

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

**Назначение**:
Функция проверяет и, при необходимости, добавляет префикс `https://` к предоставленному URL или ID товара. Если входные данные представлены в виде ID товара, функция формирует полный URL товара на AliExpress.

**Параметры**:
- `prod_id` (str): URL или ID товара для проверки и модификации.

**Возвращает**:
- `str`: URL с префиксом `https://`.

**Вызывает исключения**:
- `ValueError`: Если `prod_id` является экземпляром `WindowsPath`.

**Как работает функция**:
1. Функция принимает на вход строку `prod_id`, которая может быть как отдельным URL, так и ID товара.
2. Вызывается функция `extract_prod_ids(prod_id)`, которая извлекает ID товара из переданной строки.
3. Проверяется, был ли успешно извлечен ID товара.
4. Если ID товара был успешно извлечен, функция возвращает URL товара на AliExpress, собранный с использованием префикса `https://` и извлеченного ID товара.
5. Если ID товара не был извлечен, в лог записывается сообщение об ошибке, и функция возвращает исходную строку `prod_id`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.utils.ensure_https import ensure_https
# Пример 1: Преобразование ID товара в URL с https
product_id = "1234567890"
https_url = ensure_https(product_id)
print(https_url)  # Вывод: https://www.aliexpress.com/item/1234567890.html

# Пример 2: Проверка URL с https
https_url = "https://www.aliexpress.com/item/1234567890.html"
ensured_url = ensure_https(https_url)
print(ensured_url)  # Вывод: https://www.aliexpress.com/item/1234567890.html

# Пример 3: Список ID товаров
product_ids = ["1234567890", "0987654321"]
https_urls = ensure_https(product_ids)
print(https_urls)
# Вывод: ['https://www.aliexpress.com/item/1234567890.html', 'https://www.aliexpress.com/item/0987654321.html']

# Пример 4: Смешанный список URL и ID товаров
mixed_list = ["1234567890", "https://www.example.com/item/0987654321.html"]
mixed_https_urls = ensure_https(mixed_list)
print(mixed_https_urls)
# Вывод: ['https://www.aliexpress.com/item/1234567890.html', 'https://www.example.com/item/0987654321.html']