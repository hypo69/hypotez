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
This code block demonstrates how to interact with a Fast API server through an XML-RPC client. It utilizes the `xmlrpc.client` module to establish a connection with the server and then performs various actions like starting and stopping servers, adding new routes, and retrieving server status.

Execution Steps
-------------------------
1. **Create an XML-RPC Client**: The code establishes a connection to the Fast API server running on `http://localhost:9000` using `ServerProxy`. The `allow_none=True` parameter ensures that the client can handle `None` values.
2. **Start Server**: The `start_server()` method is called to start the server on a specified port (8001 in this example). The port and host address are provided as arguments.
3. **Add New Route**: The `add_new_route()` method adds a new route to the server. It takes the route path, the function to be executed for the route, and a list of allowed HTTP methods as arguments. In this case, it adds a route `/test_route` that returns a JSON response containing the message "Hello from test_route" when accessed using a GET request.
4. **Get Server Status**: The `status_servers()` method retrieves the status of all running servers.
5. **Stop Server**: The `stop_server()` method stops the server running on the specified port.
6. **Shutdown RPC Server**: The `shutdown()` method terminates the XML-RPC client connection.

Usage Example
-------------------------

```python
from xmlrpc.client import ServerProxy
import time

# Create an XML-RPC client
rpc_client = ServerProxy("http://localhost:9000", allow_none=True)

# Start the server on port 8001
print("Starting server on port 8001...")
rpc_client.start_server(8001, "127.0.0.1")
time.sleep(1)

# Add a new route '/test_route'
print("Adding new route /test_route...")
rpc_client.add_new_route("/test_route", 'lambda: {"message": "Hello from test_route"}\', ["GET"])
time.sleep(1)

# Get the server status
print("Getting server status...")
rpc_client.status_servers()
time.sleep(1)

# Stop the server on port 8001
print("Stopping server on port 8001...")
rpc_client.stop_server(8001)
time.sleep(1)

# Get the server status again
print("Getting server status...")
rpc_client.status_servers()
time.sleep(1)

# Shutdown the RPC server
print("Shutting down RPC server")
rpc_client.shutdown()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".