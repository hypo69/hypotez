# Модуль `product_async.py`

## Обзор

Модуль `product_async.py` предназначен для управления продуктами в PrestaShop с использованием асинхронных операций. Он обеспечивает взаимодействие между веб-сайтом, данными о продуктах и API PrestaShop. Модуль позволяет добавлять новые продукты, обновлять информацию о продуктах и выполнять другие операции, связанные с управлением продуктами, используя асинхронный подход для повышения производительности.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает асинхронное взаимодействие с PrestaShop для управления продуктами. Он включает в себя класс `PrestaProductAsync`, который наследуется от `PrestaShopAsync` и использует `ProductFields` для представления данных о продукте. Модуль использует `asyncio` для выполнения асинхронных операций, что позволяет эффективно обрабатывать запросы к API PrestaShop и управлять продуктами в интернет-магазине.

## Классы

### `PrestaProductAsync`

**Описание**: Класс `PrestaProductAsync` предназначен для выполнения операций с продуктами в PrestaShop. Он позволяет добавлять, обновлять и удалять продукты, а также получать информацию о них через API PrestaShop. Класс использует асинхронные методы для обеспечения высокой производительности.

**Наследует**:
- `PrestaShopAsync`: Предоставляет базовые методы для взаимодействия с API PrestaShop.

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

**Назначение**: Инициализирует объект `PrestaProductAsync`, вызывая конструктор родительского класса `PrestaShopAsync` и создавая экземпляр класса `PrestaCategoryAsync` для работы с категориями продуктов.

**Параметры**:
- `*args`: Произвольный список аргументов.
- `**kwargs`: Произвольный словарь аргументов.

**Как работает функция**:
1. Вызывает конструктор родительского класса `PrestaShopAsync` для инициализации базовых параметров.
2. Создает экземпляр класса `PrestaCategoryAsync`, который используется для работы с категориями продуктов.

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

**Назначение**: Асинхронно добавляет новый продукт в PrestaShop.

**Параметры**:
- `f` (`ProductFields`): Объект класса `ProductFields`, содержащий информацию о продукте.

**Возвращает**:
- `ProductFields | None`: Объект `ProductFields` с установленным `id_product`, если продукт был успешно добавлен, иначе `None`.

**Как работает функция**:

1. **Получение дополнительных категорий**:
   - `f.additional_categories = await self.presta_category_async.get_parent_categories_list(f.id_category_default)`: Получает список родительских категорий для продукта, используя метод `get_parent_categories_list` класса `PrestaCategoryAsync`. Результат сохраняется в атрибуте `additional_categories` объекта `f`.
2. **Преобразование данных продукта в словарь**:
   - `presta_product_dict:dict = f.to_dict()`: Преобразует объект `ProductFields` в словарь, который будет отправлен в API PrestaShop.
3. **Создание продукта в PrestaShop**:
   - `new_f:ProductFields = await self.create('products', presta_product_dict)`: Отправляет запрос к API PrestaShop для создания нового продукта, используя метод `create` класса `PrestaShopAsync`. Результат (объект `ProductFields` с установленным `id_product`) сохраняется в переменной `new_f`.
4. **Обработка ошибок при создании продукта**:
   - `if not new_f:`: Проверяет, был ли продукт успешно создан. Если `new_f` равен `None`, это означает, что произошла ошибка.
   - `logger.error(f"Товар не был добавлен в базу данных Presyashop")`: Логирует сообщение об ошибке с использованием модуля `logger`.
   - `return`: Возвращает `None`, указывая на неудачное добавление продукта.
5. **Создание бинарного изображения продукта**:
   - `if await self.create_binary(f'images/products/{new_f.id_product}', f.local_image_path, new_f.id_product):`: Отправляет запрос к API PrestaShop для создания бинарного изображения продукта, используя метод `create_binary` класса `PrestaShopAsync`. Путь к изображению формируется как `images/products/{new_f.id_product}`.
   - `return True`: Если изображение было успешно создано, возвращает `True`.
6. **Обработка ошибок при создании изображения**:
   - `else:`: Если создание изображения завершилось неудачно.
   - `logger.error(f"Не подналось изображение")`: Логирует сообщение об ошибке с использованием модуля `logger`.
   - `return`: Возвращает `None`, указывая на неудачное добавление изображения.

**ASCII flowchart**:

```
    Начало
    │
    └──> Получение дополнительных категорий
    │
    └──> Преобразование данных продукта в словарь
    │
    └──> Создание продукта в PrestaShop
    │
    └──> Проверка успешности создания продукта
        │
        ├──> Да: Создание бинарного изображения продукта
        │   │
        │   └──> Проверка успешности создания изображения
        │       │
        │       ├──> Да: Возврат True (успех)
        │       │
        │       └──> Нет: Логирование ошибки и возврат None (ошибка)
        │
        └──> Нет: Логирование ошибки и возврат None (ошибка)
```

**Примеры**:

```python
# Пример использования функции add_new_product_async
product = PrestaProductAsync()
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
    id_category_default=3
)

async def add_product():
    new_product = await product.add_new_product_async(product_fields)
    if new_product:
        print(f'New product id = {new_product.id_product}')
    else:
        print('Error adding new product')

asyncio.run(add_product())
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

**Назначение**: Функция `main` является точкой входа для асинхронного выполнения операций с продуктами. Она создает экземпляр класса `ProductAsync`, устанавливает параметры продукта и добавляет его в PrestaShop.

**Как работает функция**:
1. Создает экземпляр класса `ProductAsync`.
2. Создает экземпляр класса `ProductFields` и устанавливает параметры продукта.
3. Вызывает метод `get_parent_categories` для получения списка родительских категорий.
4. Вызывает метод `add_new_product` для добавления нового продукта в PrestaShop.
5. Выводит информацию о результате добавления продукта.
6. Вызывает метод `fetch_data_async` для получения данных о продукте.