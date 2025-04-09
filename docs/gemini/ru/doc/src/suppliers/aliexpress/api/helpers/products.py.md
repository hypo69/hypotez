# Модуль для парсинга продуктов AliExpress

## Обзор

Модуль `src.suppliers.aliexpress.api.helpers.products` предназначен для обработки данных о продуктах, полученных из API AliExpress. Он содержит функции для парсинга как одного продукта, так и списка продуктов, приводя данные к нужному формату.

## Подробней

Этот модуль используется для преобразования структуры данных продуктов, полученных из API AliExpress, в формат, удобный для дальнейшей обработки и использования в проекте `hypotez`. Основная задача модуля - извлечение и форматирование информации о продуктах, такой как URL маленьких изображений продуктов.

## Функции

### `parse_product`

**Назначение**: Обрабатывает информацию об одном продукте, извлекая URL маленьких изображений.

```python
def parse_product(product):
    """Преобразует поле `product_small_image_urls` объекта product из BeautifulSoup элемента в строку.

    Args:
        product: Объект продукта, содержащий информацию о продукте, полученную из API AliExpress.

    Returns:
        product: Объект продукта с преобразованным полем `product_small_image_urls`.

    Пример:
        >>> product = BeautifulSoup("<product><product_small_image_urls>url1, url2</product_small_image_urls></product>", 'xml').product
        >>> parsed_product = parse_product(product)
        >>> parsed_product.product_small_image_urls
        'url1, url2'
    """
    product.product_small_image_urls = product.product_small_image_urls.string
    return product
```

**Как работает функция**:

-   Функция принимает объект `product` в качестве аргумента. Предполагается, что это объект BeautifulSoup, полученный после парсинга XML/HTML ответа API AliExpress.
-   Извлекает значение атрибута `string` из поля `product.product_small_image_urls`. Это необходимо, поскольку BeautifulSoup возвращает элементы в виде объектов, а не строк.
-   Возвращает модифицированный объект `product` с обновленным значением поля `product_small_image_urls`.

**Примеры**:

```python
from bs4 import BeautifulSoup

product = BeautifulSoup("<product><product_small_image_urls>url1, url2</product_small_image_urls></product>", 'xml').product
parsed_product = parse_product(product)
print(parsed_product.product_small_image_urls)  # Вывод: url1, url2
```

### `parse_products`

**Назначение**: Обрабатывает список продуктов, применяя функцию `parse_product` к каждому элементу списка.

```python
def parse_products(products):
    """Применяет функцию `parse_product` к каждому элементу списка продуктов.

    Args:
        products: Список объектов продуктов, полученных из API AliExpress.

    Returns:
        new_products: Список объектов продуктов, где поле `product_small_image_urls` преобразовано в строку для каждого продукта.

    Пример:
        >>> products = [BeautifulSoup("<product><product_small_image_urls>url1</product_small_image_urls></product>", 'xml').product, BeautifulSoup("<product><product_small_image_urls>url2</product_small_image_urls></product>", 'xml').product]
        >>> parsed_products = parse_products(products)
        >>> [p.product_small_image_urls for p in parsed_products]
        ['url1', 'url2']
    """
    new_products = []

    for product in products:
        new_products.append(parse_product(product))

    return new_products
```

**Как работает функция**:

-   Функция принимает список `products` в качестве аргумента. Каждый элемент этого списка представляет собой объект продукта, полученный из API AliExpress.
-   Создает пустой список `new_products` для хранения обработанных продуктов.
-   Итерируется по списку `products` и применяет функцию `parse_product` к каждому продукту. Результат добавляется в список `new_products`.
-   Возвращает список `new_products`, содержащий обработанные объекты продуктов.

**Примеры**:

```python
from bs4 import BeautifulSoup

products = [BeautifulSoup("<product><product_small_image_urls>url1</product_small_image_urls></product>", 'xml').product, BeautifulSoup("<product><product_small_image_urls>url2</product_small_image_urls></product>", 'xml').product]
parsed_products = parse_products(products)
print([p.product_small_image_urls for p in parsed_products]) # Вывод: ['url1', 'url2']