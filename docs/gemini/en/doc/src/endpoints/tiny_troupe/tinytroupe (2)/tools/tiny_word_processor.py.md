# Tiny Word Processor

## Overview

This module provides the `TinyWordProcessor` class, a basic word processing tool that allows agents to write documents.  The class integrates with `TinyTool` to facilitate document creation and enrichment.

## Details

The `TinyWordProcessor` class enables agents to generate documents using a streamlined process. It handles document creation, enrichment, and export to various formats. The class uses a JSON-based format to specify document details and employs the `TinyTool` framework for consistent operation.

## Classes

### `TinyWordProcessor`

**Description**: A basic word processor tool that allows agents to write documents.

**Inherits**: `TinyTool`

**Attributes**: 
- `owner`:  (Optional[str]) - The owner of the tool. 
- `exporter`:  (Optional[str]) - The exporter used for saving artifacts.
- `enricher`: (Optional[str]) - The enricher used for enhancing the document content.

**Methods**: 
- `write_document(title: str, content: str, author: str = None) -> None`:  Creates a new document.

- `_process_action(agent: Any, action: dict) -> bool`: Processes an agent's action to write a document.

- `actions_definitions_prompt() -> str`: Provides a prompt describing the available actions.

- `actions_constraints_prompt() -> str`: Provides a prompt detailing the constraints related to actions.

## Class Methods

### `write_document(title: str, content: str, author: str = None) -> None`:

**Purpose**: Creates a new document with the specified title, content, and optional author. 

**Parameters**:
- `title` (str):  The title of the document.
- `content` (str): The content of the document.
- `author` (Optional[str]): The author of the document. Defaults to `None`.

**How the Function Works**:

1.  The function logs a debug message indicating the start of document creation.
2.  If an enricher is configured, the function enriches the content using the `enrich_content` method of the enricher.
3.  The function exports the document in various formats (Markdown, Docx, JSON) using the configured exporter. 
4.  The function creates a JSON representation of the document and also exports it using the exporter.

**Examples**:

```python
# Example 1: Create a document with a title and content
word_processor = TinyWordProcessor()
word_processor.write_document(title="My Document", content="This is the content of my document.")

# Example 2: Create a document with a title, content, and author
word_processor.write_document(title="My Document", content="This is the content of my document.", author="John Doe")
```

### `_process_action(agent: Any, action: dict) -> bool`:

**Purpose**: Processes an agent's action to write a document.

**Parameters**:
- `agent` (Any): The agent requesting the action.
- `action` (dict): The action to be processed.  Must contain the 'type' and 'content' keys.

**How the Function Works**:

1.  The function checks if the action type is `WRITE_DOCUMENT`.
2.  If it is, the function parses the JSON content from the action.
3.  The function verifies if the JSON content contains valid keys (`title`, `content`, `author`).
4.  The function uses the extracted information to call the `write_document` method to create the document.

**Returns**: 
- `bool`: Returns `True` if the action is processed successfully, otherwise `False`.

**Raises Exceptions**: 
- `json.JSONDecodeError`: If an error occurs while parsing the JSON content.
- `Exception`: If any other error occurs during action processing.

**Examples**:

```python
# Example 1: Process a WRITE_DOCUMENT action with valid JSON content
agent = ...  # An agent object
action = {"type": "WRITE_DOCUMENT", "content": {"title": "My Document", "content": "This is the content of my document."}}
word_processor = TinyWordProcessor()
result = word_processor._process_action(agent, action)  # result will be True

# Example 2: Process a WRITE_DOCUMENT action with invalid JSON content
agent = ...  # An agent object
action = {"type": "WRITE_DOCUMENT", "content": "Invalid JSON content"}
word_processor = TinyWordProcessor()
result = word_processor._process_action(agent, action)  # result will be False
```

### `actions_definitions_prompt() -> str`:

**Purpose**: Provides a prompt describing the available actions.

**Returns**:
- `str`: A formatted string with a description of the available actions and their expected input format.

**Examples**:
```python
word_processor = TinyWordProcessor()
prompt = word_processor.actions_definitions_prompt()
print(prompt)
```

### `actions_constraints_prompt() -> str`:

**Purpose**: Provides a prompt detailing the constraints related to actions.

**Returns**:
- `str`: A formatted string with constraints for the actions.

**Examples**:

```python
word_processor = TinyWordProcessor()
prompt = word_processor.actions_constraints_prompt()
print(prompt)
```

## Parameter Details

- `owner` (Optional[str]):  The owner of the tool. Defaults to `None`. 
- `exporter` (Optional[str]): The exporter used for saving artifacts. Defaults to `None`.
- `enricher` (Optional[str]): The enricher used for enhancing the document content. Defaults to `None`.
- `title` (str): The title of the document.
- `content` (str): The content of the document.
- `author` (Optional[str]): The author of the document. Defaults to `None`. 
- `agent` (Any): The agent requesting the action.
- `action` (dict): The action to be processed.  Must contain the 'type' and 'content' keys.

## Examples

```python
# Example 1: Creating a TinyWordProcessor instance with an exporter and enricher
from tinytroupe.tools.tiny_exporter import TinyExporter
from tinytroupe.tools.tiny_enricher import TinyEnricher

exporter = TinyExporter(target_dir="./")  # Creating an exporter instance
enricher = TinyEnricher(model_name="text-davinci-003")  # Creating an enricher instance

word_processor = TinyWordProcessor(exporter=exporter, enricher=enricher)

# Example 2: Writing a document using the TinyWordProcessor instance
title = "My Document"
content = "This is the content of my document."
word_processor.write_document(title=title, content=content, author="John Doe")

# Example 3: Processing an agent action to write a document
agent = ...  # An agent object
action = {"type": "WRITE_DOCUMENT", "content": {"title": "My Document", "content": "This is the content of my document."}}
result = word_processor._process_action(agent, action)
```