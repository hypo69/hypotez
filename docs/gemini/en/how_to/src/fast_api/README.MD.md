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
This code block provides an overview of the FastAPI server manager project, highlighting its features, requirements, installation process, usage, architecture, dependencies, and license.

Execution Steps
-------------------------
1. **Project Overview:** The code block begins with a description of the project's purpose, which is to provide tools for managing FastAPI servers using both a Python CLI and a PowerShell script.
2. **Feature List:** The block details the various features of the project, such as its singleton pattern, interactive management capabilities, customizable options, asynchronous management, status tracking, collision prevention, interactive menu, port checking, and error handling.
3. **Requirements:** The code block outlines the necessary prerequisites for running the project, including Python version, operating system, and required dependencies for both the Python CLI and the PowerShell script.
4. **Installation Instructions:** The block provides step-by-step instructions on installing the project, including cloning the repository or copying the files, setting up a virtual environment (for Python CLI), installing dependencies, and ensuring `python.exe` is accessible in the `PATH` environment variable (for the PowerShell script).
5. **Usage Section:** The code block provides a comprehensive explanation of how to use both the Python CLI and PowerShell script for server management. It covers the available commands, options, and examples for starting, stopping, viewing server status, and exiting the tools.
6. **Architecture Breakdown:** The block details the project's architecture, outlining the main components such as the `FastApiServer` class, `main.py` (Python CLI), `server_manager.ps1` (PowerShell script), and the relevant dependencies used in each component.
7. **Dependency List:** The block lists the dependencies used in the project, including `python.exe`, `fastapi`, `typer`, `uvicorn`, `pydantic`, and `loguru`.
8. **License Information:** The block concludes with a placeholder for the project's license information.

Usage Example
-------------------------

```python
# Example usage of the Python CLI:
python main.py start --port 8080 # Starts the server on port 8080
python main.py status # Displays the server status
python main.py stop --port 8080 # Stops the server on port 8080

# Example usage of the PowerShell script:
.\server_manager.ps1 # Runs the PowerShell script
# Select option '1' from the menu to start the server
# Select option '2' from the menu to stop the server
# Select option '3' from the menu to stop all servers
# Select option '4' from the menu to view server status
# Select option '5' from the menu to exit
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".