# Модуль: Модели категорий AliExpress
## Обзор

Этот модуль содержит модели данных для представления категорий товаров на AliExpress. Модели используются для работы с API AliExpress и хранения информации о категориях.

## Подробней

Этот файл содержит два класса: `Category` и `ChildCategory`, которые используются для представления категорий товаров на AliExpress. 

* `Category`: Базовый класс для представления категории на AliExpress.
* `ChildCategory`:  Класс, представляющий подкатегорию, наследуется от `Category` и добавляет атрибут для идентификатора родительской категории.

## Классы

### `Category`

**Описание**: Базовый класс для представления категории на AliExpress.

**Атрибуты**:

- `category_id` (int): Идентификатор категории.
- `category_name` (str): Название категории.

**Пример использования**:

```python
from src.suppliers.aliexpress.api.models.category import Category

category = Category(category_id=12345, category_name="Одежда")

print(f"ID категории: {category.category_id}")
print(f"Название категории: {category.category_name}")
```

### `ChildCategory`

**Описание**: Класс, представляющий подкатегорию на AliExpress. Наследуется от `Category`.

**Атрибуты**:

- `parent_category_id` (int): Идентификатор родительской категории.

**Пример использования**:

```python
from src.suppliers.aliexpress.api.models.category import ChildCategory

child_category = ChildCategory(
    category_id=67890,
    category_name="Женская одежда",
    parent_category_id=12345,
)

print(f"ID категории: {child_category.category_id}")
print(f"Название категории: {child_category.category_name}")
print(f"ID родительской категории: {child_category.parent_category_id}")
```

## Примеры

**Пример 1: Создание объекта `Category`**:

```python
from src.suppliers.aliexpress.api.models.category import Category

category = Category(category_id=12345, category_name="Одежда")
```

**Пример 2: Создание объекта `ChildCategory`**:

```python
from src.suppliers.aliexpress.api.models.category import ChildCategory

child_category = ChildCategory(
    category_id=67890,
    category_name="Женская одежда",
    parent_category_id=12345,
)