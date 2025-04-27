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
This code defines the command-line interface (CLI) for the GPT4Free application. It sets up the command-line arguments for running the API, GUI, and other functionalities.

Execution Steps
-------------------------
1. **Defines CLI Structure:** The code creates an `ArgumentParser` object to manage command-line arguments.
2. **Adds Subparsers:** Subparsers are added to allow for different modes of operation, such as 'api' and 'gui'.
3. **Adds API Arguments:** `get_api_parser` function defines arguments specifically for running the API, including `bind`, `port`, `debug`, `model`, `provider`, `workers`, `proxy`, etc.
4. **Adds GUI Arguments:**  `gui_parser` (defined in `g4f.gui.run`) is used to define arguments for the GUI.
5. **Parses Arguments:** The code parses the user-provided command-line arguments.
6. **Executes Based on Mode:** It calls different functions (e.g., `run_api_args`, `run_gui_args`) based on the specified 'mode' (API or GUI).
7. **Runs API:** `run_api_args` configures the API application based on the parsed arguments and launches the API server.

Usage Example
-------------------------

```python
# Run the API with default settings
python -m g4f api

# Run the API with custom port and debug enabled
python -m g4f api -p 5000 -d

# Run the API with a specific provider
python -m g4f api --provider OpenAI

# Run the GUI
python -m g4f gui
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".