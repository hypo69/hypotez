## Как использовать блок кода `parse_product` и `parse_products`
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для обработки данных о товарах AliExpress. Функция `parse_product` преобразует объект `product`, извлекая из него список URL-адресов изображений товара в маленьком формате (`product_small_image_urls`). 

Функция `parse_products` обрабатывает список объектов `products`, применяя функцию `parse_product` к каждому объекту. В результате возвращается новый список обработанных товаров.

Шаги выполнения
-------------------------
1. **`parse_product`**:
    - Извлекает строковое значение из атрибута `product_small_image_urls` объекта `product`.
    - Возвращает объект `product` с обновленным атрибутом `product_small_image_urls`, содержащим список URL-адресов в виде строки.
2. **`parse_products`**:
    - Создает новый список `new_products`.
    - Проходит по каждому товару `product` в списке `products`.
    - Вызывает функцию `parse_product` для каждого `product` и добавляет результат в список `new_products`.
    - Возвращает новый список `new_products` с обработанными данными.

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.helpers.products import parse_products

# Предположим, у нас есть список объектов товаров:
products = [
    {
        "product_small_image_urls": "<a href='https://images.example.com/image1.jpg'>Image 1</a><a href='https://images.example.com/image2.jpg'>Image 2</a>",
        # ... другие поля товара
    },
    {
        "product_small_image_urls": "<a href='https://images.example.com/image3.jpg'>Image 3</a>",
        # ... другие поля товара
    },
    # ... другие товары
]

# Обрабатываем список товаров
parsed_products = parse_products(products)

# Теперь список `parsed_products` содержит обработанные товары:
print(parsed_products[0]["product_small_image_urls"])  # Вывод: https://images.example.com/image1.jpg,https://images.example.com/image2.jpg
print(parsed_products[1]["product_small_image_urls"])  # Вывод: https://images.example.com/image3.jpg
```