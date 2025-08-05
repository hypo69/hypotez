# FastAPI Server with XML-RPC Interface for Remote Control

## Overview

This module provides a FastAPI server with an XML-RPC interface for remote control. It allows you to manage the server and its routes, including starting and stopping servers on different ports, adding new routes, and querying server status and routes.

## Details

The module utilizes the `uvicorn` library to run the FastAPI server and `SimpleXMLRPCServer` for the XML-RPC interface. The `j_loads_ns` function from the `src.utils.jjson` module is used to load configuration from a JSON file.

### Configuration

The server configuration is read from the `fast_api.json` file located in the `src/fast_api` directory. It specifies settings like the server host and port.

### Usage

You can use this module to manage the FastAPI server through the following commands:

- **start <port>**: Start the server on the specified port.
- **status**: Show the status of all served ports.
- **routes**: Show all registered routes.
- **stop <port>**: Stop the server on the specified port.
- **stop_all**: Stop all running servers.
- **add_route <path> <module_name> <func_name>**: Add a new route to the server.
- **shutdown**: Stop all servers and exit.
- **help**: Show this help menu.
- **exit**: Exit the program.

## Classes

### `FastApiServer`

**Description**: This class represents the FastAPI server and provides methods for managing its routes and server instances.

**Inherits**: `object`

**Attributes**:

- `_instance` (Any): Singleton instance of the server.
- `app` (FastAPI): The FastAPI application instance.
- `host` (str): The server host address.
- `port` (int): The server port.
- `router` (APIRouter): The FastAPI router instance.
- `server_tasks` (dict): A dictionary to store server tasks.
- `servers` (dict): A dictionary to store server instances.

**Methods**:

- `__new__(cls, *args, **kwargs)`:  Initializes the singleton instance of the class.
- `__init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs)`:  Initializes the FastAPI server instance with specified settings.
- `add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs)`:  Adds a new route to the FastAPI application.
- `_start_server(self, port: int)`:  Starts the uvicorn server asynchronously on the specified port.
- `start(self, port: int, as_thread:bool = True)`:  Starts the FastAPI server on the specified port.
- `stop(self, port: int)`:  Stops the FastAPI server on the specified port.
- `stop_all(self)`:  Stops all running servers.
- `get_servers_status(self)`:  Returns the status of all servers.
- `get_routes(self)`:  Returns a list of all registered routes.
- `get_app(self)`:  Returns the FastAPI application instance.
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs)`:  Adds a new route to the running application.

## Functions

### `telegram_webhook()`

**Purpose**: A placeholder function for handling Telegram webhooks.

**Parameters**: None

**Returns**:  `str`: "Hello, World!".

**How the Function Works**:  This function currently simply returns a static message. You can replace it with your actual Telegram webhook handler logic.

**Examples**:

```python
>>> telegram_webhook()
'Hello, World!'
```

### `test_function()`

**Purpose**: A test function that returns a basic message.

**Parameters**: None

**Returns**:  `str`: "It is working!!!".

**How the Function Works**:  This function demonstrates a simple example of a route handler.

**Examples**:

```python
>>> test_function()
'It is working!!!'
```

### `test_post(data: Dict[str, str])`

**Purpose**: A test function for handling POST requests.

**Parameters**:

- `data` (Dict[str, str]):  A dictionary containing the data from the POST request.

**Returns**:  `dict`: A dictionary containing the message "post ok" and the received data.

**How the Function Works**:  This function demonstrates how to handle POST requests and return data.

**Examples**:

```python
>>> test_post({"name": "Alice", "age": 30})
{'result': 'post ok', 'data': {'name': 'Alice', 'age': 30}}
```

### `start_server(port: int, host: str)`

**Purpose**: Starts the FastAPI server on the specified port.

**Parameters**:

- `port` (int): The port to start the server on.
- `host` (str): The host address of the server.

**Returns**: None

**How the Function Works**:  Creates a new instance of the `FastApiServer` class, if not already created, and calls its `start` method to initiate the server.

**Examples**:

```python
>>> start_server(8000, "127.0.0.1")
```

### `stop_server(port: int)`

**Purpose**: Stops the FastAPI server on the specified port.

**Parameters**:

- `port` (int): The port to stop the server on.

**Returns**: None

**How the Function Works**:  Calls the `stop` method of the `FastApiServer` instance to stop the server on the specified port.

**Examples**:

```python
>>> stop_server(8000)
```

### `stop_all_servers()`

**Purpose**: Stops all running FastAPI servers.

**Parameters**: None

**Returns**: None

**How the Function Works**:  Calls the `stop_all` method of the `FastApiServer` instance to stop all running servers.

**Examples**:

```python
>>> stop_all_servers()
```

### `status_servers()`

**Purpose**: Displays the status of all running servers.

**Parameters**: None

**Returns**: None

**How the Function Works**:  Retrieves the status of all servers from the `FastApiServer` instance and prints it to the console.

**Examples**:

```python
>>> status_servers()
Server initialized on host 127.0.0.1
  - Port 8000: Running
  - Port 8001: Stopped
```

### `get_routes()`

**Purpose**: Displays all registered routes.

**Parameters**: None

**Returns**: None

**How the Function Works**:  Retrieves the list of registered routes from the `FastApiServer` instance and prints it to the console.

**Examples**:

```python
>>> get_routes()
Available routes:
  - Path: /hello, Methods: ['GET']
  - Path: /post, Methods: ['POST']
```

### `add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`

**Purpose**: Adds a new route to the running server.

**Parameters**:

- `path` (str): The path of the new route.
- `module_name` (str): The name of the module containing the function to be registered as the route handler.
- `func_name` (str): The name of the function to be registered as the route handler.
- `methods` (List[str], optional): The HTTP methods allowed for this route. Defaults to ["GET"].

**Returns**: None

**How the Function Works**:  Dynamically imports the specified module, retrieves the function by name, and adds it to the `FastApiServer` instance as a route handler.

**Examples**:

```python
>>> add_new_route("/new_route", "my_module", "my_function", methods=["GET", "POST"])
Route added: /new_route, methods=['GET', 'POST']
```

### `parse_port_range(range_str)`

**Purpose**: Parses a string representing a range of ports.

**Parameters**:

- `range_str` (str): The string representing the port range.

**Returns**:  `list`: A list of integers representing the ports in the range.

**How the Function Works**:  Parses the input string to extract the starting and ending ports of the range. It handles both single port values and ranges (e.g., "8000" or "8000-8005").

**Examples**:

```python
>>> parse_port_range("8000")
[8000]

>>> parse_port_range("8000-8005")
[8000, 8001, 8002, 8003, 8004, 8005]

>>> parse_port_range("invalid-range")
[]
```

### `CommandHandler`

**Description**: This class handles commands for the FastAPI server through XML-RPC.

**Inherits**:  `object`

**Attributes**:

- `rpc_port` (int): The port for the XML-RPC server.
- `rpc_server` (SimpleXMLRPCServer): The XML-RPC server instance.

**Methods**:

- `__init__(self, rpc_port=9000)`:  Initializes the command handler with the specified XML-RPC port.
- `start_server(self, port: int, host: str)`:  Calls the `start_server` function to start the FastAPI server.
- `stop_server(self, port: int)`:  Calls the `stop_server` function to stop the FastAPI server.
- `stop_all_servers(self)`:  Calls the `stop_all_servers` function to stop all servers.
- `status_servers(self)`:  Calls the `status_servers` function to display server status.
- `get_routes(self)`:  Calls the `get_routes` function to display registered routes.
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`:  Calls the `add_new_route` function to add a new route.
- `shutdown(self)`:  Stops all servers, shuts down the XML-RPC server, and exits the program.

## Inner Functions

### `display_menu()`

**Purpose**:  Displays the menu of available commands for the FastAPI server.

**Parameters**: None

**Returns**: None

**How the Function Works**:  Prints a list of available commands to the console.

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

**Purpose**: The main function for managing the server.

**Parameters**: None

**Returns**: None

**How the Function Works**:  Initializes a `CommandHandler` instance and enters a loop that continuously prompts the user for commands. It then calls the appropriate methods on the `CommandHandler` based on the user's input.

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
Server started on: 127.0.0.1:8000
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
Server initialized on host 127.0.0.1
  - Port 8000: Running
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
RPC server shutdown
```

## Parameter Details

- `port` (int): The port number for the server or the XML-RPC connection.
- `host` (str): The host address of the server.
- `path` (str): The path of the route.
- `module_name` (str): The name of the module containing the route handler function.
- `func_name` (str): The name of the route handler function.
- `methods` (List[str]): The HTTP methods allowed for the route.
- `range_str` (str): A string representing a range of ports.
- `data` (Dict[str, str]): Data received from a POST request.

## Examples

- **Starting the server:**

```python
>>> start_server(8000, "127.0.0.1")
```

- **Stopping the server on port 8000:**

```python
>>> stop_server(8000)
```

- **Adding a new route:**

```python
>>> add_new_route("/new_route", "my_module", "my_function", methods=["GET", "POST"])
```

- **Displaying server status:**

```python
>>> status_servers()
```

- **Displaying registered routes:**

```python
>>> get_routes()
```

- **Exiting the program:**

```python
>>> shutdown()
```

## Your Behavior During Code Analysis

- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.