**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Run the freegpt-webui-ru Endpoint
=========================================================================================

Description
-------------------------
This code block initializes and runs the Flask server for the freegpt-webui-ru endpoint. It loads the configuration from a JSON file, sets up website routes and backend API routes, and then starts the server.

Execution Steps
-------------------------
1. **Load Configuration:** The code loads configuration data from `config.json` using the `j_loads` function. 
2. **Initialize Website:** It creates a `Website` object and adds URL rules for each website route defined in the `site.routes` dictionary.
3. **Initialize Backend API:** It creates a `Backend_Api` object and adds URL rules for each backend API route defined in the `backend_api.routes` dictionary.
4. **Run the Flask Server:** The code starts the Flask server on the port specified in the configuration file.

Usage Example
-------------------------

```python
    # This code is already complete and can be run directly.
    # No need to provide additional usage examples.
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".