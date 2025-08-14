# # \file /src/utils/path.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""`` `RST
    ..: Module: src.utils.path
`` `
The module defining the root path to the project. All imports are built on this path.
=================================================================================================================="""
from pathlib import Path
from typing import Optional

def get_relative_path(full_path: str, relative_from: str) -> Optional[str]:
    """Returns part of the path starting from the specified segment to the end.

    Args:
        Full_Path (str): Full path.
        Relative_from (str): the segment of the path from which you need to start extracting.

    Returns:
        Optional [str]: the relative path starting with `reta_from, or none, if the segment is not found."""
    # We convert the lines into objects Path
    path = Path(full_path)
    parts = path.parts

    # Find the segment index Relative_from
    if relative_from in parts:
        start_index = parts.index(relative_from)
        # We form the path starting with the specified segment
        relative_path = Path(*parts[start_index:])
        return relative_path.as_posix()
    else:
        return None


