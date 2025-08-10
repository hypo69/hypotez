## \file src/webdriver/pydoll/llib/elements/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides classes for interacting with web elements.
==============================================================

This module contains the `WebElement` class, which is a wrapper around a DOM element
and provides methods for interacting with it, such as clicking, typing text,
and taking screenshots.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.elements.web_element import WebElement

    # Example of creating a WebElement (requires object_id and connection_handler)
    # element = WebElement(object_id="some_id", connection_handler=some_handler)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/elements/__init__.py
"""

from src.webdriver.pydoll.llib.elements.mixins.find_elements_mixin import FindElementsMixin
from src.webdriver.pydoll.llib.elements.web_element import WebElement

__all__ = [
    'FindElementsMixin',
    'WebElement',
]
