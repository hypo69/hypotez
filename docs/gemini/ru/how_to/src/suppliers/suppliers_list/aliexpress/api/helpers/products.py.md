## \file /src/suppliers/aliexpress/api/helpers/products.py
# -*- coding: utf-8 -*-
 # <- venv win
## ~~~~~~~~~~~~

""" module: src.suppliers.suppliers_list.aliexpress.api.helpers """

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет две функции: `parse_product` и `parse_products`. Функция `parse_product` извлекает строковое значение из атрибута `product_small_image_urls` объекта `product`. Функция `parse_products` применяет функцию `parse_product` к каждому элементу в списке `products`.

Шаги выполнения
-------------------------
1. **Функция `parse_product(product)`**:
   - Функция принимает объект `product` в качестве аргумента.
   - Извлекает строковое значение из атрибута `product.product_small_image_urls.string` и присваивает его обратно атрибуту `product.product_small_image_urls`.
   - Функция возвращает измененный объект `product`.

2. **Функция `parse_products(products)`**:
   - Функция принимает список объектов `products` в качестве аргумента.
   - Инициализирует пустой список `new_products`.
   - Функция итерируется по каждому `product` в списке `products`.
   - Для каждого `product` функция вызывает функцию `parse_product(product)` и добавляет возвращенный результат в список `new_products`.
   - Функция возвращает список `new_products`, содержащий измененные объекты `product`.

Пример использования
-------------------------

```python
# Пример использования
from bs4 import BeautifulSoup

# Пример объекта product (имитация)
html = """
<div class="product">
    <div class="product_small_image_urls">
        <p>https://example.com/image1.jpg</p>
    </div>
</div>
"""
soup = BeautifulSoup(html, 'html.parser')
product = soup.find('div', class_='product')
product.product_small_image_urls = product.find('div', class_='product_small_image_urls')


def parse_product(product):
    product.product_small_image_urls = product.product_small_image_urls.string
    return product


def parse_products(products):
    new_products = []

    for product in products:
        new_products.append(parse_product(product))

    return new_products


# Вызов функции parse_product
parsed_product = parse_product(product)
print(parsed_product.product_small_image_urls)

# Пример списка products (имитация)
products = [product] * 3

# Вызов функции parse_products
parsed_products = parse_products(products)
for p in parsed_products:
    print(p.product_small_image_urls)