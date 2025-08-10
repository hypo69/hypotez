## \file src/webdriver/pydoll/llib/protocol/fetch/types.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines types related to fetch operations in the Chrome DevTools Protocol.
===================================================================================

This module contains `TypedDict` definitions for various fetch-related types,
such as `HeaderEntry`, `AuthChallengeResponseDict`, and `RequestPattern`.
These types are used to represent information about HTTP headers, authentication
challenges, and request patterns for interception.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.fetch.types import HeaderEntry

    # Example of a HeaderEntry object
    header: HeaderEntry = {"name": "Content-Type", "value": "application/json"}
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/fetch/types.py
"""

from typing_extensions import NotRequired, TypedDict

from src.webdriver.pydoll.llib.constants import AuthChallengeResponseValues, RequestStage, ResourceType


class HeaderEntry(TypedDict):
    """HTTP header entry structure."""

    name: str
    value: str


class AuthChallengeResponseDict(TypedDict):
    response: AuthChallengeResponseValues
    username: NotRequired[str]
    password: NotRequired[str]


class RequestPattern(TypedDict):
    urlPattern: str
    resourceType: NotRequired[ResourceType]
    requestStage: NotRequired[RequestStage]
