# Модуль PrestaProductAsync

## Обзор

Модуль `PrestaProductAsync` предоставляет функции для взаимодействия с товарами в PrestaShop. Он использует асинхронные методы для ускорения процесса обработки. 

## Подробнее

Модуль `PrestaProductAsync` предназначен для управления товарами в PrestaShop. Он наследует класс `PrestaShopAsync`, который предоставляет базовые функции для работы с API PrestaShop. 

`PrestaProductAsync` используется в проекте для добавления новых товаров в PrestaShop, а также для получения данных о товарах из внешних источников. 

## Классы

### `PrestaProductAsync`

**Описание**: Класс `PrestaProductAsync` предоставляет функции для работы с товарами в PrestaShop. 

**Наследует**: 
    - `PrestaShopAsync`

**Атрибуты**:

- `presta_category_async`:  Экземпляр класса `PrestaCategoryAsync`, используемый для работы с категориями товаров.

**Методы**:

- `add_new_product_async()`:  Добавляет новый товар в PrestaShop. 
- `create_binary()`:  Загружает изображение товара.

## Функции

### `add_new_product_async`

**Назначение**: Добавляет новый товар в PrestaShop.

**Параметры**:

- `f` (`ProductFields`):  Объект `ProductFields`, содержащий информацию о товаре.

**Возвращает**:
- `ProductFields | None`: Объект `ProductFields` с установленным `id_product`, если товар был добавлен успешно.  `None`, если товар не был добавлен.

**Вызывает исключения**:

- `Exception`:  Если возникает ошибка при добавлении товара или загрузки изображения.

**Как работает функция**:

1. Получает список родительских категорий для `id_category_default` товара с помощью метода `get_parent_categories_list` класса `PrestaCategoryAsync`.
2. Преобразует объект `ProductFields` в словарь с помощью метода `to_dict`.
3. Вызывает метод `create` базового класса `PrestaShopAsync` для добавления товара в PrestaShop.
4. Если товар был добавлен успешно, функция загружает изображение с помощью метода `create_binary`.
5. Возвращает объект `ProductFields` с установленным `id_product`, если товар был добавлен успешно.  `None`, если товар не был добавлен.

**Пример**:

```python
# Создание инстанса класса PrestaProductAsync
product = PrestaProductAsync()

# Создание объекта ProductFields с информацией о товаре
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
)

# Добавление товара в PrestaShop
new_product = await product.add_new_product_async(product_fields)

# Проверка результата
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print(f'Error add new product')
```

### `create_binary`

**Назначение**: Загружает изображение товара в PrestaShop.

**Параметры**:

- `file_path` (str): Путь к файлу с изображением.

**Возвращает**:
- `bool`: `True`, если изображение было загружено успешно, `False` в противном случае.

**Вызывает исключения**:

- `Exception`:  Если возникает ошибка при загрузке изображения.

**Как работает функция**:

1. Вызывает метод `create_binary` базового класса `PrestaShopAsync` для загрузки изображения.
2. Возвращает `True`, если изображение было загружено успешно, `False` в противном случае.

## Примеры

```python
# Создание инстанса класса PrestaProductAsync
product = PrestaProductAsync()

# Создание объекта ProductFields с информацией о товаре
product_fields = ProductFields(
    lang_index=1,
    name='Test Product Async',
    price=19.99,
    description='This is an asynchronous test product.',
)

# Добавление товара в PrestaShop
new_product = await product.add_new_product_async(product_fields)

# Проверка результата
if new_product:
    print(f'New product id = {new_product.id_product}')
else:
    print(f'Error add new product')