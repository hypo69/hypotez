# JsApi Module

## Overview

The `JsApi` module defines a class that acts as an interface between the server-side Python code and the client-side JavaScript code in the GPT4Free GUI application. It handles communication between the two components, allowing the JavaScript front-end to interact with the server's functionality, including:

- Managing conversations with AI models
- Selecting and uploading images
- Capturing images from the camera
- Retrieving available models and providers

## Details

The `JsApi` class inherits from the `Api` class and extends its functionality with methods specific to the GUI application. 

## Classes

### `class JsApi`

**Description**: The `JsApi` class represents an interface for the client-side JavaScript code. It handles communication between the server-side Python code and the client-side JavaScript code in the GPT4Free GUI application, allowing the JavaScript front-end to interact with the server's functionality.

**Inherits**: `Api`

**Methods**:

- `get_conversation(self, options: dict, message_id: str = None, scroll: bool = None) -> Iterator`: This method handles the sending of messages to the AI model and retrieves the response. It allows the client-side to interact with the server-side conversation logic.
    - **Purpose**:  This method handles the sending of messages to the AI model and retrieves the response. It allows the client-side to interact with the server-side conversation logic.
    - **Parameters**:
        - `options (dict)`: A dictionary containing options for the conversation.
        - `message_id (str, optional)`: The ID of the message being sent. Defaults to None.
        - `scroll (bool, optional)`:  Whether to scroll to the bottom of the conversation after the message is added. Defaults to None.
    - **Returns**: `Iterator`: An iterator that yields responses from the AI model.
- `choose_image()`: This method opens a file dialog for the user to select an image file.
    - **Purpose**:  This method opens a file dialog for the user to select an image file.
- `take_picture()`: This method triggers the camera to capture a picture and saves it to the user's picture directory.
    - **Purpose**:  This method triggers the camera to capture a picture and saves it to the user's picture directory.
- `on_image_selection(self, filename)`: This method handles the selection of an image from the file dialog.
    - **Purpose**: This method handles the selection of an image from the file dialog.
    - **Parameters**:
        - `filename (str)`: The path to the selected image file.
- `on_camera(self, filename)`: This method handles the capture of an image from the camera.
    - **Purpose**:  This method handles the capture of an image from the camera.
    - **Parameters**:
        - `filename (str)`: The path to the captured image file.
- `set_selected(self, input_id: str = None)`: This method updates the selected input element (image or camera) in the GUI.
    - **Purpose**:  This method updates the selected input element (image or camera) in the GUI.
    - **Parameters**:
        - `input_id (str, optional)`: The ID of the input element to select. Defaults to None.
- `get_version()`: This method retrieves the current version of the GPT4Free server.
    - **Purpose**: This method retrieves the current version of the GPT4Free server.
- `get_models()`: This method retrieves a list of available AI models.
    - **Purpose**:  This method retrieves a list of available AI models.
- `get_providers()`: This method retrieves a list of available AI model providers.
    - **Purpose**: This method retrieves a list of available AI model providers.
- `get_provider_models(self, provider: str, **kwargs)`: This method retrieves a list of AI models supported by a specific provider.
    - **Purpose**:  This method retrieves a list of AI models supported by a specific provider.
    - **Parameters**:
        - `provider (str)`: The name of the provider.

## Inner Functions

None

## How the JsApi Class Works

The `JsApi` class functions as a communication bridge between the client-side JavaScript code and the server-side Python code. It provides methods for interacting with AI models, handling image input, and managing user interface elements.  

## Examples

### Creating a `JsApi` instance:

```python
from hypotez.src.endpoints.gpt4free.g4f.gui.server.js_api import JsApi

js_api = JsApi()
```

### Sending a message to an AI model:

```python
# Example of sending a message with some options
options = {"provider": "openai", "model": "gpt-3.5-turbo"}
messages = js_api.get_conversation(options, message_id="1234", scroll=True)

# Iterate over responses from the AI model
for message in messages:
    print(message)
```

### Selecting an image:

```python
js_api.choose_image()
```

### Capturing a picture from the camera:

```python
js_api.take_picture()
```

### Retrieving available AI models:

```python
models = js_api.get_models()
print(models)
```

### Retrieving available providers:

```python
providers = js_api.get_providers()
print(providers)
```

### Retrieving AI models for a specific provider:

```python
models = js_api.get_provider_models(provider="openai")
print(models)
```