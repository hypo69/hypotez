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
This code block defines two dictionaries containing default headers for HTTP requests. The `DEFAULT_HEADERS` dictionary contains common headers used for standard web requests, while the `WEBVIEW_HAEDERS` dictionary is specifically designed for requests made within a webview context.

Execution Steps
-------------------------
1. The code attempts to import the `brotli` library. If successful, it sets the `has_brotli` variable to `True`, indicating that the system supports Brotli compression. Otherwise, `has_brotli` is set to `False`.
2. The `DEFAULT_HEADERS` dictionary is created. It includes standard headers like `accept`, `accept-encoding`, `accept-language`, and `user-agent`. The `accept-encoding` header dynamically includes "br" if Brotli compression is supported by the system.
3. The `WEBVIEW_HAEDERS` dictionary is defined, containing headers specifically used for webview requests.

Usage Example
-------------------------

```python
    # Using DEFAULT_HEADERS
    import requests
    response = requests.get("https://www.example.com", headers=DEFAULT_HEADERS)

    # Using WEBVIEW_HAEDERS (replace with actual webview request details)
    webview_response = requests.post("https://api.example.com/webview", headers=WEBVIEW_HAEDERS, data={"key": "value"})
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".