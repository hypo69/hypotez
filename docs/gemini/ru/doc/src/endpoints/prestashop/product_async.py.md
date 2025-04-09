# Модуль для асинхронного управления продуктами в PrestaShop

## Обзор

Модуль `product_async.py` предназначен для асинхронного взаимодействия с PrestaShop API с целью управления продуктами. Он включает в себя добавление новых продуктов, получение информации о категориях и загрузку изображений. Модуль использует асинхронные вызовы для оптимизации работы с API.

## Подробней

Модуль предоставляет класс `PrestaProductAsync`, который наследуется от `PrestaShopAsync` и содержит методы для выполнения операций с продуктами, такими как добавление новых продуктов.  Он также включает вспомогательные функции, такие как `main`, для демонстрации использования основных функций модуля. Расположение файла в структуре проекта указывает на его роль в качестве компонента, отвечающего за взаимодействие с PrestaShop API для управления продуктами.

## Классы

### `PrestaProductAsync`

**Описание**: Класс для выполнения операций с продуктами в PrestaShop. Он позволяет добавлять новые продукты, получать информацию о категориях и загружать изображения, используя асинхронные вызовы API.

**Наследует**:
- `PrestaShopAsync`: Предоставляет базовую функциональность для взаимодействия с PrestaShop API.

**Методы**:
- `__init__(self, *args, **kwargs)`: Инициализирует объект `PrestaProductAsync` и вызывает конструктор родительского класса `PrestaShopAsync`. Также инициализирует объект `PrestaCategoryAsync` для работы с категориями.
- `add_new_product_async(self, f: ProductFields) -> ProductFields | None`: Асинхронно добавляет новый продукт в PrestaShop.

### `__init__(self, *args, **kwargs)`

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

**Назначение**: Инициализирует объект `PrestaProductAsync`.

**Параметры**:
- `*args`: Произвольный список позиционных аргументов.
- `**kwargs`: Произвольный словарь именованных аргументов.

**Как работает функция**:
1. Вызывает конструктор родительского класса `PrestaShopAsync` для инициализации базовых параметров API.
2. Создает экземпляр класса `PrestaCategoryAsync` для работы с категориями PrestaShop.

```ascii
Создание экземпляра PrestaProductAsync
│
├─── Вызов __init__ родительского класса PrestaShopAsync
│
└─── Создание экземпляра PrestaCategoryAsync для управления категориями
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

**Назначение**: Асинхронно добавляет новый продукт в PrestaShop, используя данные из объекта `ProductFields`.

**Параметры**:
- `f` (ProductFields): Объект `ProductFields`, содержащий информацию о продукте.

**Возвращает**:
- `ProductFields | None`: Объект `ProductFields` с установленным `id_product` в случае успешного добавления продукта, `None` в противном случае.

**Как работает функция**:

1. **Получение дополнительных категорий**:
   - Вызывает `self.presta_category_async.get_parent_categories_list(f.id_category_default)` для получения списка родительских категорий продукта на основе `id_category_default`.

2. **Преобразование данных продукта**:
   - Преобразует объект `ProductFields` в словарь `presta_product_dict` с помощью метода `f.to_dict()`.

3. **Создание продукта в PrestaShop**:
   - Вызывает метод `self.create('products', presta_product_dict)` для создания продукта в PrestaShop.
   - Если продукт не создан, регистрирует ошибку и возвращает `None`.

4. **Загрузка изображения продукта**:
   - Вызывает метод `self.create_binary(f'images/products/{new_f.id_product}', f.local_image_path, new_f.id_product)` для загрузки изображения продукта.
   - Если изображение загружено успешно, возвращает `True`. В противном случае регистрирует ошибку и возвращает `None`.

```ascii
Добавление нового продукта в PrestaShop
│
├─── Получение дополнительных категорий
│   │
│   └─── Вызов get_parent_categories_list()
│
├─── Преобразование ProductFields в словарь
│   │
│   └─── Вызов to_dict()
│
├─── Создание продукта в PrestaShop
│   │
│   └─── Вызов create()
│
├─── Загрузка изображения продукта (если продукт создан)
│   │
│   └─── Вызов create_binary()
│
└─── Возврат результата или None в случае ошибки
```

## Функции

### `main()`

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

**Назначение**: Функция `main` является асинхронной функцией, которая демонстрирует пример использования класса `PrestaProductAsync` для добавления нового продукта в PrestaShop.

**Как работает функция**:

1. **Создание экземпляра `ProductAsync`**:
   - Создается экземпляр класса `ProductAsync`.

2. **Создание экземпляра `ProductFields`**:
   - Создается экземпляр класса `ProductFields` с параметрами тестового продукта.

3. **Получение родительских категорий**:
   - Вызывается функция `Product.get_parent_categories(id_category=3)` для получения списка родительских категорий продукта.

4. **Добавление нового продукта**:
   - Вызывается метод `product.add_new_product(product_fields)` для добавления нового продукта в PrestaShop.
   - Если продукт добавлен успешно, выводится его `id`. В противном случае выводится сообщение об ошибке.

5. **Получение данных**:
   - Вызывается метод `product.fetch_data_async()` для получения данных.

```ascii
Выполнение функции main()
│
├─── Создание экземпляра ProductAsync
│
├─── Создание экземпляра ProductFields
│
├─── Получение родительских категорий
│
├─── Добавление нового продукта
│
└─── Получение данных