## \file hypotez/src/llm/dialogflow/README.MD
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module::  src.llm.dialogflow
:platform: Windows, Unix
:synopsis: Dialogflow integration module.

This module provides integration with Dialogflow, a natural language understanding (NLU) platform.
It allows you to create conversational AI applications by leveraging Dialogflow's capabilities for intent detection,
entity recognition, context management, and integrations with various platforms.

The **dialogflow** submodule offers the following features:

- **Intent Detection:** Determines user intents based on the input text.
- **Entity Recognition:** Extracts key data from user phrases.
- **Contexts:** Manages the conversation by retaining information about the current state of the dialogue.
- **Integrations:** Supports integration with various platforms such as Google Assistant, Facebook Messenger, Slack, Telegram, and others.
- **Webhook:** Supports Webhook integrations for calling external services and APIs.


**About Dialogflow**
===============================================================
For more information about Dialogflow, refer to the official documentation:
https://dialogflow.com/docs/getting-started/basics

**Example Usage**
===============================================================

```python
from src.llm.dialogflow import Dialogflow

project_id = "your-project-id"  # Replace with your Dialogflow project ID
session_id = "unique-session-id"  # Replace with a unique session ID for your user

dialogflow_client = Dialogflow(project_id, session_id)

# Example usage of methods
intent_response = dialogflow_client.detect_intent("Hello")
print("Detected Intent:", intent_response)

intents = dialogflow_client.list_intents()
print("List of Intents:", intents)

new_intent = dialogflow_client.create_intent(
    display_name="NewIntent",
    training_phrases_parts=["new phrase", "another phrase"],
    message_texts=["This is a new intent"]
)
print("Created Intent:", new_intent)

# Deleting an intent (make sure to replace intent_id with a real ID)
# dialogflow_client.delete_intent("your-intent-id")
```

**How to use this module**
===============================================================

**Description**
-------------------------
This module provides an interface to interact with Dialogflow's API for creating and managing conversational AI applications. It handles the communication with Dialogflow's services, allowing you to perform tasks like:

- Detect user intents from text input
- Extract entities from user phrases
- Manage conversation contexts
- Create, list, and delete intents
- Integrate with various platforms
- Implement webhook functionality

**Steps**
-------------------------
1. **Create a Dialogflow project**
   - Go to the Dialogflow console: https://dialogflow.com/
   - Create a new project.
   - Get your project ID from the project settings.
2. **Initialize the Dialogflow client**
   - Import the `Dialogflow` class from the `src.llm.dialogflow` module.
   - Create an instance of the `Dialogflow` client, providing your project ID and a unique session ID for your user.
3. **Use the provided methods**
   - The `Dialogflow` client provides methods for performing various Dialogflow operations:
     - `detect_intent(text)`: Detects the user's intent based on the provided text.
     - `list_intents()`: Retrieves a list of all intents in your Dialogflow project.
     - `create_intent(display_name, training_phrases_parts, message_texts)`: Creates a new intent with the given information.
     - `delete_intent(intent_id)`: Deletes the intent with the specified ID.
     - And more...

**Example Usage**
-------------------------

```python
from src.llm.dialogflow import Dialogflow

# Replace with your project ID and session ID
project_id = "your-project-id"
session_id = "unique-session-id"

# Initialize the Dialogflow client
dialogflow_client = Dialogflow(project_id, session_id)

# Detect intent from user input
text = "Hello"
intent_response = dialogflow_client.detect_intent(text)
print("Detected Intent:", intent_response)
```

**Further Information**
===============================================================

Refer to the Dialogflow documentation for a comprehensive overview of its features and API:

https://dialogflow.com/docs/

**Contribution**
===============================================================

Contributions are welcome! Feel free to open an issue or submit a pull request.
"""