## \file src/webdriver/pydoll/llib/connection/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides a connection handler for the Chrome DevTools Protocol.
=========================================================================

This module contains the `ConnectionHandler` class, which is responsible for
managing the WebSocket connection to the Chrome DevTools Protocol, sending commands,
and receiving events.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.connection import ConnectionHandler

    handler = ConnectionHandler(connection_port=9222)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/connection/__init__.py
"""

from src.webdriver.pydoll.llib.connection.connection_handler import ConnectionHandler

__all__ = [
    'ConnectionHandler',
]
