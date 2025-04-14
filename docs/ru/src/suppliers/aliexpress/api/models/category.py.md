# Модуль для работы с категориями товаров AliExpress
=====================================================

Модуль содержит классы `Category` и `ChildCategory`, которые используются для представления категорий товаров, полученных через API AliExpress.

## Обзор

Этот модуль определяет структуры данных для представления категорий товаров AliExpress. Он включает базовый класс `Category` с основными атрибутами категории, а также класс `ChildCategory`, наследующий `Category` и добавляющий информацию о родительской категории.

## Классы

### `Category`

**Описание**:
Базовый класс для представления категории товара.

**Атрибуты**:
- `category_id` (int): Уникальный идентификатор категории.
- `category_name` (str): Название категории.

**Принцип работы**:
Класс `Category` служит основой для представления категорий товаров. Он содержит идентификатор и название категории.

### `ChildCategory(Category)`

**Описание**:
Класс для представления подкатегории товара, наследующий класс `Category`.

**Наследует**:
- `Category`: Класс `ChildCategory` наследует все атрибуты и методы класса `Category`.

**Атрибуты**:
- `parent_category_id` (int): Уникальный идентификатор родительской категории.

**Принцип работы**:
Класс `ChildCategory` расширяет класс `Category`, добавляя информацию о родительской категории, что позволяет представлять иерархические структуры категорий.

## Параметры классов

- `category_id` (int): Уникальный идентификатор категории.
- `category_name` (str): Название категории.
- `parent_category_id` (int): Уникальный идентификатор родительской категории.

## Примеры

### Использование класса `Category`

```python
category = Category()
category.category_id = 123
category.category_name = 'Электроника'
print(category.category_id)
print(category.category_name)
```

### Использование класса `ChildCategory`

```python
child_category = ChildCategory()
child_category.category_id = 456
child_category.category_name = 'Смартфоны'
child_category.parent_category_id = 123
print(child_category.category_id)
print(child_category.category_name)
print(child_category.parent_category_id)