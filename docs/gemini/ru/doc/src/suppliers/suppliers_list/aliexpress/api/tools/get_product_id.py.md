# Модуль для извлечения идентификатора продукта

## Обзор

Модуль предназначен для извлечения идентификатора продукта из различных форматов входных данных, таких как URL или произвольный текст. Он использует регулярные выражения для поиска и извлечения идентификатора.

## Подробней

Этот модуль является частью проекта `hypotez` и используется для получения идентификатора продукта AliExpress из различных источников. Он пытается найти идентификатор продукта в предоставленной строке и возвращает его. Если идентификатор не найден, выбрасывается исключение.

## Функции

### `get_product_id`

```python
def get_product_id(raw_product_id: str) -> str:
    """Returns the product ID from a given text. Raises ProductIdNotFoundException on fail."""
```

**Назначение**: Извлекает и возвращает идентификатор продукта из предоставленной строки.

**Параметры**:

-   `raw_product_id` (str): Строка, содержащая потенциальный идентификатор продукта (например, URL или просто ID).

**Возвращает**:

-   `str`: Идентификатор продукта.

**Вызывает исключения**:

-   `ProductIdNotFoundException`: Если идентификатор продукта не найден в предоставленной строке.

**Как работает функция**:

Функция `get_product_id` использует функцию `extract_prod_ids` для извлечения идентификатора продукта из входной строки `raw_product_id`. Если идентификатор не найден, выбрасывается исключение `ProductIdNotFoundException`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.suppliers_list.aliexpress.errors import ProductIdNotFoundException

try:
    product_id1 = get_product_id("1234567890")
    print(f"Product ID 1: {product_id1}")

    product_id2 = get_product_id("https://www.aliexpress.com/item/1234567890.html")
    print(f"Product ID 2: {product_id2}")

    product_id3 = get_product_id("no_id_here")
    print(f"Product ID 3: {product_id3}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")