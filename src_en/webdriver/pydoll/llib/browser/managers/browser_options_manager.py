## \file src/webdriver/pydoll/llib/browser/managers/browser_options_manager.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides a manager for browser options.
====================================================

This module contains the `ChromiumOptionsManager` class, which is responsible for
managing the browser options for Chromium-based browsers.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.browser.managers.browser_options_manager import ChromiumOptionsManager
    from src.webdriver.pydoll.llib.browser.options import ChromiumOptions

    options = ChromiumOptions()
    options_manager = ChromiumOptionsManager(options)
    initialized_options = options_manager.initialize_options()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/browser/managers/browser_options_manager.py
"""

from typing import Optional
from header import __root__
from src.webdriver.pydoll.llib.browser.interfaces import BrowserOptionsManager
from src.webdriver.pydoll.llib.browser.options import ChromiumOptions
from src.webdriver.pydoll.llib.exceptions import InvalidOptionsObject

from src.webdriver.pydoll.options import Options


class ChromiumOptionsManager(BrowserOptionsManager):
    """
    Manages browser options configuration for Chromium-based browsers.

    Handles options creation, validation, and applies default CDP arguments
    for Chrome and Edge browsers.
    """

    def __init__(self, options: Optional[Options] = None):
        self.options = options

    def initialize_options(
        self,
    ) -> ChromiumOptions:
        """
        Initialize and validate browser options.

        Creates ChromiumOptions if none provided, validates existing options,
        and applies default CDP arguments.

        Returns:
            Properly configured ChromiumOptions instance.

        Raises:
            InvalidOptionsObject: If provided options is not ChromiumOptions.
        """
        if self.options is None:
            self.options = ChromiumOptions()

        if not isinstance(self.options,(ChromiumOptions | Options)):
            raise InvalidOptionsObject(f'Expected ChromiumOptions, got {type(self.options)}')
            ...

        self.add_default_arguments()
        return self.options

    def add_default_arguments(self):
        """Add default arguments required for CDP integration."""
        self.options.add_argument('--no-first-run')
        self.options.add_argument('--no-default-browser-check')
