## \file src/webdriver/pydoll/llib/protocol/browser/params.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines parameter structures for browser operations in the Chrome DevTools Protocol.
============================================================================================

This module contains `TypedDict` definitions for the parameters used in various
browser-related commands in the Chrome DevTools Protocol, such as setting window
bounds and download behavior.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.browser.params import SetWindowBoundsParams
    from src.webdriver.pydoll.llib.protocol.browser.types import WindowBoundsDict
    from src.webdriver.pydoll.llib.constants import WindowState

    # Example of creating SetWindowBoundsParams
    bounds: WindowBoundsDict = {
        "windowState": WindowState.NORMAL,
        "width": 800,
        "height": 600
    }
    params = SetWindowBoundsParams(windowId=1, bounds=bounds)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/browser/params.py
"""

from typing_extensions import NotRequired

from src.webdriver.pydoll.llib.constants import DownloadBehavior, PermissionType
from src.webdriver.pydoll.llib.protocol.base import CommandParams
from src.webdriver.pydoll.llib.protocol.browser.types import WindowBoundsDict


class GetWindowForTargetParams(CommandParams):
    """Parameters for getting window by target ID."""

    targetId: str


class SetDownloadBehaviorParams(CommandParams):
    """Parameters for setting download behavior."""

    behavior: DownloadBehavior
    downloadPath: NotRequired[str]
    browserContextId: NotRequired[str]
    eventsEnabled: NotRequired[bool]


class SetWindowBoundsParams(CommandParams):
    """Parameters for setting window bounds."""

    windowId: int
    bounds: WindowBoundsDict


class ResetPermissionsParams(CommandParams):
    """Parameters for resetting permissions."""

    browserContextId: NotRequired[str]


class CancelDownloadParams(CommandParams):
    """Parameters for cancelling downloads."""

    guid: str
    browserContextId: NotRequired[str]


class GrantPermissionsParams(CommandParams):
    """Parameters for granting permissions."""

    permissions: list[PermissionType]
    origin: NotRequired[str]
    browserContextId: NotRequired[str]
