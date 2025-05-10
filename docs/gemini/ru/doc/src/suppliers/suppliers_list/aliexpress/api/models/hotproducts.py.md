# Модуль HotProductsResponse

## Обзор

Модуль содержит модель `HotProductsResponse`, представляющую собой объект, возвращаемый API AliExpress при запросе популярных товаров. 

## Подробнее

Модель `HotProductsResponse` используется для структурирования данных, получаемых при вызове API AliExpress.  Она представляет собой структуру с информацией о  популярных товарах, включая:

*  **current_page_no**: номер текущей страницы в ответе (int).
*  **current_record_count**: количество записей на текущей странице (int).
*  **total_record_count**: общее количество записей (int).
*  **products**: список объектов `Product`, представляющих  информацию о популярных товарах (List[Product]).

## Классы

### `HotProductsResponse`

**Описание**: Модель для представления данных, полученных от API AliExpress, включающая информацию о популярных товарах.

**Атрибуты**:

*  **current_page_no**: номер текущей страницы в ответе (int).
*  **current_record_count**: количество записей на текущей странице (int).
*  **total_record_count**: общее количество записей (int).
*  **products**: список объектов `Product`, представляющих информацию о популярных товарах (List[Product]).

**Примеры**:

```python
from src.suppliers.aliexpress.api.models.hotproducts import HotProductsResponse

# Пример создания объекта HotProductsResponse
hot_products_response = HotProductsResponse(
    current_page_no=1,
    current_record_count=10,
    total_record_count=100,
    products=[
        Product(
            product_id=1234567890,
            product_title="Название товара",
            product_url="https://aliexpress.com/item/1234567890",
            product_image="https://images.aliexpress.com/image/product/1234567890",
            product_price=10.00,
            product_discount=5.00,
            product_rating=4.5,
            product_reviews=100,
        )
    ]
)

# Доступ к атрибутам объекта
print(hot_products_response.current_page_no) # Вывод: 1
print(hot_products_response.products[0].product_title) # Вывод: Название товара
```