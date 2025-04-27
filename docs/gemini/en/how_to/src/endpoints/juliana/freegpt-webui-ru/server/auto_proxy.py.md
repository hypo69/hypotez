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
This code block defines functions for fetching, testing, and managing proxy servers. 

Execution Steps
-------------------------
1. **`fetch_proxies()`:** Retrieves a list of potential proxy servers from `proxyscrape.com`. 
2. **`test_proxy()`:** Tests a given proxy server using a provided test prompt and timeout. 
    - If the proxy responds within the timeout, it's considered working and added to the `working_proxies` list.
3. **`add_working_proxy()`:** Appends a working proxy to the global `working_proxies` list.
4. **`remove_proxy()`:** Removes a specified proxy from the `working_proxies` list.
5. **`get_working_proxies()`:** Fetches a list of proxies, tests them using `test_proxy()`, and populates the `working_proxies` list.
6. **`update_working_proxies()`:** Continuously updates the `working_proxies` list by fetching and testing proxies every 30 minutes. 
7. **`get_random_proxy()`:** Returns a randomly selected working proxy server from the `working_proxies` list.

Usage Example
-------------------------

```python
# Fetch, test, and manage proxy servers
proxies = fetch_proxies()  # Get a list of proxies
test_prompt = "What is the capital of France?"  # Define a test prompt

for proxy in proxies:
    test_proxy(proxy, test_prompt, timeout=5)  # Test each proxy

random_proxy = get_random_proxy()  # Get a random working proxy
print(f"Using proxy: {random_proxy}")

# Update the working proxies list every 30 minutes
update_working_proxies()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".