# Модуль `category`

## Обзор

Модуль содержит классы для представления категорий товаров, в частности класс `Category` и `ChildCategory`, предназначенные для хранения информации о категориях и подкатегориях товаров, соответственно.

## Подробней

Этот модуль предоставляет структуру данных для работы с категориями товаров, полученных от AliExpress API. Классы позволяют удобно хранить и передавать информацию о категориях, такую как идентификатор и название. `ChildCategory` расширяет базовую информацию, добавляя сведения о родительской категории.

## Классы

### `Category`

**Описание**: Базовый класс для представления категории товара.

**Атрибуты**:
- `category_id` (int): Уникальный идентификатор категории.
- `category_name` (str): Название категории.

**Принцип работы**:
Класс `Category` служит основой для представления любой категории товара. Он содержит два атрибута: уникальный идентификатор категории (`category_id`) и её название (`category_name`).

**Примеры**:

```python
category = Category()
category.category_id = 12345
category.category_name = "Электроника"
print(category.category_id) # Вывод: 12345
print(category.category_name) # Вывод: Электроника
```

### `ChildCategory`

**Описание**: Класс для представления подкатегории товара, наследуется от класса `Category`.

**Наследует**:
- `Category`: класс `ChildCategory` наследует атрибуты `category_id` и `category_name` от класса `Category`.

**Атрибуты**:
- `parent_category_id` (int): Идентификатор родительской категории.

**Принцип работы**:
Класс `ChildCategory` расширяет класс `Category`, добавляя информацию о родительской категории (`parent_category_id`). Это позволяет представить иерархию категорий товаров.

**Примеры**:

```python
child_category = ChildCategory()
child_category.category_id = 67890
child_category.category_name = "Смартфоны"
child_category.parent_category_id = 12345
print(child_category.category_id) # Вывод: 67890
print(child_category.category_name) # Вывод: Смартфоны
print(child_category.parent_category_id) # Вывод: 12345
```