## \file /src/suppliers/suppliers_list/chat_gpt/converstions_parser.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.chat_gpt.converstions_parser
    :platform: Windows, Unix
    :synopsis: Module for parsing ChatGPT conversation HTML files.

ChatGPT Conversation Parser
=========================================================================================

This module provides functionality to parse HTML files containing ChatGPT conversations,
extracting individual conversation blocks.

Example usage
-------------

```python
    from pathlib import Path
    from src.suppliers.suppliers_list.chat_gpt.converstions_parser import extract_conversations_from_html
    from src import gs # Assuming gs is configured to point to your project root

    # Example usage
    file_path = Path(gs.path.data / 'chat_gpt'  / 'chat.html')
    for conversation in extract_conversations_from_html(file_path):
        print(conversation.prettify())  # Print the content of each found conversation
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/chat_gpt/converstions_parser.py
"""

import header
from src import gs

from pathlib import Path
from bs4 import BeautifulSoup

def extract_conversations_from_html(file_path: Path):
    """Generator that reads one .html file and extracts all <div class="conversation"> elements.

    Args:
        file_path (Path): The path to the .html file.

    Yields:
        BeautifulSoup.Tag: Each found conversation div.
    """
    # Open the file and parse its content
    with file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Find all <div class="conversation">
        conversations = soup.find_all('div', class_='conversation')
        # Yield each found conversation
        for conversation in conversations:
            yield conversation

# Example usage
file_path = Path(gs.path.data / 'chat_gpt'  / 'chat.html')
for conversation in extract_conversations_from_html(file_path):
    print(conversation.prettify())  # Print the content of each found conversation
