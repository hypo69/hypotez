# Модуль для фильтрации категорий и подкатегорий API Aliexpress

## Обзор

Модуль содержит функции для фильтрации категорий и подкатегорий, полученных из API Aliexpress. Он предоставляет инструменты для выделения родительских категорий и дочерних категорий на основе идентификатора родительской категории.

## Подробнее

Этот модуль предназначен для облегчения обработки данных, возвращаемых API Aliexpress, когда необходимо разделить категории на основе их иерархии. Он включает две основные функции: `filter_parent_categories` и `filter_child_categories`.

## Функции

### `filter_parent_categories`

```python
def filter_parent_categories(categories: List[models.Category | models.ChildCategory]) -> List[models.Category]:
    """
    Фильтрует и возвращает список категорий, у которых нет родительской категории.

    Args:
        categories (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.

    Returns:
        List[models.Category]: Список объектов категорий без родительской категории.
    """
```

**Назначение**: Фильтрация списка категорий для получения только родительских категорий, то есть тех, у которых отсутствует `parent_category_id`.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список категорий, которые нужно отфильтровать.

**Возвращает**:
- `List[models.Category]`: Список категорий, являющихся родительскими (не имеющих `parent_category_id`).

**Как работает функция**:
1. Инициализируется пустой список `filtered_categories`.
2. Проверяется, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, то он преобразуется в список, чтобы обеспечить совместимость с дальнейшей логикой.
3. Перебираются элементы списка `categories`.
4. Для каждого элемента проверяется наличие атрибута `parent_category_id`. Если атрибут отсутствует, категория добавляется в список `filtered_categories`.
5. Возвращается список `filtered_categories`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api import models
# Допустим, у нас есть список категорий
categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2')
]

# Вызываем функцию для фильтрации родительских категорий
parent_categories = filter_parent_categories(categories)

# Выводим результат
# Должны получить список с Category 1 и Category 3
print(parent_categories)
```

### `filter_child_categories`

```python
def filter_child_categories(categories: List[models.Category | models.ChildCategory],
                            parent_category_id: int) -> List[models.ChildCategory]:
    """
    Фильтрует и возвращает список дочерних категорий, принадлежащих указанной родительской категории.

    Args:
        categories (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.
        parent_category_id (int): ID родительской категории, по которой нужно отфильтровать дочерние категории.

    Returns:
        List[models.ChildCategory]: Список объектов дочерних категорий с указанным ID родительской категории.
    """
```

**Назначение**: Фильтрация списка категорий для получения только дочерних категорий, принадлежащих определенной родительской категории.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список категорий для фильтрации.
- `parent_category_id` (int): ID родительской категории, по которому происходит фильтрация.

**Возвращает**:
- `List[models.ChildCategory]`: Список дочерних категорий, принадлежащих указанной родительской категории.

**Как работает функция**:
1. Инициализируется пустой список `filtered_categories`.
2. Проверяется, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, то он преобразуется в список, чтобы обеспечить совместимость с дальнейшей логикой.
3. Перебираются элементы списка `categories`.
4. Для каждого элемента проверяется наличие атрибута `parent_category_id` и соответствие значения этого атрибута значению `parent_category_id`, переданному в функцию. Если оба условия выполняются, категория добавляется в список `filtered_categories`.
5. Возвращается список `filtered_categories`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.api import models

# Допустим, у нас есть список категорий
categories = [
    models.Category(id=1, name='Category 1'),
    models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1),
    models.Category(id=3, name='Category 2'),
    models.ChildCategory(id=4, name='Child Category 2', parent_category_id=3)
]

# Вызываем функцию для фильтрации дочерних категорий с parent_category_id=1
child_categories = filter_child_categories(categories, parent_category_id=1)

# Выводим результат
# Должны получить список только с Child Category 1
print(child_categories)