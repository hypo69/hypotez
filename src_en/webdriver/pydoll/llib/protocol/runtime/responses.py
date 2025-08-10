## \file src/webdriver/pydoll/llib/protocol/runtime/responses.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines response structures for runtime operations in the Chrome DevTools Protocol.
===========================================================================================

This module contains `TypedDict` definitions for the responses returned by various
runtime-related commands in the Chrome DevTools Protocol, such as evaluating expressions,
calling functions, and getting properties of objects.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.runtime.responses import EvaluateResponse

    # Example of an EvaluateResponse object
    response: EvaluateResponse = {
        "result": {
            "result": {"type": "number", "value": 2},
            "exceptionDetails": None
        }
    }
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/runtime/responses.py
"""

from typing_extensions import NotRequired, TypedDict

from src.webdriver.pydoll.llib.protocol.runtime.types import (
    ExceptionDetails,
    InternalPropertyDescriptor,
    PrivatePropertyDescriptor,
    PropertyDescriptor,
    RemoteObject,
)


class AwaitPromiseResultDict(TypedDict):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class CallFunctionOnResultDict(TypedDict):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class CompileScriptResultDict(TypedDict):
    scriptId: NotRequired[str]
    exceptionDetails: NotRequired[ExceptionDetails]


class EvaluateResultDict(TypedDict):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class GetPropertiesResultDict(TypedDict):
    result: list[PropertyDescriptor]
    internalProperties: NotRequired[list[InternalPropertyDescriptor]]
    privateProperties: NotRequired[list[PrivatePropertyDescriptor]]
    exceptionDetails: NotRequired[ExceptionDetails]


class GlobalLexicalScopeNamesResultDict(TypedDict):
    names: list[str]


class QueryObjectsResultDict(TypedDict):
    objects: list[RemoteObject]


class RunScriptResultDict(TypedDict):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class GetExceptionDetailsResultDict(TypedDict):
    exceptionDetails: ExceptionDetails


class GetHeapUsageResultDict(TypedDict):
    usedSize: float
    totalSize: float
    embedderHeapUsedSize: float
    backingStorageSize: float


class GetIsolateIdResultDict(TypedDict):
    id: str


class AwaitPromiseResponse(TypedDict):
    result: AwaitPromiseResultDict


class CallFunctionOnResponse(TypedDict):
    result: CallFunctionOnResultDict


class CompileScriptResponse(TypedDict):
    result: CompileScriptResultDict


class EvaluateResponse(TypedDict):
    result: EvaluateResultDict


class GetPropertiesResponse(TypedDict):
    result: GetPropertiesResultDict


class GlobalLexicalScopeNamesResponse(TypedDict):
    result: GlobalLexicalScopeNamesResultDict


class QueryObjectsResponse(TypedDict):
    result: QueryObjectsResultDict


class RunScriptResponse(TypedDict):
    result: RunScriptResultDict


class GetHeapUsageResponse(TypedDict):
    result: GetHeapUsageResultDict


class GetIsolateIdResponse(TypedDict):
    result: GetIsolateIdResultDict
