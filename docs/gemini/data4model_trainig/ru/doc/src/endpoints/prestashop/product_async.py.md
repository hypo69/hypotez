# Модуль `product_async`

## Обзор

Модуль `product_async` предназначен для организации взаимодействия между веб-сайтом, информацией о товарах и PrestaShop. Он определяет поведение продукта в проекте, позволяя асинхронно добавлять новые продукты в PrestaShop, получать информацию о категориях и загружать изображения продуктов.

## Подробнее

Модуль содержит класс `PrestaProductAsync`, который расширяет класс `PrestaShopAsync` и предоставляет методы для работы с продуктами в PrestaShop. Он использует другие модули, такие как `PrestaCategoryAsync` для работы с категориями, `ProductFields` для представления полей продукта, а также утилиты для преобразования данных и логирования.

## Классы

### `PrestaProductAsync`

**Описание**: Класс для управления продуктами в PrestaShop. Позволяет добавлять новые продукты, загружать изображения и получать информацию о категориях.

**Наследует**: `PrestaShopAsync`

**Методы**:

- `__init__(self, *args, **kwargs)`: Инициализирует объект `PrestaProductAsync`.
- `add_new_product_async(self, f: ProductFields) -> ProductFields | None`: Асинхронно добавляет новый продукт в PrestaShop.

### `__init__`

```python
def __init__(self, *args, **kwargs):
    """
    Initializes a Product object.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    PrestaShopAsync.__init__(self, *args, **kwargs)
    self.presta_category_async = PrestaCategoryAsync(*args, **kwargs)
```

**Назначение**: Инициализирует объект `PrestaProductAsync`, вызывая конструктор родительского класса `PrestaShopAsync` и создавая экземпляр класса `PrestaCategoryAsync` для работы с категориями.

**Параметры**:

- `*args`: Список позиционных аргументов, передаваемых в конструктор родительского класса.
- `**kwargs`: Словарь именованных аргументов, передаваемых в конструктор родительского класса.

**Как работает функция**:

- Вызывает конструктор родительского класса `PrestaShopAsync` для инициализации общих параметров.
- Создает экземпляр класса `PrestaCategoryAsync`, который будет использоваться для работы с категориями продуктов.

**Примеры**:

```python
product = PrestaProductAsync(api_url='https://example.com/api', api_key='YOUR_API_KEY')
```

### `add_new_product_async`

```python
async def add_new_product_async(self, f: ProductFields) -> ProductFields | None:
    """
    Add a new product to PrestaShop.

    Args:
        f (ProductFields): An instance of the ProductFields data class containing the product information.

    Returns:
        ProductFields | None: Returns the `ProductFields` object with `id_product` set, if the product was added successfully, `None` otherwise.
    """

    f.additional_categories = await self.presta_category_async.get_parent_categories_list(f.id_category_default)
    
    presta_product_dict:dict = f.to_dict()
    
    new_f:ProductFields = await self.create('products', presta_product_dict)

    if not new_f:
        logger.error(f"Товар не был добавлен в базу данных Presyashop")
        ...
        return

    if await self.create_binary(f'images/products/{new_f.id_product}', f.local_image_path, new_f.id_product):
        return True

    else:
        logger.error(f"Не подналось изображение")
        ...
        return
    ...
```

**Назначение**: Асинхронно добавляет новый продукт в PrestaShop, используя информацию, содержащуюся в объекте `ProductFields`.

**Параметры**:

- `f` (`ProductFields`): Объект класса `ProductFields`, содержащий информацию о продукте, который нужно добавить.

**Возвращает**:

- `ProductFields | None`: Возвращает объект `ProductFields` с установленным `id_product` в случае успешного добавления продукта, в противном случае возвращает `None`.

**Как работает функция**:

1.  Получает список родительских категорий для продукта, используя метод `get_parent_categories_list` класса `PrestaCategoryAsync`.
2.  Преобразует объект `ProductFields` в словарь.
3.  Создает новый продукт в PrestaShop, используя метод `create` родительского класса `PrestaShopAsync`.
4.  Если продукт не был создан, логирует ошибку и возвращает `None`.
5.  Загружает изображение продукта, используя метод `create_binary`.
6.  Если изображение не было загружено, логирует ошибку и возвращает `None`.
7.  В случае успешного добавления продукта и загрузки изображения возвращает `True`.

**Примеры**:

```python
product = PrestaProductAsync(api_url='https://example.com/api', api_key='YOUR_API_KEY')
product_fields = ProductFields(name='Test Product', price=19.99, id_category_default=3)
new_product = await product.add_new_product_async(product_fields)
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print('Error adding new product')
```

## Функции

### `main`

```python
async def main():
    # Example usage
    product = ProductAsync()
    product_fields = ProductFields(
        lang_index = 1,
        name='Test Product Async',
        price=19.99,
        description='This is an asynchronous test product.',
    )
    
    parent_categories = await Product.get_parent_categories(id_category=3)
    print(f'Parent categories: {parent_categories}')


    new_product = await product.add_new_product(product_fields)
    if new_product:
        print(f'New product id = {new_product.id_product}')
    else:
        print(f'Error add new product')

    await product.fetch_data_async()
```

**Назначение**: Пример использования класса `PrestaProductAsync` и его методов.

**Как работает функция**:

1.  Создает экземпляр класса `ProductAsync`.
2.  Создает экземпляр класса `ProductFields` с данными о продукте.
3.  Получает список родительских категорий для продукта.
4.  Добавляет новый продукт в PrestaShop, используя метод `add_new_product`.
5.  Выводит информацию о результате добавления продукта.
6.  Вызывает метод `fetch_data_async`.

**Примеры**:

```python
if __name__ == '__main__':
    asyncio.run(main())