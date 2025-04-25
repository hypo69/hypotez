# Модуль для работы с категориями API Aliexpress

## Обзор

Модуль содержит функции для фильтрации категорий и подкатегорий API Aliexpress. 

## Классы

### `models.Category`

**Описание**: Модель категории API Aliexpress.

**Атрибуты**:

- `category_id` (int): Идентификатор категории.
- `name` (str): Название категории.
- `parent_category_id` (int): Идентификатор родительской категории.
- `parent_category_name` (str): Название родительской категории.

### `models.ChildCategory`

**Описание**: Модель подкатегории API Aliexpress.

**Атрибуты**:

- `child_category_id` (int): Идентификатор подкатегории.
- `name` (str): Название подкатегории.
- `parent_category_id` (int): Идентификатор родительской категории.

## Функции

### `filter_parent_categories`

**Назначение**: Фильтрует и возвращает список категорий, у которых нет родительской категории.

**Параметры**:

- `categories` (List[models.Category | models.ChildCategory]): Список объектов категории или подкатегории.

**Возвращает**:

- `List[models.Category]`: Список объектов категории без родительской категории.

**Как работает функция**:

- Функция проверяет наличие атрибута `parent_category_id` у каждого объекта в списке `categories`.
- Если атрибут отсутствует, объект добавляется в список `filtered_categories`.
- Функция возвращает список `filtered_categories`.

**Примеры**:

```python
from src.suppliers.aliexpress.api.helpers import categories
from src.suppliers.aliexpress.api import models

# Пример 1: Список с одним объектом категории
category = models.Category(category_id=1, name="Одежда", parent_category_id=None)
filtered_categories = categories.filter_parent_categories([category])
print(filtered_categories)  # Вывод: [<models.Category object>]

# Пример 2: Список с одним объектом подкатегории
child_category = models.ChildCategory(child_category_id=2, name="Женская одежда", parent_category_id=1)
filtered_categories = categories.filter_parent_categories([child_category])
print(filtered_categories)  # Вывод: []

# Пример 3: Список с несколькими объектами
categories_list = [
    models.Category(category_id=1, name="Одежда", parent_category_id=None),
    models.ChildCategory(child_category_id=2, name="Женская одежда", parent_category_id=1),
    models.Category(category_id=3, name="Обувь", parent_category_id=None),
]
filtered_categories = categories.filter_parent_categories(categories_list)
print(filtered_categories)  # Вывод: [<models.Category object>, <models.Category object>]
```

### `filter_child_categories`

**Назначение**: Фильтрует и возвращает список подкатегорий, которые относятся к указанной родительской категории.

**Параметры**:

- `categories` (List[models.Category | models.ChildCategory]): Список объектов категории или подкатегории.
- `parent_category_id` (int): Идентификатор родительской категории, по которой нужно отфильтровать подкатегории.

**Возвращает**:

- `List[models.ChildCategory]`: Список объектов подкатегории с указанным идентификатором родительской категории.

**Как работает функция**:

- Функция проверяет наличие атрибута `parent_category_id` у каждого объекта в списке `categories`.
- Если атрибут присутствует и его значение равно `parent_category_id`, объект добавляется в список `filtered_categories`.
- Функция возвращает список `filtered_categories`.

**Примеры**:

```python
from src.suppliers.aliexpress.api.helpers import categories
from src.suppliers.aliexpress.api import models

# Пример 1: Список с одним объектом категории
category = models.Category(category_id=1, name="Одежда", parent_category_id=None)
filtered_categories = categories.filter_child_categories([category], parent_category_id=1)
print(filtered_categories)  # Вывод: []

# Пример 2: Список с одним объектом подкатегории
child_category = models.ChildCategory(child_category_id=2, name="Женская одежда", parent_category_id=1)
filtered_categories = categories.filter_child_categories([child_category], parent_category_id=1)
print(filtered_categories)  # Вывод: [<models.ChildCategory object>]

# Пример 3: Список с несколькими объектами
categories_list = [
    models.Category(category_id=1, name="Одежда", parent_category_id=None),
    models.ChildCategory(child_category_id=2, name="Женская одежда", parent_category_id=1),
    models.ChildCategory(child_category_id=3, name="Мужская одежда", parent_category_id=1),
    models.Category(category_id=4, name="Обувь", parent_category_id=None),
]
filtered_categories = categories.filter_child_categories(categories_list, parent_category_id=1)
print(filtered_categories)  # Вывод: [<models.ChildCategory object>, <models.ChildCategory object>]
```