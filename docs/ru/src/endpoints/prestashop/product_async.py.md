# Модуль `product_async`

## Обзор

Модуль `product_async` предназначен для взаимодействия с веб-сайтом, базой данных товаров и PrestaShop. Он определяет поведение товара в проекте, позволяя добавлять новые товары, получать информацию о родительских категориях и выполнять другие операции, связанные с товарами, асинхронно. Модуль использует PrestaShop API для управления товарами.

## Подробнее

Модуль содержит класс `PrestaProductAsync`, который наследует `PrestaShopAsync` и предоставляет методы для работы с товарами в PrestaShop. Он позволяет добавлять новые товары, получая данные о товаре с веб-страницы и взаимодействуя с PrestaShop API. Также в модуле определены функции для асинхронного выполнения операций.

## Классы

### `PrestaProductAsync`

**Описание**: Класс для выполнения операций с товарами. Инициализирует граббер для получения данных со страницы товара и взаимодействует с PrestaShop API.
**Наследует**: `PrestaShopAsync`

**Методы**:
- `__init__`: Инициализирует объект `PrestaProductAsync`.
- `add_new_product_async`: Добавляет новый товар в PrestaShop.

#### `__init__`

```python
def __init__(self, *args, **kwargs):
    """
    Initializes a Product object.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
```

**Назначение**: Инициализирует объект `PrestaProductAsync`, вызывая конструктор родительского класса `PrestaShopAsync` и создавая экземпляр класса `PrestaCategoryAsync`.

**Параметры**:
- `*args`: Список позиционных аргументов, передаваемых в конструктор родительского класса.
- `**kwargs`: Словарь именованных аргументов, передаваемых в конструктор родительского класса.

**Как работает функция**:
- Вызывает конструктор родительского класса `PrestaShopAsync` с переданными аргументами.
- Создает экземпляр класса `PrestaCategoryAsync`, который используется для работы с категориями товаров.

#### `add_new_product_async`

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

**Назначение**: Асинхронно добавляет новый товар в PrestaShop, используя API.

**Параметры**:
- `f` (ProductFields): Объект класса `ProductFields`, содержащий информацию о товаре.

**Возвращает**:
- `ProductFields | None`: Объект `ProductFields` с установленным `id_product`, если товар успешно добавлен, иначе `None`.

**Как работает функция**:
1.  Функция извлекает дополнительные категории, используя `presta_category_async.get_parent_categories_list(f.id_category_default)`.
2.  Преобразует объект `ProductFields` в словарь `presta_product_dict`.
3.  Использует метод `create` для создания товара в PrestaShop. Если товар не создан, функция логирует ошибку и возвращает `None`.
4.  После успешного создания товара, функция пытается создать бинарное представление изображения товара, используя `create_binary`. Если изображение успешно создано, функция возвращает `True`. В противном случае, функция логирует ошибку и возвращает `None`.

## Функции

### `main`

```python
async def main():
    """
    Пример использования класса `ProductAsync` и его методов.
    """
```

**Назначение**: Пример использования класса `PrestaProductAsync` и его методов.

**Как работает функция**:
1.  Создает экземпляр класса `PrestaProductAsync`.
2.  Создает экземпляр класса `ProductFields` с данными о товаре.
3.  Получает родительские категории товара.
4.  Добавляет новый товар, используя метод `add_new_product_async`.
5.  Выводит информацию о результате добавления товара.
6.  Вызывает метод `fetch_data_async`.

**Примеры**:
```python
# Пример использования
product = PrestaProductAsync()
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