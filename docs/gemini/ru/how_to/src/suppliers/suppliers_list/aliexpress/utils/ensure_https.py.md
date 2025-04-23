## \file /src/suppliers/aliexpress/utils/ensure_https.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.utils
	:platform: Windows, Unix
	:synopsis: Ensures that the provided URL string(s) contain the https:// prefix.
If the input is a product ID, it constructs a full URL with https:// prefix.

```python
# Example usage
url = "example_product_id"
url_with_https = ensure_https(url)
print(url_with_https)  # Output: https://www.aliexpress.com/item/example_product_id.html

urls = ["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"]
urls_with_https = ensure_https(urls)
print(urls_with_https)  # Output: ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']
```

"""

from src.logger.logger import logger
from .extract_product_id import extract_prod_ids


def ensure_https(prod_ids: str | list[str]) -> str | list[str]:
    """
    Функция проверяет, содержит ли предоставленная URL-строка или список URL-строк префикс https://.
    Если входные данные являются ID товара, функция формирует полный URL с префиксом https://.

    Args:
        prod_ids (str | list[str]): URL-строка или список URL-строк для проверки и изменения при необходимости.

    Returns:
        str | list[str]: URL-строка или список URL-строк с префиксом https://.

    Raises:
        ValueError: Если `prod_ids` является экземпляром `WindowsPath`.

    Example:
        >>> ensure_https("example_product_id")
        'https://www.aliexpress.com/item/example_product_id.html'

        >>> ensure_https(["example_product_id1", "https://www.aliexpress.com/item/example_product_id2.html"])
        ['https://www.aliexpress.com/item/example_product_id1.html', 'https://www.aliexpress.com/item/example_product_id2.html']

        >>> ensure_https("https://www.example.com/item/example_product_id")
        'https://www.example.com/item/example_product_id'
    """

    def ensure_https_single(prod_id: str) -> str:
        """
        Функция проверяет, содержит ли предоставленная URL-строка префикс https://.
        Если входные данные являются ID товара, функция формирует полный URL с префиксом https://.

        Args:
            prod_id (str): URL-строка для проверки и изменения при необходимости.

        Returns:
            str: URL-строка с префиксом https://.

        Raises:
            ValueError: Если `prod_id` является экземпляром `WindowsPath`.

        Example:
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

    if isinstance(prod_ids, list):
        return [ensure_https_single(prod_id) for prod_id in prod_ids]
    else:
        return ensure_https_single(prod_ids)


Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Код обеспечивает добавление префикса `https://` к URL-адресам или идентификаторам товаров, проверяя, является ли входная строка уже URL-адресом с `https://` или просто идентификатором товара. В последнем случае он формирует полный URL-адрес товара на AliExpress.

Шаги выполнения
-------------------------
1. Функция `ensure_https` принимает на вход строку или список строк (`prod_ids`).
2. Если входные данные являются списком, функция применяет функцию `ensure_https_single` к каждому элементу списка и возвращает новый список с обработанными URL-адресами.
3. Если входные данные являются строкой, функция вызывает `ensure_https_single` для этой строки.
4. Функция `ensure_https_single` проверяет, является ли входная строка идентификатором товара. Для этого вызывается функция `extract_prod_ids`.
5. Если `extract_prod_ids` возвращает значение (т.е. строка является идентификатором товара), функция формирует URL-адрес товара на AliExpress с использованием этого идентификатора и префикса `https://`.
6. Если `extract_prod_ids` возвращает `None` (т.е. строка не является идентификатором товара), функция логирует ошибку и возвращает исходную строку.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.utils.ensure_https import ensure_https

# Пример 1: Обработка одного ID товара
product_id = "1234567890"
https_url = ensure_https(product_id)
print(https_url)
# Функция возвращает: https://www.aliexpress.com/item/1234567890.html

# Пример 2: Обработка списка ID товаров и URL-адресов
product_ids = ["1234567890", "https://example.com/item/9876543210"]
https_urls = ensure_https(product_ids)
print(https_urls)
# Функция возвращает: ['https://www.aliexpress.com/item/1234567890.html', 'https://example.com/item/9876543210']