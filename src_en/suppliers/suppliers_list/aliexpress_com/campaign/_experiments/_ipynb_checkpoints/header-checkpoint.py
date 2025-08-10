## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/_ipynb_checkpoints/header-checkpoint.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments._ipynb_checkpoints
    :platform: Windows, Unix
    :synopsis: Header checkpoint for AliExpress campaign experiments.

This module provides a common header for various AliExpress campaign experiments,
including path configurations and imports for necessary modules.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments._ipynb_checkpoints.header-checkpoint import dir_root

    print(f"Project root directory: {dir_root}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/_ipynb_checkpoints/header-checkpoint.py
"""
MODE = 'dev'


import os
import sys
from pathlib import Path

dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7]) ## <- Project root directory
sys.path.append (str (dir_root) )  # Add root directory to sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) # Add working directory to sys.path
