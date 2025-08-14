## \file /src/suppliers/suppliers_list/chat_gpt/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.chat_gpt
    :platform: Windows, Unix
    :synopsis: Initialization file for ChatGPT supplier-specific functionalities.

ChatGPT Supplier Initialization
=========================================================================================

This module serves as the initialization file for the ChatGPT supplier package.
It defines the package structure and imports key components like `GptGs`.

Example usage
-------------

```python
    # No direct example usage for __init__.py, as it defines the package.
    # Components within this package would be imported and used as follows:
    # from src.suppliers.suppliers_list.chat_gpt.gsheet import GptGs
    # gpt_gs_instance = GptGs() # Example initialization
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/chat_gpt/__init__.py
"""


from .gsheet import GptGs