# Module for auto-proxy server selection 
====================================================

This module provides functionality for automatically fetching, testing, and selecting working proxy servers from a list. It is designed to improve the reliability and efficiency of web requests by automatically switching between proxy servers when one becomes unresponsive.

## Details

This module is crucial for the `hypotez` project, particularly in scenarios where web requests are frequently made to external services, like OpenAI's API, that require a stable network connection. By employing a dynamic proxy server system, the project can maintain its functionality even if a particular proxy server fails or becomes unavailable.

## Classes

### `fetch_proxies`

**Description**: This function fetches a list of proxy servers from `proxyscrape.com`. It retrieves the list of proxy servers, filters out invalid entries, and returns a list of working proxies in the format "IP:Port".

**Purpose**: To obtain a list of potential proxy servers from a reliable source.

**Parameters**: None

**Returns**:
- `list`: A list of proxy servers in the format "IP:Port".

**Examples**:

```python
proxies = fetch_proxies()
print(f'Proxies: {proxies}') 
```

### `test_proxy`

**Description**: This function tests a given proxy server by sending a request to a specified endpoint with a test prompt. It measures the response time and determines if the proxy server is working within a given timeout.

**Purpose**: To evaluate the performance and availability of a proxy server.

**Parameters**:

- `proxy (str)`: The proxy server in the format "IP:Port".
- `prompt (str)`: The test prompt to be used for testing.
- `timeout (int)`: The maximum time in seconds allowed for the test.

**Returns**: None

**Examples**:

```python
test_proxy(proxy='123.456.789.0:1234', prompt='What is the capital of France?', timeout=5)
```


### `add_working_proxy`

**Description**: This function adds a working proxy server to the global `working_proxies` list. It ensures that the proxy server is appended only if it is deemed functional.

**Purpose**: To maintain a list of known working proxy servers for future use.

**Parameters**:

- `proxy (str)`: The proxy server in the format "IP:Port".

**Returns**: None

**Examples**:

```python
add_working_proxy(proxy='123.456.789.0:1234')
```


### `remove_proxy`

**Description**: This function removes a proxy server from the global `working_proxies` list. It checks if the provided proxy server exists in the list and removes it accordingly.

**Purpose**: To update the `working_proxies` list by removing inactive or unresponsive proxy servers.

**Parameters**:

- `proxy (str)`: The proxy server in the format "IP:Port".

**Returns**: None

**Examples**:

```python
remove_proxy(proxy='123.456.789.0:1234')
```


### `get_working_proxies`

**Description**: This function fetches a list of proxy servers, tests them in parallel using threading, and adds any working proxies to the global `working_proxies` list. It performs a series of requests to test each proxy server against a specified test prompt and timeout, updating the `working_proxies` list based on the results.

**Purpose**: To dynamically discover and maintain a pool of functional proxy servers.

**Parameters**:

- `prompt (str)`: The test prompt to be used for testing.
- `timeout (int, optional)`: The maximum time in seconds allowed for testing. Defaults to 5.

**Returns**: None

**Examples**:

```python
get_working_proxies(prompt='What is the capital of France?', timeout=5)
```


### `update_working_proxies`

**Description**: This function continuously updates the global `working_proxies` list with working proxy servers. It operates in a loop, clearing the `working_proxies` list, fetching and testing proxies, and updating the list every 30 minutes.

**Purpose**: To ensure that the `working_proxies` list remains up-to-date and contains only functional proxy servers.

**Parameters**: None

**Returns**: None

**Examples**:

```python
update_working_proxies()
```

### `get_random_proxy`

**Description**: This function returns a random working proxy server from the global `working_proxies` list. It selects a random element from the `working_proxies` list, ensuring that the chosen proxy server is currently functioning.

**Purpose**: To provide a mechanism for selecting a random working proxy server when making web requests.

**Parameters**: None

**Returns**:
- `str`: A random working proxy server in the format "IP:Port".

**Examples**:

```python
random_proxy = get_random_proxy()
print(f'Random proxy: {random_proxy}') 
```

## Parameter Details
- `prompt (str)`: The test prompt to be used for testing the proxy servers. It is a string containing a question or statement used to assess the responsiveness and functionality of a proxy server.
- `timeout (int)`: The maximum time in seconds allowed for testing a proxy server. It specifies the duration for which a request to the proxy server is attempted.
- `proxy (str)`: The proxy server in the format "IP:Port". It is a string representation of the proxy server address and port.


## Examples
```python
from src.endpoints.freegpt-webui-ru.server.auto_proxy import fetch_proxies, test_proxy, add_working_proxy, remove_proxy, get_working_proxies, update_working_proxies, get_random_proxy

# Fetch a list of proxy servers
proxy_list = fetch_proxies()

# Test a single proxy server
test_proxy(proxy='123.456.789.0:1234', prompt='What is the capital of France?', timeout=5)

# Add a working proxy server to the list
add_working_proxy(proxy='123.456.789.0:1234')

# Remove a proxy server from the list
remove_proxy(proxy='123.456.789.0:1234')

# Fetch and test proxy servers, adding working ones to the list
get_working_proxies(prompt='What is the capital of France?', timeout=5)

# Update the list of working proxy servers periodically
update_working_proxies()

# Get a random working proxy server
random_proxy = get_random_proxy()
```

This code showcases the various functions available in the module, including fetching proxy servers, testing their functionality, managing a list of working proxies, and retrieving a random working proxy for use in web requests.