## \file /src/suppliers/suppliers_list/de_hexcel_com/header.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.de_hexcel_com.header
    :platform: Windows, Unix
    :synopsis: Header module for Hexcel (Germany) supplier-specific functionalities.

Hexcel (Germany) Supplier Header
=========================================================================================

This module provides a common header for Hexcel (Germany) supplier-specific functionalities,
primarily defining the project root and ensuring it's added to the system path for module imports.

Example usage
-------------

```python
    # This module is typically imported at the beginning of other modules
    # within the Hexcel (Germany) supplier package to set up the project root.
    # import header
    # from header import __root__
    # print(f"Project root: {__root__}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/de_hexcel_com/header.py
"""

import sys
import json
from pathlib import Path

def set_project_root(marker_files=('__root__','.git')) -> Path:
    """
    Finds the root directory of the project starting from the current file's directory,
    searching upwards and stopping at the first directory containing any of the marker files.

    Args:
        marker_files (tuple): Filenames or directory names to identify the project root.
    
    Returns:
        Path: Path to the root directory if found, otherwise the directory where the script is located.
    """
    __root__:Path
    current_path:Path = Path(__file__).resolve().parent
    __root__ = current_path
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            __root__ = parent
            break
    if __root__ not in sys.path:
        sys.path.insert(0, str(__root__))
    return __root__


# Get the root directory of the project
__root__: Path = set_project_root()
"""__root__ (Path): Path to the root directory of the project"""