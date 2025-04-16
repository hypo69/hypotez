# Модуль для управления категориями в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.category` предназначен для управления категориями в PrestaShop. Он содержит класс `PrestaCategory`, который позволяет получать информацию о родительских категориях.

## Подробней

Модуль предоставляет функциональность для извлечения иерархии категорий товаров в PrestaShop, что может быть полезно для навигации, фильтрации и организации товаров.

## Классы

### `PrestaCategory`

**Описание**: Класс для управления категориями в PrestaShop.

**Наследует**:

*   `PrestaShop`: Предоставляет базовые методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибутов, но наследует атрибуты от класса `PrestaShop`, такие как `api_key` и `api_domain`.

**Методы**:

*   `__init__(api_key: str, api_domain: str, *args, **kwargs) -> None`: Инициализирует объект `PrestaCategory`.
*   `get_parent_categories_list(id_category: str | int, parent_categories_list: Optional[List[int | str]] = None) -> List[int | str]`: Извлекает список родительских категорий для заданной категории.

## Методы класса `PrestaCategory`

### `__init__`

```python
def __init__(self, api_key: str, api_domain: str, *args, **kwargs) -> None:
```

**Назначение**: Инициализирует объект `PrestaCategory`.

**Параметры**:

*   `api_key` (str): Ключ API для доступа к PrestaShop.
*   `api_domain` (str): Доменное имя PrestaShop.

**Возвращает**:

*   `None`

**Как работает функция**:

1.  Вызывает конструктор родительского класса `PrestaShop` с переданными параметрами.

**Примеры**:

```python
from src.endpoints.prestashop.category import PrestaCategory

category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
```

### `get_parent_categories_list`

```python
def get_parent_categories_list(
    self, id_category: str | int, parent_categories_list: Optional[List[int | str]] = None
) -> List[int | str]:
```

**Назначение**: Извлекает родительские категории из PrestaShop для заданной категории.

**Параметры**:

*   `id_category` (str | int): ID категории, для которой нужно получить родительские категории.
*   `parent_categories_list` (Optional[List[int | str]], optional): Список родительских категорий. По умолчанию `None`.

**Возвращает**:

*   `List[int | str]`: Список ID родительских категорий.

**Вызывает исключения**:

*   `ValueError`: Если отсутствует ID категории.
*   `Exception`: Если возникает ошибка при получении данных о категории.

**Как работает функция**:

1.  Проверяет, передан ли `id_category`. Если нет, логирует ошибку и возвращает пустой список.
2.  Вызывает метод `get` родительского класса `PrestaShop` для получения информации о категории из API PrestaShop.
3.  Если категория не найдена, логирует ошибку и возвращает переданный `parent_categories_list` или пустой список.
4.  Извлекает `id_parent` из полученной информации о категории.
5.  Добавляет `id_parent` в список `parent_categories_list`.
6.  Если `id_parent` меньше или равен 2, возвращает `parent_categories_list`.
7.  Иначе рекурсивно вызывает саму себя с `id_parent` в качестве `id_category` и обновленным `parent_categories_list`.

**Примеры**:

```python
from src.endpoints.prestashop.category import PrestaCategory

category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
parent_categories = category.get_parent_categories_list(id_category='10')
print(parent_categories)
# [2, 10]