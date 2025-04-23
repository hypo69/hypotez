### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для извлечения ID товара из входной строки, которая может быть как самим ID, так и URL-адресом страницы товара. Он использует функцию `extract_prod_ids` для поиска и возврата ID товара. В случае, если ID не найден, выбрасывается исключение `ProductIdNotFoundException`.

Шаги выполнения
-------------------------
1. Функция `get_product_id` принимает строку `raw_product_id` в качестве аргумента.
2. Вызывается функция `extract_prod_ids` с аргументом `raw_product_id`.
3. Функция `extract_prod_ids` извлекает и возвращает ID товара из строки.
4. Если ID товара не найден, функция `extract_prod_ids` выбрасывает исключение `ProductIdNotFoundException`.
5. Функция `get_product_id` возвращает извлеченный ID товара.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.tools.get_product_id import get_product_id
from src.suppliers.suppliers_list.aliexpress.errors import ProductIdNotFoundException

try:
    product_id = get_product_id("1234567890")
    print(f"Product ID: {product_id}")  # Выведет: Product ID: 1234567890
except ProductIdNotFoundException as e:
    print(f"Error: {e}")

try:
    product_id = get_product_id("https://aliexpress.com/item/1234567890.html")
    print(f"Product ID: {product_id}")  # Выведет: Product ID: 1234567890
except ProductIdNotFoundException as e:
    print(f"Error: {e}")

try:
    product_id = get_product_id("No product ID here")
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as e:
    print(f"Error: {e}")  # Выведет сообщение об ошибке, если ID не найден