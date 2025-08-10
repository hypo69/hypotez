## \file src/webdriver/pydoll/llib/connection/managers/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides a set of managers for handling connections.
==============================================================

This module contains the following managers:

- `CommandsManager`: Manages the execution of commands.
- `EventsManager`: Manages the handling of events.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.connection.managers import CommandsManager

    commands_manager = CommandsManager()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/connection/managers/__init__.py
"""

from src.webdriver.pydoll.llib.connection.managers.commands_manager import CommandsManager
from src.webdriver.pydoll.llib.connection.managers.events_manager import EventsManager

__all__ = [
    'CommandsManager',
    'EventsManager',
]
