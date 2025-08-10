## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/header.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Header for AliExpress campaign experiments.

This module provides a common header for various AliExpress campaign experiments,
including path configurations and imports for necessary modules.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.header import __root__

    print(f"Project root directory: {__root__}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/header.py
"""


""" Header  """



import sys,os
from pathlib import Path
__root__ : Path = os.getcwd() [:os.getcwd().rfind(r'hypotez')+7]
sys.path.append (__root__)
