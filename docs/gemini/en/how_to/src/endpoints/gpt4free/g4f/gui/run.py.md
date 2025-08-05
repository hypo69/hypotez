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
This code block runs the GPT4Free GUI, handling arguments, cookie loading, debug mode, and ignored providers.

Execution Steps
-------------------------
1. **Imports**: Import necessary modules for GUI parsing, cookie management, running the GUI, and interacting with providers.
2. **Run GUI Arguments Handling**:
    - **Debug Mode**: If the `debug` argument is provided, enable debug logging.
    - **Cookie Loading**: If `ignore_cookie_files` is not provided, read cookie files from the system.
    - **Browser Configuration**: Configure the browsers to be used by reading the `cookie_browsers` argument.
    - **Ignored Providers**: If `ignored_providers` is provided, mark the corresponding providers as inactive.
3. **Start the GUI**: Run the GUI using the `run_gui` function, passing the host, port, and debug settings.
4. **Main Execution**:
    - **Parse Arguments**: Use `gui_parser` to parse command-line arguments.
    - **Run GUI with Arguments**: Call `run_gui_args` to execute the GUI with the parsed arguments.

Usage Example
-------------------------

```python
    python src/endpoints/gpt4free/g4f/gui/run.py --host localhost --port 5000 --debug --cookie_browsers chrome firefox --ignored_providers bing google
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".