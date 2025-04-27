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
The code snippet defines a `Utils` class that provides a function to retrieve cookies from different browsers. The `get_cookies` function iterates through a list of popular browsers, attempts to retrieve cookies for a specified domain, and returns a dictionary of cookies.

Execution Steps
-------------------------
1. The `get_cookies` function is called with a domain name as input, optionally specifying a cookie name to retrieve and a specific browser to use.
2. If a specific browser is not provided, the function iterates through all supported browsers: Chrome, Safari, Firefox, Edge, Opera, Brave, Opera GX, and Vivaldi.
3. For each browser, the function attempts to retrieve cookies for the specified domain using the `browser_cookie3` library.
4. If a specific cookie name is provided, the function returns a dictionary containing only that cookie. Otherwise, it returns a dictionary of all retrieved cookies.
5. If the specified cookie is not found, the function prints an error message and exits.

Usage Example
-------------------------

```python
from src.endpoints.juliana.freegpt-webui-ru.g4f.utils import Utils

# Get all cookies for example.com
cookies = Utils.get_cookies(domain='example.com')
print(cookies)

# Get only the 'session_id' cookie
session_cookie = Utils.get_cookies(domain='example.com', setName='session_id')
print(session_cookie)

# Get cookies from Chrome
chrome_cookies = Utils.get_cookies(domain='example.com', setBrowser='chrome')
print(chrome_cookies)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".