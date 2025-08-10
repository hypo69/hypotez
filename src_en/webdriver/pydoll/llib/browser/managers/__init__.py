## \file src/webdriver/pydoll/llib/browser/managers/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides a set of managers for the browser.
======================================================

This module contains the following managers:

- `ChromiumOptionsManager`: Manages the options for Chromium-based browsers.
- `BrowserProcessManager`: Manages the browser process.
- `ProxyManager`: Manages the proxy settings.
- `TempDirectoryManager`: Manages the temporary directories.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.browser.managers import ChromiumOptionsManager

    options_manager = ChromiumOptionsManager()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/browser/managers/__init__.py
"""

from header import __root__
from src.webdriver.pydoll.llib.browser.managers.browser_options_manager import (
    ChromiumOptionsManager,
)
from src.webdriver.pydoll.llib.browser.managers.browser_process_manager import (
    BrowserProcessManager,
)
from src.webdriver.pydoll.llib.browser.managers.proxy_manager import ProxyManager
from src.webdriver.pydoll.llib.browser.managers.temp_dir_manager import TempDirectoryManager

__all__ = [
    'ChromiumOptionsManager',
    'BrowserProcessManager',
    'ProxyManager',
    'TempDirectoryManager',
]
