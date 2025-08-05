# Модуль для управления категориями в PrestaShop

## Обзор

Этот модуль предоставляет функциональность для работы с категориями в PrestaShop. Он включает класс `PrestaCategory`, который позволяет получать информацию о родительских категориях. 

## Подробнее

Модуль предназначен для взаимодействия с API PrestaShop и получения данных о категориях. Класс `PrestaCategory` наследует класс `PrestaShop` и предоставляет метод `get_parent_categories_list`, который позволяет извлечь список родительских категорий для заданной категории.

## Классы

### `PrestaCategory`

**Описание**: Класс для управления категориями в PrestaShop.

**Наследует**: `PrestaShop` 

**Атрибуты**:

- `api_key` (str): Ключ API для доступа к PrestaShop.
- `api_domain` (str): Доменное имя PrestaShop.

**Методы**:

- `get_parent_categories_list()`: Извлекает список родительских категорий для заданной категории. 


### `get_parent_categories_list`

**Назначение**: Извлекает список родительских категорий для заданной категории из PrestaShop. 

**Параметры**:

- `id_category` (str | int): ID категории, для которой нужно получить родительские категории.
- `parent_categories_list` (Optional[List[int | str]], optional): Список родительских категорий. По умолчанию `None`.

**Возвращает**:

- `List[int | str]`: Список ID родительских категорий.

**Вызывает исключения**:

- `ValueError`: Если отсутствует ID категории.
- `Exception`: Если возникает ошибка при получении данных о категории.

**Как работает функция**:

- Проверяет наличие `id_category`. 
- Вызывает метод `get()` родительского класса `PrestaShop` для получения данных о категории по заданному `id_category`. 
- Извлекает значение `id_parent` из полученного словаря.
- Добавляет `id_parent` в список `parent_categories_list`.
- Если значение `id_parent` меньше или равно 2, возвращает список `parent_categories_list`.
- В противном случае, рекурсивно вызывает функцию `get_parent_categories_list` с новым `id_category` (которым является `id_parent`) и списком `parent_categories_list`.

**Примеры**:

```python
>>> category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
>>> parent_categories = category.get_parent_categories_list(id_category='10')
>>> print(parent_categories)
[2, 10]