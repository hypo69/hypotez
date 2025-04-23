# Модуль для извлечения ID товара из текста
## Обзор

Модуль `get_product_id.py` предназначен для извлечения идентификатора товара (product ID) из различных форматов входных данных, таких как URL или простой текст. Он использует функцию `extract_prod_ids` для поиска и возврата ID товара. В случае, если ID товара не найден, выбрасывается исключение `ProductIdNotFoundException`.

## Подробнее

Этот модуль является частью системы для работы с AliExpress API и служит для стандартизации процесса получения ID товара, что необходимо для дальнейшего взаимодействия с API. Он обрабатывает различные варианты представления ID товара, такие как числовой ID или ID, встроенный в URL.

## Функции

### `get_product_id`

```python
def get_product_id(raw_product_id: str) -> str:
    """Returns the product ID from a given text. Raises ProductIdNotFoundException on fail."""
```

**Назначение**: Извлекает и возвращает ID товара из предоставленной строки.

**Параметры**:

- `raw_product_id` (str): Строка, содержащая ID товара или URL, из которого нужно извлечь ID.

**Возвращает**:

- `str`: ID товара.

**Вызывает исключения**:

- `ProductIdNotFoundException`: Если ID товара не найден в предоставленной строке.

**Как работает функция**:

1.  Функция вызывает `extract_prod_ids` с входной строкой `raw_product_id`.
2.  `extract_prod_ids` пытается извлечь ID товара из строки.
3.  Если ID товара найден, он возвращается.
4.  Если ID товара не найден, `extract_prod_ids` выбрасывает исключение `ProductIdNotFoundException`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.suppliers_list.aliexpress.errors import ProductIdNotFoundException

try:
    product_id = get_product_id("1234567890")
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")
```

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.suppliers_list.aliexpress.errors import ProductIdNotFoundException

try:
    product_id = get_product_id("https://example.com/item/1234567890.html")
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")
```
```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.suppliers_list.aliexpress.errors import ProductIdNotFoundException

try:
    product_id = get_product_id("Invalid product ID")
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")