# Модуль `product`

## Обзор

Модуль предназначен для взаимодействия с товарами в PrestaShop. Он предоставляет классы и функции для получения информации о товарах, добавления новых товаров, а также для управления категориями товаров.

## Подробнее

Модуль `product` является частью проекта `hypotez` и отвечает за взаимодействие с API PrestaShop для управления товарами. Он включает в себя классы для конфигурации подключения к PrestaShop, для работы с API PrestaShop, а также функции для выполнения различных операций с товарами, такими как добавление новых товаров и получение информации о существующих товарах.

## Содержание

- [Классы](#Классы)
  - [Config](#Config)
  - [PrestaProduct](#PrestaProduct)
- [Функции](#Функции)
  - [example_add_new_product](#example_add_new_product)
  - [example_get_product](#example_get_product)

## Классы

### `Config`

**Описание**: Класс конфигурации для настроек продукта PrestaShop.

**Атрибуты**:

-   `MODE` (str): Режим работы (например, `'dev'`). По умолчанию `'dev'`.
-   `API_DOMAIN` (str): Домен API PrestaShop. По умолчанию `''`.
-   `API_KEY` (str): Ключ API PrestaShop. По умолчанию `''`.

**Принцип работы**:

Класс `Config` предназначен для хранения конфигурационных данных, необходимых для подключения к API PrestaShop. Он использует переменные окружения, если `USE_ENV` установлен в `True`, в противном случае использует значения из `gs.credentials.presta`. В зависимости от значения `MODE` выбираются различные доступы к API.

### `PrestaProduct`

**Описание**: Класс для манипуляций с товарами.

**Наследует**:

-   `PrestaShop`: Наследует функциональность для взаимодействия с API PrestaShop.

**Атрибуты**:

-   `api_key` (Optional[str]): Ключ API PrestaShop.
-   `api_domain` (Optional[str]): Домен API PrestaShop.

**Методы**:

-   `__init__(api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None`
-   `get_product_schema(resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict`
-   `get_parent_category(id_category: int) -> Optional[int]`
-   `_add_parent_categories(f: ProductFields) -> None`
-   `get_product(id_product: int, **kwards) -> dict`
-   `add_new_product(f: ProductFields) -> dict`

#### `__init__`

```python
def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None
```

**Назначение**: Инициализирует объект `PrestaProduct`.

**Параметры**:

-   `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `''`.
-   `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `''`.
-   `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.

**Возвращает**:

-   `None`

**Как работает функция**:

Вызывает конструктор родительского класса `PrestaShop` с переданными ключом API и доменом API, если они указаны, или использует значения по умолчанию из класса `Config`.

#### `get_product_schema`

```python
def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict
```

**Назначение**: Получает схему ресурса товара из PrestaShop.

**Параметры**:

-   `resource_id` (Optional[str | int], optional): ID ресурса товара. По умолчанию `None`.
-   `schema` (Optional[str], optional): Тип схемы. Может быть `'blank'`, `'synopsis'` или `None`. По умолчанию `None`.

**Возвращает**:

-   `dict`: Схема ресурса товара.

**Как работает функция**:

Вызывает метод `get_schema` родительского класса `PrestaShop` для получения схемы ресурса товара.

#### `get_parent_category`

```python
def get_parent_category(self, id_category: int) -> Optional[int]
```

**Назначение**: Рекурсивно получает родительские категории из PrestaShop для заданной категории.

**Параметры**:

-   `id_category` (int): ID категории.

**Возвращает**:

-   `Optional[int]`: ID родительской категории или `None`, если родительская категория не найдена или произошла ошибка.

**Как работает функция**:

1.  Выполняет чтение данных о категории из PrestaShop по заданному `id_category`.
2.  Извлекает `id_parent` из полученных данных.
3.  Возвращает `id_parent` в виде целого числа.
4.  Обрабатывает исключения и логирует ошибки, возвращая `None` в случае неудачи.

#### `_add_parent_categories`

```python
def _add_parent_categories(self, f: ProductFields) -> None:
```

**Назначение**: Вычисляет и добавляет все уникальные родительские категории для списка ID категорий в объект `ProductFields`.

**Параметры**:

-   `f` (ProductFields): Объект `ProductFields`, в который добавляются уникальные родительские категории.

**Как работает функция**:

1.  Создает множество `seen_ids` для отслеживания всех ID категорий (начальных и добавленных).
2.  Заполняет множество ID из начального списка `f.additional_categories`.
3.  Итерируется по начальным категориям для поиска их родителей.
4.  Для каждой категории получает родительскую категорию с помощью метода `self.get_parent_category`.
5.  Если родительская категория найдена и еще не добавлена в `seen_ids`, добавляет ее в `f.additional_categories` и `seen_ids`.
6.  Повторяет шаги 4 и 5, пока не достигнет корневой категории или не найдет родительскую категорию.
7.  Логирует финальный набор уникальных ID категорий.

#### `get_product`

```python
def get_product(self, id_product: int, **kwards) -> dict
```

**Назначение**: Возвращает словарь полей товара из магазина PrestaShop.

**Параметры**:

-   `id_product` (int): Значение поля ID в таблице `product` PrestaShop.
-   `**kwards`: Дополнительные параметры запроса.

**Возвращает**:

-   `dict`: Словарь, содержащий информацию о товаре.

**Как работает функция**:

1.  Устанавливает параметр `data_format` в `'JSON'` для запроса.
2.  Вызывает метод `self.read` для получения информации о товаре с заданным `id_product`.
3.  Возвращает полученный словарь.

#### `add_new_product`

```python
def add_new_product(self, f: ProductFields) -> dict
```

**Назначение**: Добавляет новый товар в PrestaShop.

**Параметры**:

-   `f` (ProductFields): Экземпляр класса `ProductFields`, содержащий информацию о товаре.

**Возвращает**:

-   `dict`: Объект `SimpleNamespace` с данными добавленного товара, если товар был успешно добавлен, в противном случае - пустой словарь.

**Как работает функция**:

1.  Добавляет `id_category_default` в поле `additional_categories` для поиска ее родительских категорий.
2.  Вызывает метод `self._add_parent_categories` для добавления родительских категорий.
3.  Преобразует объект `ProductFields` в словарь формата PrestaShop.
4.  Преобразует словарь в XML.
5.  Вызывает метод `self.create` для добавления товара в PrestaShop.
6.  Сохраняет XML представление запроса в файл.
7.  Если товар был успешно добавлен, загружает изображение товара (если указано) и возвращает объект `SimpleNamespace` с данными добавленного товара.
8.  В случае ошибки логирует ошибку и возвращает пустой словарь.

## Функции

### `example_add_new_product`

```python
def example_add_new_product() -> None
```

**Назначение**: Пример добавления товара в PrestaShop.

**Параметры**:

-   `None`

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создает экземпляр класса `PrestaProduct`.
2.  Загружает пример данных о товаре из JSON-файла.
3.  Преобразует данные в формат XML.
4.  Вызывает метод `_exec` для добавления товара в PrestaShop.
5.  Выводит ответ от API PrestaShop.

### `example_get_product`

```python
def example_get_product(id_product: int, **kwards) -> None
```

**Назначение**: Пример получения информации о товаре из PrestaShop.

**Параметры**:

-   `id_product` (int): ID товара.
-   `**kwards`: Дополнительные параметры запроса.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создает экземпляр класса `PrestaProduct`.
2.  Вызывает метод `get_product` для получения информации о товаре с заданным ID.
3.  Сохраняет полученную информацию в JSON-файл.