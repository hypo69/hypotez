# Модуль для фильтрации категорий API Aliexpress

## Обзор

Модуль содержит функции для фильтрации категорий и подкатегорий, полученных из API Aliexpress. Он предоставляет инструменты для выделения категорий верхнего уровня (не имеющих родительских категорий) и подкатегорий, принадлежащих определенной родительской категории.

## Подробней

Этот модуль предназначен для обработки данных категорий, полученных из API Aliexpress, и фильтрации их в соответствии с заданными критериями. Он используется для организации иерархической структуры категорий товаров, что упрощает навигацию и поиск товаров на платформе Aliexpress.

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

**Назначение**: Фильтрация списка категорий для выделения только тех, которые не имеют родительской категории (то есть являются категориями верхнего уровня).

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список категорий, которые необходимо отфильтровать. Список может содержать объекты как родительских категорий (`models.Category`), так и дочерних категорий (`models.ChildCategory`).

**Возвращает**:
- `List[models.Category]`: Список категорий, у которых отсутствует атрибут `parent_category_id`.

**Как работает функция**:

- Функция принимает на вход список категорий, которые могут быть как родительскими, так и дочерними.
- Проверяет, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, то преобразует его в список, содержащий только этот элемент. Это необходимо для обработки случаев, когда в функцию передается одно значение вместо списка.
- Функция итерируется по каждой категории в предоставленном списке.
- Для каждой категории проверяется, существует ли атрибут `parent_category_id`.
- Если атрибут `parent_category_id` отсутствует, категория считается родительской и добавляется в список `filtered_categories`.
- В конце функция возвращает список `filtered_categories`, содержащий только родительские категории.

**Примеры**:

Предположим, у нас есть следующий список категорий:

```python
from typing import List
from typing import Optional
class Category:
    def __init__(self, category_id: int, category_name: str, parent_category_id: Optional[int] = None):
        self.category_id = category_id
        self.category_name = category_name
        self.parent_category_id = parent_category_id

class ChildCategory:
    def __init__(self, category_id: int, category_name: str, parent_category_id: int):
        self.category_id = category_id
        self.category_name = category_name
        self.parent_category_id = parent_category_id

# Создаем экземпляры категорий
category1 = Category(category_id=1, category_name='Электроника')
category2 = ChildCategory(category_id=101, category_name='Смартфоны', parent_category_id=1)
category3 = Category(category_id=2, category_name='Одежда')

categories_list = [category1, category2, category3]

# Вызываем функцию filter_parent_categories
filtered_categories = filter_parent_categories(categories_list)

# Выводим результат
for category in filtered_categories:
    print(f"ID: {category.category_id}, Name: {category.category_name}")

#  ID: 1, Name: Электроника
#  ID: 2, Name: Одежда
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

**Назначение**: Фильтрация списка категорий для выделения только тех, которые являются дочерними категориями заданной родительской категории.

**Параметры**:
- `categories` (List[models.Category | models.ChildCategory]): Список категорий, которые необходимо отфильтровать. Список может содержать объекты как родительских категорий (`models.Category`), так и дочерних категорий (`models.ChildCategory`).
- `parent_category_id` (int): ID родительской категории, по которому нужно отфильтровать дочерние категории.

**Возвращает**:
- `List[models.ChildCategory]`: Список дочерних категорий, у которых атрибут `parent_category_id` соответствует переданному значению.

**Как работает функция**:

- Функция принимает на вход список категорий и ID родительской категории.
- Проверяет, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, то преобразует его в список, содержащий только этот элемент. Это необходимо для обработки случаев, когда в функцию передается одно значение вместо списка.
- Функция итерируется по каждой категории в предоставленном списке.
- Для каждой категории проверяется наличие атрибута `parent_category_id` и соответствие его значения переданному `parent_category_id`.
- Если категория является дочерней и её `parent_category_id` соответствует заданному, она добавляется в список `filtered_categories`.
- В конце функция возвращает список `filtered_categories`, содержащий только дочерние категории, принадлежащие указанной родительской категории.

**Примеры**:

Предположим, у нас есть следующий список категорий:

```python
from typing import List
from typing import Optional

class Category:
    def __init__(self, category_id: int, category_name: str, parent_category_id: Optional[int] = None):
        self.category_id = category_id
        self.category_name = category_name
        self.parent_category_id = parent_category_id

class ChildCategory:
    def __init__(self, category_id: int, category_name: str, parent_category_id: int):
        self.category_id = category_id
        self.category_name = category_name
        self.parent_category_id = parent_category_id

# Создаем экземпляры категорий
category1 = Category(category_id=1, category_name='Электроника')
category2 = ChildCategory(category_id=101, category_name='Смартфоны', parent_category_id=1)
category3 = Category(category_id=2, category_name='Одежда')
category4 = ChildCategory(category_id=201, category_name='Футболки', parent_category_id=2)

categories_list = [category1, category2, category3, category4]

# Вызываем функцию filter_child_categories
filtered_categories = filter_child_categories(categories_list, parent_category_id=1)

# Выводим результат
for category in filtered_categories:
    print(f"ID: {category.category_id}, Name: {category.category_name}, Parent ID: {category.parent_category_id}")
# ID: 101, Name: Смартфоны, Parent ID: 1