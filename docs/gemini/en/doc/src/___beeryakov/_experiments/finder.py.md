# Module for working with categories
## Overview

This module provides a function `find_categories` for locating categories within a project directory. It searches for directories named "category" or files named "category.py" within the specified directory and its subdirectories.

## Details

This module is designed to help identify and locate categories within a larger project, such as `hypotez`. It iterates through the directory structure and its subdirectories, looking for directories named "category" or files named "category.py".  

## Functions

### `find_categories`

**Purpose:**
- This function searches for directories named "category" or files named "category.py" within a given directory and its subdirectories.

**Parameters:**
- `directory` (str): The path to the directory to search.

**Returns:**
- `list`: A list containing the full paths of found categories.

**Examples:**
```python
src = str(Path(gs.path.src))
found_categories = find_categories(src)
for item in found_categories:
    print(item)
```

**How the Function Works:**
- The function uses `os.walk` to traverse the directory tree.
- For each directory (`root`) and files (`files`) found:
    - It checks if the directory "category" exists within the current directory.
    - It checks if the file "category.py" exists within the current directory.
- If either condition is true, the corresponding path is added to the `categories` list.
- Finally, the function returns the `categories` list.

## Example File

```python
## \file /src/___beeryakov/_experiments/finder.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.___beeryakov._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

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
    Функция поиска категорий в директории.

    Args:
        directory (str): Путь к директории для поиска.

    Returns:
        list: Список с полными путями к найденным категориям.
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
```