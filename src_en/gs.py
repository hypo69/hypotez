## \file /src/gs.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.gs
    :platform: Windows, Unix
    :synopsis: Loading program parameters without using KeePass storage.

Loading program parameters without using KeePass storage
=======================================================================
In this case, the `USE_ENV` constant is set to `True`, and data about keys, APIs, passwords, and so on will be loaded from `.env` files.
Extremely inconvenient method.
Don't do that!

Example usage
-------------

```python
    from src.gs import gs

    print(gs.some_config_value)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/gs.py
"""
import header
from header import __root__
from src.utils.jjson import j_loads_ns
from pathlib import Path

gs = j_loads_ns(__root__ / 'src' / 'config.json')
