**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
The `JsApi` class provides methods to handle interactions between the GUI and the backend, including:
- Sending conversation requests with optional images.
- Selecting images from the user's file system.
- Taking pictures using the device camera.
- Managing the state of the selected input (image or camera).
- Retrieving version information, available models, and provider-specific models.

Execution Steps
-------------------------
1. **Initialize JsApi:** Create an instance of `JsApi` to access its methods.
2. **Send Conversation Request:** Call `get_conversation()` to send a conversation request. This method handles sending the request, processing the response, and updating the GUI with the messages.
3. **Choose Image:** Call `choose_image()` to allow the user to select an image from their file system.
4. **Take Picture:** Call `take_picture()` to capture an image using the device camera.
5. **Set Selected Input:** Call `set_selected()` to update the GUI with the selected input (image or camera).
6. **Retrieve Version Information:** Call `get_version()` to get the version of the API.
7. **Retrieve Available Models:** Call `get_models()` to get a list of available models.
8. **Retrieve Provider-Specific Models:** Call `get_provider_models()` to get a list of models for a specific provider.

Usage Example
-------------------------

```python
    # Initialize JsApi
    js_api = JsApi()

    # Send a conversation request
    js_api.get_conversation(options={'conversation_id': '123', 'provider': 'gpt-3.5-turbo', 'message': 'Hello, world!'})

    # Allow the user to choose an image
    js_api.choose_image()

    # Take a picture
    js_api.take_picture()

    # Get the version of the API
    version = js_api.get_version()

    # Get a list of available models
    models = js_api.get_models()

    # Get a list of models for the "gpt-3.5-turbo" provider
    provider_models = js_api.get_provider_models(provider='gpt-3.5-turbo')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".