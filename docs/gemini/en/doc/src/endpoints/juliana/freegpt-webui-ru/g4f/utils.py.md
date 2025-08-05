# Utils Module 

## Overview

The `Utils` module provides a collection of utility functions for managing browser cookies. It is designed to work with the `browser_cookie3` library, which allows for efficient access to cookies stored in different browsers. This module serves as a central point for handling cookie retrieval and manipulation in the project.

## Details

This module is specifically designed to work with different browser cookies, including Chrome, Safari, Firefox, Edge, Opera, Brave, Opera GX, and Vivaldi. It prioritizes the retrieval of cookies from these browsers based on their market share, aiming to get the most relevant and widely used cookies. The `get_cookies` function is the primary tool for retrieving cookies and can be used to gather cookies for a specified domain, optionally targeting a specific browser and cookie name.

## Classes

### `Utils`

**Description**: The `Utils` class encapsulates a set of utility functions for working with browser cookies.  It defines a list of supported browsers and the `get_cookies` method for retrieving cookies.

**Attributes**:

- `browsers` (list): A list containing browser functions from the `browser_cookie3` library, each corresponding to a specific browser. This list represents the order of priority for retrieving cookies from different browsers.

**Methods**:

- `get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict`: Retrieves cookies from the specified browsers for the given domain.

## Class Methods

### `get_cookies`

```python
    def get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict:
        """Функция для получения cookies из различных браузеров.
        Args:
            domain (str): Домен, из которого нужно получить cookies.
            setName (str, optional): Имя cookie, которое нужно получить. Defaults to None.
            setBrowser (str, optional): Имя браузера, из которого нужно получить cookies. Defaults to False.

        Returns:
            dict: Словарь с cookies.

        Raises:
            ValueError: Если cookie с указанным именем не найден в браузере.
        """
        cookies = {}
        
        if setBrowser != False:
            for browser in Utils.browsers:
                if browser.__name__ == setBrowser:
                    try:
                        for c in browser(domain_name=domain):
                            if c.name not in cookies:
                                cookies = cookies | {c.name: c.value} 
                    
                    except Exception as e:
                        pass
        
        else:
            for browser in Utils.browsers:
                try:
                    for c in browser(domain_name=domain):
                        if c.name not in cookies:
                            cookies = cookies | {c.name: c.value} 
                
                except Exception as e:
                    pass
        
        if setName:
            try:
                return {setName: cookies[setName]}
            
            except ValueError:
                print(f'Error: could not find {setName} cookie in any browser.')
                exit(1)
        
        else:
            return cookies
```

**Purpose**: The `get_cookies` function retrieves cookies from supported browsers for a specified domain. It iterates through the list of browser functions (`Utils.browsers`) and attempts to get cookies from each browser, prioritizing browsers based on their market share. If a `setName` is provided, the function returns only the cookie with that name.

**Parameters**:

- `domain` (str): The domain from which to retrieve cookies.
- `setName` (str, optional): The name of the cookie to retrieve. Defaults to `None`.
- `setBrowser` (str, optional): The name of the browser from which to retrieve cookies. Defaults to `False`.

**Returns**:

- `dict`: A dictionary containing the retrieved cookies. If a `setName` is provided, the dictionary will contain a single key-value pair with the specified cookie name and its value. If `setName` is not provided, the dictionary will contain all retrieved cookies as key-value pairs.

**Raises Exceptions**:

- `ValueError`: If a cookie with the specified name (`setName`) is not found in any browser.

**How the Function Works**:

1. **Initialize `cookies` dictionary**:  The function starts by initializing an empty dictionary `cookies` to store the retrieved cookies.
2. **Conditional browser selection**: If `setBrowser` is provided (not `False`), the function iterates through the `Utils.browsers` list to find the matching browser function. If found, it retrieves cookies from that specific browser.
3. **Iterate through all browsers (if `setBrowser` is `False`):** If `setBrowser` is not provided, the function iterates through all browsers in the `Utils.browsers` list.
4. **Retrieve cookies from each browser**: For each browser, the function uses `browser(domain_name=domain)` to retrieve cookies from the specified domain. It iterates through the retrieved cookies and adds them to the `cookies` dictionary, only if the cookie's name is not already present.
5. **Handle exceptions**: Each iteration uses a `try-except` block to handle any potential exceptions that might occur during cookie retrieval. If an exception is raised, the function logs the exception but continues processing.
6. **Return specified cookie or all cookies**: After retrieving cookies from all browsers, the function checks if `setName` is provided. If so, it returns a dictionary containing only the specified cookie. Otherwise, it returns the entire `cookies` dictionary.

**Examples**:

```python
# Retrieve all cookies from the 'example.com' domain
cookies = Utils.get_cookies('example.com')
print(cookies)

# Retrieve only the 'session_id' cookie from 'example.com'
session_cookie = Utils.get_cookies('example.com', setName='session_id')
print(session_cookie)

# Retrieve cookies from Firefox only for the 'example.com' domain
firefox_cookies = Utils.get_cookies('example.com', setBrowser='firefox')
print(firefox_cookies)
```

**Parameter Details**:

- `domain` (str): The domain for which cookies are being retrieved. It is essential to pass a valid domain name to ensure accurate cookie retrieval.
- `setName` (str, optional): The specific cookie name to retrieve. If a cookie with this name is not found in any browser, a `ValueError` will be raised.
- `setBrowser` (str, optional):  The specific browser from which to retrieve cookies. The browser name must match the `__name__` attribute of one of the browser functions in the `Utils.browsers` list.

**Inner Functions**:  None. 

**How the Function Works**:

- **Retrieve cookies from all supported browsers**: The function iterates through each browser in the `Utils.browsers` list and attempts to retrieve cookies for the specified domain.
- **Prioritize browsers based on market share**: The `Utils.browsers` list is ordered based on the estimated market share of each browser. 
- **Handle exceptions during retrieval**:  The function uses `try-except` blocks to handle potential exceptions during cookie retrieval.
- **Return cookies based on user input**: If a `setName` is provided, the function returns only the cookie with that name. Otherwise, it returns all retrieved cookies.

**Example**:

```python
# Retrieve all cookies from the 'example.com' domain
cookies = Utils.get_cookies('example.com')
print(cookies)

# Retrieve only the 'session_id' cookie from 'example.com'
session_cookie = Utils.get_cookies('example.com', setName='session_id')
print(session_cookie)

# Retrieve cookies from Firefox only for the 'example.com' domain
firefox_cookies = Utils.get_cookies('example.com', setBrowser='firefox')
print(firefox_cookies)
```

**Detailed Explanation**: 

The `Utils` class offers a convenient way to access and manage cookies from multiple browsers. The `get_cookies` function handles the intricacies of retrieving cookies from different browsers, addressing potential exceptions and allowing users to retrieve specific cookies or all cookies based on their needs.