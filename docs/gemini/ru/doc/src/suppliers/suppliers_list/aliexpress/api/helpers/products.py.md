# Модуль `products.py`

## Обзор

Модуль `products.py` содержит две функции для обработки данных о товарах AliExpress:

- `parse_product`: Функция для парсинга отдельного объекта товара. 
- `parse_products`: Функция для парсинга списка объектов товаров.

## Классы

### `products.py`
**Описание**:  Модуль для работы с данными о товарах AliExpress.

**Методы**:

- `parse_product`: Функция для обработки объекта товара.
- `parse_products`: Функция для обработки списка объектов товаров.

## Функции

### `parse_product`

**Назначение**: Функция парсит объект товара AliExpress и преобразует строку `product_small_image_urls` в текстовое значение.

**Параметры**:

- `product`: Объект товара AliExpress.

**Возвращает**:

- `product`: Объект товара AliExpress с преобразованной строкой `product_small_image_urls`.


**Примеры**:

```python
>>> from src.suppliers.aliexpress.api.helpers.products import parse_product
>>> product = {"product_small_image_urls": "<img src='image_url'>"}
>>> parsed_product = parse_product(product)
>>> parsed_product['product_small_image_urls']
'image_url'

```

### `parse_products`

**Назначение**: Функция парсит список объектов товаров AliExpress, применяя функцию `parse_product` к каждому элементу списка.

**Параметры**:

- `products`: Список объектов товаров AliExpress.

**Возвращает**:

- `new_products`: Новый список обработанных объектов товаров.

**Примеры**:

```python
>>> from src.suppliers.aliexpress.api.helpers.products import parse_products
>>> products = [{"product_small_image_urls": "<img src='image_url1'>"}, {"product_small_image_urls": "<img src='image_url2'>"}, {"product_small_image_urls": "<img src='image_url3'>"},]
>>> parsed_products = parse_products(products)
>>> parsed_products[0]['product_small_image_urls']
'image_url1'
>>> parsed_products[1]['product_small_image_urls']
'image_url2'
>>> parsed_products[2]['product_small_image_urls']
'image_url3'
```