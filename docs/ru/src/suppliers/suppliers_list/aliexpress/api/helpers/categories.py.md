# Модуль `categories.py`

## Обзор

Модуль содержит функции для фильтрации категорий и подкатегорий, полученных из API Aliexpress. Он предоставляет инструменты для выделения главных категорий (не имеющих родительских категорий) и дочерних категорий, принадлежащих определённой родительской категории.

## Подробней

Этот модуль предназначен для обработки данных, полученных из API Aliexpress, и предоставляет функции для фильтрации категорий. Он включает в себя функции `filter_parent_categories` и `filter_child_categories`, которые позволяют выделить категории верхнего уровня и дочерние категории на основе их `parent_category_id`.

## Функции

### `filter_parent_categories`

```python
def filter_parent_categories(categories: List[models.Category | models.ChildCategory]) -> List[models.Category]:
    """
    Filters and returns a list of categories that do not have a parent category.

    @param categories: List of category or child category objects.
    @return: List of category objects without a parent category.
    """
```

**Назначение**: Фильтрует и возвращает список категорий, у которых отсутствует родительская категория.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.

**Возвращает**:
- `List[models.Category]`: Список объектов категорий, не имеющих родительской категории.

**Как работает функция**:
- Функция принимает список категорий, которые могут быть как родительскими, так и дочерними.
- Проверяет, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если это так, он преобразует его в список. Это делается для обработки случаев, когда передается одно значение, а не список.
- Итерируется по каждой категории в списке `categories`.
- Для каждой категории проверяет, есть ли у неё атрибут `parent_category_id`. Если атрибут отсутствует, это означает, что категория является родительской (не дочерней), и она добавляется в список `filtered_categories`.
- Возвращает список `filtered_categories`, содержащий только родительские категории.

**Примеры**:

Предположим, у нас есть следующий список категорий:

```python
from src.suppliers.suppliers_list.aliexpress.api import models

categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2')
]
```

Вызов функции:

```python
filtered_categories = filter_parent_categories(categories)
for category in filtered_categories:
    print(category.name)
# Category 1
# Category 3
```

### `filter_child_categories`

```python
def filter_child_categories(categories: List[models.Category | models.ChildCategory],
                            parent_category_id: int) -> List[models.ChildCategory]:
    """
    Filters and returns a list of child categories that belong to the specified parent category.

    @param categories: List of category or child category objects.
    @param parent_category_id: The ID of the parent category to filter child categories by.
    @return: List of child category objects with the specified parent category ID.
    """
```

**Назначение**: Фильтрует и возвращает список дочерних категорий, принадлежащих указанной родительской категории.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.
- `parent_category_id` (int): Идентификатор родительской категории, по которому нужно отфильтровать дочерние категории.

**Возвращает**:
- `List[models.ChildCategory]`: Список объектов дочерних категорий с указанным идентификатором родительской категории.

**Как работает функция**:
- Функция принимает список категорий (как родительских, так и дочерних) и идентификатор родительской категории.
- Проверяет, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если это так, он преобразует его в список. Это делается для обработки случаев, когда передается одно значение, а не список.
- Итерируется по каждой категории в списке `categories`.
- Для каждой категории проверяет, есть ли у неё атрибут `parent_category_id` и соответствует ли значение этого атрибута заданному `parent_category_id`. Если оба условия выполняются, категория добавляется в список `filtered_categories`.
- Возвращает список `filtered_categories`, содержащий только дочерние категории, принадлежащие указанной родительской категории.

**Примеры**:

Предположим, у нас есть следующий список категорий:

```python
from src.suppliers.suppliers_list.aliexpress.api import models

categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2'),
    models.ChildCategory(id=4, name='Child Category 2', parent_category_id=3)
]
```

Вызов функции:

```python
filtered_categories = filter_child_categories(categories, 1)
for category in filtered_categories:
    print(category.name)
# Child Category 1