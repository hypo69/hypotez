# Модуль `HotProductsResponse`
## Обзор

Модуль содержит класс `HotProductsResponse`, который используется для представления ответа от API AliExpress, содержащего информацию о популярных товарах.

## Детали

Данный модуль импортируется в другие части проекта для работы с данными о популярных товарах на платформе AliExpress. 

## Классы

### `HotProductsResponse`

**Описание**: Класс представляет собой модель ответа от API AliExpress, содержащего информацию о популярных товарах.

**Атрибуты**:

- `current_page_no` (int): Номер текущей страницы в результатах поиска.
- `current_record_count` (int): Количество записей на текущей странице.
- `total_record_count` (int): Общее количество записей.
- `products` (List[Product]): Список объектов `Product`, представляющих информацию о каждом товаре.

## Параметры

- `current_page_no`: Номер текущей страницы в результатах поиска. 
- `current_record_count`: Количество записей на текущей странице.
- `total_record_count`: Общее количество записей.
- `products`: Список объектов `Product`, представляющих информацию о каждом товаре.

## Примеры

```python
# Пример создания объекта HotProductsResponse
hot_products_response = HotProductsResponse()
hot_products_response.current_page_no = 1
hot_products_response.current_record_count = 10
hot_products_response.total_record_count = 100
hot_products_response.products = [
    Product(product_id=123456, product_name="Товар 1"),
    Product(product_id=789012, product_name="Товар 2"),
    # ... другие товары
]
```

**Примечание:** В данном примере используются объекты `Product` из модуля `src.suppliers.aliexpress.api.models.product`.

## Дополнительные сведения

- Модуль `src.suppliers.suppliers_list.aliexpress.api.models` предоставляет  классы для работы с данными AliExpress.
- Класс `HotProductsResponse` используется для получения данных о популярных товарах с API AliExpress.
- Класс `Product`  используется для представления информации о товаре.