### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный блок кода содержит функции для фильтрации категорий и подкатегорий, полученных из API Aliexpress. Он включает две функции: `filter_parent_categories` и `filter_child_categories`, которые позволяют извлекать категории верхнего уровня и дочерние категории соответственно.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются типы `List` и `Union` из модуля `typing` для аннотации типов.
   - Импортируется модуль `models` из текущего пакета (`..`) для работы с объектами категорий.

2. **Функция `filter_parent_categories`**:
   - **Описание**: Эта функция фильтрует список категорий, чтобы вернуть только те, у которых нет родительской категории (то есть категории верхнего уровня).
   - **Шаги выполнения**:
     1. Инициализируется пустой список `filtered_categories` для хранения отфильтрованных категорий.
     2. Проверяется, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, он преобразуется в список, чтобы избежать ошибок при итерации.
     3. Перебираются все элементы в списке `categories`.
     4. Для каждого элемента проверяется, отсутствует ли атрибут `parent_category_id`. Если атрибут отсутствует, категория добавляется в список `filtered_categories`.
     5. Возвращается список `filtered_categories`, содержащий только категории без родительской категории.

3. **Функция `filter_child_categories`**:
   - **Описание**: Эта функция фильтрует список категорий, чтобы вернуть только те, которые являются дочерними категориями для указанной родительской категории.
   - **Шаги выполнения**:
     1. Инициализируется пустой список `filtered_categories` для хранения отфильтрованных категорий.
     2. Проверяется, является ли входной параметр `categories` экземпляром `str`, `int` или `float`. Если да, он преобразуется в список, чтобы избежать ошибок при итерации.
     3. Перебираются все элементы в списке `categories`.
     4. Для каждого элемента проверяется наличие атрибута `parent_category_id` и соответствие значения этого атрибута значению `parent_category_id`, переданному в функцию. Если оба условия выполняются, категория добавляется в список `filtered_categories`.
     5. Возвращается список `filtered_categories`, содержащий только дочерние категории с указанным `parent_category_id`.

Пример использования
-------------------------

```python
from typing import List
from .. import models
# Assuming you have defined models.Category and models.ChildCategory

# Example data
categories: List[models.Category | models.ChildCategory] = [
    models.Category(category_id=1, category_name="Electronics"),
    models.Category(category_id=2, category_name="Clothing"),
    models.ChildCategory(category_id=3, category_name="Smartphones", parent_category_id=1),
    models.ChildCategory(category_id=4, category_name="T-Shirts", parent_category_id=2),
    models.Category(category_id=5, category_name="Home & Garden")
]

# Filter parent categories
parent_categories = filter_parent_categories(categories)
for cat in parent_categories:
    print(f"Parent Category: {cat.category_name}")

# Filter child categories for parent category ID 1
child_categories = filter_child_categories(categories, parent_category_id=1)
for cat in child_categories:
    print(f"Child Category for ID 1: {cat.category_name}")
```