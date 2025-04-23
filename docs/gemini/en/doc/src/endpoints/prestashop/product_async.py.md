# Module src.endpoints.prestashop.product_async

## Overview

The module defines the `PrestaProductAsync` class, which is responsible for interacting with the PrestaShop API to manipulate products. It includes functionality for adding new products to PrestaShop.

## More details

This module is designed to streamline the process of managing products in a PrestaShop store. It uses asynchronous requests to improve performance and efficiency.  The module is used to automate product management tasks such as adding new products, including their images.

## Classes

### `PrestaProductAsync`

**Description**: This class provides methods for interacting with the PrestaShop API to manipulate products. It inherits from `PrestaShopAsync`.

**Inherits**:
- `PrestaShopAsync`: Provides asynchronous communication with the PrestaShop API.

**Attributes**:
- `presta_category_async` (PrestaCategoryAsync): An instance of the `PrestaCategoryAsync` class for working with product categories.

**Methods**:
- `__init__(self, *args, **kwargs)`: Initializes a `PrestaProductAsync` object.
- `add_new_product_async(self, f: ProductFields) -> ProductFields | None`: Adds a new product to PrestaShop.

### `PrestaProductAsync` Methods

#### `__init__(self, *args, **kwargs)`

```python
def __init__(self, *args, **kwargs):
    """
    Initializes a Product object.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
```

**Parameters**:
- `*args`: Variable length argument list.
- `**kwargs`: Arbitrary keyword arguments.

**How the function works**:
- Initializes the `PrestaProductAsync` class, calling the constructor of the parent class `PrestaShopAsync`.
- Creates an instance of `PrestaCategoryAsync` to handle product categories.

**Examples**:
```python
product = PrestaProductAsync()
```

#### `add_new_product_async(self, f: ProductFields) -> ProductFields | None`

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

**Purpose**: Adds a new product to PrestaShop.

**Parameters**:
- `f` (ProductFields): An instance of the `ProductFields` data class containing the product information.

**Returns**:
- `ProductFields | None`: Returns the `ProductFields` object with `id_product` set, if the product was added successfully, `None` otherwise.

**How the function works**:
1. **Извлекает** дополнительные категории товара, используя `presta_category_async.get_parent_categories_list(f.id_category_default)`.
2. **Преобразовывает** объект `ProductFields` в словарь `presta_product_dict`.
3. **Создает** новый продукт в PrestaShop, вызывая метод `create('products', presta_product_dict)`.
4. **Проверяет**, был ли продукт успешно добавлен. Если нет, логирует ошибку и возвращает `None`.
5. **Создает** бинарное изображение продукта, вызывая метод `create_binary(f'images/products/{new_f.id_product}', f.local_image_path, new_f.id_product)`.
6. **Проверяет**, было ли изображение успешно добавлено. Если нет, логирует ошибку и возвращает `None`.

**Examples**:
```python
product = PrestaProductAsync()
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
)
new_product = await product.add_new_product_async(product_fields)
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print('Error adding new product')
```

## Functions

### `main()`

```python
async def main():
    """
    Пример использования асинхронных функций для добавления продукта в PrestaShop.
    """
```

**Purpose**: Demonstrates the usage of asynchronous functions for adding a product to PrestaShop.

**How the function works**:
1. **Создает** экземпляр класса `ProductAsync`.
2. **Создает** экземпляр класса `ProductFields` с данными тестового продукта.
3. **Получает** родительские категории продукта, используя `Product.get_parent_categories(id_category=3)`.
4. **Добавляет** новый продукт, используя метод `add_new_product(product_fields)`.
5. **Выводит** результат добавления продукта в консоль.
6. **Вызывает** метод `fetch_data_async()` для получения данных.

**Examples**:
```python
asyncio.run(main())