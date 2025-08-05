# Hypotez Fast API Main Module

## Overview

This module (`hypotez/src/fast_api/main.py`) is responsible for managing and interacting with a Fast API server. It provides a command-line interface to start, stop, configure, and manage the server.

## Details

This module acts as a central control point for the Fast API server. It allows users to interact with the server using a set of commands. It handles tasks like:

- Starting and stopping the server on specific ports.
- Checking the status of all running servers.
- Listing all registered routes.
- Adding new routes to the server.
- Shutting down all servers and exiting the application.

## Functions

### `display_menu()`

**Purpose**: This function displays a menu of available commands for the Fast API server.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**: The function prints a list of available commands to the console.

**Examples**:

```python
>>> display_menu()
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
```

### `main()`

**Purpose**: This function is the main entry point for the Fast API server management application. It handles user input and executes commands related to the server.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. **Initialization**: It creates an instance of `CommandHandler` to handle server operations.
2. **Loop**: It enters an infinite loop that continues until the user enters a command to exit the application.
3. **Input**: Inside the loop, it prompts the user to enter a command.
4. **Command Parsing**: It parses the command line input, extracting the command and any associated parameters.
5. **Command Handling**: Depending on the command, it calls the appropriate methods from `CommandHandler`.
6. **Error Handling**: It catches and logs any exceptions that might occur during command execution.
7. **Exit**: It exits the loop and terminates the application when the user enters the "shutdown" or "exit" commands.

**Inner Functions**: None

**Examples**:

```python
>>> main()
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: start 8000
Enter host address (default: 127.0.0.1): 
Server started on port 8000
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: status
Server on port 8000 is running
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: shutdown
Shutting down all servers.
```

## Parameter Details

- **port**: An integer representing the port number on which the server should be started or stopped.
- **host**: A string representing the hostname or IP address of the server.

## Examples

```python
>>> main()
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: start 8000
Enter host address (default: 127.0.0.1): 192.168.1.100
Server started on port 8000 with host 192.168.1.100
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: add_route /test
Enter HTTP methods (comma-separated, default: GET): GET,POST
Route added: /test with methods GET, POST
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: routes
Registered routes:
/test : GET, POST
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: stop 8000
Server stopped on port 8000
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
Enter command: exit
Exiting the program.
```