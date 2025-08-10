## \file src/webdriver/pydoll/llib/protocol/network/responses.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines response structures for network operations in the Chrome DevTools Protocol.
===========================================================================================

This module contains `TypedDict` definitions for the responses returned by various
network-related commands in the Chrome DevTools Protocol, such as getting cookies,
retrieving request POST data, and getting response bodies.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.network.responses import GetCookiesResponse

    # Example of a GetCookiesResponse object
    response: GetCookiesResponse = {
        "result": {
            "cookies": [
                {
                    "name": "my_cookie",
                    "value": "my_value",
                    "domain": ".example.com",
                    "path": "/",
                    "expires": 1678886400,
                    "size": 16,
                    "httpOnly": False,
                    "secure": False,
                    "session": False,
                    "sameSite": "None",
                    "priority": "Medium"
                }
            ]
        }
    }
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/network/responses.py
"""

from typing_extensions import NotRequired, TypedDict

from src.webdriver.pydoll.llib.protocol.fetch.types import HeaderEntry
from src.webdriver.pydoll.llib.protocol.network.types import Cookie, SearchMatch, SecurityIsolationStatus


class GetCookiesResultDict(TypedDict):
    """Response result for getCookies command."""

    cookies: list[Cookie]


class GetRequestPostDataResultDict(TypedDict):
    """Response result for getRequestPostData command."""

    postData: str


class GetResponseBodyResultDict(TypedDict):
    """Response result for getResponseBody command."""

    body: str
    base64Encoded: bool


class GetResponseBodyForInterceptionResultDict(TypedDict):
    """Response result for getResponseBodyForInterception command."""

    body: str
    base64Encoded: bool


class GetCertificateResultDict(TypedDict):
    """Response result for getCertificate command."""

    tableNames: list[str]


class SearchInResponseBodyResultDict(TypedDict):
    """Response result for searchInResponseBody command."""

    result: list[SearchMatch]


class SetCookieResultDict(TypedDict):
    """Response result for setCookie command."""

    success: bool


class StreamResourceContentResultDict(TypedDict):
    """Response result for streamResourceContent command."""

    bufferedData: str


class TakeResponseBodyForInterceptionAsStreamResultDict(TypedDict):
    """Response result for takeResponseBodyForInterceptionAsStream command."""

    stream: str


class CanClearBrowserCacheResultDict(TypedDict):
    """Response result for canClearBrowserCache command."""

    result: bool


class CanClearBrowserCookiesResultDict(TypedDict):
    """Response result for canClearBrowserCookies command."""

    result: bool


class CanEmulateNetworkConditionsResultDict(TypedDict):
    """Response result for canEmulateNetworkConditions command."""

    result: bool


class GetSecurityIsolationStatusResultDict(TypedDict):
    """Response result for getSecurityIsolationStatus command."""

    status: SecurityIsolationStatus


class LoadNetworkResourceResultDict(TypedDict):
    """Response result for loadNetworkResource command."""

    success: bool
    netError: NotRequired[float]
    netErrorName: NotRequired[str]
    httpStatusCode: NotRequired[float]
    stream: NotRequired[str]
    headers: NotRequired[list[HeaderEntry]]


# Response classes that inherit from Response
class GetCookiesResponse(TypedDict):
    """Response for getCookies command."""

    result: GetCookiesResultDict


class GetRequestPostDataResponse(TypedDict):
    """Response for getRequestPostData command."""

    result: GetRequestPostDataResultDict


class GetResponseBodyResponse(TypedDict):
    """Response for getResponseBody command."""

    result: GetResponseBodyResultDict


class GetResponseBodyForInterceptionResponse(TypedDict):
    """Response for getResponseBodyForInterception command."""

    result: GetResponseBodyForInterceptionResultDict


class GetCertificateResponse(TypedDict):
    """Response for getCertificate command."""

    result: GetCertificateResultDict


class SearchInResponseBodyResponse(TypedDict):
    """Response for searchInResponseBody command."""

    result: SearchInResponseBodyResultDict


class SetCookieResponse(TypedDict):
    """Response for setCookie command."""

    result: SetCookieResultDict


class StreamResourceContentResponse(TypedDict):
    """Response for streamResourceContent command."""

    result: StreamResourceContentResultDict


class TakeResponseBodyForInterceptionAsStreamResponse(TypedDict):
    """Response for takeResponseBodyForInterceptionAsStream command."""

    result: TakeResponseBodyForInterceptionAsStreamResultDict


class CanClearBrowserCacheResponse(TypedDict):
    """Response for canClearBrowserCache command."""

    result: CanClearBrowserCacheResultDict


class CanClearBrowserCookiesResponse(TypedDict):
    """Response for canClearBrowserCookies command."""

    result: CanClearBrowserCookiesResultDict


class CanEmulateNetworkConditionsResponse(TypedDict):
    """Response for canEmulateNetworkConditions command."""

    result: CanEmulateNetworkConditionsResultDict


class GetSecurityIsolationStatusResponse(TypedDict):
    """Response for getSecurityIsolationStatus command."""

    result: GetSecurityIsolationStatusResultDict


class LoadNetworkResourceResponse(TypedDict):
    """Response for loadNetworkResource command."""

    result: LoadNetworkResourceResultDict
