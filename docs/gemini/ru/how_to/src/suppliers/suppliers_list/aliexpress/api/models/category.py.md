## \file /src/suppliers/aliexpress/api/models/category.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль определяет модели данных для представления категорий товаров.
=====================================================================

Этот модуль содержит классы `Category` и `ChildCategory`, которые используются
для структурированного представления информации о категориях товаров,
полученных из API AliExpress.

 .. module:: src.suppliers.suppliers_list.aliexpress.api.models
"""


class Category:
    category_id: int
    category_name: str


class ChildCategory(Category):
    parent_category_id: int


Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет две модели данных: `Category` и `ChildCategory`. Класс `Category` используется для представления основной информации о категории, такой как её идентификатор (`category_id`) и название (`category_name`). Класс `ChildCategory` наследуется от `Category` и добавляет информацию об идентификаторе родительской категории (`parent_category_id`).

Шаги выполнения
-------------------------
1. **Определение класса `Category`**: Определяется класс `Category` с полями `category_id` (целое число) и `category_name` (строка). Эти поля представляют идентификатор и название категории товара соответственно.
2. **Определение класса `ChildCategory`**: Определяется класс `ChildCategory`, наследуемый от класса `Category`. Он добавляет поле `parent_category_id` (целое число), которое указывает на идентификатор родительской категории.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models import Category, ChildCategory

# Пример создания экземпляра класса Category
category = Category()
category.category_id = 12345
category.category_name = "Electronics"

print(f"Category ID: {category.category_id}")
print(f"Category Name: {category.category_name}")

# Пример создания экземпляра класса ChildCategory
child_category = ChildCategory()
child_category.category_id = 67890
child_category.category_name = "Smartphones"
child_category.parent_category_id = 12345

print(f"Child Category ID: {child_category.category_id}")
print(f"Child Category Name: {child_category.category_name}")
print(f"Parent Category ID: {child_category.parent_category_id}")