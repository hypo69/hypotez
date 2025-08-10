## \file src/webdriver/pydoll/llib/protocol/dom/types.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module defines types related to DOM operations in the Chrome DevTools Protocol.
=================================================================================

This module contains `TypedDict` definitions for various DOM-related types,
such as `Node`, `Rect`, `BoxModel`, and `EventFileChooserOpened`.
These types are used to represent information about DOM elements, their geometry,
and events related to file choosers.

Example usage
-------------

```python
    from src.webdriver.pydoll.llib.protocol.dom.types import Node, Rect

    # Example of a Node object
    node: Node = {
        "nodeId": 1,
        "backendNodeId": 101,
        "nodeType": 1,
        "nodeName": "DIV",
        "localName": "div",
        "nodeValue": "",
    }

    # Example of a Rect object
    rect: Rect = {"x": 10, "y": 20, "width": 100, "height": 50}
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/protocol/dom/types.py
"""

from typing import Annotated, Any

from typing_extensions import NotRequired, TypedDict

from src.webdriver.pydoll.llib.constants import CompatibilityMode, PseudoType, ShadowRootType

Quad = Annotated[list[float], 'Format: [x1, y1, x2, y2, x3, y3, x4, y4]']


class Rect(TypedDict):
    """Rectangle for capturing screenshot or clip rectangle."""

    x: float
    y: float
    width: float
    height: float


class CSSComputedStyleProperty(TypedDict):
    name: str
    value: str


class BackendNode(TypedDict):
    nodeType: int
    nodeName: str
    backendNodeId: int


class Node(TypedDict):
    nodeId: int
    parentId: NotRequired[int]
    backendNodeId: int
    nodeType: int
    nodeName: str
    localName: str
    nodeValue: str
    childNodeCount: NotRequired[int]
    children: NotRequired[list['Node']]
    attributes: NotRequired[list[str]]
    documentURL: NotRequired[str]
    baseURL: NotRequired[str]
    publicId: NotRequired[str]
    systemId: NotRequired[str]
    internalSubset: NotRequired[str]
    xmlVersion: NotRequired[str]
    name: NotRequired[str]
    value: NotRequired[str]
    pseudoType: NotRequired[PseudoType]
    pseudoIdentifier: NotRequired[str]
    shadowRootType: NotRequired[ShadowRootType]
    frameId: NotRequired[str]
    contentDocument: NotRequired['Node']
    shadowRoots: NotRequired[list['Node']]
    templateContent: NotRequired['Node']
    pseudoElements: NotRequired[list['Node']]
    importedDocument: NotRequired['Node']
    distributedNodes: NotRequired[list[BackendNode]]
    isSVG: NotRequired[bool]
    compatibilityMode: NotRequired[CompatibilityMode]
    assignedSlot: NotRequired[BackendNode]
    isScrollable: NotRequired[bool]


class DetachedElementInfo(TypedDict):
    treeNode: Node
    retainedNodeIds: list[int]


class ShapeOutsideInfo(TypedDict):
    bounds: Quad
    shape: list[Any]
    marginShape: list[Any]


class BoxModel(TypedDict):
    content: Quad
    padding: Quad
    border: Quad
    margin: Quad
    width: int
    height: int
    shapeOutside: NotRequired[ShapeOutsideInfo]


class EventFileChooserOpenedParams(TypedDict):
    frameId: str
    mode: str
    backendNodeId: int


class EventFileChooserOpened(TypedDict):
    method: str
    params: EventFileChooserOpenedParams
