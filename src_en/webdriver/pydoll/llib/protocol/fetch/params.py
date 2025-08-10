## \file src/webdriver/pydoll/llib/protocol/fetch/params.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines parameter structures for fetch operations in the Chrome DevTools Protocol.
==========================================================================================

This module contains `TypedDict` definitions for the parameters used in various
fetch-related commands in the Chrome DevTools Protocol, such as continuing requests,
enabling fetch interception, and fulfilling requests with custom responses.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.fetch.params import ContinueRequestParams

    # Example of creating ContinueRequestParams
    params = ContinueRequestParams(requestId="some_request_id", url="https://www.example.com")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/fetch/params.py
"""

from typing_extensions import NotRequired

from src.webdriver.pydoll.llib.constants import NetworkErrorReason, RequestMethod
from src.webdriver.pydoll.llib.protocol.base import CommandParams
from src.webdriver.pydoll.llib.protocol.fetch.types import (
    AuthChallengeResponseDict,
    HeaderEntry,
    RequestPattern,
)


class ContinueRequestParams(CommandParams):
    """Parameters for continuing a request."""

    requestId: str
    url: NotRequired[str]
    method: NotRequired[RequestMethod]
    postData: NotRequired[str]
    headers: NotRequired[list[HeaderEntry]]
    interceptResponse: NotRequired[bool]


class ContinueWithAuthParams(CommandParams):
    requestId: str
    authChallengeResponse: AuthChallengeResponseDict


class FetchEnableParams(CommandParams):
    patterns: NotRequired[list[RequestPattern]]
    handleAuthRequests: NotRequired[bool]


class FailRequestParams(CommandParams):
    requestId: str
    errorReason: NetworkErrorReason


class FulfillRequestParams(CommandParams):
    requestId: str
    responseCode: int
    responseHeaders: NotRequired[list[HeaderEntry]]
    body: NotRequired[str]
    responsePhrase: NotRequired[str]


class GetResponseBodyParams(CommandParams):
    requestId: str


class TakeResponseBodyAsStreamParams(CommandParams):
    requestId: str


class ContinueResponseParams(CommandParams):
    requestId: str
    responseCode: NotRequired[int]
    responsePhrase: NotRequired[str]
    responseHeaders: NotRequired[list[HeaderEntry]]
