**Instructions for Generating Code Documentation**

How to Use TinyWordProcessor
=========================================================================================

Description
-------------------------
This code defines a `TinyWordProcessor` class, which is a basic word processing tool for agents. The class allows agents to write documents and export them in different formats (Markdown, JSON, and docx).

Execution Steps
-------------------------
1. **Initialization**: The `TinyWordProcessor` is initialized with optional parameters for `owner`, `exporter`, and `enricher`.
2. **Writing a Document**: The `write_document` method creates a new document with a given title, content, and optional author. It optionally enriches the content using the `enricher` and exports the document in different formats using the `exporter`.
3. **Action Processing**: The `_process_action` method processes incoming actions from the agent. If the action type is `WRITE_DOCUMENT`, it parses the content and uses the `write_document` method to create the document.
4. **Action Definitions**: The `actions_definitions_prompt` method returns a prompt describing the available actions and their required parameters.
5. **Action Constraints**: The `actions_constraints_prompt` method returns a prompt specifying the constraints and guidelines for using the actions.

Usage Example
-------------------------

```python
from tinytroupe.tools import TinyWordProcessor

# Initialize the TinyWordProcessor
word_processor = TinyWordProcessor()

# Write a document
doc_spec = {
    "title": "My Document",
    "content": "This is the content of my document.",
    "author": "John Doe"
}
word_processor.write_document(**doc_spec)

# Process an action
action = {
    'type': 'WRITE_DOCUMENT',
    'content': {
        'title': 'My Other Document',
        'content': 'This is another document.',
        'author': 'Jane Doe'
    }
}
word_processor._process_action(None, action)
```