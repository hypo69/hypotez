# Модуль для извлечения ID товара AliExpress
## Обзор

Модуль `get_product_id.py` предназначен для извлечения идентификатора товара (product ID) из различных форматов входных данных, таких как URL или просто строка с номером. Он использует функцию `extract_prod_ids` для поиска и возврата ID товара. В случае, если ID товара не найден, вызывается исключение `ProductIdNotFoundException`.

## Подробней

Этот модуль играет важную роль в процессе автоматизации работы с AliExpress, позволяя идентифицировать товары по их уникальным идентификаторам. Он абстрагирует логику извлечения ID товара, что упрощает использование этой функциональности в других частях проекта.

## Функции

### `get_product_id`

```python
def get_product_id(raw_product_id: str) -> str:
    """Возвращает ID товара из предоставленной строки. Вызывает исключение ProductIdNotFoundException в случае неудачи.

    Args:
        raw_product_id (str): Строка, содержащая ID товара в различном формате (например, URL или просто номер).

    Returns:
        str: ID товара.

    Raises:
        ProductIdNotFoundException: Если ID товара не найден в предоставленной строке.
    """
    return extract_prod_ids(raw_product_id)
```

**Назначение**: Извлечение ID товара из строки.

**Параметры**:
- `raw_product_id` (str): Строка, содержащая ID товара.

**Возвращает**:
- `str`: ID товара.

**Вызывает исключения**:
- `ProductIdNotFoundException`: Вызывается, если ID товара не найден.

**Как работает функция**:
Функция `get_product_id` принимает строку `raw_product_id` в качестве аргумента и передает её функции `extract_prod_ids`. Функция `extract_prod_ids` выполняет поиск ID товара в переданной строке. Если ID товара найден, он возвращается. В противном случае функция `extract_prod_ids` должна вызвать исключение `ProductIdNotFoundException`, которое будет обработано вызывающей стороной.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.suppliers_list.aliexpress.api.errors import ProductIdNotFoundException

# Пример 1: Извлечение ID товара из строки с числом
try:
    product_id = get_product_id("1234567890")
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")

# Пример 2: Извлечение ID товара из URL
try:
    product_id = get_product_id("https://www.aliexpress.com/item/1234567890.html")
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")

# Пример 3: Обработка случая, когда ID товара не найден
try:
    product_id = get_product_id("No product ID here")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")