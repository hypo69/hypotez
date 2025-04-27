# Модуль: `src.suppliers.aliexpress.api.helpers.products`

## Обзор

Модуль `src.suppliers.aliexpress.api.helpers.products` предоставляет функции для обработки данных о товарах, полученных из API AliExpress.

## Детали

Модуль используется для преобразования и форматирования данных о товарах, полученных из API AliExpress. 

## Функции

### `parse_product(product)`

**Описание**: Функция `parse_product` обрабатывает один объект товара, полученный из API AliExpress, и форматирует его в соответствии с требованиями проекта.

**Параметры**:

- `product`: Объект товара, полученный из API AliExpress.

**Возвращает**:

- `product`: Измененный объект товара.

**Как работает функция**:

- Функция принимает объект товара, полученный из API AliExpress.
- Она преобразует значение атрибута `product_small_image_urls` в строку, используя метод `string` объекта.
- Функция возвращает измененный объект товара.

**Пример**:

```python
product = {
    'product_small_image_urls': [
        'https://img.alicdn.com/imgextra/i1/2202108131/O1CN01218M8c1X1X68N2d58_!!2202108131.jpg_400x400.jpg',
        'https://img.alicdn.com/imgextra/i3/2202108131/O1CN01218M8c1X1X68N2d58_!!2202108131.jpg_400x400.jpg'
    ],
    ...
}

parsed_product = parse_product(product)

print(parsed_product['product_small_image_urls'])
# Output: 'https://img.alicdn.com/imgextra/i1/2202108131/O1CN01218M8c1X1X68N2d58_!!2202108131.jpg_400x400.jpg'
```

### `parse_products(products)`

**Описание**: Функция `parse_products` обрабатывает список объектов товаров, полученных из API AliExpress, и форматирует их в соответствии с требованиями проекта.

**Параметры**:

- `products`: Список объектов товаров, полученных из API AliExpress.

**Возвращает**:

- `new_products`: Новый список обработанных объектов товаров.

**Как работает функция**:

- Функция принимает список объектов товаров, полученных из API AliExpress.
- Она итерирует по каждому объекту товара в списке.
- Для каждого объекта товара она вызывает функцию `parse_product`, чтобы обработать его.
- Функция добавляет обработанный объект товара в новый список.
- Функция возвращает новый список обработанных объектов товаров.

**Пример**:

```python
products = [
    {
        'product_small_image_urls': [
            'https://img.alicdn.com/imgextra/i1/2202108131/O1CN01218M8c1X1X68N2d58_!!2202108131.jpg_400x400.jpg',
            'https://img.alicdn.com/imgextra/i3/2202108131/O1CN01218M8c1X1X68N2d58_!!2202108131.jpg_400x400.jpg'
        ],
        ...
    },
    {
        'product_small_image_urls': [
            'https://img.alicdn.com/imgextra/i1/2202108132/O1CN01218M8c1X1X68N2d59_!!2202108132.jpg_400x400.jpg',
            'https://img.alicdn.com/imgextra/i3/2202108132/O1CN01218M8c1X1X68N2d59_!!2202108132.jpg_400x400.jpg'
        ],
        ...
    }
]

parsed_products = parse_products(products)

print(parsed_products[0]['product_small_image_urls'])
# Output: 'https://img.alicdn.com/imgextra/i1/2202108131/O1CN01218M8c1X1X68N2d58_!!2202108131.jpg_400x400.jpg'
```