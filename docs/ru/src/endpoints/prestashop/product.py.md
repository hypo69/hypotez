# Модуль `product`

## Обзор

Модуль предназначен для взаимодействия с товарами в PrestaShop. Он предоставляет классы и функции для получения информации о товарах, добавления новых товаров и выполнения других операций, связанных с товарами.

## Подробнее

Модуль содержит класс `PrestaProduct`, который наследует от класса `PrestaShop` и реализует методы для работы с API PrestaShop, специфичные для товаров. Он использует другие модули проекта, такие как `src.endpoints.prestashop.api`, `src.endpoints.prestashop.category`, `src.endpoints.prestashop.product_fields` и другие, для выполнения различных задач, таких как преобразование данных, отправка запросов к API и обработка ответов.

## Классы

### `Config`

**Описание**: Класс конфигурации для настроек товара PrestaShop.

**Атрибуты**:

-   `MODE` (str): Режим работы (`dev` или `prod`). По умолчанию `'dev'`.
-   `API_DOMAIN` (str): Домен API PrestaShop. По умолчанию `''`.
-   `API_KEY` (str): Ключ API PrestaShop. По умолчанию `''`.

**Принцип работы**:

Класс `Config` определяет параметры конфигурации для работы с API PrestaShop. Он использует переменные окружения, если `USE_ENV` равно `True`, или значения из `gs.credentials`, если `USE_ENV` равно `False`.

### `PrestaProduct`

**Описание**: Класс для управления товарами в PrestaShop.

**Наследует**: `PrestaShop`

**Методы**:

-   `__init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None`: Инициализирует объект `PrestaProduct`.
-   `get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict`: Возвращает схему для ресурса товара из PrestaShop.
-   `get_parent_category(self, id_category: int) -> Optional[int]`: Рекурсивно извлекает родительские категории из PrestaShop для заданной категории.
-   `_add_parent_categories(self, f: ProductFields) -> None`: Вычисляет и добавляет все уникальные родительские категории для списка ID категорий в объект `ProductFields`.
-   `get_product(self, id_product: int, **kwargs) -> dict`: Возвращает словарь полей товара из магазина PrestaShop.
-   `add_new_product(self, f: ProductFields) -> dict`: Добавляет новый товар в PrestaShop.

## Методы класса

### `__init__`

```python
def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
    """Инициализирует объект `PrestaProduct`.

    Args:
        api_key (Optional[str], optional): Ключ API PrestaShop. По умолчанию ''.
        api_domain (Optional[str], optional): Домен API PrestaShop. По умолчанию ''.

    Returns:
        None
    """
```

**Назначение**: Инициализация объекта класса `PrestaProduct`.

**Параметры**:

-   `api_key` (Optional[str], optional): Ключ API PrestaShop. Если не указан, используется значение из `Config.API_KEY`. По умолчанию `''`.
-   `api_domain` (Optional[str], optional): Домен API PrestaShop. Если не указан, используется значение из `Config.API_DOMAIN`. По умолчанию `''`.
-   `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:

Функция вызывает конструктор родительского класса `PrestaShop` с переданными параметрами или значениями по умолчанию из класса `Config`.

### `get_product_schema`

```python
def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:
    """Возвращает схему для ресурса товара из PrestaShop.

    Args:
        resource_id (Optional[str  |  int], optional): ID ресурса товара. По умолчанию `None`.
        schema (Optional[str], optional): Тип схемы. По умолчанию `'blank'`.
            - blank: Пустой шаблон ресурса: все поля присутствуют, но без значений. Обычно используется для создания нового объекта.
            - synopsis: Минимальный набор полей: только обязательные поля и краткая структура. Подходит для быстрого обзора.
            - null / не передавать параметр: Возвращает полную схему ресурса со всеми возможными полями, типами и ограничениями.

    Returns:
        dict: Схема для ресурса товара.
    """
```

**Назначение**: Получение схемы для ресурса товара из PrestaShop.

**Параметры**:

-   `resource_id` (Optional[str  |  int], optional): ID ресурса товара. По умолчанию `None`.
-   `schema` (Optional[str], optional): Тип схемы. Может быть `blank`, `synopsis` или `None`. По умолчанию `'blank'`.

**Возвращает**:

-   `dict`: Схема для ресурса товара.

**Как работает функция**:

Функция вызывает метод `get_schema` родительского класса `PrestaShop` с указанными параметрами и возвращает полученную схему.

### `get_parent_category`

```python
def get_parent_category(self, id_category: int) -> Optional[int]:
    """Рекурсивно извлекает родительские категории из PrestaShop для заданной категории.

    Args:
        id_category (int): ID категории.

    Returns:
        Optional[int]: ID родительской категории (int).
    """
```

**Назначение**: Рекурсивное извлечение родительских категорий из PrestaShop для заданной категории.

**Параметры**:

-   `id_category` (int): ID категории.

**Возвращает**:

-   `Optional[int]`: ID родительской категории (int).

**Как работает функция**:

Функция отправляет запрос к API PrestaShop для получения информации о категории с заданным ID. Затем извлекает ID родительской категории из ответа и возвращает его. Если категория не найдена или произошла ошибка, возвращается `None`.

### `_add_parent_categories`

```python
def _add_parent_categories(self, f: ProductFields) -> None:
    """
    Вычисляет и добавляет все уникальные родительские категории
    для списка ID категорий в объект ProductFields.

    Args:
        f (ProductFields): Объект ProductFields, в который добавляются
                           уникальные родительские категории.
    """
```

**Назначение**: Вычисление и добавление всех уникальных родительских категорий для списка ID категорий в объект `ProductFields`.

**Параметры**:

-   `f` (ProductFields): Объект `ProductFields`, в который добавляются уникальные родительские категории.

**Как работает функция**:

1.  Создает множество для отслеживания всех ID категорий (начальных и добавленных).
2.  Заполняет множество ID из начального списка `f.additional_categories`.
3.  Итерирует по начальным категориям для поиска их родителей.
4.  Поднимается по иерархии категорий, пока не дойдет до корня.
5.  Проверяет, найден ли родитель и не является ли он корнем.
6.  Проверяет на дубликат перед добавлением.
7.  Добавляет родителя в `f.additional_categories`.
8.  Добавляет ID нового родителя в множество отслеживания.
9.  Переходит к следующему родителю вверх по иерархии.
10. После завершения итерации `f.additional_categories` содержит исходные категории + уникальные родительские.

### `get_product`

```python
def get_product(self, id_product: int, **kwargs) -> dict:
    """Возваращает словарь полей товара из магазина Prestasop

    Args:
        id_product (int): значение поля ID в таблице `product` Preastashop

    Returns:
        dict:
        {
            'product':
                {... product fields}
        }
    """
```

**Назначение**: Возвращает словарь полей товара из магазина PrestaShop.

**Параметры**:

-   `id_product` (int): ID товара в таблице `product` PrestaShop.
-   `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:

-   `dict`: Словарь, содержащий информацию о товаре.

**Как работает функция**:

Функция вызывает метод `read` родительского класса `PrestaShop` с указанными параметрами и возвращает полученный словарь.

### `add_new_product`

```python
def add_new_product(self, f: ProductFields) -> dict:
    """Добавляет новый товар в PrestaShop.

    Преобразовывает объект `ProducFields` в словарь формата `Prestashop` и отрапавлет его в API Престашоп

    Args:
        f (ProductFields): Экземпляр класса данных `ProductFields`, содержащий информацию о товаре.

    Returns:
        dict: Возвращает объект `ProductFields` с установленным `id_product`, если товар был успешно добавлен, в противном случае `None`.
    """
```

**Назначение**: Добавление нового товара в PrestaShop.

**Параметры**:

-   `f` (ProductFields): Объект `ProductFields`, содержащий информацию о товаре.

**Возвращает**:

-   `dict`: Объект `ProductFields` с установленным `id_product`, если товар был успешно добавлен, в противном случае пустой словарь.

**Как работает функция**:

1.  Добавляет `id_category_default` в поле `additional_categories` для поиска её родительских категорий.
2.  Вызывает метод `_add_parent_categories` для добавления родительских категорий.
3.  Преобразует объект `ProductFields` в словарь формата PrestaShop.
4.  Преобразует словарь в XML.
5.  Отправляет XML в API PrestaShop для создания нового товара.
6.  Если товар успешно добавлен, извлекает ID добавленного товара из ответа и возвращает объект `ProductFields` с установленным `id_product`.

**Внутренние функции**: Отсутствуют

## Примеры

### `example_add_new_product`

```python
def example_add_new_product() -> None:
    """Пример для добавления товара в Prestashop"""
```

**Назначение**: Пример добавления товара в PrestaShop.

**Как работает функция**:

1.  Создает экземпляр класса `PrestaProduct`.
2.  Загружает пример данных из JSON-файла.
3.  Преобразует данные в XML.
4.  Отправляет запрос к API PrestaShop для добавления нового товара.
5.  Выводит ответ от API.

### `example_get_product`

```python
def example_get_product(id_product: int, **kwargs) -> None:
    """"""
```

**Назначение**: Пример получения информации о товаре из PrestaShop.

**Параметры**:

-   `id_product` (int): ID товара.
-   `**kwargs`: Дополнительные параметры запроса.

**Как работает функция**:

1.  Создает экземпляр класса `PrestaProduct`.
2.  Вызывает метод `get_product` для получения информации о товаре.
3.  Сохраняет полученную информацию в JSON-файл.