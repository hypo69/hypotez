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
This code snippet defines a function `get_free_port()` that searches for an available port on a specified host within a given range, or starting from a certain port upwards.

Execution Steps
-------------------------
1. The function `get_free_port()` takes two arguments: `host` (the address of the host to check) and `port_range` (optional, specifies a range or list of ranges of ports to search within).
2. If `port_range` is provided:
    - It parses the `port_range` into a list of port ranges.
    - It iterates through each range and checks if any port in that range is available using the `_is_port_in_use()` function.
    - If an available port is found, it returns that port.
    - If no available port is found in any of the specified ranges, it raises a `ValueError`.
3. If `port_range` is not provided:
    - It starts searching for an available port from port 1024 and increments the port number until it finds an available one.
    - If it reaches the maximum port number (65535) without finding an available port, it raises a `ValueError`.

Usage Example
-------------------------

```python
    # Find a free port within the range 3000-3005 on 'localhost'
    free_port = get_free_port('localhost', '3000-3005')
    print(f"Free port found: {free_port}")

    # Find a free port within the ranges [4000-4005, 5000-5010] on 'localhost'
    free_port = get_free_port('localhost', ['4000-4005', [5000, 5010]])
    print(f"Free port found: {free_port}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".