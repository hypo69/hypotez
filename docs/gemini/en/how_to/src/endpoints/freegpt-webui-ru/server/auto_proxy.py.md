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
This code block defines functions for fetching, testing, and managing a list of proxy servers. 

Execution Steps
-------------------------
1. **Fetch Proxies**: The `fetch_proxies()` function retrieves a list of proxy servers from a website called proxyscrape.com.
2. **Test Proxy**: The `test_proxy()` function tests the given proxy server with a specified prompt and timeout. It uses a simple test request to check if the proxy server is working. 
3. **Add Working Proxy**: The `add_working_proxy()` function adds a working proxy server to a global list called `working_proxies`.
4. **Remove Proxy**: The `remove_proxy()` function removes a proxy server from the global `working_proxies` list.
5. **Get Working Proxies**: The `get_working_proxies()` function fetches and tests proxy servers, adding working ones to the `working_proxies` list. It uses multiple threads to speed up the process.
6. **Update Working Proxies**: The `update_working_proxies()` function continuously updates the `working_proxies` list by fetching and testing new proxies every 30 minutes.
7. **Get Random Proxy**: The `get_random_proxy()` function returns a random working proxy server from the `working_proxies` list.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.freegpt-webui-ru.server.auto_proxy import get_random_proxy

# Get a random working proxy server
proxy = get_random_proxy()

# Use the proxy server in your requests
response = requests.get('https://example.com', proxies={'http': proxy})

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".