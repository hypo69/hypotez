# Модуль асинхронного взаимодействия с товарами в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.product_async` предоставляет инструменты для асинхронного взаимодействия с товарами в PrestaShop. Он определяет поведение товара в проекте.

## Подробней

Модуль предоставляет класс `PrestaProductAsync` для асинхронного добавления новых товаров в PrestaShop.

## Классы

### `PrestaProductAsync`

**Описание**: Класс для асинхронного управления товарами в PrestaShop.

**Наследует**:

*   `PrestaShopAsync`: Предоставляет асинхронные методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   `presta_category_async` (PrestaCategoryAsync): Экземпляр класса `PrestaCategoryAsync` для работы с категориями PrestaShop.

**Методы**:

*   `__init__(self, *args, **kwargs)`: Инициализирует объект `PrestaProductAsync`.
*   `add_new_product_async(self, f: ProductFields) -> ProductFields | None`: Асинхронно добавляет новый товар в PrestaShop.

## Методы класса `PrestaProductAsync`

### `__init__`

```python
def __init__(self, *args, **kwargs):
```

**Назначение**: Инициализирует объект `PrestaProductAsync`.

**Параметры**:

*   `*args`: Произвольные аргументы.
*   `**kwargs`: Произвольные именованные аргументы.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaShopAsync` с переданными аргументами.
2.  Создает экземпляр класса `PrestaCategoryAsync`.

### `add_new_product_async`

```python
async def add_new_product_async(self, f: ProductFields) -> ProductFields | None:
```

**Назначение**: Асинхронно добавляет новый товар в PrestaShop.

**Параметры**:

*   `f` (ProductFields): Объект `ProductFields`, содержащий информацию о товаре.

**Возвращает**:

*   `ProductFields | None`: Объект `ProductFields` с установленным `id_product`, если товар успешно добавлен, `None` в противном случае.

**Как работает функция**:

1.  Асинхронно получает список родительских категорий, используя `presta_category_async.get_parent_categories_list(f.id_category_default)`.
2.  Преобразует объект `ProductFields` в словарь `presta_product_dict`.
3.  Асинхронно вызывает метод `create` для добавления нового товара в PrestaShop API.
4.  Если добавление товара не удалось, логирует ошибку и возвращает `None`.
5.  Асинхронно создает бинарные данные для изображения товара, вызывая метод `create_binary` и передавая необходимые параметры.
6.  Если создание бинарных данных прошло успешно, возвращает `True`, иначе логирует ошибку и возвращает `None`.

## Примеры

### `main` (заглушка)

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

**Назначение**: Пример асинхронного добавления товара в PrestaShop.

**Как работает функция**:

1.  Создает экземпляр класса `ProductAsync`.
2.  Создает экземпляр класса `ProductFields` с данными товара.
3.  Асинхронно вызывает метод `get_parent_categories` для получения родительских категорий (пример).
4.  Асинхронно вызывает метод `add_new_product` для добавления нового товара.
5.  Выводит информацию о результате добавления товара.