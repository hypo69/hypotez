# Модуль `categories.py`

## Обзор

Модуль содержит функции для фильтрации категорий и подкатегорий, полученных через API Aliexpress.
Он предоставляет инструменты для разделения категорий на родительские и дочерние, что упрощает обработку данных, полученных из API.

## Подробней

Модуль предназначен для работы с категориями товаров Aliexpress, полученными через API. Он содержит функции, которые позволяют фильтровать список категорий, разделяя их на основе наличия или отсутствия родительской категории, а также по идентификатору родительской категории. Это полезно для организации и структурирования данных о категориях товаров, полученных из API Aliexpress.

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

**Назначение**:
Функция фильтрует список категорий и возвращает только те, которые не имеют родительской категории.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.

**Возвращает**:
- `List[models.Category]`: Список объектов категорий, у которых отсутствует родительская категория.

**Как работает функция**:
1. Инициализируется пустой список `filtered_categories` для хранения отфильтрованных категорий.
2. Проверяется, является ли входной параметр `categories` строкой, целым числом или числом с плавающей точкой. Если это так, он преобразуется в список, чтобы обеспечить совместимость с логикой итерации.
3. Перебирается каждая категория в списке `categories`.
4. Для каждой категории проверяется, отсутствует ли атрибут `parent_category_id`.
5. Если атрибут отсутствует (т.е. категория не является дочерней), категория добавляется в список `filtered_categories`.
6. Возвращается список `filtered_categories`, содержащий только родительские категории.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api import models
# Пример использования
categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2')
]

parent_categories = filter_parent_categories(categories)
# Результат: [models.Category(id=1, name='Category 1'), models.Category(id=3, name='Category 2')]
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

**Назначение**:
Функция фильтрует список категорий и возвращает только те дочерние категории, которые принадлежат указанной родительской категории.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.
- `parent_category_id` (int): Идентификатор родительской категории, по которому нужно фильтровать дочерние категории.

**Возвращает**:
- `List[models.ChildCategory]`: Список объектов дочерних категорий, у которых совпадает идентификатор родительской категории.

**Как работает функция**:
1. Инициализируется пустой список `filtered_categories` для хранения отфильтрованных категорий.
2. Проверяется, является ли входной параметр `categories` строкой, целым числом или числом с плавающей точкой. Если это так, он преобразуется в список, чтобы обеспечить совместимость с логикой итерации.
3. Перебирается каждая категория в списке `categories`.
4. Для каждой категории проверяется наличие атрибута `parent_category_id` и соответствие значения этого атрибута значению `parent_category_id`, переданному в функцию.
5. Если оба условия выполняются, категория добавляется в список `filtered_categories`.
6. Возвращается список `filtered_categories`, содержащий только дочерние категории, принадлежащие указанной родительской категории.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api import models
# Пример использования
categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2'),
    models.ChildCategory(id=4, name='Child Category 2', parent_category_id=3)
]

child_categories = filter_child_categories(categories, 1)
# Результат: [models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1)]