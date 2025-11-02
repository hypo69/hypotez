# Модуль `finder` 

## Обзор

Модуль `finder` предназначен для поиска и сбора данных о категориях товаров в проекте `hypotez`. Он позволяет найти все папки, содержащие информацию о категориях, а также файлы с описанием категорий.

## Подробней

Модуль `finder` используется в проекте `hypotez` для автоматизации процесса сбора данных о категориях товаров. Он позволяет:

*  **Поиск категорий**: Найти все папки, содержащие информацию о категориях товаров.
* **Сбор данных**:  Собирать данные из найденных папок и файлов, что позволит использовать эту информацию для других частей проекта.

## Функции

### `find_categories`

**Назначение**: Функция ищет все папки, содержащие информацию о категориях товаров, а также файлы с описанием категорий.

**Параметры**:

- `directory` (str): Путь к каталогу, в котором нужно выполнить поиск.

**Возвращает**:

- `List[str]`: Список путей к найденным папкам и файлам с описанием категорий.

**Как работает функция**:

1. **Перебор директорий**:  Функция использует `os.walk` для перебора всех поддиректорий в заданном каталоге.
2. **Поиск папок**:  Проверяет,  содержит ли текущая директория подпапку с названием `category`.  
3. **Поиск файлов**:  Проверяет, содержит ли текущая директория файл с названием `category.py`.
4. **Добавление в список**: Если функция находит папку `category` или файл `category.py`, она добавляет путь к этой папке или файлу в список `categories`.

**Примеры**:

```python
# Пример 1: Поиск в корневом каталоге проекта
src = str(Path(gs.path.src))
found_categories = find_categories(src)
print(found_categories)

# Пример 2: Поиск в конкретной директории
directory = 'path/to/directory'
found_categories = find_categories(directory)
print(found_categories)

```

##  Пример использования
```python
# Пример использования
src = str(Path(gs.path.src))
found_categories = find_categories(src)
for item in found_categories:
    print(item)
```


```python
                ## \\file /src/___beeryakov/_experiments/finder.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.___beeryakov._experiments 
\t:platform: Windows, Unix
\t:synopsis:

"""


"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.___beeryakov._experiments """


import os
from pathlib import Path
import header
from src import gs

def find_categories(directory):
    """
    Функция ищет все папки, содержащие информацию о категориях товаров, а также файлы с описанием категорий.
    Args:
        directory (str): Путь к каталогу, в котором нужно выполнить поиск.

    Returns:
        List[str]: Список путей к найденным папкам и файлам с описанием категорий.
    """
    categories = []
    for root, dirs, files in os.walk(directory):
        if 'category' in dirs:
            categories.append(os.path.join(root, 'translator'))
        if 'category.py' in files:
            categories.append(os.path.join(root, 'category.py'))
    return categories

# Пример использования
src = str(Path(gs.path.src))
found_categories = find_categories(src)
for item in found_categories:
    print(item)