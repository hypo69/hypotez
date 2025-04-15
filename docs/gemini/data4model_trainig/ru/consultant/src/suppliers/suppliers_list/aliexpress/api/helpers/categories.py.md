### **Анализ кода модуля `categories.py`**

## \file /src/suppliers/aliexpress/api/helpers/categories.py

Модуль содержит функции для фильтрации категорий и подкатегорий API Aliexpress.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура функций.
    - Наличие docstring для каждой функции.
    - Логика фильтрации категорий достаточно проста и понятна.
- **Минусы**:
    - Использование английского языка в docstring (не соответствует требованиям).
    - Не все переменные аннотированы типами.
    - Не обрабатываются исключения.
    - Используется `Union` вместо `|` в аннотациях типов.
    - Нет обработки ошибок или логирования.
    - В docstring используется `@param` и `@return` вместо общепринятого `Args:` и `Returns:`.
    - Не указаны примеры использования функций в docstring.
    - Не указаны возможные исключения в docstring (секция `Raises:`).

**Рекомендации по улучшению:**

1.  **Перевод docstring на русский язык**: Перевести все docstring на русский язык, чтобы соответствовать требованиям.
2.  **Использование аннотаций типов**: Добавить аннотации типов для всех переменных, где это необходимо.
3.  **Обработка исключений**: Добавить обработку исключений для повышения надежности кода.
4.  **Заменить `Union` на `|`**: Использовать `|` вместо `Union` для аннотаций типов.
5.  **Добавить логирование**: Использовать модуль `logger` для логирования важных событий, особенно ошибок.
6.  **Изменить формат docstring**: Привести docstring к требуемому формату, включая разделы `Args:`, `Returns:`, `Raises:` и `Example:`.
7.  **Добавить примеры использования**: Добавить примеры использования функций в docstring.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/api/helpers/categories.py
# -*- coding: utf-8 -*-
# <- venv win
## ~~~~~~~~~~~~

"""
Модуль для фильтрации категорий и подкатегорий API Aliexpress
=============================================================

Модуль содержит функции :func:`filter_parent_categories` и :func:`filter_child_categories`
для фильтрации категорий и подкатегорий, полученных из API Aliexpress.

Пример использования
----------------------

>>> from src.suppliers.aliexpress.api import models
>>> categories = [models.Category(id=1, name='Category 1'), models.ChildCategory(id=2, name='Child Category 1', parent_category_id=1)]
>>> parent_categories = filter_parent_categories(categories)
>>> print(parent_categories)
[<src.suppliers.aliexpress.api.models.Category object at ...>]
"""

from typing import List
from .. import models
from src.logger import logger  # Импорт модуля logger

def filter_parent_categories(categories: List[models.Category | models.ChildCategory]) -> List[models.Category]:
    """
    Фильтрует и возвращает список категорий, у которых нет родительской категории.

    Args:
        categories (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.

    Returns:
        List[models.Category]: Список объектов категорий без родительской категории.

    Raises:
        TypeError: Если передан некорректный тип данных в categories.

    Example:
        >>> from src.suppliers.aliexpress.api import models
        >>> categories = [models.Category(id=1, name='Category 1'), models.ChildCategory(id=2, name='Child Category 2', parent_category_id=1)]
        >>> filter_parent_categories(categories)
        [<src.suppliers.aliexpress.api.models.Category object at ...>]
    """
    filtered_categories: List[models.Category] = []

    if not isinstance(categories, list):
        logger.error(f'Некорректный тип данных для categories: {type(categories)}')
        raise TypeError('Ожидается список категорий.')

    for category in categories:
        if not hasattr(category, 'parent_category_id'):
            filtered_categories.append(category)

    return filtered_categories


def filter_child_categories(categories: List[models.Category | models.ChildCategory],
                            parent_category_id: int) -> List[models.ChildCategory]:
    """
    Фильтрует и возвращает список дочерних категорий, принадлежащих указанной родительской категории.

    Args:
        categories (List[models.Category | models.ChildCategory]): Список объектов категорий или дочерних категорий.
        parent_category_id (int): ID родительской категории, по которой фильтруются дочерние категории.

    Returns:
        List[models.ChildCategory]: Список объектов дочерних категорий с указанным ID родительской категории.

    Raises:
        TypeError: Если передан некорректный тип данных в categories.

    Example:
        >>> from src.suppliers.aliexpress.api import models
        >>> categories = [models.Category(id=1, name='Category 1'), models.ChildCategory(id=2, name='Child Category 2', parent_category_id=1)]
        >>> filter_child_categories(categories, 1)
        [<src.suppliers.aliexpress.api.models.ChildCategory object at ...>]
    """
    filtered_categories: List[models.ChildCategory] = []

    if not isinstance(categories, list):
        logger.error(f'Некорректный тип данных для categories: {type(categories)}')
        raise TypeError('Ожидается список категорий.')

    for category in categories:
        if hasattr(category, 'parent_category_id') and category.parent_category_id == parent_category_id:
            filtered_categories.append(category)

    return filtered_categories