# Module for working with ChatGPT data
## Overview

The `ChatGpt` module is responsible for processing and managing data related to ChatGPT conversations. It utilizes the `src.gs` module for accessing global settings and the `src.utils.file` module for reading files recursively.

## Details

This module provides a class named `ChatGpt` that handles the process of extracting HTML files representing ChatGPT conversations from a designated directory. 

## Classes

### `ChatGpt`

**Description**: This class provides methods for managing and accessing ChatGPT conversation data.

**Attributes**: None

**Methods**:

- `yeld_conversations_htmls()`:  This method iterates through a directory containing HTML files representing ChatGPT conversations and yields the content of each file.

## Class Methods

### `yeld_conversations_htmls()`

```python
    def yeld_conversations_htmls(self) -> str:
        """"""
        ...
        conversation_directory = Path(gs.path.data / 'chat_gpt' / 'conversations')
        html_files = conversation_directory.glob("*.html")

```

**Purpose**: This method iterates through a directory containing HTML files representing ChatGPT conversations and yields the content of each file.

**Parameters**: None

**Returns**: 
- `str`: The content of an HTML file representing a ChatGPT conversation.

**Raises Exceptions**: 
-  `Exception`: If an error occurs during the file reading process.

**How the Function Works**:
- The function first identifies the directory containing HTML files representing ChatGPT conversations using the `gs.path.data` variable from the `src.gs` module.
- It then iterates through the HTML files using the `glob` function and yields the content of each file.

**Examples**:
```python
from src.suppliers.chat_gpt import ChatGpt
from src.gs import path

# Create a ChatGpt object
chatgpt = ChatGpt()

# Iterate through the HTML files and print their content
for conversation_html in chatgpt.yeld_conversations_htmls():
    print(conversation_html)
```