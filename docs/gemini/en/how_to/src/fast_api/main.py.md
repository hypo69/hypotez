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
This code block implements a command-line interface for managing Fast API servers. It provides commands to start, stop, manage routes, and display server status. The code handles user input, parses commands, and executes corresponding actions through the `CommandHandler` class.

Execution Steps
-------------------------
1. The code starts by displaying a menu of available commands.
2. It takes user input and parses the command line into parts.
3. It identifies the command and executes the corresponding action, such as:
    - Starting a server on a specified port.
    - Stopping a server on a specified port.
    - Displaying server status.
    - Adding new routes to the server.
    - Shutting down all servers and exiting the program.
4. The code handles invalid input and unexpected errors gracefully.
5. The `main` function initiates the command loop and manages the server operations.


Usage Example
-------------------------

```python
    # Start a server on port 8000:
    Enter command: start 8000

    # Display the status of all servers:
    Enter command: status

    # Stop a server on port 8000:
    Enter command: stop 8000

    # Add a new route to the server:
    Enter command: add_route /new_route
    # Enter HTTP methods (comma-separated, default: GET): GET, POST
    # Example route with GET and POST methods added to /new_route path
    Enter command: shutdown 
    # Exit the program.
    Enter command: exit 

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".