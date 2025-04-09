# Модуль `categories.py`

## Обзор

Модуль `categories.py` содержит функции для фильтрации категорий и подкатегорий, полученных через API Aliexpress. Он предоставляет инструменты для разделения категорий на родительские и дочерние, что упрощает дальнейшую обработку данных о категориях товаров.

## Подробней

Этот модуль предоставляет функции `filter_parent_categories` и `filter_child_categories`, которые позволяют выделить из общего списка категорий те, которые являются родительскими (не имеют `parent_category_id`) и дочерними (принадлежат определенной родительской категории). Данный функционал полезен при построении иерархии категорий товаров на Aliexpress.

## Функции

### `filter_parent_categories`

```python
def filter_parent_categories(categories: List[models.Category | models.ChildCategory]) -> List[models.Category]:
    """
    Filters and returns a list of categories that do not have a parent category.

    @param categories: List of category or child category objects.
    @return: List of category objects without a parent category.
    """
    ...
```

**Назначение**: Фильтрация списка категорий для выделения категорий, не имеющих родительской категории.

**Параметры**:

- `categories` (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.

**Возвращает**:

- `List[models.Category]`: Список объектов категорий, не имеющих родительской категории.

**Как работает функция**:

1.  Инициализируется пустой список `filtered_categories`.
2.  Проверяется, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, то он преобразуется в список для унификации обработки.
3.  Перебирается каждая категория в списке `categories`.
4.  Для каждой категории проверяется отсутствие атрибута `parent_category_id`.
5.  Если атрибут отсутствует, категория добавляется в список `filtered_categories`.
6.  Функция возвращает список `filtered_categories`.

```
Начало
   │
   ├─── Проверка типа `categories`
   │    │
   │    └─── Если `str`, `int` или `float` -> Преобразование в список
   │
   │
   └─── Перебор категорий в `categories`
        │
        ├─── Проверка наличия атрибута `parent_category_id`
        │    │
        │    └─── Если отсутствует -> Добавление категории в `filtered_categories`
        │
        │
        └─── Возврат `filtered_categories`
```

**Примеры**:

```python
from src.suppliers.aliexpress.api import models
# Пример использования
categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2')
]

parent_categories = filter_parent_categories(categories)
# parent_categories будет содержать [models.Category(id=1, name='Category 1'), models.Category(id=3, name='Category 2')]
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
    ...
```

**Назначение**: Фильтрация списка категорий для выделения дочерних категорий, принадлежащих указанной родительской категории.

**Параметры**:

- `categories` (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.
- `parent_category_id` (int): ID родительской категории, по которому фильтруются дочерние категории.

**Возвращает**:

- `List[models.ChildCategory]`: Список объектов дочерних категорий, принадлежащих указанной родительской категории.

**Как работает функция**:

1.  Инициализируется пустой список `filtered_categories`.
2.  Проверяется, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, то он преобразуется в список для унификации обработки.
3.  Перебирается каждая категория в списке `categories`.
4.  Для каждой категории проверяется наличие атрибута `parent_category_id` и соответствие значения этого атрибута значению `parent_category_id`, переданному в функцию.
5.  Если оба условия выполняются, категория добавляется в список `filtered_categories`.
6.  Функция возвращает список `filtered_categories`.

```
Начало
   │
   ├─── Проверка типа `categories`
   │    │
   │    └─── Если `str`, `int` или `float` -> Преобразование в список
   │
   │
   └─── Перебор категорий в `categories`
        │
        ├─── Проверка наличия атрибута `parent_category_id` и его соответствия `parent_category_id`
        │    │
        │    └─── Если оба условия выполняются -> Добавление категории в `filtered_categories`
        │
        │
        └─── Возврат `filtered_categories`
```

**Примеры**:

```python
from src.suppliers.aliexpress.api import models
# Пример использования
categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2'),
    models.ChildCategory(id=4, name='Child Category 2', parent_category_id=1)
]

child_categories = filter_child_categories(categories, parent_category_id=1)
# child_categories будет содержать [models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1), models.ChildCategory(id=4, name='Child Category 2', parent_category_id=1)]