## \file /src/suppliers/suppliers_list/chat_gpt/chat_gpt.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.chat_gpt.chat_gpt
    :platform: Windows, Unix
    :synopsis: Module for interacting with ChatGPT data and conversations.

ChatGPT Data Interaction Module
=========================================================================================

This module provides functionalities for interacting with ChatGPT-related data,
such as yielding HTML conversation files.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.chat_gpt.chat_gpt import ChatGpt

    chat_gpt_instance = ChatGpt()
    for html_content in chat_gpt_instance.yeld_conversations_htmls():
        print(f"Processing HTML content: {html_content[:50]}...")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/chat_gpt/chat_gpt.py
"""

import header
from pathlib import Path
from src import gs
from src.utils.file import recursively_read_text_files
class ChatGpt:

    def yeld_conversations_htmls(self) -> str:
        """Yields HTML content of ChatGPT conversation files.

        This method iterates through HTML files located in the 'chat_gpt/conversations'
        directory within the project's data path and yields their content.

        Yields:
            str: The content of an HTML conversation file.
        """
        conversation_directory = Path(gs.path.data / 'chat_gpt' / 'conversations')
        html_files = conversation_directory.glob("*.html")

        for html_file in html_files:
            yield html_file.read_text()

