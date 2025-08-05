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
This code block defines a function `gui_parser()` that creates an argument parser for the GPT4Free GUI application. It defines various command-line arguments that can be used to customize the GUI's behavior.

Execution Steps
-------------------------
1. The function creates an `ArgumentParser` object with a description "Run the GUI."
2. It defines the following arguments:
    - `--host`: The hostname to listen on (default: "0.0.0.0").
    - `--port`: The port to listen on (default: 8080).
    - `--debug`: Enables debug mode.
    - `--ignore-cookie-files`: Prevents the GUI from reading cookie files.
    - `--ignored-providers`: A list of providers to ignore when processing requests.
    - `--cookie-browsers`: A list of browsers to access or retrieve cookies from.
3. The function returns the constructed `ArgumentParser` object.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.gui.gui_parser import gui_parser

    parser = gui_parser()
    args = parser.parse_args()

    # Access the parsed arguments
    host = args.host
    port = args.port
    debug = args.debug
    ignore_cookie_files = args.ignore_cookie_files
    ignored_providers = args.ignored_providers
    cookie_browsers = args.cookie_browsers
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".