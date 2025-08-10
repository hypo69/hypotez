## \file src/webdriver/pydoll/llib/protocol/browser/responses.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines response structures for browser operations in the Chrome DevTools Protocol.
===========================================================================================

This module contains `TypedDict` definitions for the responses returned by various
browser-related commands in the Chrome DevTools Protocol, such as getting window
information and browser version details.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.browser.responses import GetVersionResponse

    # Example of a GetVersionResponse object
    response: GetVersionResponse = {
        "result": {
            "protocolVersion": "1.3",
            "product": "Chrome/123.0.6312.105",
            "revision": "@123456",
            "userAgent": "Mozilla/5.0 ...",
            "jsVersion": "12.3.456.78"
        }
    }
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/browser/responses.py
"""

from typing import TypedDict

from src.webdriver.pydoll.llib.protocol.browser.types import WindowBoundsDict


class GetWindowForTargetResultDict(TypedDict):
    """Result structure for GetWindowForTarget command."""

    windowId: int
    bounds: WindowBoundsDict


class GetVersionResultDict(TypedDict):
    """Result structure for GetVersion command."""

    protocolVersion: str
    product: str
    revision: str
    userAgent: str
    jsVersion: str


class GetWindowForTargetResponse(TypedDict):
    """Response structure for GetWindowForTarget command."""

    result: GetWindowForTargetResultDict


class GetVersionResponse(TypedDict):
    """Response structure for GetVersion command."""

    result: GetVersionResultDict
