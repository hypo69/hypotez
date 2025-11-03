## \file src/endpoints/aistros/header.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль определения корневой директории проекта для aistros endpoint
====================================================================

.. module:: src.endpoints.aistros.header
"""

import sys
from pathlib import Path


def set_project_root(marker_files=('__root__', '.git')) -> Path:
    """
    Функция находит корневую директорию проекта, начиная с текущей директории файла,
    поднимаясь вверх и останавливаясь на первой директории, содержащей маркерный файл.

    Args:
        marker_files (tuple): Имена файлов или директорий для идентификации корня проекта.
    
    Returns:
        Path: Путь к корневой директории, если найдена, иначе директория, где расположен скрипт.
    """
    __root__: Path
    current_path: Path = Path(__file__).resolve().parent
    __root__ = current_path
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            __root__ = parent
            break
    if __root__ not in sys.path:
        sys.path.insert(0, str(__root__))
    return __root__


# Получение корневой директории проекта
__root__: Path = set_project_root()
"""__root__ (Path): Путь к корневой директории проекта"""
