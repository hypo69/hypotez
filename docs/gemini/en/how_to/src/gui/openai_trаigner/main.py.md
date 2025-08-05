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
The code block defines a `AssistantMainWindow` class, which represents the main window of an assistant application. This window integrates a web browser, provides a URL bar, and offers functionalities like minimizing to the system tray, going fullscreen, and closing the window.

Execution Steps
-------------------------
1. The class inherits from `QMainWindow` and overrides the `__init__` method to initialize the window's properties.
2. The window is set to a specific size and location, and the user is prompted to select their default browser.
3. A browser profile is created based on the selected browser, and a `QWebEngineView` is added to the window to display the web content.
4. A title bar is created with input fields for URL, a button to load the URL, and buttons for minimizing, maximizing, and closing the window.
5. A system tray icon is created with a context menu to restore the window or quit the application.
6. Menus are created for selecting frequently used services from Google and choosing different AI models.
7. The `load_url` method handles loading a URL into the browser.
8. The `hide_to_tray` method minimizes the window to the system tray.
9. The `quit_app` method closes the application.
10. The `closeEvent` method intercepts the window close event and minimizes the window to the system tray instead of closing it.

Usage Example
-------------------------

```python
from src.gui.openai_trаigner.main import AssistantMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = AssistantMainWindow()
    window.show()

    sys.exit(app.exec())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".