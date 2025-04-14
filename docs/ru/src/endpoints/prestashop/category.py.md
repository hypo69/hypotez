# Модуль для управления категориями в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.category` предназначен для работы с категориями товаров в интернет-магазине, работающем на платформе PrestaShop. Он предоставляет класс `PrestaCategory`, который позволяет получать информацию о родительских категориях для заданной категории.

## Подробнее

Модуль содержит класс `PrestaCategory`, который наследует функциональность из класса `PrestaShop`. Он используется для управления категориями в PrestaShop, предоставляя возможность получения списка родительских категорий для заданной категории.

## Классы

### `PrestaCategory`

**Описание**: Класс для управления категориями в PrestaShop. Предоставляет методы для получения информации о родительских категориях.

**Наследует**:
- `PrestaShop`: Класс для взаимодействия с API PrestaShop.

**Атрибуты**:
- Отсутствуют, все атрибуты определяются в родительском классе `PrestaShop`.

**Методы**:
- `__init__`: Инициализирует объект `PrestaCategory`.
- `get_parent_categories_list`: Получает список родительских категорий для заданной категории.

#### `__init__`

```python
def __init__(self, api_key: str, api_domain: str, *args, **kwargs) -> None:
    """Initializes a Product object.

    Args:
        api_key (str): Ключ API для доступа к PrestaShop.
        api_domain (str): Доменное имя PrestaShop.

    Returns:
        None

    Example:
        >>> category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
    """
    ...
```

**Назначение**: Инициализирует объект `PrestaCategory`, вызывая конструктор родительского класса `PrestaShop`.

**Параметры**:
- `api_key` (str): Ключ API для доступа к PrestaShop.
- `api_domain` (str): Доменное имя PrestaShop.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Возвращает**:
- `None`

**Как работает функция**:
1. Вызывает конструктор родительского класса `PrestaShop` с переданными аргументами.

#### `get_parent_categories_list`

```python
def get_parent_categories_list(
    self, id_category: str | int, parent_categories_list: Optional[List[int | str]] = None
) -> List[int | str]:
    """Retrieve parent categories from PrestaShop for a given category.

    Args:
        id_category (str | int): ID категории, для которой нужно получить родительские категории.
        parent_categories_list (Optional[List[int | str]], optional): Список родительских категорий. Defaults to None.

    Returns:
        List[int | str]: Список ID родительских категорий.

    Raises:
        ValueError: Если отсутствует ID категории.
        Exception: Если возникает ошибка при получении данных о категории.

    Example:
        >>> category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
        >>> parent_categories = category.get_parent_categories_list(id_category='10')
        >>> print(parent_categories)
        [2, 10]
    """
    ...
```

**Назначение**: Получает список родительских категорий для заданной категории в PrestaShop. Рекурсивно поднимается по дереву категорий, добавляя ID каждой родительской категории в список.

**Параметры**:
- `id_category` (str | int): ID категории, для которой нужно получить родительские категории.
- `parent_categories_list` (Optional[List[int | str]], optional): Список родительских категорий. По умолчанию `None`.

**Возвращает**:
- `List[int | str]`: Список ID родительских категорий.

**Вызывает исключения**:
- `ValueError`: Если отсутствует ID категории.
- `Exception`: Если возникает ошибка при получении данных о категории.

**Как работает функция**:

1. **Проверка ID категории**: Проверяет, передан ли ID категории. Если ID отсутствует, логирует ошибку и возвращает пустой список.
2. **Получение данных о категории**: Использует метод `get` родительского класса `PrestaShop` для получения данных о категории из PrestaShop API.
3. **Обработка ошибки получения данных**: Если данные о категории не получены, логирует ошибку и возвращает текущий список родительских категорий.
4. **Определение ID родительской категории**: Извлекает ID родительской категории из полученных данных.
5. **Добавление родительской категории в список**: Добавляет ID родительской категории в список `parent_categories_list`.
6. **Рекурсивный вызов**: Если ID родительской категории больше 2, рекурсивно вызывает функцию `get_parent_categories_list` для получения списка родительских категорий для текущей родительской категории.
7. **Возврат списка**: Если ID родительской категории меньше или равен 2, возвращает список родительских категорий.

**ASII flowchart**:

```
A [Проверка ID категории]
|
B [Получение данных о категории]
|
C [Обработка ошибки получения данных]
|
D [Определение ID родительской категории]
|
E [Добавление родительской категории в список]
|
F [Проверка ID родительской категории > 2]
|
G [Рекурсивный вызов get_parent_categories_list]
|
H [Возврат списка родительских категорий]
```

**Примеры**:

```python
# Пример 1: Получение списка родительских категорий для категории с ID '10'
category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
parent_categories = category.get_parent_categories_list(id_category='10')
print(parent_categories)  # Вывод: [2, 10]

# Пример 2: Получение списка родительских категорий для категории с ID 5
category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
parent_categories = category.get_parent_categories_list(id_category=5)
print(parent_categories)