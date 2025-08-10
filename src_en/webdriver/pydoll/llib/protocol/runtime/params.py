## \file src/webdriver/pydoll/llib/protocol/runtime/params.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines parameter structures for runtime operations in the Chrome DevTools Protocol.
===========================================================================================

This module contains `TypedDict` definitions for the parameters used in various
runtime-related commands in the Chrome DevTools Protocol, such as adding bindings,
awaiting promises, and calling functions on objects.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.runtime.params import EvaluateParams

    # Example of creating EvaluateParams
    params = EvaluateParams(expression="1 + 1")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/runtime/params.py
"""

from typing_extensions import NotRequired

from src.webdriver.pydoll.llib.protocol.base import CommandParams
from src.webdriver.pydoll.llib.protocol.runtime.types import CallArgument, SerializationOptions


class AddBindingParams(CommandParams):
    name: str
    executionContextName: NotRequired[str]


class AwaitPromiseParams(CommandParams):
    promiseObjectId: str
    returnByValue: NotRequired[bool]
    generatePreview: NotRequired[bool]


class CallFunctionOnParams(CommandParams):
    functionDeclaration: str
    objectId: NotRequired[str]
    arguments: NotRequired[list[CallArgument]]
    silent: NotRequired[bool]
    returnByValue: NotRequired[bool]
    generatePreview: NotRequired[bool]
    userGesture: NotRequired[bool]
    awaitPromise: NotRequired[bool]
    executionContextId: NotRequired[str]
    objectGroup: NotRequired[str]
    throwOnSideEffect: NotRequired[bool]
    uniqueContextId: NotRequired[str]
    serializationOptions: NotRequired[SerializationOptions]


class CompileScriptParams(CommandParams):
    expression: str
    sourceURL: NotRequired[str]
    persistScript: NotRequired[bool]
    executionContextId: NotRequired[str]


class EvaluateParams(CommandParams):
    expression: str
    objectGroup: NotRequired[str]
    includeCommandLineAPI: NotRequired[bool]
    silent: NotRequired[bool]
    contextId: NotRequired[str]
    returnByValue: NotRequired[bool]
    generatePreview: NotRequired[bool]
    userGesture: NotRequired[bool]
    awaitPromise: NotRequired[bool]
    throwOnSideEffect: NotRequired[bool]
    timeout: NotRequired[float]
    disableBreaks: NotRequired[bool]
    replMode: NotRequired[bool]
    allowUnsafeEvalBlockedByCSP: NotRequired[bool]
    uniqueContextId: NotRequired[str]
    serializationOptions: NotRequired[SerializationOptions]


class GetPropertiesParams(CommandParams):
    objectId: str
    ownProperties: NotRequired[bool]
    accessorPropertiesOnly: NotRequired[bool]
    generatePreview: NotRequired[bool]
    nonIndexedPropertiesOnly: NotRequired[bool]


class GlobalLexicalScopeNamesParams(CommandParams):
    executionContextId: NotRequired[str]


class QueryObjectsParams(CommandParams):
    prototypeObjectId: str
    objectGroup: NotRequired[str]


class ReleaseObjectParams(CommandParams):
    objectId: str


class ReleaseObjectGroupParams(CommandParams):
    objectGroup: str


class RemoveBindingParams(CommandParams):
    name: str


class RunScriptParams(CommandParams):
    scriptId: str
    executionContextId: NotRequired[str]
    objectGroup: NotRequired[str]
    silent: NotRequired[bool]
    includeCommandLineAPI: NotRequired[bool]
    returnByValue: NotRequired[bool]
    generatePreview: NotRequired[bool]
    awaitPromise: NotRequired[bool]


class SetAsyncCallStackDepthParams(CommandParams):
    maxDepth: int


class GetExceptionDetailsParams(CommandParams):
    errorObjectId: str


class SetCustomObjectFormatterEnabledParams(CommandParams):
    enabled: bool


class SetMaxCallStackSizeToCaptureParams(CommandParams):
    size: int
