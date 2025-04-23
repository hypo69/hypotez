### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `extract_prod_ids` извлекает идентификаторы товаров (product IDs) из URL-адресов AliExpress или возвращает их, если они уже предоставлены в виде строки или списка строк. Она использует регулярное выражение для поиска числовых идентификаторов в URL-адресах, содержащих "item/" или заканчивающихся на ".html".

Шаги выполнения
-------------------------
1. **Определение регулярного выражения**: Определяется регулярное выражение `pattern` для поиска идентификаторов товаров в URL-адресах AliExpress.
2. **Функция `extract_id`**: 
   - Принимает URL или идентификатор товара в качестве аргумента.
   - Проверяет, является ли входная строка числовым идентификатором товара. Если да, возвращает её.
   - Если входная строка не является идентификатором, пытается извлечь идентификатор из URL с помощью регулярного выражения.
   - Если идентификатор найден, возвращает его; в противном случае возвращает `None`.
3. **Обработка входных данных**:
   - Если входные данные являются списком URL-адресов или идентификаторов, функция применяет `extract_id` к каждому элементу списка, исключая `None` значения.
   - Если входные данные являются строкой (URL или идентификатор), функция вызывает `extract_id` для этой строки.
4. **Возврат результата**:
   - Если входные данные были списком, функция возвращает список извлеченных идентификаторов, исключая `None` значения. Если список пуст, возвращает `None`.
   - Если входные данные были строкой, функция возвращает извлеченный идентификатор или `None`, если идентификатор не найден.

Пример использования
-------------------------

```python
import re
from src.logger.logger import logger

def extract_prod_ids(urls: str | list[str]) -> str | list[str] | None:
    """ Извлекает item IDs из списка URL-адресов или непосредственно возвращает IDs, если они предоставлены.

    Args:
        urls (str | list[str]): URL, список URL-адресов или product IDs.

    Returns:
        str | list[str] | None: Список извлеченных item IDs, одиночный ID или `None`, если не найден действительный ID.

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
    # Регулярное выражение для поиска идентификаторов товаров
    pattern = re.compile(r"(?:item/|/)?(\d+)\.html")

    def extract_id(url: str) -> str | None:
        """ Извлекает product ID из заданного URL или проверяет product ID.

        Args:
            url (str): URL или product ID.

        Returns:
            str | None: Извлеченный product ID или сам ввод, если это действительный ID, или `None`, если не найден действительный ID.

        Examples:
            >>> extract_id("https://www.aliexpress.com/item/123456.html")
            '123456'

            >>> extract_id("7891011")
            '7891011'

            >>> extract_id("https://www.example.com/item/abcdef.html")
            None
        """
        # Проверка, является ли ввод действительным product ID
        if url.isdigit():
            return url

        # В противном случае попытка извлечь ID из URL
        match = pattern.search(url)
        if match:
            return match.group(1)
        return

    if isinstance(urls, list):
        extracted_ids = [extract_id(url) for url in urls if extract_id(url) is not None]
        return extracted_ids if extracted_ids else None
    else:
        return extract_id(urls)


# Пример использования
url1 = "https://www.aliexpress.com/item/123456.html"
url2 = "7891011"
url3 = "https://www.example.com/item/abcdef.html"
url_list = ["https://www.aliexpress.com/item/123456.html", "7891011.html", "https://www.example.com/item/abcdef.html"]

print(extract_prod_ids(url1))
print(extract_prod_ids(url2))
print(extract_prod_ids(url3))
print(extract_prod_ids(url_list))