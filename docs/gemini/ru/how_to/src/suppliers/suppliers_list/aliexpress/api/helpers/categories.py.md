## Как использовать блок кода для фильтрации категорий и подкатегорий API Aliexpress
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет две функции для фильтрации категорий и подкатегорий API Aliexpress:

1. `filter_parent_categories`: извлекает список категорий, которые не имеют родительской категории.
2. `filter_child_categories`: извлекает список подкатегорий, которые принадлежат заданной родительской категории.

Шаги выполнения
-------------------------
1. **`filter_parent_categories(categories: List[models.Category | models.ChildCategory]) -> List[models.Category]`**:
    - Принимает список объектов категорий или подкатегорий.
    - Проверяет, имеет ли каждый объект атрибут `parent_category_id`.
    - Если атрибут отсутствует, объект добавляется в список `filtered_categories`.
    - Возвращает список объектов категорий, которые не имеют родительской категории.
2. **`filter_child_categories(categories: List[models.Category | models.ChildCategory], parent_category_id: int) -> List[models.ChildCategory]`**:
    - Принимает список объектов категорий или подкатегорий, а также ID родительской категории.
    - Проверяет, имеет ли каждый объект атрибут `parent_category_id`, и совпадает ли его значение с переданным `parent_category_id`.
    - Если объект имеет `parent_category_id` и он совпадает с переданным ID, объект добавляется в список `filtered_categories`.
    - Возвращает список объектов подкатегорий, которые принадлежат заданной родительской категории.

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.helpers.categories import filter_parent_categories, filter_child_categories
from src.suppliers.aliexpress.api import models

# Пример списка категорий и подкатегорий
categories = [
    models.Category(category_id=1, name="Electronics"),
    models.ChildCategory(category_id=2, parent_category_id=1, name="Smartphones"),
    models.Category(category_id=3, name="Clothing"),
    models.ChildCategory(category_id=4, parent_category_id=3, name="T-shirts"),
    models.ChildCategory(category_id=5, parent_category_id=3, name="Dresses"),
]

# Получение списка категорий без родительской категории
parent_categories = filter_parent_categories(categories)
print(f"Parent categories: {parent_categories}") # Output: Parent categories: [<Category: category_id=1, name=Electronics>, <Category: category_id=3, name=Clothing>]

# Получение списка подкатегорий, принадлежащих категории "Electronics" (category_id=1)
child_categories = filter_child_categories(categories, parent_category_id=1)
print(f"Child categories of Electronics: {child_categories}") # Output: Child categories of Electronics: [<ChildCategory: category_id=2, parent_category_id=1, name=Smartphones>]
```