## Как использовать класс `Category`
=========================================================================================

Описание
-------------------------
Классы `Category` и `ChildCategory` представляют собой модели данных, которые используются для представления категорий товаров на AliExpress. 

**`Category`** - базовый класс, который содержит идентификатор (id) и название категории. 
**`ChildCategory`** - наследуется от `Category` и добавляет атрибут для идентификатора родительской категории.

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте объект класса `Category` или `ChildCategory` и укажите значения для атрибутов `category_id` и `category_name`. В случае с `ChildCategory` также задайте значение для `parent_category_id`.
2. **Доступ к данным**: 
    - Доступ к атрибутам (id, название, id родительской категории) осуществляется через имя атрибута объекта, например: `category.category_id`, `category.category_name`, `child_category.parent_category_id`.

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.models.category import Category, ChildCategory

# Создание объекта Category
category = Category(category_id=1234, category_name="Одежда")

# Вывод информации о категории
print(f"ID категории: {category.category_id}")
print(f"Название категории: {category.category_name}")

# Создание объекта ChildCategory
child_category = ChildCategory(category_id=5678, category_name="Платья", parent_category_id=1234)

# Вывод информации о дочерней категории
print(f"ID категории: {child_category.category_id}")
print(f"Название категории: {child_category.category_name}")
print(f"ID родительской категории: {child_category.parent_category_id}")
```

## Дополнительные замечания
-------------------------
- Классы `Category` и `ChildCategory` служат для удобной работы с данными о категориях, которые вы получаете из API AliExpress. 
- Используйте эти классы для сохранения и обработки информации о категориях в вашем проекте.