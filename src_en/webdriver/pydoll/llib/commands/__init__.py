## \file src/webdriver/pydoll/llib/commands/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides a set of classes for creating commands for the Chrome DevTools Protocol.
==========================================================================================

This module contains the following classes:

- `BrowserCommands`: A class for creating Browser commands.
- `DomCommands`: A class for creating DOM commands.
- `FetchCommands`: A class for creating Fetch commands.
- `InputCommands`: A class for creating Input commands.
- `NetworkCommands`: A class for creating Network commands.
- `PageCommands`: A class for creating Page commands.
- `RuntimeCommands`: A class for creating Runtime commands.
- `StorageCommands`: A class for creating Storage commands.
- `TargetCommands`: A class for creating Target commands.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.commands import PageCommands

    # Create a command to navigate to a URL
    navigate_command = PageCommands.navigate(url="https://www.google.com")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/commands/__init__.py
"""

# global imports
from src.webdriver.pydoll.llib.commands.browser_commands import BrowserCommands
from src.webdriver.pydoll.llib.commands.dom_commands import DomCommands
from src.webdriver.pydoll.llib.commands.fetch_commands import FetchCommands
from src.webdriver.pydoll.llib.commands.input_commands import InputCommands
from src.webdriver.pydoll.llib.commands.network_commands import NetworkCommands
from src.webdriver.pydoll.llib.commands.page_commands import PageCommands
from src.webdriver.pydoll.llib.commands.runtime_commands import RuntimeCommands
from src.webdriver.pydoll.llib.commands.storage_commands import StorageCommands
from src.webdriver.pydoll.llib.commands.target_commands import TargetCommands

__all__ = [
    'DomCommands',
    'FetchCommands',
    'InputCommands',
    'NetworkCommands',
    'PageCommands',
    'RuntimeCommands',
    'StorageCommands',
    'BrowserCommands',
    'TargetCommands',
]
