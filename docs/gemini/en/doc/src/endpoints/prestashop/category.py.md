# Module `src.endpoints.prestashop.category`

## Overview

Модуль предназначен для управления категориями в PrestaShop. Он содержит класс `PrestaCategory`, который позволяет получать информацию о родительских категориях.

## More details

Этот модуль предоставляет функциональность для взаимодействия с категориями в PrestaShop. Он используется для получения списка родительских категорий для заданной категории, что может быть полезно для навигации и организации товаров в интернет-магазине. Класс `PrestaCategory` наследуется от класса `PrestaShop`, что позволяет ему использовать общие методы для взаимодействия с API PrestaShop.

## Classes

### `PrestaCategory`

**Description**: Класс для управления категориями в PrestaShop.

**Inherits**:
- `PrestaShop`: Наследует методы для взаимодействия с API PrestaShop.

**Attributes**:
- Нет специфических атрибутов, кроме тех, что наследуются от `PrestaShop`.

**Methods**:
- `get_parent_categories_list`: Получает список родительских категорий для заданной категории.

**Working principle**:
Класс `PrestaCategory` инициализируется с использованием ключа API и доменного имени PrestaShop. Он предоставляет метод `get_parent_categories_list`, который рекурсивно получает родительские категории для заданной категории, пока не достигнет корневой категории.

```python
class PrestaCategory(PrestaShop):
    """Class for managing categories in PrestaShop."""

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
        super().__init__(api_key=api_key, api_domain=api_domain, *args, **kwargs)

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
        if not id_category:
            logger.error(\'Missing category ID.\')
            return parent_categories_list or []

        category: Optional[Dict] = super().get(
            \'categories\', resource_id=id_category, display=\'full\', io_format=\'JSON\'
        )
        if not category:
            logger.error(\'Issue with retrieving categories.\')
            return parent_categories_list or []

        _parent_category: int = int(category[\'id_parent\'])\n        parent_categories_list = parent_categories_list or []
        parent_categories_list.append(_parent_category)

        if _parent_category <= 2:
            return parent_categories_list
        else:
            return self.get_parent_categories_list(_parent_category, parent_categories_list)
```

## Class Methods

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
    super().__init__(api_key=api_key, api_domain=api_domain, *args, **kwargs)
```

**Purpose**:
Инициализирует объект класса `PrestaCategory`.

**Parameters**:
- `api_key` (str): Ключ API для доступа к PrestaShop.
- `api_domain` (str): Доменное имя PrestaShop.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Returns**:
- `None`

**How the function works**:
Вызывает конструктор родительского класса `PrestaShop` с переданными параметрами `api_key` и `api_domain`.

**Examples**:
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
    if not id_category:
        logger.error(\'Missing category ID.\')
        return parent_categories_list or []

    category: Optional[Dict] = super().get(
        \'categories\', resource_id=id_category, display=\'full\', io_format=\'JSON\'
    )
    if not category:
        logger.error(\'Issue with retrieving categories.\')
        return parent_categories_list or []

    _parent_category: int = int(category[\'id_parent\'])\n    parent_categories_list = parent_categories_list or []
    parent_categories_list.append(_parent_category)

    if _parent_category <= 2:
        return parent_categories_list
    else:
        return self.get_parent_categories_list(_parent_category, parent_categories_list)
```

**Purpose**:
Получает список родительских категорий для заданной категории.

**Parameters**:
- `id_category` (str | int): ID категории, для которой нужно получить родительские категории.
- `parent_categories_list` (Optional[List[int | str]], optional): Список родительских категорий. По умолчанию `None`.

**Returns**:
- `List[int | str]`: Список ID родительских категорий.

**Raises**:
- `ValueError`: Если отсутствует ID категории.
- `Exception`: Если возникает ошибка при получении данных о категории.

**How the function works**:
1. Проверяет, передан ли ID категории. Если нет, возвращает пустой список или переданный список родительских категорий.
2. Получает информацию о категории из PrestaShop API, используя метод `get` родительского класса `PrestaShop`.
3. Если информация о категории не получена, возвращает пустой список или переданный список родительских категорий и логирует ошибку.
4. Извлекает ID родительской категории из полученной информации.
5. Добавляет ID родительской категории в список родительских категорий.
6. Если ID родительской категории меньше или равен 2, возвращает список родительских категорий.
7. Иначе рекурсивно вызывает себя с ID родительской категории и списком родительских категорий.

**Examples**:
```python
category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
parent_categories = category.get_parent_categories_list(id_category='10')
print(parent_categories) #  [2, 10]
```

## Class Parameters

- `api_key` (str): Ключ API для доступа к PrestaShop. Используется для аутентификации при запросах к API.
- `api_domain` (str): Доменное имя PrestaShop. Используется для формирования URL-адресов API.
- `id_category` (str | int): ID категории, для которой нужно получить родительские категории. Используется для запроса информации о категории из API.
- `parent_categories_list` (Optional[List[int | str]], optional): Список родительских категорий. Используется для хранения списка родительских категорий при рекурсивных вызовах функции. По умолчанию `None`.