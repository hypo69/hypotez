# Модуль для взаимодействия с товарами в PrestaShop (`product.py`)

## Обзор

Модуль `product.py` предназначен для взаимодействия с товарами в PrestaShop. Он включает в себя классы и функции для получения информации о товарах, добавления новых товаров, а также для работы с категориями товаров.

## Подробней

Этот модуль предоставляет инструменты для работы с API PrestaShop, позволяя автоматизировать процессы управления товарами. Он использует конфигурационные данные для подключения к API и предоставляет методы для выполнения различных операций, связанных с товарами, таких как получение схемы товара, добавление новых товаров и получение информации о родительских категориях.

## Классы

### `Config`

**Описание**: Класс конфигурации для настроек продукта PrestaShop.

**Атрибуты**:

- `USE_ENV` (bool): Указывает, использовать ли переменные окружения. По умолчанию `False`.
- `MODE` (str): Режим работы (`dev`, `dev8`, `prod`). По умолчанию `'dev'`.
- `POST_FORMAT` (str): Формат данных для отправки (`XML`). По умолчанию `'XML'`.
- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

**Принцип работы**:
Класс `Config` определяет параметры конфигурации, необходимые для подключения к API PrestaShop. Он проверяет, использовать ли переменные окружения или значения, заданные в коде, в зависимости от режима работы. В зависимости от значения `MODE` и `USE_ENV` выбираются учетные данные для подключения к PrestaShop API.

### `PrestaProduct`

**Описание**: Класс для работы с товарами в PrestaShop.

**Наследует**:
- `PrestaShop`: Наследует функциональность для взаимодействия с API PrestaShop.

**Методы**:

- `__init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None`: Инициализирует объект `PrestaProduct`.
- `get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = 'blank') -> dict`: Возвращает схему для ресурса продукта из PrestaShop.
- `get_parent_category(self, id_category: int) -> Optional[int]`: Рекурсивно получает родительские категории из PrestaShop для заданной категории.
- `_add_parent_categories(self, f: ProductFields) -> None`: Вычисляет и добавляет все родительские категории для списка ID категорий к объекту `ProductFields`.
- `get_product(self, id_product: int, **kwards) -> dict`: Возвращает словарь полей товара из магазина PrestaShop.
- `add_new_product(self, f: ProductFields) -> dict`: Добавляет новый продукт в PrestaShop.

## Методы класса `PrestaProduct`

### `__init__`

```python
def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
```

**Назначение**: Инициализирует объект `PrestaProduct`.

**Параметры**:

- `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `''`.
- `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `''`.
- `*args`: Произвольные позиционные аргументы, которые передаются в конструктор родительского класса `PrestaShop`.
- `**kwargs`: Произвольные именованные аргументы, которые передаются в конструктор родительского класса `PrestaShop`.

**Возвращает**:
- `None`

**Как работает функция**:
Конструктор класса `PrestaProduct` вызывает конструктор родительского класса `PrestaShop`, передавая ему ключ API и домен API. Если `api_key` и `api_domain` не переданы в качестве аргументов, используются значения из класса `Config`.

**Примеры**:

```python
product = PrestaProduct(api_key='your_api_key', api_domain='your_api_domain')
```

### `get_product_schema`

```python
def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = 'blank') -> dict:
```

**Назначение**: Получает схему для ресурса продукта из PrestaShop.

**Параметры**:

- `resource_id` (Optional[str | int], optional): ID ресурса продукта. По умолчанию `None`.
- `schema` (Optional[str], optional): Тип схемы. По умолчанию `'blank'`.

**Возвращает**:
- `dict`: Схема для ресурса продукта.

**Как работает функция**:
Метод `get_product_schema` вызывает метод `get_schema` родительского класса `PrestaShop` для получения схемы продукта. Он передает параметры `resource`, `resource_id`, `schema` и `display` для формирования запроса к API PrestaShop.

**Примеры**:

```python
product = PrestaProduct()
schema = product.get_product_schema(resource_id=123, schema='full')
print(schema)
```

### `get_parent_category`

```python
def get_parent_category(self, id_category: int) -> Optional[int]:
```

**Назначение**: Рекурсивно получает родительские категории из PrestaShop для заданной категории.

**Параметры**:

- `id_category` (int): ID категории.

**Возвращает**:
- `Optional[int]`: ID родительской категории (int) или `None` в случае ошибки или если родительская категория не найдена.

**Как работает функция**:
Метод `get_parent_category` выполняет запрос к API PrestaShop для получения информации о категории с заданным `id_category`. Затем он извлекает `id_parent` из ответа и возвращает его. Если категория не найдена или возникает ошибка при запросе, метод возвращает `None`.

**Примеры**:

```python
product = PrestaProduct()
parent_category_id = product.get_parent_category(id_category=456)
if parent_category_id:
    print(f"Parent category ID: {parent_category_id}")
else:
    print("Parent category not found or error occurred.")
```

### `_add_parent_categories`

```python
def _add_parent_categories(self, f: ProductFields) -> None:
```

**Назначение**: Вычисляет и добавляет все родительские категории для списка ID категорий к объекту `ProductFields`.

**Параметры**:

- `f` (ProductFields): Объект `ProductFields`, к которому нужно добавить родительские категории.

**Как работает функция**:
Метод `_add_parent_categories` итерируется по списку дополнительных категорий в объекте `ProductFields`. Для каждой категории он получает её `id` и, если `id` не является корневой категорией (1 или 2), рекурсивно получает родительские категории с помощью метода `get_parent_category`. Полученные родительские категории добавляются в объект `ProductFields` с помощью метода `additional_category_append`.

**Примеры**:

```python
from src.endpoints.prestashop.product_fields import ProductFields

product = PrestaProduct()
product_fields = ProductFields()
product_fields.additional_categories = [{'id': '123'}, {'id': '456'}]
product._add_parent_categories(product_fields)
print(product_fields.additional_categories)
```

### `get_product`

```python
def get_product(self, id_product: int, **kwards) -> dict:
```

**Назначение**: Возвращает словарь полей товара из магазина PrestaShop.

**Параметры**:

- `id_product` (int): Значение поля ID в таблице `product` PrestaShop.
- `**kwards`: Дополнительные именованные аргументы для передачи в метод `read`.

**Возвращает**:

- `dict`: Словарь с информацией о продукте.
  ```
  {
      'product':
          {... product fields}
  }
  ```

**Как работает функция**:
Метод `get_product` вызывает метод `read` родительского класса `PrestaShop` для получения информации о продукте с заданным `id_product`. Он передает параметры `resource`, `resource_id` и `kwards` для формирования запроса к API PrestaShop.

**Примеры**:

```python
product = PrestaProduct()
product_data = product.get_product(id_product=789)
print(product_data)
```

### `add_new_product`

```python
def add_new_product(self, f: ProductFields) -> dict:
```

**Назначение**: Добавляет новый продукт в PrestaShop.

**Параметры**:

- `f` (ProductFields): Экземпляр класса `ProductFields`, содержащий информацию о продукте.

**Возвращает**:

- `dict`: Возвращает объект `ProductFields` с установленным `id_product`, если продукт был успешно добавлен, в противном случае `None`.

**Как работает функция**:
Метод `add_new_product` преобразует объект `ProductFields` в словарь формата PrestaShop и отправляет его в API PrestaShop. Сначала он добавляет `id_category_default` в поле `additional_categories` для поиска родительских категорий. Затем он вызывает метод `_add_parent_categories` для добавления родительских категорий. Далее, объект `ProductFields` преобразуется в словарь и отправляется в API PrestaShop с использованием метода `create`. После добавления продукта метод пытается загрузить изображение продукта.

**Примеры**:

```python
from src.endpoints.prestashop.product_fields import ProductFields

product = PrestaProduct()
product_fields = ProductFields()
product_fields.name = 'Test Product'
product_fields.price = 99.99
added_product = product.add_new_product(product_fields)
if added_product:
    print(f"Product added with ID: {added_product.id}")
else:
    print("Failed to add product.")
```

## Функции

### `example_add_new_product`

```python
def example_add_new_product() -> None:
```

**Назначение**: Пример для добавления товара в PrestaShop.

**Как работает функция**:
Функция `example_add_new_product` демонстрирует процесс добавления нового продукта в PrestaShop. Она инициализирует объект `PrestaProduct`, загружает пример данных о продукте из JSON-файла, преобразует данные в формат XML и отправляет их в API PrestaShop.

**Примеры**:

```python
example_add_new_product()
```

### `example_get_product`

```python
def example_get_product(id_product: int, **kwards) -> None:
```

**Назначение**: Пример для получения товара из PrestaShop.

**Параметры**:

- `id_product` (int): ID товара для получения.
- `**kwards`: Дополнительные параметры для передачи в метод `get_product`.

**Как работает функция**:
Функция `example_get_product` демонстрирует процесс получения информации о товаре из PrestaShop. Она инициализирует объект `PrestaProduct`, задает параметры запроса и вызывает метод `get_product` для получения информации о товаре с заданным `id_product`.

**Примеры**:

```python
example_get_product(id_product=2191)