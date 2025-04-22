# Модуль `hotproducts.py`

## Обзор

Модуль `hotproducts.py` предназначен для определения модели ответа, содержащей список популярных товаров (hot products) с платформы AliExpress. Он включает класс `HotProductsResponse`, который хранит информацию о текущей странице, количестве записей на странице, общем количестве записей и списке самих товаров.

## Подробнее

Этот модуль определяет структуру данных для представления ответа, содержащего список популярных товаров, полученных через API AliExpress. Он использует класс `Product` из модуля `product.py` для представления каждого отдельного товара и включает информацию о пагинации результатов.

## Классы

### `HotProductsResponse`

**Описание**: Класс `HotProductsResponse` представляет структуру ответа, содержащую список популярных товаров с AliExpress, а также метаданные о пагинации.

**Атрибуты**:

- `current_page_no` (int): Номер текущей страницы в ответе.
- `current_record_count` (int): Количество записей (товаров) на текущей странице.
- `total_record_count` (int): Общее количество записей (товаров) во всем ответе.
- `products` (List[Product]): Список объектов `Product`, представляющих товары на текущей странице.

**Принцип работы**:

Класс `HotProductsResponse` служит контейнером для хранения данных, возвращаемых API AliExpress при запросе списка популярных товаров. Он агрегирует информацию о товарах и метаданные о пагинации, что упрощает обработку и представление данных в приложении.

## Параметры класса `HotProductsResponse`

- `current_page_no` (int): Номер текущей страницы результатов. Показывает, какая по счету страница товаров представлена в данном ответе.
- `current_record_count` (int): Количество товаров, представленных на текущей странице.
- `total_record_count` (int): Общее количество товаров, соответствующих запросу, доступных на всех страницах.
- `products` (List[Product]): Список объектов `Product`, каждый из которых содержит информацию об одном товаре.

**Примеры**:

```python
from typing import List

class Product:
    product_id: int
    product_title: str

class HotProductsResponse:
    current_page_no: int
    current_record_count: int
    total_record_count: int
    products: List[Product]

# Пример создания экземпляра класса HotProductsResponse
product1 = Product()
product1.product_id = 123
product1.product_title = "Example Product 1"

product2 = Product()
product2.product_id = 456
product2.product_title = "Example Product 2"

hot_products_response = HotProductsResponse()
hot_products_response.current_page_no = 1
hot_products_response.current_record_count = 2
hot_products_response.total_record_count = 100
hot_products_response.products = [product1, product2]