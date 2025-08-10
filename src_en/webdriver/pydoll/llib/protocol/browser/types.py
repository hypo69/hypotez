## \file src/webdriver/pydoll/llib/protocol/browser/types.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines types related to browser operations in the Chrome DevTools Protocol.
=====================================================================================

This module contains `TypedDict` definitions for various browser-related types,
primarily focusing on window management and bounds.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.browser.types import WindowBoundsDict
    from src.webdriver.pydoll.llib.constants import WindowState

    # Example of creating a WindowBoundsDict
    bounds: WindowBoundsDict = {
        "windowState": WindowState.NORMAL,
        "width": 800,
        "height": 600,
        "x": 100,
        "y": 100
    }
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/browser/types.py
"""

from typing_extensions import NotRequired, TypedDict

from src.webdriver.pydoll.llib.constants import WindowState


class WindowBoundsDict(TypedDict):
    """Structure for window bounds parameters."""

    windowState: WindowState
    width: NotRequired[int]
    height: NotRequired[int]
    x: NotRequired[int]
    y: NotRequired[int]
