## Как использовать класс `HotProductsResponse`
=========================================================================================

### Описание
-------------------------
Класс `HotProductsResponse` представляет собой модель данных для ответа от API AliExpress, содержащего информацию о популярных товарах.

### Шаги выполнения
-------------------------
1. **Инициализация объекта:** Создайте экземпляр класса `HotProductsResponse` и присвойте значения атрибутам:
    - `current_page_no` - номер текущей страницы результатов.
    - `current_record_count` - количество записей на текущей странице.
    - `total_record_count` - общее количество записей.
    - `products` - список объектов `Product`, представляющих популярные товары.
2. **Доступ к данным:** После инициализации объекта вы можете получить доступ к его атрибутам, таким как:
    - `hot_products.current_page_no` - возвращает номер текущей страницы.
    - `hot_products.products` - возвращает список товаров.

### Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.models.hotproducts import HotProductsResponse
from src.suppliers.aliexpress.api.models.product import Product

# Пример данных из API AliExpress
api_response = {
    "current_page_no": 1,
    "current_record_count": 20,
    "total_record_count": 100,
    "products": [
        {
            "product_id": 1234567890,
            "product_name": "Товар 1",
            # ... другие атрибуты товара ...
        },
        {
            "product_id": 9876543210,
            "product_name": "Товар 2",
            # ... другие атрибуты товара ...
        },
        # ... другие товары ...
    ]
}

# Создание объекта HotProductsResponse из данных API
hot_products = HotProductsResponse(
    current_page_no=api_response["current_page_no"],
    current_record_count=api_response["current_record_count"],
    total_record_count=api_response["total_record_count"],
    products=[Product(**product) for product in api_response["products"]],
)

# Доступ к данным из объекта
print(f"Текущая страница: {hot_products.current_page_no}")
print(f"Всего записей: {hot_products.total_record_count}")

# Использование данных о товарах
for product in hot_products.products:
    print(f"ID товара: {product.product_id}")
    print(f"Название товара: {product.product_name}")
```

### Дополнительные замечания:
- Класс `HotProductsResponse` является моделью данных для ответа от API AliExpress, содержащего информацию о популярных товарах.
- Для создания объекта `HotProductsResponse` нужно предоставить значения атрибутов, которые соответствуют данным, полученным из API AliExpress.
- После создания объекта вы можете получить доступ к его атрибутам и использовать информацию о товарах.