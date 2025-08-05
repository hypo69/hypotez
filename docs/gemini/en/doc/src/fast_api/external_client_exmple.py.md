# External RPC Client for Fast API Server

## Overview

This module provides an example of an XML-RPC client for managing a Fast API server from external Python code. It demonstrates how to interact with the server remotely using XML-RPC to perform various tasks, such as starting/stopping the server, adding new routes, and checking its status.

## Details

The `external_client.py` file serves as a demonstration of how to interact with the Fast API server from external code. The `ServerProxy` class from the `xmlrpc.client` library is used to establish a connection with the server. This code leverages the XML-RPC protocol to execute commands remotely, allowing for control of the server's behavior.

## Functions

### `main`

**Purpose**: The main function for managing the Fast API server via RPC from external code. 

**How the Function Works**:
1. **Connect to the RPC server**:  The function establishes a connection to the RPC server using `ServerProxy`. The server URL is specified as an argument (`"http://localhost:9000"`).
2. **Start and Stop Server**: Demonstrates the ability to start and stop the server on a specific port (`8001` in this case).
3. **Add a New Route**: Shows how to dynamically add new routes to the server with their respective HTTP methods.
4. **Check Server Status**: Provides an example of querying the server's status.
5. **Shut down RPC server**: The `shutdown` method of the `rpc_client` is called to cleanly terminate the RPC connection.

**Example**:
```python
def main():
    """Основная функция для управления сервером через RPC из внешнего кода."""
    rpc_client = ServerProxy("http://localhost:9000", allow_none=True)
    
    try:
        # Пример: Запуск сервера на порту 8001
        print("Starting server on port 8001...")
        rpc_client.start_server(8001, "127.0.0.1")
        time.sleep(1)
        
        # Пример: Добавление нового маршрута /test_route
        print("Adding new route /test_route...")
        rpc_client.add_new_route("/test_route", 'lambda: {"message": "Hello from test_route"}\', ["GET"])
        time.sleep(1)

        # Пример: Получение статуса серверов
        print("Getting server status...")
        rpc_client.status_servers()
        time.sleep(1)

       # Пример: Остановка сервера на порту 8001
        print("Stopping server on port 8001...")
        rpc_client.stop_server(8001)
        time.sleep(1)
        
        # Пример: Получение статуса серверов
        print("Getting server status...")
        rpc_client.status_servers()
        time.sleep(1)

    except Exception as ex:
        print(f"An error occurred: {ex}")
    finally:
        print("Shutting down RPC server")
        rpc_client.shutdown()

```

## Parameter Details

- `rpc_client` (`ServerProxy`): An instance of `ServerProxy` that handles communication with the XML-RPC server.
- `8001` (int): The port on which the server is being started or stopped.
- `/test_route` (str): The path of the new route being added.
- `lambda: {"message": "Hello from test_route"}\'` (lambda): A lambda function that defines the response for the `/test_route` endpoint.
- `["GET"]` (list): A list of HTTP methods allowed for the new route.


## Examples

**Example 1**: Starting and stopping the server on port `8001`.
```python
rpc_client.start_server(8001, "127.0.0.1")
time.sleep(1)
rpc_client.stop_server(8001)
```

**Example 2**: Adding a new route `"/test_route"` with GET method.
```python
rpc_client.add_new_route("/test_route", 'lambda: {"message": "Hello from test_route"}\', ["GET"])
```

**Example 3**: Getting the server status.
```python
rpc_client.status_servers()
```