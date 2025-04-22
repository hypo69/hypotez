# Модуль `product_async.py`

## Обзор

Модуль `product_async.py` предназначен для управления товарами в PrestaShop посредством асинхронного взаимодействия с API. Он обеспечивает добавление новых товаров, получение информации о категориях и загрузку изображений. Модуль взаимодействует с веб-сайтом, продуктом и PrestaShop, определяя поведение товара в проекте.

## Подробнее

Модуль предоставляет класс `PrestaProductAsync`, который расширяет класс `PrestaShopAsync` и включает методы для работы с товарами, такие как добавление новых товаров и получение информации о категориях. Взаимодействие с PrestaShop API осуществляется асинхронно, что позволяет повысить производительность и отзывчивость приложения.

## Классы

### `PrestaProductAsync`

**Описание**: Класс для управления товарами в PrestaShop.

**Наследует**: `PrestaShopAsync`

**Методы**:

- `__init__(self, *args, **kwargs)`: Инициализирует объект класса `PrestaProductAsync`.
- `add_new_product_async(self, f: ProductFields) -> ProductFields | None`: Асинхронно добавляет новый товар в PrestaShop.

## Методы класса

### `__init__(self, *args, **kwargs)`

```python
def __init__(self, *args, **kwargs):
    """
    Инициализирует объект Product.

    Args:
        *args: Список позиционных аргументов.
        **kwargs: Словарь именованных аргументов.
    """
```

**Назначение**: Инициализирует объект класса `PrestaProductAsync`, вызывая конструктор родительского класса `PrestaShopAsync` и инициализируя атрибут `presta_category_async` экземпляром класса `PrestaCategoryAsync`.

**Параметры**:

- `*args`: Список позиционных аргументов, передаваемых в конструктор родительского класса `PrestaShopAsync`.
- `**kwargs`: Словарь именованных аргументов, передаваемых в конструктор родительского класса `PrestaShopAsync`.

**Как работает функция**:

- Вызывает конструктор родительского класса `PrestaShopAsync` с переданными аргументами.
- Инициализирует атрибут `presta_category_async` экземпляром класса `PrestaCategoryAsync`, также передавая аргументы.

**Примеры**:

```python
product = PrestaProductAsync(api_url='https://example.com/api', api_key='your_api_key')
```

### `add_new_product_async(self, f: ProductFields) -> ProductFields | None`

```python
async def add_new_product_async(self, f: ProductFields) -> ProductFields | None:
    """
    Add a new product to PrestaShop.

    Args:
        f (ProductFields): An instance of the ProductFields data class containing the product information.

    Returns:
        ProductFields | None: Returns the `ProductFields` object with `id_product` set, if the product was added successfully, `None` otherwise.
    """
```

**Назначение**: Асинхронно добавляет новый товар в PrestaShop.

**Параметры**:

- `f` (`ProductFields`): Объект класса `ProductFields`, содержащий информацию о товаре.

**Возвращает**:

- `ProductFields | None`: Объект `ProductFields` с установленным `id_product` в случае успешного добавления товара, в противном случае - `None`.

**Как работает функция**:

1.  Получает список родительских категорий товара с использованием метода `get_parent_categories_list` класса `PrestaCategoryAsync`.
2.  Преобразует объект `ProductFields` в словарь.
3.  Создает новый товар в PrestaShop с использованием метода `create`.
4.  Если товар не был добавлен, логирует ошибку и возвращает `None`.
5.  Загружает изображение товара с использованием метода `create_binary`.
6.  Если загрузка изображения прошла успешно, возвращает `True`, иначе логирует ошибку и возвращает `None`.

**Примеры**:

```python
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
    id_category_default=3
)

new_product = await product.add_new_product_async(product_fields)
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print('Error add new product')
```