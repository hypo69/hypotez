## \file /src/suppliers/suppliers_list/aliexpress_com/gui/styles.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.gui.styles
    :platform: Windows, Unix
    :synopsis: Common styling functions for AliExpress GUI elements.

AliExpress GUI Styling Utilities
=========================================================================================

This module provides utility functions for applying common styles and layouts to PyQt6 widgets
used in the AliExpress GUI application, such as setting fixed sizes for UI elements.

Example usage
-------------

```python
    from PyQt6 import QtWidgets
    from src.suppliers.suppliers_list.aliexpress_com.gui.styles import set_fixed_size

    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    button = QtWidgets.QPushButton("Click Me")
    set_fixed_size(button, 100, 30)
    layout = QtWidgets.QVBoxLayout(window)
    layout.addWidget(button)
    window.show()
    app.exec()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/aliexpress_com/gui/styles.py
"""




""" Common styling functions for UI elements """

from PyQt6 import QtWidgets

def set_fixed_size(widget: QtWidgets.QWidget, width: int, height: int):
    """ Set a fixed size for a given widget """
    widget.setFixedSize(width, height)
