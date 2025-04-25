# Модуль `get_product_id`

## Обзор

Этот модуль предоставляет функцию `get_product_id`, которая извлекает ID продукта из заданного текста. Функция использует регулярные выражения для поиска ID продукта в тексте.

## Подробнее

Модуль используется для извлечения ID продукта из различных источников, таких как URL, текстовые описания и т.д. 

## Функции

### `get_product_id`

**Назначение**: Извлекает ID продукта из заданного текста.

**Параметры**:

- `raw_product_id` (str): Текст, из которого необходимо извлечь ID продукта.

**Возвращает**:

- `str`: ID продукта, если он был найден.

**Вызывает исключения**:

- `ProductIdNotFoundException`: Если ID продукта не был найден в тексте.

**Пример**:

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id

raw_product_id = "https://www.aliexpress.com/item/10000000000000.html"
product_id = get_product_id(raw_product_id)
print(f"Product ID: {product_id}") 
```

**Как работает функция**:

Функция использует функцию `extract_prod_ids` из модуля `src.suppliers.suppliers_list.aliexpress.utils.extract_product_id` для извлечения ID продукта. 

**Примеры**:

```python
>>> get_product_id("https://www.aliexpress.com/item/10000000000000.html")
'10000000000000'

>>> get_product_id("Product ID: 1234567890")
'1234567890'

>>> get_product_id("This is a product description. The product ID is 9876543210.")
'9876543210'

>>> get_product_id("No product ID here.")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/src/suppliers/aliexpress/api/tools/get_product_id.py", line 11, in get_product_id
    raise ProductIdNotFoundException('Product id not found: ' + text)
src.suppliers.suppliers_list.aliexpress.errors.ProductIdNotFoundException: Product id not found: No product ID here.
```