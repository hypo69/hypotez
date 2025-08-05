# Dialogflow Integration Module

## Overview

The `dialogflow` submodule provides integration with Dialogflow, a powerful natural language understanding (NLU) platform. It empowers you to create sophisticated conversational AI applications by leveraging Dialogflow's capabilities for intent detection, entity recognition, context management, and platform integrations. 

## Details

The `dialogflow` submodule provides a convenient interface for interacting with Dialogflow API. It simplifies the process of setting up Dialogflow agents and using its core features within your Python projects. 

## Classes

### `Dialogflow`

**Description**: The `Dialogflow` class serves as a primary interface for interacting with Dialogflow API. It provides methods for managing intents, entities, contexts, and other core aspects of conversational AI development.

**Parameters**:

- `project_id` (str): The ID of your Dialogflow project.
- `session_id` (str): A unique session identifier for the current conversation.

**Methods**:

- `detect_intent(text: str) -> Dict[str, Any]`: Detects the user's intent based on the provided text.
    - **Parameters**: 
        - `text` (str): The user's input text.
    - **Returns**: A dictionary containing the detected intent information, including intent name, confidence score, and extracted entities.
- `list_intents() -> List[Dict[str, Any]]`: Retrieves a list of all intents defined in the Dialogflow agent.
    - **Returns**: A list of dictionaries representing each intent, including its display name, training phrases, and responses.
- `create_intent(display_name: str, training_phrases_parts: List[str], message_texts: List[str]) -> Dict[str, Any]`: Creates a new intent in the Dialogflow agent.
    - **Parameters**:
        - `display_name` (str): The display name of the new intent.
        - `training_phrases_parts` (List[str]): A list of phrases used to train the intent.
        - `message_texts` (List[str]): A list of responses associated with the intent.
    - **Returns**: A dictionary representing the newly created intent.
- `delete_intent(intent_id: str) -> None`: Deletes an existing intent from the Dialogflow agent.
    - **Parameters**:
        - `intent_id` (str): The ID of the intent to delete.

## Examples

```python
from src.ai.dialogflow import Dialogflow

# Set your Dialogflow project ID and session ID
project_id = "your-project-id"
session_id = "unique-session-id"

# Initialize Dialogflow client
dialogflow_client = Dialogflow(project_id, session_id)

# Detect intent from user input
intent_response = dialogflow_client.detect_intent("Hello")
print("Detected Intent:", intent_response)

# List existing intents
intents = dialogflow_client.list_intents()
print("List of Intents:", intents)

# Create a new intent
new_intent = dialogflow_client.create_intent(
    display_name="NewIntent",
    training_phrases_parts=["new phrase", "another phrase"],
    message_texts=["This is a new intent"]
)
print("Created Intent:", new_intent)

# Delete an intent (replace "your-intent-id" with a real ID)
# dialogflow_client.delete_intent("your-intent-id")
```