### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код определяет структуру данных для представления ответа, содержащего список популярных товаров с AliExpress. Класс `HotProductsResponse` включает информацию о текущей странице, количестве записей на странице, общем количестве записей и списке товаров, представленных классом `Product`.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируется класс `Product` из модуля `.product`.
   - Импортируется `List` из модуля `typing` для аннотации типов.

2. **Определение класса `HotProductsResponse`**:
   - Создается класс `HotProductsResponse`, который представляет структуру ответа, содержащего список популярных товаров.
   - Определяются атрибуты класса:
     - `current_page_no` (int): Номер текущей страницы.
     - `current_record_count` (int): Количество записей на текущей странице.
     - `total_record_count` (int): Общее количество записей.
     - `products` (List[Product]): Список объектов класса `Product`, представляющих товары.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models.hotproducts import HotProductsResponse
from src.suppliers.suppliers_list.aliexpress.api.models.product import Product
from typing import List

# Пример создания экземпляра класса Product
product1 = Product(
    product_id="12345",
    product_title="Cool Gadget",
    product_price=25.00,
    product_url="https://example.com/gadget123"
)

product2 = Product(
    product_id="67890",
    product_title="Awesome Device",
    product_price=50.00,
    product_url="https://example.com/device678"
)

# Пример создания списка товаров
products_list: List[Product] = [product1, product2]

# Пример создания экземпляра класса HotProductsResponse
hot_products_response = HotProductsResponse()
hot_products_response.current_page_no = 1
hot_products_response.current_record_count = 2
hot_products_response.total_record_count = 20
hot_products_response.products = products_list

# Вывод информации о полученных данных
print(f"Current Page No: {hot_products_response.current_page_no}")
print(f"Current Record Count: {hot_products_response.current_record_count}")
print(f"Total Record Count: {hot_products_response.total_record_count}")
print("Products:")
for product in hot_products_response.products:
    print(f"  - ID: {product.product_id}, Title: {product.product_title}, Price: {product.product_price}")