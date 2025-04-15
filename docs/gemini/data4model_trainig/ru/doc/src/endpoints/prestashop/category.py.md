# Модуль для управления категориями в PrestaShop

## Обзор

Модуль `category.py` предназначен для управления категориями в PrestaShop. Он содержит класс `PrestaCategory`, который позволяет получать информацию о родительских категориях. Модуль использует API PrestaShop для взаимодействия с данными категорий.

## Подробней

Этот модуль предоставляет функциональность для извлечения иерархической информации о категориях в PrestaShop, что может быть полезно для навигации, создания карты сайта и других задач, связанных с организацией контента. Он использует классы `PrestaShop` и `PrestaShopAsync` из модуля `src.endpoints.prestashop.api` для выполнения API-запросов.

## Классы

### `PrestaCategory`

**Описание**: Класс для управления категориями в PrestaShop. Позволяет получать список родительских категорий для заданной категории.

**Наследует**: `PrestaShop`

**Атрибуты**:
- `api_key` (str): Ключ API для доступа к PrestaShop.
- `api_domain` (str): Доменное имя PrestaShop.

**Методы**:
- `get_parent_categories_list`: Получает список родительских категорий для заданной категории.

**Принцип работы**:
Класс `PrestaCategory` инициализируется с использованием ключа API и доменного имени PrestaShop. Он наследует функциональность для выполнения API-запросов от класса `PrestaShop`. Метод `get_parent_categories_list` рекурсивно запрашивает родительские категории, пока не достигнет корневой категории (с ID меньше или равным 2).

## Методы класса

### `__init__`

```python
def __init__(self, api_key: str, api_domain: str, *args, **kwargs) -> None:
    """Initializes a Product object.

    Args:
        api_key (str): Ключ API для доступа к PrestaShop.
        api_domain (str): Доменное имя PrestaShop.

    Returns:
        None

    Example:
        >>> category = PrestaCategory(api_key=\'your_api_key\', api_domain=\'your_domain\')
    """
    ...
```

**Назначение**: Инициализирует объект `PrestaCategory`.

**Параметры**:
- `api_key` (str): Ключ API для доступа к PrestaShop.
- `api_domain` (str): Доменное имя PrestaShop.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Возвращает**:
- `None`

**Как работает функция**:
Конструктор вызывает конструктор родительского класса `PrestaShop` с переданными аргументами `api_key` и `api_domain`.

**Примеры**:

```python
category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
```

### `get_parent_categories_list`

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
        >>> category = PrestaCategory(api_key=\'your_api_key\', api_domain=\'your_domain\')
        >>> parent_categories = category.get_parent_categories_list(id_category=\'10\')
        >>> print(parent_categories)
        [2, 10]
    """
    ...
```

**Назначение**: Получает список родительских категорий для заданной категории.

**Параметры**:
- `id_category` (str | int): ID категории, для которой нужно получить родительские категории.
- `parent_categories_list` (Optional[List[int | str]], optional): Список родительских категорий. По умолчанию `None`.

**Возвращает**:
- `List[int | str]`: Список ID родительских категорий.

**Вызывает исключения**:
- `ValueError`: Если отсутствует ID категории.
- `Exception`: Если возникает ошибка при получении данных о категории.

**Как работает функция**:
1. Проверяет, передан ли `id_category`. Если нет, записывает ошибку в лог и возвращает пустой список или переданный `parent_categories_list`.
2. Использует метод `super().get` (унаследованный от `PrestaShop`) для получения информации о категории из PrestaShop API. Запрашивает данные в формате JSON.
3. Если информация о категории не получена, записывает ошибку в лог и возвращает пустой список или переданный `parent_categories_list`.
4. Извлекает `id_parent` (ID родительской категории) из полученных данных.
5. Добавляет `id_parent` в `parent_categories_list`.
6. Если `id_parent` меньше или равен 2 (корневая категория), возвращает `parent_categories_list`.
7. В противном случае рекурсивно вызывает `self.get_parent_categories_list` с `id_parent` и обновленным `parent_categories_list`.

**Примеры**:

```python
category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
parent_categories = category.get_parent_categories_list(id_category='10')
print(parent_categories)  # [2, 10]