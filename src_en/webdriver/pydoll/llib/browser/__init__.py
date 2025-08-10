## \file src/webdriver/pydoll/llib/browser/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides classes for working with browsers.
====================================================

This module contains the following classes:

- `Chrome`: A class for working with Google Chrome.
- `Edge`: A class for working with Microsoft Edge.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.browser import Chrome

    browser = Chrome()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/browser/__init__.py
"""

from header import __root__
from src.webdriver.pydoll.llib.browser.chromium.chrome import Chrome
from src.webdriver.pydoll.llib.browser.chromium.edge import Edge

__all__ = ['Chrome', 'Edge']
