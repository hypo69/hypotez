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

