# Модуль для взаимодействия с товарами в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.product` предназначен для взаимодействия с товарами в PrestaShop. Он определяет логику взаимодействия с товарами `Prestashop`.

## Подробней

Модуль предоставляет класс `PrestaProduct` для выполнения различных операций с товарами, таких как получение схемы товара, добавление нового товара и получение информации о родительской категории.

## Классы

### `Config`

**Описание**: Класс конфигурации для настроек товаров PrestaShop.

**Атрибуты**:

*   `MODE` (str): Режим работы (`'dev'`, `'dev8'` или `'prod'`).
*   `API_DOMAIN` (str): Домен API.
*   `API_KEY` (str): Ключ API.

**Принцип работы**:

Класс `Config` определяет параметры конфигурации для работы с API PrestaShop. Он использует переменные окружения, если `USE_ENV` установлен в `True`, иначе использует значения из базы данных паролей `keepass`.

### `PrestaProduct`

**Описание**: Класс для управления товарами в PrestaShop.

**Наследует**:

*   `PrestaShop`: Предоставляет базовые методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибуты, но наследует атрибуты от класса `PrestaShop`, такие как `api_key` и `api_domain`.

**Методы**:

*   `__init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None`: Инициализирует объект `PrestaProduct`.
*   `get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict`: Получает схему для ресурса товара из PrestaShop.
*   `get_parent_category(self, id_category: int) -> Optional[int]`: Рекурсивно извлекает родительские категории из PrestaShop для заданной категории.
*   `_add_parent_categories(self, f: ProductFields) -> None`: Вычисляет и добавляет все родительские категории для списка ID категорий в объект `ProductFields`.
*   `get_product(self, id_product: int, **kwards) -> dict`: Возвращает словарь полей товара из магазина PrestaShop.
*   `add_new_product(self, f: ProductFields) -> dict`: Добавляет новый товар в PrestaShop.

## Методы класса `PrestaProduct`

### `__init__`

```python
def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
```

**Назначение**: Инициализирует объект `PrestaProduct`.

**Параметры**:

*   `api_key` (Optional[str], optional): Ключ API PrestaShop. Defaults to ''.
*   `api_domain` (Optional[str], optional): Домен API PrestaShop. Defaults to ''.

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaShop`, передавая ему значения `api_key` и `api_domain` из аргументов или из класса `Config`, если они не указаны.

### `get_product_schema`

```python
def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:
```

**Назначение**: Получает схему для ресурса товара из PrestaShop.

**Параметры**:

*   `resource_id` (Optional[str | int], optional): ID ресурса товара. Defaults to `None`.
*   `schema` (Optional[str], optional): Тип схемы. Defaults to `'blank'`. Возможные значения:
    *   `'blank'`: Пустой шаблон ресурса (все поля присутствуют, но без значений).
    *   `'synopsis'`: Минимальный набор полей (только обязательные поля и краткая структура).
    *   `None`: Полная схема ресурса со всеми возможными полями, типами и ограничениями.

**Возвращает**:

*   `dict`: Схема для ресурса товара.

**Как работает функция**:

1.  Вызывает метод `get_schema` родительского класса `PrestaShop` с указанными параметрами.

### `get_parent_category`

```python
def get_parent_category(self, id_category: int) -> Optional[int]:
```

**Назначение**: Рекурсивно извлекает родительские категории из PrestaShop для заданной категории.

**Параметры**:

*   `id_category` (int): ID категории.

**Возвращает**:

*   `Optional[int]`: ID родительской категории (int).

**Как работает функция**:

1.  Асинхронно вызывает метод `read` для получения информации о категории из API PrestaShop.
2.  Извлекает `id_parent` из полученной информации.
3.  Возвращает `id_parent` в виде целого числа.
4.  В случае ошибки логирует информацию об ошибке и возвращает `None`.

### `_add_parent_categories`

```python
def _add_parent_categories(self, f: ProductFields) -> None:
```

**Назначение**: Вычисляет и добавляет все родительские категории для списка ID категорий в объект `ProductFields`.

**Параметры**:

*   `f` (ProductFields): Объект `ProductFields`, к которому нужно добавить родительские категории.

**Как работает функция**:

1.  Создает новый список, включая только элементы, у которых .get('id') истинно
2.  Выполняет итерацию по категориям, начиная с `id_category_default`.
3.  Рекурсивно вызывает метод `get_parent_category` для получения родительской категории.
4.  Добавляет ID родительской категории в список `additional_categories`.
5.  Останавливает цикл, когда достигает корневой категории (ID меньше или равен 2).

### `get_product`

```python
def get_product(self, id_product: int, **kwards) -> dict:
```

**Назначение**: Возвращает словарь полей товара из магазина PrestaShop.

**Параметры**:

*   `id_product` (int): Значение поля ID в таблице `product` Preastashop.

**Возвращает**:

*   `dict`: Словарь с полями товара.

**Как работает функция**:

1.  Вызывает метод `read` для получения информации о товаре из API PrestaShop.
2.  Возвращает словарь с полями товара.

### `add_new_product`

```python
def add_new_product(self, f: ProductFields) -> dict:
```

**Назначение**: Добавляет новый товар в PrestaShop.

**Параметры**:

*   `f` (ProductFields): Объект `ProductFields`, содержащий информацию о товаре.

**Возвращает**:

*   `dict`: Объект `ProductFields` с установленным `id_product`, если товар успешно добавлен, `None` в противном случае.

**Как работает функция**:

1.  Преобразует объект `ProducFields` в словарь формата `Prestashop` и отправляет его в API Престашоп
2.  Дополняет `id_category_default` в поле `additional_categories` для поиска её родительских категорий
3.  Вызывает метод `_add_parent_categories` для добавления родительских категорий.
4.  Преобразует объект `ProductFields` в XML-формат, требуемый для API PrestaShop.
5.  Отправляет XML-данные в API PrestaShop для добавления нового товара.
6.  В случае успеха извлекает `id` добавленного товара из ответа API и возвращает объект `ProductFields` с установленным `id`.
7.  В случае ошибки логирует информацию об ошибке и возвращает `None`.

## Примеры

### `example_add_new_product`

```python
def example_add_new_product() -> None:
```

**Назначение**: Пример добавления товара в Prestashop

### `example_get_product`

```python
def example_get_product(id_product: int, **kwards) -> None:
```

**Назначение**: Пример получения информации о товаре в Prestashop