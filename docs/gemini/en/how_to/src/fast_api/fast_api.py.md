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
This code defines the `FastApiServer` class, which implements a FastAPI server with a singleton pattern. It enables the server to handle incoming requests and define routes using the `add_route` method. The `start` method initiates the server on a specified port, and the `stop` method halts the server. The `add_new_route` method allows adding new routes dynamically to the running server.

Execution Steps
-------------------------
1. The `FastApiServer` class is initialized with the host address and title.
2. The `add_route` method is used to register routes with the FastAPI server.
3. The `start` method initiates a uvicorn server to handle incoming requests.
4. The `stop` method terminates the server on a specific port.
5. The `add_new_route` method dynamically adds new routes to the existing server by importing a module and accessing a function from it.

Usage Example
-------------------------

```python
    # Create a FastAPI server instance
    server = FastApiServer(host="127.0.0.1", title="My FastAPI Server")
    
    # Add a route to the server
    server.add_route("/hello", test_function)  # test_function is defined elsewhere
    
    # Start the server on port 8000
    server.start(port=8000)
    
    # Stop the server on port 8000
    server.stop(port=8000)
    
    # Add a new route dynamically
    server.add_new_route(path="/new_route", module_name="my_module", func_name="my_function")  # my_module and my_function are defined elsewhere
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".